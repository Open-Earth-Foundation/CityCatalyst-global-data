"""Clean Project Drawdown Explorer solutions export and crosswalk to SPM.7.

Inputs
------
data/explorer-solutions-table-export.csv
    Drawdown Explorer "Download CSV" export (drawdown.org/explorer).
    NOT stored in the repo (license — see sample/README.md): download it
    from https://drawdown.org/explorer-solutions-table-export.csv to
    data/ before running. Quoted cells contain embedded newlines
    (pollutant lists) and unicode scientific notation ("1.4×10⁷/yr").
    Reviewed capture (2026-06-05): 156 rows, 55 quantified; the export
    mutates in place, so assertions below may fail on a newer capture.
    Do not commit the downloaded file or the regenerated full outputs.
../../../../ipcc/ipcc-ar6-spm7-mitigation-potentials/releases/2023/data/spm7a_mitigation_options_2030_clean.csv

Outputs
-------
data/drawdown_solutions_clean.csv   one row per solution-action, typed columns
data/drawdown_spm7_crosswalk.csv    solution -> SPM.7 option mapping + option-level comparison
stdout                              validation report + Spearman correlations

Run from this directory: python3 drawdown_extract_clean.py
"""

import re
import sys
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).parent
RAW = HERE / "data" / "explorer-solutions-table-export.csv"
SPM7 = (
    HERE
    / "../../../../ipcc/ipcc-ar6-spm7-mitigation-potentials/releases/2023/data/spm7a_mitigation_options_2030_clean.csv"
).resolve()

SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


def parse_number(s):
    """Parse Drawdown numeric strings: '1.4×10⁷/yr', '460,000', '0.085', ''.

    Returns (value: float|None, per_year: bool).
    """
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return None, False
    s = str(s).strip()
    if s in ("", "—"):
        return None, False
    per_year = s.endswith("/yr")
    if per_year:
        s = s[: -len("/yr")]
    s = s.replace(",", "").strip()
    m = re.fullmatch(r"(-?[\d.]+)×10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)", s)
    if m:
        mantissa = float(m.group(1))
        exp = int(m.group(2).translate(SUPERSCRIPTS))
        return mantissa * 10**exp, per_year
    return float(s), per_year


def parse_range(s):
    """Parse 'A to B[/yr]' -> (low, high, per_year)."""
    if s is None or (isinstance(s, float) and pd.isna(s)) or str(s).strip() in ("", "—"):
        return None, None, False
    s = str(s).strip()
    per_year = s.endswith("/yr")
    if per_year:
        s = s[: -len("/yr")]
    parts = s.split(" to ")
    assert len(parts) == 2, f"unparseable range: {s!r}"
    lo, _ = parse_number(parts[0])
    hi, _ = parse_number(parts[1])
    return lo, hi, per_year


def norm_text(s):
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return None
    return re.sub(r"\s+", " ", str(s)).strip() or None


