"""Shape the SUBDERE/SINIM municipal frame into modelled.city_finance_profile staging.

Computes the two CITY axes the score reads (methodology blend, validated against the fixture):
  autonomy = clip(1 - fcm_dependency_pct_2025/100, 0, 1)            (fillna median)
  capacity = 0.7*pctrank(staff_profesional_total_2025)
           + 0.3*pctrank(professionalization_pct_2025)             (fillna median)
  city_archetype banded from (autonomy, capacity) at 0.5.
Resolves actor_id = city locode from comuna_cut via the cl-ocha-ab lookup; rows whose comuna has
no locode are dropped (actor_id is the API key and is NOT NULL). One row per city (~341 of 345).
"""
import unicodedata

import pandas as pd

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

SOURCE = "cl-subdere/cl-subdere-sinim"
Y = 2025  # the SINIM year the model uses

OUT_COLS = ["actor_id", "autonomy", "capacity", "city_archetype",
            "country_code", "source_dataset"]


def _numstr(v):
    if v is None or pd.isna(v):
        return None
    f = float(v)
    return str(round(f, 6))


def _archetype(a, c):
    # city-facing, strength-based labels (autonomy x capacity quadrants, split at 0.5)
    if a is None or c is None or pd.isna(a) or pd.isna(c):
        return None
    hi_a, hi_c = a >= 0.5, c >= 0.5
    return {(True, True): "Self-sufficient", (False, True): "Delivery-ready",
            (True, False): "Well-resourced", (False, False): "Support-ready"}[(hi_a, hi_c)]


def _locode_by_code(locode_df):
    by_code = {}
    if locode_df is None:
        return by_code
    for _, r in locode_df.iterrows():
        loc = r.get("locode")
        if loc is None or str(loc).strip() in ("", "None", "nan"):
            continue
        code = str(r.get("comuna_code") or "").strip()
        if code:
            by_code[code] = str(loc).strip()
    return by_code


@transformer
def transform_city_finance_profile(*frames, **kwargs):
    sinim_df, locode_df = None, None
    for df in frames:
        if df is None or not len(df):
            continue
        cols = set(df.columns)
        if "locode" in cols and "comuna_code" in cols:
            locode_df = df
        elif f"fcm_dependency_pct_{Y}" in cols:
            sinim_df = df
    if sinim_df is None:
        raise ValueError("SINIM capacity frame not found upstream")

    c = sinim_df.copy()
    for col in (f"fcm_dependency_pct_{Y}", f"staff_profesional_total_{Y}", f"professionalization_pct_{Y}"):
        c[col] = pd.to_numeric(c[col], errors="coerce")

    c["autonomy"] = (1 - c[f"fcm_dependency_pct_{Y}"] / 100).clip(0, 1)
    pr = lambda s: s.rank(pct=True)
    c["capacity"] = 0.7 * pr(c[f"staff_profesional_total_{Y}"]) + 0.3 * pr(c[f"professionalization_pct_{Y}"])
    c["autonomy"] = c["autonomy"].fillna(c["autonomy"].median())
    c["capacity"] = c["capacity"].fillna(c["capacity"].median())

    by_code = _locode_by_code(locode_df)

    rows = []
    for _, r in c.iterrows():
        cut = str(r.get("comuna_cut") or "").strip()
        actor_id = by_code.get(f"CL{cut.zfill(5)}") if cut else None
        if not actor_id:
            continue  # no locode -> not queryable by the score endpoint; drop
        a, cap = r["autonomy"], r["capacity"]
        rows.append({
            "actor_id": actor_id,
            "autonomy": _numstr(a),
            "capacity": _numstr(cap),
            "city_archetype": _archetype(a, cap),
            "country_code": "CL",
            "source_dataset": SOURCE,
        })

    out = pd.DataFrame(rows, columns=OUT_COLS).drop_duplicates(subset=["actor_id"]).reset_index(drop=True)
    print(f"city_finance_profile: {len(out)} cities (of {len(c)} comunas; {len(c) - len(out)} without a locode)")
    print("  archetype:", out["city_archetype"].value_counts().to_dict())
    return out


@test
def test_output(output, *args) -> None:
    assert output is not None and len(output) > 0, "no city profiles"
    assert output["actor_id"].notna().all(), "actor_id must be non-null (the API key)"
    assert output["actor_id"].is_unique, "actor_id not unique"
    for col in ("autonomy", "capacity"):
        v = pd.to_numeric(output[col], errors="coerce").dropna()
        assert ((v >= 0) & (v <= 1)).all(), f"{col} out of [0,1]"
    bad = set(output["city_archetype"].dropna().unique()) - {
        "Self-sufficient", "Delivery-ready", "Well-resourced", "Support-ready"}
    assert not bad, f"non-canonical city_archetype: {bad}"
