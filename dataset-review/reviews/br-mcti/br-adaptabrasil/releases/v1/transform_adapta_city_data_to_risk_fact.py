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


def build_node_maps(hierarchy_pt: Path) -> tuple[dict, dict]:
    h = pd.read_csv(hierarchy_pt, dtype="string").fillna("")
    node_info: dict = {}
    has_children: dict = {}

    for row in h.itertuples(index=False):
        ids = [getattr(row, f"id_nivel_{k}") for k in range(1, 7)]
        for k in range(1, 6):
            parent = _to_int(ids[k - 1])
            child = _to_int(ids[k])
            if not pd.isna(parent) and not pd.isna(child):
                has_children[parent] = True

        names = [getattr(row, f"nome_nivel_{k}") for k in range(1, 7)]

        for k in range(1, 7):
            node_id = _to_int(ids[k - 1])
            if pd.isna(node_id):
                continue
            info = {
                "node_level": k,
                "node_name": names[k - 1],
                "sector_id": _to_int(ids[0]),
                "sector_name": names[0] or pd.NA,
                "risk_id": _to_int(ids[1]),
                "risk_name": names[1] or pd.NA,
                "risk_component_id": _to_int(ids[2]),
                "risk_component_name": names[2] or pd.NA,
                "impact_chain_id_1": _to_int(ids[3]),
                "impact_chain_name_1": names[3] or pd.NA,
                "impact_chain_id_2": _to_int(ids[4]),
                "impact_chain_name_2": names[4] or pd.NA,
                "impact_chain_id_3": _to_int(ids[5]),
                "impact_chain_name_3": names[5] or pd.NA,
            }
            if node_id not in node_info:
                node_info[node_id] = info

    return node_info, has_children


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


