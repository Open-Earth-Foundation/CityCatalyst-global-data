#!/usr/bin/env python3
"""
Transform combined AdaptaBrasil municipal CSV (from adapta_download.ipynb) into
flat rows aligned with `modelled.city_adapta_risk_fact` described in
city_adapta_api_implementation_proposal.md.

Uses:
- data/adapta_indicator_hierarchy.csv — resolve each API indicator_id to a node
  level (aggregate vs leaf) and stable id path.
- data/adapta_indicator_hierarchy_modeled_en.csv — English labels for sector
  through base indicator on the resolved path.
- Optional crosswalk for UN/LOCODE actor_id (city name + UF, or IBGE code).

Requires pandas (same as the download notebook).

Deduplication is applied per input chunk only; run a full-file dedupe on the logical keys
before loading to the warehouse if overlaps occur across chunks.

By default the transform runs a first pass over the input to build a value index,
then fills every ancestor level's ``*_value_*`` columns on each output row from
the matching indicator rows for the same municipality, year, and requested
scenario (so a leaf row repeats risk / component / chain scores from their own
API extracts). Aggregate/intermediate input rows are used for this lookup, but
are not emitted when a deeper descendant row exists for the same municipality,
year, and requested scenario. Pass ``--skip-ancestor-value-fill`` to restore the
previous single-slot behaviour (faster, one pass, no extra I/O).

Example:
  python transform_adapta_city_data_to_risk_fact.py \\
    --input sample/indicators/adapta_city_data.csv \\
    --output sample/indicators/city_adapta_risk_fact_staging.csv \\
    --crosswalk data/br_locode.csv
"""

from __future__ import annotations

import argparse
import re
import unicodedata
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

RELEASE_DIR = Path(__file__).resolve().parent
DATA_DIR = RELEASE_DIR / "data"
DEFAULT_HIERARCHY_PT = DATA_DIR / "adapta_indicator_hierarchy.csv"
DEFAULT_HIERARCHY_EN = DATA_DIR / "adapta_indicator_hierarchy_modeled_en.csv"
DEFAULT_SCENARIOS = DATA_DIR / "adapta_scenarios_extracted.csv"
DEFAULT_INPUT = RELEASE_DIR / "sample" / "indicators" / "adapta_city_data.csv"

SOURCE_DATASET_DEFAULT = "br-mcti/adaptabrasil"
RELEASE_VERSION_DEFAULT = "v1"

# Portuguese class labels from API -> English (sample_data_one_city convention)
RANGE_PT_TO_EN = {
    "muito baixo": "Very low",
    "baixo": "Low",
    "médio": "Medium",
    "medio": "Medium",
    "alto": "High",
    "muito alto": "Very high",
    "dado indisponível": "Data unavailable",
    "dado indisponivel": "Data unavailable",
}

# Manual city/UF -> LOCODE overrides for known crosswalk gaps.
MANUAL_CITY_UF_ACTOR_OVERRIDES: dict[tuple[str, str], str] = {
    ("Atílio Vivacqua", "ES"): "BR AVQ",
    ("Olho d'Água do Borges", "RN"): "BR OAB",
    ("Pingo d'Água", "MG"): "BR PGG",
}


def _to_int(v) -> int | type(pd.NA):  # noqa: ANN001
    if pd.isna(v):
        return pd.NA
    s = str(v).strip().lower()
    if s in {"", "nan", "null"}:
        return pd.NA
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return pd.NA


def _parse_city_and_region(name: str) -> tuple[str, str | type(pd.NA)]:
    if pd.isna(name) or not str(name).strip():
        return "", pd.NA
    s = str(name).strip()
    if "/" in s:
        city, region = s.rsplit("/", 1)
        return city.strip(), region.strip().upper()
    return s, pd.NA


def _normalize_city_key(name: str) -> str:
    """Normalize city names for tolerant matching across accent/punctuation variants."""
    if pd.isna(name):
        return ""
    s = str(name).strip().casefold()
    s = s.replace("’", "'").replace("`", "'")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def translate_rangelabel(label: str | float) -> str:
    if pd.isna(label) or str(label).strip() == "":
        return ""
    key = str(label).strip().lower()
    return RANGE_PT_TO_EN.get(key, str(label).strip())


def _to_float_maybe(value) -> float | type(pd.NA):  # noqa: ANN001
    """Parse API/CSV numeric strings; accepts Brazilian comma decimals."""
    if pd.isna(value):
        return pd.NA
    s = str(value).strip().replace(",", ".")
    if s.lower() in {"", "nan", "null"}:
        return pd.NA
    try:
        return float(s)
    except (TypeError, ValueError):
        return pd.NA