# Solution-level mapping to SPM.7 options (adjudicated 2026-06-05, Amanda's
# review session). Key: (Action, Solution). None = no SPM.7 counterpart.
TO_SPM7 = {
    ("Deploy", "Utility-Scale Solar PV"): "Solar",
    ("Deploy", "Onshore Wind Turbines"): "Wind",
    ("Deploy", "Offshore Wind Turbines"): "Wind",
    ("Manage", "Coal Mine Methane"): "Reduce CH4 from coal, oil and gas",
    ("Manage", "Oil & Gas Methane"): "Reduce CH4 from coal, oil and gas",
    ("Protect", "Forests: Boreal"): "Reduce conversion of natural ecosystems",
    ("Protect", "Forests: Temperate"): "Reduce conversion of natural ecosystems",
    ("Protect", "Forests: Subtropical"): "Reduce conversion of natural ecosystems",
    ("Protect", "Forests: Tropical"): "Reduce conversion of natural ecosystems",
    ("Protect", "Grasslands & Savannas: Boreal"): "Reduce conversion of natural ecosystems",
    ("Protect", "Grasslands & Savannas: Temperate"): "Reduce conversion of natural ecosystems",
    ("Protect", "Grasslands & Savannas: Subtropical"): "Reduce conversion of natural ecosystems",
    ("Protect", "Grasslands & Savannas: Tropical"): "Reduce conversion of natural ecosystems",
    ("Protect", "Peatlands: Boreal"): "Reduce conversion of natural ecosystems",
    ("Protect", "Peatlands: Temperate"): "Reduce conversion of natural ecosystems",
    ("Protect", "Peatlands: Subtropical"): "Reduce conversion of natural ecosystems",
    ("Protect", "Peatlands: Tropical"): "Reduce conversion of natural ecosystems",
    ("Protect", "Coastal Wetlands: Mangrove ecosystems"): "Reduce conversion of natural ecosystems",
    ("Protect", "Coastal Wetlands: Salt marsh ecosystems"): "Reduce conversion of natural ecosystems",
    ("Protect", "Coastal Wetlands: Seagrass ecosystems"): "Reduce conversion of natural ecosystems",
    ("Protect", "Seaweed Ecosystems"): "Reduce conversion of natural ecosystems",
    ("Restore", "Forests: Boreal"): "Ecosystem restoration, afforestation, reforestation",
    ("Restore", "Forests: Temperate"): "Ecosystem restoration, afforestation, reforestation",
    ("Restore", "Forests: Subtropical"): "Ecosystem restoration, afforestation, reforestation",
    ("Restore", "Forests: Tropical"): "Ecosystem restoration, afforestation, reforestation",
    ("Improve", "Annual Cropping"): "Carbon sequestration in agriculture",
    ("Deploy", "Silvopasture"): "Carbon sequestration in agriculture",
    ("Improve", "Diets"): "Shift to sustainable healthy diets",
    ("Reduce", "Food Loss & Waste"): "Reduce food loss and food waste",
    ("Improve", "Nutrient Management"): "Reduce CH4 and N2O in agriculture",
    ("Improve", "Rice Production"): "Reduce CH4 and N2O in agriculture",
    ("Use", "Heat Pumps"): "Efficient buildings",
    ("Improve", "Windows & Glass"): "Efficient buildings",
    ("Deploy", "Alternative Insulation Materials"): "Efficient buildings",
    ("Mobilize", "Electric Cars"): "Electric vehicles",
    ("Mobilize", "Hybrid Cars"): "Fuel efficient vehicles",
    ("Enhance", "Public Transit"): "Public transport and bicycling",
    ("Improve", "Nonmotorized Transportation"): "Public transport and bicycling",
    ("Mobilize", "Electric Bicycles: Private electric bicycles"): "Public transport and bicycling",
    ("Mobilize", "Electric Bicycles: Shared electric bicycles"): "Public transport and bicycling",
    ("Increase", "Carpooling"): "Avoid demand for energy services",
    ("Deploy", "LED Lighting"): "Efficient lighting, appliances and equipment",
    ("Improve", "Cement Production: Clinker substitution"): "Construction materials substitution",
    ("Improve", "Cement Production: Alternative fuels"): "Fuel switching",
    ("Improve", "Cement Production: Efficiency upgrades"): "Energy efficiency",
    ("Deploy", "Industrial Green Hydrogen"): "Fuel switching",
    ("Increase", "Recycling: Metals"): "Enhanced recycling",
    ("Increase", "Recycling: Paper and Cardboard"): "Enhanced recycling",
    ("Increase", "Recycling: Plastics"): "Enhanced recycling",
    ("Increase", "Recycling: Glass"): "Enhanced recycling",
    ("Increase", "Centralized Composting"): "Reduce CH4 from waste/wastewater",
    ("Improve", "Landfill Management: Methane capture"): "Reduce CH4 from waste/wastewater",
    ("Improve", "Landfill Management: Biocovers"): "Reduce CH4 from waste/wastewater",
    ("Deploy", "Alternative Refrigerants"): "Reduce emission of fluorinated gas",
    ("Deploy", "Clean Cooking"): None,  # no SPM.7 counterpart
}