def english_hierarchy_fields(mrow: pd.Series | None, pt_leaf_name: str) -> dict:
    """Map modeled_en columns into fact-table hierarchy name/id fields."""
    if mrow is None:
        return {
            "sector_id": pd.NA,
            "sector_name": "",
            "risk_id": pd.NA,
            "risk_name": "",
            "risk_component_id": pd.NA,
            "risk_component_name": "",
            "impact_chain_id_1": pd.NA,
            "impact_chain_name_1": "",
            "impact_chain_id_2": pd.NA,
            "impact_chain_name_2": "",
            "impact_chain_id_3": pd.NA,
            "impact_chain_name_3": "",
            "base_indicator_id": pd.NA,
            "base_indicator_name": "",
            "base_indicator_level": pd.NA,
        }

    return {
        "sector_id": _to_int(mrow["sector_id"]),
        "sector_name": mrow["sector_name"] or "",
        "risk_id": _to_int(mrow["risk_id"]),
        "risk_name": mrow["risk_name"] or "",
        "risk_component_id": _to_int(mrow["risk_component_id"])
        if pd.notna(mrow["risk_component_id"]) and str(mrow["risk_component_id"]).strip() != ""
        else pd.NA,
        "risk_component_name": mrow["risk_component_name"]
        if pd.notna(mrow["risk_component_name"]) and str(mrow["risk_component_name"]).strip() != ""
        else "",
        "impact_chain_id_1": _to_int(mrow["impact_chain_id_1"])
        if pd.notna(mrow["impact_chain_id_1"]) and str(mrow["impact_chain_id_1"]).strip() != ""
        else pd.NA,
        "impact_chain_name_1": mrow["impact_chain_name_1"]
        if pd.notna(mrow["impact_chain_name_1"]) and str(mrow["impact_chain_name_1"]).strip() != ""
        else "",
        "impact_chain_id_2": _to_int(mrow["impact_chain_id_2"])
        if pd.notna(mrow["impact_chain_id_2"]) and str(mrow["impact_chain_id_2"]).strip() != ""
        else pd.NA,
        "impact_chain_name_2": mrow["impact_chain_name_2"]
        if pd.notna(mrow["impact_chain_name_2"]) and str(mrow["impact_chain_name_2"]).strip() != ""
        else "",
        "impact_chain_id_3": _to_int(mrow["impact_chain_id_3"])
        if pd.notna(mrow["impact_chain_id_3"]) and str(mrow["impact_chain_id_3"]).strip() != ""
        else pd.NA,
        "impact_chain_name_3": mrow["impact_chain_name_3"]
        if pd.notna(mrow["impact_chain_name_3"]) and str(mrow["impact_chain_name_3"]).strip() != ""
        else "",
        "base_indicator_id": _to_int(mrow["base_indicator_id"]),
        "base_indicator_name": mrow["base_indicator_name"] or pt_leaf_name or "",
        "base_indicator_level": _to_int(mrow["base_indicator_level"])
        if "base_indicator_level" in mrow.index
        else pd.NA,
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
    hi = english_hierarchy_fields(mrow, str(pt["node_name"]))

    timeframe = _to_int(r.get("year"))
    req_sid = r.get("requested_scenario_id")
    scenario = scenario_text(req_sid, smap)
    scen_fam = scenario_family(req_sid, smap)

    value_numeric = r.get("value")
    try:
        vnum = float(value_numeric) if pd.notna(value_numeric) and str(value_numeric).strip() != "" else pd.NA
    except (TypeError, ValueError):
        vnum = pd.NA

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

    rec["null_type"] = assign_null_type(rec)
    return rec


def _log(message: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {message}", flush=True)


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
            "Emit row-level progress every N input rows within each chunk. "
            "Set 0 to disable."
        ),
    )
    ap.add_argument(
        "--audit-columns",
        action="store_true",
        help="Append source_requested_scenario_id and source_geocod_ibge for QA joins",
    )
    args = ap.parse_args()

    run_start = time.perf_counter()
    _log("Starting transform")
    _log(f"Loading hierarchy PT: {args.hierarchy_pt}")
    node_info, has_children = build_node_maps(args.hierarchy_pt)
    _log(
        "Loaded hierarchy PT "
        f"(nodes={len(node_info)}, aggregate_nodes={len(has_children)})"
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

    _log(
        f"Opening input CSV in chunks (input={args.input}, chunksize={args.chunksize})"
    )
    reader = pd.read_csv(args.input, chunksize=args.chunksize, dtype="string")

    for chunk_idx, chunk in enumerate(reader, start=1):
        chunk_start = time.perf_counter()
        _log(f"Chunk {chunk_idx}: read {len(chunk)} input rows")
        rows_out = []
        for row_idx, (_, row) in enumerate(chunk.iterrows(), start=1):
            d = row
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
            )
            if fact is None:
                skipped_indicator += 1
                continue
            if pd.isna(fact["actor_id"]) or str(fact["actor_id"]).strip() == "":
                unmatched_actor += 1
            rows_out.append(fact)

            if args.progress_every > 0 and row_idx % args.progress_every == 0:
                _log(
                    f"Chunk {chunk_idx}: processed {row_idx}/{len(chunk)} rows "
                    f"(output_rows_buffered={len(rows_out)})"
                )

        if not rows_out:
            chunk_elapsed = time.perf_counter() - chunk_start
            _log(
                f"Chunk {chunk_idx}: no output rows produced "
                f"(elapsed={chunk_elapsed:.1f}s)"
            )
            continue
        out_df = pd.DataFrame(rows_out, columns=out_cols)
        out_df = out_df.drop_duplicates()
        mode = "w" if first_chunk else "a"
        header = first_chunk
        out_df.to_csv(args.output, index=False, mode=mode, header=header)
        first_chunk = False
        total += len(out_df)
        chunk_elapsed = time.perf_counter() - chunk_start
        _log(
            f"Chunk {chunk_idx}: wrote {len(out_df)} rows "
            f"(running_total={total}, elapsed={chunk_elapsed:.1f}s)"
        )

    total_elapsed = time.perf_counter() - run_start
    print(
        f"Wrote {total} deduplicated rows to {args.output} "
        f"(skipped_unknown_indicator_rows={skipped_indicator}, "
        f"rows_missing_actor_id={unmatched_actor}, "
        f"elapsed_seconds={total_elapsed:.1f})"
    )


if __name__ == "__main__":
    main()