def _node_pt_slice(k: int, ids: list, names: list) -> dict:
    """
    Build hierarchy snapshot for the node at path depth ``k`` (1..6).

    Each node must only carry ids/names for ancestors and itself — not deeper
    descendants from the same CSV row (those vary by path and broke joins and
    value-column alignment for aggregate indicators).
    """
    na = pd.NA
    out: dict = {
        "node_level": k,
        "node_name": names[k - 1],
        "sector_id": _to_int(ids[0]) if ids else na,
        "sector_name": (names[0] or na) if names else na,
    }
    if k >= 2:
        out["risk_id"] = _to_int(ids[1])
        out["risk_name"] = names[1] or na
    else:
        out["risk_id"] = na
        out["risk_name"] = na
    if k >= 3:
        out["risk_component_id"] = _to_int(ids[2])
        out["risk_component_name"] = names[2] or na
    else:
        out["risk_component_id"] = na
        out["risk_component_name"] = na
    if k >= 4:
        out["impact_chain_id_1"] = _to_int(ids[3])
        out["impact_chain_name_1"] = names[3] or na
    else:
        out["impact_chain_id_1"] = na
        out["impact_chain_name_1"] = na
    if k >= 5:
        out["impact_chain_id_2"] = _to_int(ids[4])
        out["impact_chain_name_2"] = names[4] or na
    else:
        out["impact_chain_id_2"] = na
        out["impact_chain_name_2"] = na
    if k >= 6:
        out["impact_chain_id_3"] = _to_int(ids[5])
        out["impact_chain_name_3"] = names[5] or na
    else:
        out["impact_chain_id_3"] = na
        out["impact_chain_name_3"] = na
    return out


def _mask_modeled_row_for_aggregate(mrow: pd.Series, node_level: int) -> pd.Series:
    """
    Strip modeled_en leaf path fields that sit below this aggregate node's depth.

    Otherwise ``english_hierarchy_fields`` prefers modeled values and copies an
    arbitrary deep-leaf path onto a sector/risk/... aggregate row.
    """
    out = mrow.copy()
    if node_level < 3:
        out["risk_component_id"] = pd.NA
        out["risk_component_name"] = ""
    if node_level < 4:
        out["impact_chain_id_1"] = pd.NA
        out["impact_chain_name_1"] = ""
    if node_level < 5:
        out["impact_chain_id_2"] = pd.NA
        out["impact_chain_name_2"] = ""
    if node_level < 6:
        out["impact_chain_id_3"] = pd.NA
        out["impact_chain_name_3"] = ""
    out["base_indicator_id"] = pd.NA
    out["base_indicator_name"] = ""
    out["base_indicator_level"] = pd.NA
    return out