CLASSIFICATIONS = {"Highly Recommended", "Worthwhile", "Keep Watching", "Not Recommended"}


def main():
    raw = pd.read_csv(RAW, dtype=str)
    assert list(raw.columns)[:7] == [
        "Action", "Solution", "Solution Classification", "Mode", "Sector",
        "Cluster", "Adoption Unit",
    ], raw.columns.tolist()
    assert raw.shape[1] == 17, raw.shape
    bad = set(raw["Solution Classification"].dropna()) - CLASSIFICATIONS
    assert not bad, bad

    rows = []
    for _, r in raw.iterrows():
        unit = norm_text(r["Adoption Unit"])
        ghg_lo, ghg_hi, _ = parse_range(r["GHG Impact Gt CO₂-eq (100‑yr)/yr"])
        if unit == "Coming Soon":
            status = "coming_soon"
        elif ghg_lo is not None:
            status = "quantified"
        else:
            status = "tier_only"
        eff, eff_yr = parse_number(r["Effectiveness t CO₂‑eq (100-yr)/unit"])
        cur, cur_yr = parse_number(r["Adoption Current"])
        ad_lo, ad_hi, ad_yr = parse_range(r["Adoption Achievable Range"])
        cost, _ = parse_number(r["Cost US$ per t CO₂‑eq"])

        flags = []
        if status == "quantified":
            if cost is None:
                flags.append("cost_missing")
            if ghg_lo == ghg_hi:
                flags.append("degenerate_range")
            if ghg_hi is not None and ghg_hi < 0.005:
                flags.append("negligible_impact")
        rows.append(
            {
                "action": norm_text(r["Action"]),
                "solution": norm_text(r["Solution"]),
                "classification": norm_text(r["Solution Classification"]),
                "mode": norm_text(r["Mode"]),
                "sector": norm_text(r["Sector"]),
                "cluster": norm_text(r["Cluster"]),
                "status": status,
                "adoption_unit": None if unit == "Coming Soon" else unit,
                "effectiveness_tco2e_per_unit": eff,
                "effectiveness_per_year": eff_yr,
                "adoption_current": cur,
                "adoption_current_per_year": cur_yr,
                "adoption_achievable_low": ad_lo,
                "adoption_achievable_high": ad_hi,
                "adoption_achievable_per_year": ad_yr,
                "ghg_impact_low_gt": ghg_lo,
                "ghg_impact_high_gt": ghg_hi,
                "ghg_impact_mid_gt": None if ghg_lo is None else round((ghg_lo + ghg_hi) / 2, 3),
                "cost_usd_per_tco2e": cost,
                "pollutants": norm_text(r["Climate Pollutants Mitigated"]),
                "speed_of_action": norm_text(r["Speed of Action"]),
                "adaptation_benefits": norm_text(r["Climate Adaptation Benefits"]),
                "environment_benefits": norm_text(r["Environment Benefits"]),
                "wellbeing_benefits": norm_text(r["Human Well-being Benefits"]),
                "flags": ";".join(flags) or None,
            }
        )
    clean = pd.DataFrame(rows)
    clean.to_csv(HERE / "data" / "drawdown_solutions_clean.csv", index=False)

    q = clean[clean.status == "quantified"].copy()
    print(f"rows total={len(clean)} quantified={len(q)} "
          f"tier_only={(clean.status == 'tier_only').sum()} "
          f"coming_soon={(clean.status == 'coming_soon').sum()}")
    print("by classification:")
    print(clean.groupby(["classification", "status"]).size().to_string())

    # internal consistency: effectiveness × achievable adoption ≈ GHG impact
    # (units vary; check only order-of-magnitude agreement where both ends parse)
    chk = q.dropna(subset=["effectiveness_tco2e_per_unit", "adoption_achievable_low"]).copy()
    implied_lo = chk.effectiveness_tco2e_per_unit * chk.adoption_achievable_low / 1e9
    ratio = implied_lo / chk.ghg_impact_low_gt
    ok = ratio.between(0.5, 2.0)
    print(f"\neffectiveness×adoption vs GHG impact (low end): {ok.sum()}/{len(chk)} within 2x")
    for _, r in chk[~ok].iterrows():
        print(f"  off: {r.action} {r.solution}: implied {implied_lo[r.name]:.3f} "
              f"vs stated {r.ghg_impact_low_gt}")

    # ---- crosswalk ----
    q["spm7_option"] = q.apply(lambda r: TO_SPM7.get((r.action, r.solution), "UNMAPPED"), axis=1)
    missing = q[q.spm7_option == "UNMAPPED"]
    assert missing.empty, missing[["action", "solution"]]

    spm7 = pd.read_csv(SPM7)
    agg = (
        q[q.spm7_option.notna()]
        .groupby("spm7_option")
        .agg(
            dd_n_solutions=("solution", "size"),
            dd_impact_low_gt=("ghg_impact_low_gt", "sum"),
            dd_impact_high_gt=("ghg_impact_high_gt", "sum"),
            dd_impact_mid_gt=("ghg_impact_mid_gt", "sum"),
        )
        .reset_index()
    )
    comp = agg.merge(
        spm7[["option", "total", "unc_low", "unc_high"]].rename(
            columns={"option": "spm7_option", "total": "spm7_total_gt",
                     "unc_low": "spm7_unc_low", "unc_high": "spm7_unc_high"}
        ),
        on="spm7_option",
        how="left",
    )
    assert comp.spm7_total_gt.notna().all(), comp[comp.spm7_total_gt.isna()]

    rho_mid, p_mid = spearmanr(comp.dd_impact_mid_gt, comp.spm7_total_gt)
    rho_hi, p_hi = spearmanr(comp.dd_impact_high_gt, comp.spm7_total_gt)
    print(f"\nmatched SPM.7 options: {len(comp)} (from {q.spm7_option.notna().sum()} solutions)")
    print(f"Spearman dd_mid  vs spm7_total: {rho_mid:.2f} (p={p_mid:.4f})")
    print(f"Spearman dd_high vs spm7_total: {rho_hi:.2f} (p={p_hi:.4f})")

    spm7_unmatched = set(spm7.option) - set(comp.spm7_option)
    print(f"\nSPM.7 options with no quantified Drawdown counterpart ({len(spm7_unmatched)}):")
    for o in sorted(spm7_unmatched):
        print(f"  - {o}")

    # per-solution crosswalk rows, then option-level comparison rows
    xwalk = q[
        ["action", "solution", "spm7_option", "ghg_impact_low_gt",
         "ghg_impact_high_gt", "ghg_impact_mid_gt", "cost_usd_per_tco2e"]
    ].sort_values(["spm7_option", "solution"])
    xwalk.to_csv(HERE / "data" / "drawdown_spm7_crosswalk.csv", index=False)
    comp.sort_values("spm7_total_gt", ascending=False).to_csv(
        HERE / "data" / "drawdown_spm7_option_comparison.csv", index=False
    )
    print("\nwrote drawdown_solutions_clean.csv, drawdown_spm7_crosswalk.csv, "
          "drawdown_spm7_option_comparison.csv")
    print("\noption-level comparison (Gt CO2-eq/yr):")
    print(
        comp.sort_values("spm7_total_gt", ascending=False)[
            ["spm7_option", "dd_n_solutions", "dd_impact_mid_gt", "spm7_total_gt"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    sys.exit(main())
