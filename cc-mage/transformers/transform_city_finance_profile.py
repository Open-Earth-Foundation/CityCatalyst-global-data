"""Project the reviewed v3 city profile into modelled staging.

The S3 input already contains the reviewed capacity and autonomy axes. This block does not
recalculate or impute either value: it validates the 345-comuna release, verifies the existing
0.5 archetype contract, and resolves actor_id from comuna CUT via cl-ocha-ab. The fixed 2021
lookup has four comunas without a locode, so 341 queryable city rows are emitted.
"""

import pandas as pd

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

SOURCE = "oef/cl-city-action-fundability"
EXPECTED_INPUT_ROWS = 345
EXPECTED_OUTPUT_ROWS = 341
PROFILE_COLUMNS = {"comuna_cut", "autonomy", "capacity", "city_archetype"}

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
    profile_df, locode_df = None, None
    for df in frames:
        if df is None or not len(df):
            continue
        cols = set(df.columns)
        if "locode" in cols and "comuna_code" in cols:
            locode_df = df
        elif PROFILE_COLUMNS.issubset(cols):
            profile_df = df
    if profile_df is None:
        raise ValueError("reviewed v3 city-profile frame not found upstream")
    if locode_df is None:
        raise ValueError("cl-ocha-ab locode frame not found upstream")

    c = profile_df.copy()
    c["comuna_cut"] = c["comuna_cut"].astype(str).str.strip().str.zfill(5)
    assert len(c) == EXPECTED_INPUT_ROWS, (
        f"expected {EXPECTED_INPUT_ROWS} reviewed comunas, got {len(c)}"
    )
    assert c["comuna_cut"].is_unique, "comuna_cut not unique in reviewed profile"
    assert c["comuna_cut"].str.fullmatch(r"\d{5}").all(), "invalid comuna_cut"

    for col in ("autonomy", "capacity"):
        c[col] = pd.to_numeric(c[col], errors="coerce")
        assert c[col].notna().all(), f"{col} contains null or non-numeric values"
        assert c[col].between(0, 1).all(), f"{col} outside [0,1]"

    if "_source_dataset" in c.columns:
        source_values = set(c["_source_dataset"].dropna().astype(str).str.strip())
        assert source_values == {SOURCE}, f"unexpected source identity: {source_values}"

    expected_archetype = [
        _archetype(a, cap) for a, cap in zip(c["autonomy"], c["capacity"])
    ]
    actual_archetype = c["city_archetype"].astype(str).str.strip().tolist()
    mismatches = sum(actual != expected for actual, expected in zip(actual_archetype, expected_archetype))
    assert mismatches == 0, f"{mismatches} city_archetype values disagree with the 0.5 bands"

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
            "city_archetype": str(r["city_archetype"]).strip(),
            "country_code": "CL",
            "source_dataset": SOURCE,
        })

    out = pd.DataFrame(rows, columns=OUT_COLS).drop_duplicates(subset=["actor_id"]).reset_index(drop=True)
    print(f"city_finance_profile: {len(out)} cities (of {len(c)} comunas; {len(c) - len(out)} without a locode)")
    print("  archetype:", out["city_archetype"].value_counts().to_dict())
    return out


@test
def test_output(output, *args) -> None:
    assert output is not None, "no city profiles"
    assert len(output) == EXPECTED_OUTPUT_ROWS, (
        f"expected {EXPECTED_OUTPUT_ROWS} locode-resolved profiles, got {len(output)}"
    )
    assert output["actor_id"].notna().all(), "actor_id must be non-null (the API key)"
    assert output["actor_id"].is_unique, "actor_id not unique"
    assert output["source_dataset"].eq(SOURCE).all(), "retired source identity in output"
    for col in ("autonomy", "capacity"):
        v = pd.to_numeric(output[col], errors="coerce").dropna()
        assert ((v >= 0) & (v <= 1)).all(), f"{col} out of [0,1]"
    bad = set(output["city_archetype"].dropna().unique()) - {
        "Self-sufficient", "Delivery-ready", "Well-resourced", "Support-ready"}
    assert not bad, f"non-canonical city_archetype: {bad}"