def load_scenario_map(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    df = pd.read_csv(path, dtype="string")

    def label_en(pt_label: str) -> str:
        if not isinstance(pt_label, str):
            return ""
        s = pt_label.strip()
        if not s:
            return ""
        if s.lower() == "otimista":
            return "optimistic"
        if s.lower() == "pessimista":
            return "pessimistic"
        return s

    def family_from_description(desc_en: str, label: str) -> str:
        text = (desc_en or "").lower()
        if "ssp" in text:
            return "SSP"
        if "rcp" in text:
            return "RCP"
        if "swl" in text or str(label).upper().startswith("SWL"):
            return "SWL"
        return ""

    out: dict[str, dict[str, str]] = {}
    for row in df.itertuples(index=False):
        raw_value = getattr(row, "scenario_value", None)
        if pd.isna(raw_value):
            continue
        key = str(raw_value).strip()
        if not key:
            continue
        label_pt = getattr(row, "label", "") or ""
        desc_en = getattr(row, "description_en", "") or ""
        lbl = label_en(label_pt)
        fam = family_from_description(desc_en, lbl)
        out[key] = {"label": lbl, "family": fam}
    return out


def scenario_text(req_id: str | float, smap: dict[str, dict[str, str]]) -> str:
    """Source-faithful scenario text for the fact table (English short label + SWL)."""
    if pd.isna(req_id):
        return "current"
    s = str(req_id).strip().lower()
    if s in {"", "null", "nan"}:
        return "current"
    info = smap.get(s)
    if info and info.get("label"):
        return info["label"]
    return str(req_id).strip()


def scenario_family(req_id: str | float, smap: dict[str, dict[str, str]]) -> str:
    if pd.isna(req_id):
        return ""
    s = str(req_id).strip().lower()
    if s in {"", "null", "nan"}:
        return ""
    info = smap.get(s)
    return (info or {}).get("family", "") if info else ""


def build_node_maps(hierarchy_pt: Path) -> tuple[dict, dict, dict[int, set[int]]]:
    h = pd.read_csv(hierarchy_pt, dtype="string").fillna("")
    node_info: dict = {}
    has_children: dict = {}
    descendants: dict[int, set[int]] = {}

    for row in h.itertuples(index=False):
        ids = [getattr(row, f"id_nivel_{k}") for k in range(1, 7)]
        int_ids = [_to_int(v) for v in ids]
        for k in range(1, 6):
            parent = int_ids[k - 1]
            child = int_ids[k]
            if not pd.isna(parent) and not pd.isna(child) and int(parent) != int(child):
                has_children[int(parent)] = True

        for i, parent in enumerate(int_ids[:-1]):
            if pd.isna(parent):
                continue
            p = int(parent)
            for child in int_ids[i + 1 :]:
                if pd.isna(child):
                    continue
                c = int(child)
                if c != p:
                    descendants.setdefault(p, set()).add(c)

        names = [getattr(row, f"nome_nivel_{k}") for k in range(1, 7)]

        for k in range(1, 7):
            node_id = _to_int(ids[k - 1])
            if pd.isna(node_id):
                continue
            info = _node_pt_slice(k, ids, names)
            if node_id not in node_info:
                node_info[node_id] = info

    return node_info, has_children, descendants


def modeled_row_for_node(
    modeled: pd.DataFrame,
    indicator_id: int,
    node_level: int,
    pt_info: dict,
    is_aggregate: bool,
) -> pd.Series | None:
    """
    Pick one modeled_en row for English labels, using node id + ancestor ids
    from the Portuguese hierarchy node to disambiguate repeated impact-chain ids.

    Leaf (base-indicator) metrics always resolve by ``base_indicator_id``; aggregates
    use the node's level plus ancestor IDs from the Portuguese hierarchy snapshot.
    """
    mid = str(indicator_id)
    if not is_aggregate:
        sub = modeled[modeled["base_indicator_id"].astype(str) == mid]
        return sub.iloc[0] if not sub.empty else None

    sid = pt_info["sector_id"]
    rid = pt_info["risk_id"]
    rc = pt_info["risk_component_id"]
    ic1 = pt_info["impact_chain_id_1"]
    ic2 = pt_info["impact_chain_id_2"]
    ic3 = pt_info["impact_chain_id_3"]
    m = modeled
    if node_level == 1:
        sub = m[m["sector_id"].astype(str) == mid]
    elif node_level == 2:
        sub = m[m["risk_id"].astype(str) == mid]
    elif node_level == 3:
        sub = m[
            (m["risk_component_id"].astype(str) == mid)
            & (m["risk_id"].astype(str) == str(rid))
            & (m["sector_id"].astype(str) == str(sid))
        ]
    elif node_level == 4:
        sub = m[
            (m["impact_chain_id_1"].astype(str) == mid)
            & (m["risk_component_id"].astype(str) == str(rc))
            & (m["risk_id"].astype(str) == str(rid))
            & (m["sector_id"].astype(str) == str(sid))
        ]
    elif node_level == 5:
        sub = m[
            (m["impact_chain_id_2"].astype(str) == mid)
            & (m["impact_chain_id_1"].astype(str) == str(ic1))
            & (m["risk_component_id"].astype(str) == str(rc))
            & (m["risk_id"].astype(str) == str(rid))
            & (m["sector_id"].astype(str) == str(sid))
        ]
    elif node_level == 6:
        sub = m[
            (m["impact_chain_id_3"].astype(str) == mid)
            & (m["impact_chain_id_2"].astype(str) == str(ic2))
            & (m["impact_chain_id_1"].astype(str) == str(ic1))
            & (m["risk_component_id"].astype(str) == str(rc))
            & (m["risk_id"].astype(str) == str(rid))
            & (m["sector_id"].astype(str) == str(sid))
        ]
    else:
        sub = m[m["base_indicator_id"].astype(str) == mid]

    if sub is None or sub.empty:
        return None
    return sub.iloc[0]


def english_hierarchy_fields(
    mrow: pd.Series | None, pt_info: dict, pt_leaf_name: str
) -> dict:
    """Map modeled_en columns into fact-table hierarchy name/id fields."""
    def pick_int(modeled_value, pt_value):  # noqa: ANN001
        mv = _to_int(modeled_value)
        if pd.notna(mv):
            return mv
        pv = _to_int(pt_value)
        return pv if pd.notna(pv) else pd.NA

    def pick_name(modeled_value, pt_value):  # noqa: ANN001
        mtxt = str(modeled_value).strip() if pd.notna(modeled_value) else ""
        if mtxt:
            return mtxt
        ptxt = str(pt_value).strip() if pd.notna(pt_value) else ""
        return ptxt

    if mrow is None:
        return {
            "sector_id": pick_int(pd.NA, pt_info.get("sector_id")),
            "sector_name": pick_name("", pt_info.get("sector_name")),
            "risk_id": pick_int(pd.NA, pt_info.get("risk_id")),
            "risk_name": pick_name("", pt_info.get("risk_name")),
            "risk_component_id": pick_int(pd.NA, pt_info.get("risk_component_id")),
            "risk_component_name": pick_name("", pt_info.get("risk_component_name")),
            "impact_chain_id_1": pick_int(pd.NA, pt_info.get("impact_chain_id_1")),
            "impact_chain_name_1": pick_name("", pt_info.get("impact_chain_name_1")),
            "impact_chain_id_2": pick_int(pd.NA, pt_info.get("impact_chain_id_2")),
            "impact_chain_name_2": pick_name("", pt_info.get("impact_chain_name_2")),
            "impact_chain_id_3": pick_int(pd.NA, pt_info.get("impact_chain_id_3")),
            "impact_chain_name_3": pick_name("", pt_info.get("impact_chain_name_3")),
            "base_indicator_id": pd.NA,
            "base_indicator_name": "",
            "base_indicator_level": pd.NA,
        }

    bid = _to_int(mrow["base_indicator_id"])
    if pd.notna(bid):
        bname = pick_name(mrow["base_indicator_name"], "")
        if not str(bname).strip():
            bname = str(pt_leaf_name).strip() if pt_leaf_name else ""
        bless = (
            _to_int(mrow["base_indicator_level"])
            if "base_indicator_level" in mrow.index
            else pd.NA
        )
    else:
        bid = pd.NA
        bname = ""
        bless = pd.NA

    return {
        "sector_id": pick_int(mrow["sector_id"], pt_info.get("sector_id")),
        "sector_name": pick_name(mrow["sector_name"], pt_info.get("sector_name")),
        "risk_id": pick_int(mrow["risk_id"], pt_info.get("risk_id")),
        "risk_name": pick_name(mrow["risk_name"], pt_info.get("risk_name")),
        "risk_component_id": pick_int(
            mrow["risk_component_id"], pt_info.get("risk_component_id")
        ),
        "risk_component_name": pick_name(
            mrow["risk_component_name"], pt_info.get("risk_component_name")
        ),
        "impact_chain_id_1": pick_int(
            mrow["impact_chain_id_1"], pt_info.get("impact_chain_id_1")
        ),
        "impact_chain_name_1": pick_name(
            mrow["impact_chain_name_1"], pt_info.get("impact_chain_name_1")
        ),
        "impact_chain_id_2": pick_int(
            mrow["impact_chain_id_2"], pt_info.get("impact_chain_id_2")
        ),
        "impact_chain_name_2": pick_name(
            mrow["impact_chain_name_2"], pt_info.get("impact_chain_name_2")
        ),
        "impact_chain_id_3": pick_int(
            mrow["impact_chain_id_3"], pt_info.get("impact_chain_id_3")
        ),
        "impact_chain_name_3": pick_name(
            mrow["impact_chain_name_3"], pt_info.get("impact_chain_name_3")
        ),
        "base_indicator_id": bid,
        "base_indicator_name": bname,
        "base_indicator_level": bless,
    }


def build_name_crosswalk(path: Path) -> dict[tuple[str, str], str]:
    cw = pd.read_csv(path, dtype="string")
    cols = {c.lower(): c for c in cw.columns}

    # Supported schemas:
    # 1) actor_id, city_name, region_code (project-native)
    # 2) LOCODE, Name, SubDiv (UN/LOCODE export used by user)
    actor_col = cols.get("actor_id")
    city_col = cols.get("city_name")
    region_col = cols.get("region_code")

    if not (actor_col and city_col and region_col):
        actor_col = cols.get("locode")
        city_col = cols.get("name")
        region_col = cols.get("subdiv")

    if not (actor_col and city_col and region_col):
        raise ValueError(
            "Name crosswalk requires either [actor_id, city_name, region_code] "
            "or [LOCODE, Name, SubDiv] columns."
        )

    out: dict[tuple[str, str], str] = {}
    out_norm: dict[tuple[str, str], str] = {}
    for row in cw.itertuples(index=False):
        city = str(getattr(row, city_col, "")).strip()
        region = str(getattr(row, region_col, "")).strip().upper()
        actor = str(getattr(row, actor_col, "")).strip().upper()
        if not city or not region or not actor:
            continue
        out[(city.lower(), region)] = actor
        norm_city = _normalize_city_key(city)
        if norm_city:
            out_norm[(norm_city, region)] = actor

    # Inject explicit overrides (exact + normalized keys).
    for (city, region), actor in MANUAL_CITY_UF_ACTOR_OVERRIDES.items():
        c = str(city).strip()
        r = str(region).strip().upper()
        a = str(actor).strip().upper()
        if not c or not r or not a:
            continue
        out[(c.lower(), r)] = a
        norm_city = _normalize_city_key(c)
        if norm_city:
            out_norm[(norm_city, r)] = a
    return {**out_norm, **out}


def build_ibge_crosswalk(path: Path) -> dict[str, str]:
    df = pd.read_csv(path, dtype="string")
    cols = {c.lower(): c for c in df.columns}
    geo_col = cols.get("geocod_ibge") or cols.get("ibge") or cols.get("geocódigo")
    act_col = cols.get("actor_id") or cols.get("locode")
    if not geo_col or not act_col:
        raise ValueError(
            "IBGE crosswalk requires columns geocod_ibge (or ibge) and actor_id"
        )
    out = {}
    for row in df.itertuples(index=False):
        geo = _strip_ibge(str(getattr(row, geo_col, "")))
        act = str(getattr(row, act_col, "")).strip().upper()
        if geo and act:
            out[geo] = act
    return out


def _strip_ibge(s: str) -> str:
    s = s.strip().replace("-", "").replace(".", "")
    if s.endswith(".0"):
        s = s[:-2]
    return s.zfill(7) if s.isdigit() else s


# (hierarchy id column on the fact row, numeric value column, string value column)
# Sector and risk both roll into risk_value_* in this schema (same as aggregate mapping).
PATH_VALUE_LOOKUP: list[tuple[str, str, str]] = [
    ("sector_id", "risk_value_numeric", "risk_value_string"),
    ("risk_id", "risk_value_numeric", "risk_value_string"),
    ("risk_component_id", "risk_component_value_numeric", "risk_component_value_string"),
    ("impact_chain_id_1", "impact_chain_1_value_numeric", "impact_chain_1_value_string"),
    ("impact_chain_id_2", "impact_chain_2_value_numeric", "impact_chain_2_value_string"),
    ("impact_chain_id_3", "impact_chain_3_value_numeric", "impact_chain_3_value_string"),
    ("base_indicator_id", "base_indicator_value_numeric", "base_indicator_value_string"),
]


def _value_index_coord_keys(row: pd.Series) -> tuple[str, str, str] | None:
    """
    (geocod_ibge_norm, year_str, requested_scenario_id_norm) for joining API rows.

    Rows without a usable IBGE code are skipped so unrelated cities never share keys.
    """
    geo = _strip_ibge(str(row.get("geocod_ibge", "")))
    if not geo:
        return None
    yv = row.get("year")
    if pd.isna(yv) or str(yv).strip() == "":
        y = ""
    else:
        ti = _to_int(yv)
        y = str(int(ti)) if pd.notna(ti) else str(yv).strip()
    req = row.get("requested_scenario_id")
    if pd.isna(req) or str(req).strip().lower() in {"", "nan", "null"}:
        rk = ""
    else:
        rk = str(req).strip().lower()
    return geo, y, rk


def _value_index_full_key(row: pd.Series) -> tuple[str, str, str, int] | None:
    ind = _to_int(row.get("indicator_id"))
    if pd.isna(ind):
        return None
    ck = _value_index_coord_keys(row)
    if ck is None:
        return None
    return (*ck, int(ind))


def build_value_index(
    input_path: Path,
    chunksize: int,
    *,
    progress_every: int,
) -> dict[tuple[str, str, str, int], tuple]:
    """
    Map (geocod_ibge, year, requested_scenario_id, indicator_id) -> (numeric, string).

    Last duplicate key wins (identical replays from the download are harmless).
    """
    out: dict[tuple[str, str, str, int], tuple] = {}
    t0 = time.perf_counter()
    rows_seen = 0
    skipped_no_key = 0
    chunk_idx = 0
    for chunk in pd.read_csv(input_path, chunksize=chunksize, dtype="string"):
        chunk_idx += 1
        chunk_t0 = time.perf_counter()
        inner = 0
        for row_idx, (_, row) in enumerate(chunk.iterrows(), start=1):
            inner += 1
            key = _value_index_full_key(row)
            if key is None:
                skipped_no_key += 1
                continue
            vnum = _to_float_maybe(row.get("value"))
            vstr = translate_rangelabel(row.get("rangelabel"))
            out[key] = (vnum, vstr)
            if progress_every > 0 and row_idx % progress_every == 0:
                _log(
                    f"Pass 1 chunk {chunk_idx}: inner {row_idx:,}/{len(chunk):,} rows "
                    f"(index_keys={len(out):,})"
                )
        rows_seen += len(chunk)
        chunk_elapsed = time.perf_counter() - chunk_t0
        _log(
            f"Pass 1 chunk {chunk_idx} done: +{len(chunk):,} rows in {chunk_elapsed:.1f}s "
            f"(cumulative_input_rows={rows_seen:,}, index_keys={len(out):,}, "
            f"skipped_no_ibge_or_indicator={skipped_no_key:,})"
        )
    elapsed = time.perf_counter() - t0
    _log(
        f"Pass 1 finished: scanned {rows_seen:,} input rows, {len(out):,} index keys, "
        f"{elapsed:.1f}s total"
    )
    return out


def has_descendant_value_for_same_place_time(
    row: pd.Series,
    indicator_id: int,
    descendants: dict[int, set[int]],
    value_index: dict[tuple[str, str, str, int], tuple] | None,
) -> bool:
    """
    True when this aggregate/intermediate row has a deeper descendant value.

    In that case the row is only needed to populate ancestor ``*_value_*``
    columns on deeper rows, so Pass 2 should not emit it as its own fact row.
    """
    if value_index is None:
        return False
    child_ids = descendants.get(int(indicator_id), set())
    if not child_ids:
        return False
    ck = _value_index_coord_keys(row)
    if ck is None:
        return False
    geo, year_key, scenario_req_key = ck
    return any((geo, year_key, scenario_req_key, int(child_id)) in value_index for child_id in child_ids)


def fill_ancestor_path_values(
    rec: dict,
    value_index: dict[tuple[str, str, str, int], tuple],
    geo: str,
    year_key: str,
    scenario_req_key: str,
) -> None:
    """Copy values from ``value_index`` into every populated hierarchy id on ``rec``."""
    for id_col, num_col, str_col in PATH_VALUE_LOOKUP:
        iid = _to_int(rec.get(id_col))
        if pd.isna(iid):
            continue
        key = (geo, year_key, scenario_req_key, int(iid))
        if key not in value_index:
            continue
        vn, vs = value_index[key]
        rec[num_col] = vn
        rec[str_col] = vs


def assign_null_type(row: dict) -> str:
    base_num = row.get("base_indicator_value_numeric")
    base_str = str(row.get("base_indicator_value_string") or "").strip().lower()

    gap_strings = {"data unavailable", "dado indisponível", "dado indisponivel"}
    data_gap = (pd.isna(base_num) or str(base_num).strip() == "") and base_str in gap_strings

    rc_name = str(row.get("risk_component_name") or "")
    rc_id = row.get("risk_component_id")
    rc_empty = pd.isna(rc_id) or str(rc_name).strip() == ""

    has_base_num = bool(not pd.isna(base_num) and str(base_num).strip() != "")

    structural = rc_empty and has_base_num
    if data_gap:
        return "data_gap_null"
    if structural:
        return "structural_null"
    return "none"


def build_fact_record(
    r: pd.Series,
    node_info: dict,
    has_children: dict,
    modeled: pd.DataFrame,
    smap: dict[str, dict[str, str]],
    cw_name: dict[tuple[str, str], str],
    cw_ibge: dict[str, str],
    release_id: str,
    source_vintage: str,
    spatial_support_level: str,
    audit_columns: bool,
    value_index: dict[tuple[str, str, str, int], tuple] | None = None,
) -> dict | None:
    indicator_id = _to_int(r.get("indicator_id"))
    if pd.isna(indicator_id):
        return None
    pt = node_info.get(int(indicator_id))
    if not pt:
        return None

    level = int(pt["node_level"])
    is_aggregate = bool(has_children.get(int(indicator_id), False))

    city_name, region = _parse_city_and_region(r.get("name"))

    geo = _strip_ibge(str(r.get("geocod_ibge", "")))
    actor_id = ""
    if cw_ibge and geo in cw_ibge:
        actor_id = cw_ibge[geo]
    elif region is not pd.NA and cw_name:
        actor_id = cw_name.get((city_name.lower(), str(region)), "")

    mrow = modeled_row_for_node(
        modeled, int(indicator_id), level, pt, is_aggregate=is_aggregate
    )
    if is_aggregate and mrow is not None:
        mrow = _mask_modeled_row_for_aggregate(mrow, level)
    hi = english_hierarchy_fields(mrow, pt, str(pt["node_name"]))

    timeframe = _to_int(r.get("year"))
    req_sid = r.get("requested_scenario_id")
    scenario = scenario_text(req_sid, smap)
    scen_fam = scenario_family(req_sid, smap)

    value_numeric = r.get("value")
    vnum = _to_float_maybe(value_numeric)

    value_str_en = translate_rangelabel(r.get("rangelabel"))

    req_for_row = req_sid if pd.notna(req_sid) and str(req_sid).strip().lower() not in {"", "nan", "null"} else pd.NA

    rec = {
        "actor_id": actor_id if actor_id else pd.NA,
        "city_name": city_name,
        "country_code": "BR",
        "timeframe": timeframe if not pd.isna(timeframe) else pd.NA,
        "scenario": scenario,
        "scenario_family": scen_fam if scen_fam else pd.NA,
        "sector_id": hi["sector_id"],
        "sector_name": hi["sector_name"],
        "risk_id": hi["risk_id"],
        "risk_name": hi["risk_name"],
        "risk_component_id": hi["risk_component_id"],
        "risk_component_name": hi["risk_component_name"],
        "impact_chain_id_1": hi["impact_chain_id_1"],
        "impact_chain_name_1": hi["impact_chain_name_1"],
        "impact_chain_id_2": hi["impact_chain_id_2"],
        "impact_chain_name_2": hi["impact_chain_name_2"],
        "impact_chain_id_3": hi["impact_chain_id_3"],
        "impact_chain_name_3": hi["impact_chain_name_3"],
        "base_indicator_id": hi["base_indicator_id"],
        "base_indicator_name": hi["base_indicator_name"],
        "base_indicator_level": hi["base_indicator_level"],
        "risk_value_numeric": pd.NA,
        "risk_value_string": "",
        "risk_component_value_numeric": pd.NA,
        "risk_component_value_string": "",
        "impact_chain_1_value_numeric": pd.NA,
        "impact_chain_1_value_string": "",
        "impact_chain_2_value_numeric": pd.NA,
        "impact_chain_2_value_string": "",
        "impact_chain_3_value_numeric": pd.NA,
        "impact_chain_3_value_string": "",
        "base_indicator_value_numeric": pd.NA,
        "base_indicator_value_string": "",
        "null_type": "none",
        "release_id": release_id,
        "source_dataset": SOURCE_DATASET_DEFAULT,
        "release_version": RELEASE_VERSION_DEFAULT,
        "source_vintage": source_vintage,
        "spatial_support_level": spatial_support_level,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if audit_columns:
        rec["source_requested_scenario_id"] = req_for_row
        rec["source_geocod_ibge"] = geo if geo else pd.NA

    if is_aggregate:
        if level in (1, 2):
            rec["risk_value_numeric"] = vnum
            rec["risk_value_string"] = value_str_en
        elif level == 3:
            rec["risk_component_value_numeric"] = vnum
            rec["risk_component_value_string"] = value_str_en
        elif level == 4:
            rec["impact_chain_1_value_numeric"] = vnum
            rec["impact_chain_1_value_string"] = value_str_en
        elif level == 5:
            rec["impact_chain_2_value_numeric"] = vnum
            rec["impact_chain_2_value_string"] = value_str_en
        elif level == 6:
            rec["impact_chain_3_value_numeric"] = vnum
            rec["impact_chain_3_value_string"] = value_str_en
        else:
            rec["base_indicator_value_numeric"] = vnum
            rec["base_indicator_value_string"] = value_str_en
    else:
        rec["base_indicator_id"] = int(indicator_id)
        rec["base_indicator_name"] = hi["base_indicator_name"] or str(pt["node_name"])
        rec["base_indicator_value_numeric"] = vnum
        rec["base_indicator_value_string"] = value_str_en
        rec["base_indicator_level"] = (
            hi["base_indicator_level"] if pd.notna(hi["base_indicator_level"]) else level
        )

    if value_index is not None and geo:
        ck = _value_index_coord_keys(r)
        if ck is not None:
            geo_k, y_k, rk_k = ck
            fill_ancestor_path_values(rec, value_index, geo_k, y_k, rk_k)

    rec["null_type"] = assign_null_type(rec)
    return rec


def _log(message: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {message}", flush=True)


def _stage(title: str, detail: str = "") -> None:
    """High-visibility section header for terminal monitoring."""
    bar = "=" * 72
    print(f"\n{bar}\n  {title}\n{bar}", flush=True)
    if detail.strip():
        for line in detail.strip().split("\n"):
            print(f"  {line}", flush=True)
    print(flush=True)


def validate_required_fields(df: pd.DataFrame, required_fields: list[str]) -> None:
    """
    Fail fast if required fields contain null/blank values in the transform output.
    """
    errors: list[str] = []
    sample_frames: list[pd.DataFrame] = []
    sample_cols = [
        "actor_id",
        "city_name",
        "timeframe",
        "scenario",
        "sector_id",
        "risk_id",
        "base_indicator_id",
    ]
    for field in required_fields:
        if field not in df.columns:
            errors.append(f"{field}: missing column")
            continue
        series = df[field]
        null_count = int(series.isna().sum())
        blank_count = int((series.astype("string").str.strip() == "").fillna(False).sum())
        bad_count = null_count + blank_count
        if bad_count > 0:
            errors.append(
                f"{field}: {bad_count} invalid rows "
                f"(null={null_count}, blank={blank_count})"
            )
            bad_mask = series.isna() | (series.astype("string").str.strip() == "")
            cols = [c for c in sample_cols if c in df.columns]
            sample = df.loc[bad_mask, cols].head(10).copy()
            sample.insert(0, "invalid_field", field)
            sample_frames.append(sample)
    if errors:
        sample_text = ""
        if sample_frames:
            sample_rows = (
                pd.concat(sample_frames, ignore_index=True)
                .drop_duplicates()
                .head(10)
                .to_dict("records")
            )
            sample_text = f" Sample rows: {sample_rows}"
        raise ValueError(
            "Required-field validation failed before writing output CSV: "
            + "; ".join(errors)
            + sample_text
        )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--hierarchy-pt", type=Path, default=DEFAULT_HIERARCHY_PT)
    ap.add_argument("--hierarchy-en", type=Path, default=DEFAULT_HIERARCHY_EN)
    ap.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    ap.add_argument(
        "--crosswalk",
        type=Path,
        default=None,
        help="CSV with actor_id, city_name, region_code (name/UF match)",
    )
    ap.add_argument(
        "--ibge-crosswalk",
        type=Path,
        default=None,
        help="CSV with geocod_ibge and actor_id for direct IBGE → LOCODE",
    )
    ap.add_argument("--release-id", type=str, default="")
    ap.add_argument("--source-vintage", type=str, default="")
    ap.add_argument(
        "--spatial-support-level",
        type=str,
        default="municipal",
        help="Proposal: municipal for mapa-dados/.../municipio/...",
    )
    ap.add_argument("--chunksize", type=int, default=100_000)
    ap.add_argument(
        "--progress-every",
        type=int,
        default=10_000,
        help=(
            "Within each chunk, log every N input rows during Pass 1 (index) and Pass 2 "
            "(transform). Set 0 to disable intra-chunk row logs (chunk boundary logs "
            "still print)."
        ),
    )
    ap.add_argument(
        "--audit-columns",
        action="store_true",
        help="Append source_requested_scenario_id and source_geocod_ibge for QA joins",
    )
    ap.add_argument(
        "--skip-ancestor-value-fill",
        action="store_true",
        help=(
            "Do not run the extra input pass that fills risk/component/chain/base "
            "value columns from sibling indicator rows (legacy single-slot output)."
        ),
    )
    args = ap.parse_args()

    run_start = time.perf_counter()
    _stage(
        "AdaptaBrasil: city data → risk_fact CSV",
        f"input:  {args.input}\n"
        f"output: {args.output}\n"
        f"chunksize={args.chunksize:,}  progress_every={args.progress_every}\n"
        f"ancestor_value_fill={'disabled' if args.skip_ancestor_value_fill else 'enabled (Pass 1 index + Pass 2 transform)'}",
    )
    _log("Stage A: load hierarchy, scenarios, crosswalks")
    _log(f"Loading hierarchy PT: {args.hierarchy_pt}")
    node_info, has_children, descendants = build_node_maps(args.hierarchy_pt)
    _log(
        "Loaded hierarchy PT "
        f"(nodes={len(node_info)}, aggregate_nodes={len(has_children)}, "
        f"nodes_with_descendants={len(descendants)})"
    )
    _log(f"Loading hierarchy EN: {args.hierarchy_en}")
    modeled = pd.read_csv(args.hierarchy_en, dtype="string").fillna("")
    _log(f"Loaded hierarchy EN rows={len(modeled)}")
    _log(f"Loading scenarios: {args.scenarios}")
    smap = load_scenario_map(args.scenarios)
    _log(f"Loaded scenarios map entries={len(smap)}")

    cw_name: dict[tuple[str, str], str] = {}
    if args.crosswalk:
        _log(f"Loading name crosswalk: {args.crosswalk}")
        cw_name = build_name_crosswalk(args.crosswalk)
        _log(f"Loaded name crosswalk entries={len(cw_name)}")

    cw_ibge: dict[str, str] = {}
    if args.ibge_crosswalk:
        _log(f"Loading IBGE crosswalk: {args.ibge_crosswalk}")
        cw_ibge = build_ibge_crosswalk(args.ibge_crosswalk)
        _log(f"Loaded IBGE crosswalk entries={len(cw_ibge)}")
    _log("Stage A complete.")

    out_cols = [
        "actor_id",
        "city_name",
        "country_code",
        "timeframe",
        "scenario",
        "scenario_family",
        "sector_id",
        "sector_name",
        "risk_id",
        "risk_name",
        "risk_component_id",
        "risk_component_name",
        "impact_chain_id_1",
        "impact_chain_name_1",
        "impact_chain_id_2",
        "impact_chain_name_2",
        "impact_chain_id_3",
        "impact_chain_name_3",
        "base_indicator_id",
        "base_indicator_name",
        "base_indicator_level",
        "risk_value_numeric",
        "risk_value_string",
        "risk_component_value_numeric",
        "risk_component_value_string",
        "impact_chain_1_value_numeric",
        "impact_chain_1_value_string",
        "impact_chain_2_value_numeric",
        "impact_chain_2_value_string",
        "impact_chain_3_value_numeric",
        "impact_chain_3_value_string",
        "base_indicator_value_numeric",
        "base_indicator_value_string",
        "null_type",
        "release_id",
        "source_dataset",
        "release_version",
        "source_vintage",
        "spatial_support_level",
        "created_at",
        "updated_at",
    ]
    if args.audit_columns:
        out_cols.extend(["source_requested_scenario_id", "source_geocod_ibge"])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    first_chunk = True
    total = 0
    skipped_indicator = 0
    unmatched_actor = 0
    skipped_parent_rows = 0

    value_index: dict[tuple[str, str, str, int], tuple] | None = None
    if not args.skip_ancestor_value_fill:
        _stage(
            "Pass 1 / 2 — Build value lookup index",
            "Reading the full input once to map (IBGE, year, scenario, indicator_id) → value.\n"
            "Pass 2 will join these onto each output row for ancestor columns.",
        )
        value_index = build_value_index(
            args.input,
            args.chunksize,
            progress_every=args.progress_every,
        )
        _log(f"Value index ready: {len(value_index):,} keys")
    else:
        _stage(
            "Single pass mode",
            "--skip-ancestor-value-fill: only Pass 2 runs (no value index).",
        )

    _stage(
        "Pass 2 / 2 — Transform, validate, append to output"
        if not args.skip_ancestor_value_fill
        else "Pass 1 / 1 — Transform, validate, append to output",
        f"Streaming {args.input} (chunksize={args.chunksize:,})",
    )
    reader = pd.read_csv(args.input, chunksize=args.chunksize, dtype="string")

    for chunk_idx, chunk in enumerate(reader, start=1):
        chunk_start = time.perf_counter()
        chunk_skipped_parent_start = skipped_parent_rows
        _log(f"Pass 2 chunk {chunk_idx}: read {len(chunk):,} input rows — building fact rows…")
        rows_out = []
        for row_idx, (_, row) in enumerate(chunk.iterrows(), start=1):
            d = row
            current_indicator = _to_int(d.get("indicator_id"))
            if not pd.isna(current_indicator) and has_descendant_value_for_same_place_time(
                d,
                int(current_indicator),
                descendants,
                value_index,
            ):
                skipped_parent_rows += 1
                continue
            fact = build_fact_record(
                d,
                node_info,
                has_children,
                modeled,
                smap,
                cw_name,
                cw_ibge,
                release_id=args.release_id,
                source_vintage=args.source_vintage,
                spatial_support_level=args.spatial_support_level,
                audit_columns=args.audit_columns,
                value_index=value_index,
            )
            if fact is None:
                skipped_indicator += 1
                continue
            if pd.isna(fact["actor_id"]) or str(fact["actor_id"]).strip() == "":
                unmatched_actor += 1
            rows_out.append(fact)

            if args.progress_every > 0 and row_idx % args.progress_every == 0:
                _log(
                    f"Pass 2 chunk {chunk_idx}: rows {row_idx:,}/{len(chunk):,} "
                    f"(buffered_output={len(rows_out):,})"
                )

        if not rows_out:
            chunk_elapsed = time.perf_counter() - chunk_start
            _log(
                f"Pass 2 chunk {chunk_idx}: no output rows produced "
                f"(skipped_parent_rows={skipped_parent_rows - chunk_skipped_parent_start:,}, "
                f"elapsed={chunk_elapsed:.1f}s)"
            )
            continue
        _log(
            f"Pass 2 chunk {chunk_idx}: DataFrame ({len(rows_out):,} rows) → "
            "drop_duplicates → validate_required_fields → to_csv…"
        )
        out_df = pd.DataFrame(rows_out, columns=out_cols)
        out_df = out_df.drop_duplicates()
        validate_required_fields(out_df, ["risk_id", "sector_id"])
        mode = "w" if first_chunk else "a"
        header = first_chunk
        out_df.to_csv(args.output, index=False, mode=mode, header=header)
        first_chunk = False
        total += len(out_df)
        chunk_elapsed = time.perf_counter() - chunk_start
        _log(
            f"Pass 2 chunk {chunk_idx}: wrote {len(out_df):,} rows "
            f"(running_total={total:,}, "
            f"skipped_parent_rows={skipped_parent_rows - chunk_skipped_parent_start:,}, "
            f"chunk_elapsed={chunk_elapsed:.1f}s)"
        )

    total_elapsed = time.perf_counter() - run_start
    _stage(
        "Done",
        f"Output: {args.output}\n"
        f"Rows written (after dedupe): {total:,}\n"
        f"skipped_unknown_indicator_rows={skipped_indicator:,}\n"
        f"skipped_parent_rows_with_descendants={skipped_parent_rows:,}\n"
        f"rows_missing_actor_id={unmatched_actor:,}\n"
        f"elapsed_seconds={total_elapsed:.1f}",
    )


if __name__ == "__main__":
    main()
