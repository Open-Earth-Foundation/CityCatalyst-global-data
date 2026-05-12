"""
Add review-hint columns to data/qa/matching_eval_sample_v2.csv based on
heuristics for known matcher failure patterns. Preserves all existing data
including any partial QA grading.

Adds three columns (appended at the right of the schema):

- ``auto_review_flag``      one of the keys in PATTERNS below, or ''
- ``auto_review_note``      one-line explanation
- ``suggested_action_id``   the action_id we'd expect instead, if applicable

Heuristics target patterns surfaced during diagnostic review:

1.  ``landfill_should_match_c40_0036`` — project name matches landfill/dump
    keywords and candidate_1 isn't c40_0036.
2.  ``recycling_should_not_match_eco_park`` — recycling / composting /
    waste-truck projects matched to icare_0122 (eco-parks). The action library
    has narrower waste actions that fit better.
3.  ``park_misclassified_as_waste`` — urban park projects landed on
    emissions_waste_diversion outcome. Project-profile error upstream.
4.  ``maintenance_should_be_transport_continuity`` — REPOSICION / CONSERVACION
    on transit assets classified as modal_shift (should be transport_continuity).
5.  ``ecopark_match_seems_fair`` — project name contains ECOPARQUE / CENTRO
    INTEGRAL DE TRATAMIENTO — the icare_0122 match might be defensible here.

Writes a .bak before overwriting.
"""

from __future__ import annotations

import csv
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "data" / "qa" / "matching_eval_sample_v2.csv"

NEW_COLS = ["auto_review_flag", "auto_review_note", "suggested_action_id"]


def name_matches(name: str, keywords: list[str]) -> bool:
    n = name.upper()
    return any(re.search(rf"\b{re.escape(k)}\b", n) for k in keywords)


LANDFILL_KEYWORDS = ["RELLENO", "VERTEDERO"]
PARK_KEYWORDS = ["PARQUE URBANO", "AREA VERDE", "ÁREA VERDE", "ESPACIO PUBLICO", "ESPACIO PÚBLICO"]
ECOPARK_DEFENSIBLE = ["ECOPARQUE", "ECO-PARQUE", "ECO PARQUE",
                      "CENTRO INTEGRAL DE TRATAMIENTO",
                      "MECANICO Y BIOLOGICO", "MECÁNICO Y BIOLÓGICO"]
RECYCLING_KEYWORDS = ["RECICLAJE", "RECICLABLE", "VALORIZACION", "VALORIZACIÓN",
                      "COMPOST", "VERMICOMPOST", "CAMION", "CAMIÓN",
                      "CONTENEDOR", "CENTRO DE ACOPIO", "PUNTO LIMPIO"]
TRANSIT_MAINTENANCE_KEYWORDS = ["METRO", "FERROVIARIO", "FFCC", "TREN"]
MAINTENANCE_PREFIXES = ["REPOSICION", "REPOSICIÓN", "CONSERVACION", "CONSERVACIÓN",
                        "MANTENIMIENTO", "MEJORAMIENTO"]


def classify(row: dict) -> tuple[str, str, str]:
    """Return (flag, note, suggested_action_id). Empty strings if no pattern hits."""
    name = row.get("nombre", "") or ""
    cand1 = row.get("candidate_1_action_id", "")
    cand1_label = row.get("candidate_1_label", "")
    project_outcome = row.get("project_primary_outcome", "")
    matcher_top = row.get("matcher_top_label", "")

    # --- 1. Landfill should match c40_0036 ---
    if name_matches(name, LANDFILL_KEYWORDS):
        if cand1 and cand1 != "c40_0036":
            return ("landfill_should_match_c40_0036",
                    f"Project mentions landfill/vertedero; closest action is c40_0036 (Upgrade Landfills with Gas Capture). Matched to {cand1} instead.",
                    "c40_0036")

    # --- 2. Recycling / composting / waste-truck projects to eco-park ---
    if cand1 == "icare_0122":
        if name_matches(name, RECYCLING_KEYWORDS) and not name_matches(name, ECOPARK_DEFENSIBLE):
            return ("recycling_should_not_match_eco_park",
                    "Project is recycling / composting / waste collection — not an integrated eco-park MBT facility. Library has narrower actions (c40_0035, icare_0053, icare_0064) but they may still not fit perfectly.",
                    "")

    # --- 3. Urban park misclassified as waste ---
    if project_outcome == "emissions_waste_diversion" and name_matches(name, PARK_KEYWORDS):
        return ("park_misclassified_as_waste",
                "Project name suggests an urban park; profiler classified it as waste_diversion. Likely a project-profiling error — outcome should be carbon_sequestration or resilience_other.",
                "")

    # --- 4. Maintenance/replacement matched as modal_shift ---
    if project_outcome == "emissions_modal_shift":
        name_upper = name.upper()
        starts_with_maintenance = any(name_upper.startswith(p) for p in MAINTENANCE_PREFIXES)
        transit_asset = name_matches(name, TRANSIT_MAINTENANCE_KEYWORDS)
        if starts_with_maintenance and transit_asset:
            return ("maintenance_should_be_transport_continuity",
                    "Project is maintenance/replacement on existing transit infrastructure — should be transport_continuity, not modal_shift.",
                    "")

    # --- 5. Defensible eco-park match (positive flag, to help annotator confirm) ---
    if cand1 == "icare_0122" and name_matches(name, ECOPARK_DEFENSIBLE):
        return ("ecopark_match_seems_fair",
                "Project name matches integrated waste-treatment facility / eco-park description — icare_0122 may be a reasonable match.",
                "")

    return ("", "", "")


def main() -> int:
    if not EVAL.exists():
        print(f"error: {EVAL} not found", file=sys.stderr)
        return 1

    with open(EVAL, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    print(f"loaded {len(rows)} rows from {EVAL.name}")

    out_fields = list(fields)
    for c in NEW_COLS:
        if c not in out_fields:
            out_fields.append(c)

    flag_counts = Counter()
    for r in rows:
        flag, note, suggested = classify(r)
        r["auto_review_flag"] = flag
        r["auto_review_note"] = note
        r["suggested_action_id"] = suggested
        flag_counts[flag or "(none)"] += 1

    bak = EVAL.with_suffix(EVAL.suffix + ".bak")
    shutil.copy2(EVAL, bak)
    print(f"backup: {bak}")

    with open(EVAL, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {EVAL}\n")

    print("Flag distribution:")
    for k, v in flag_counts.most_common():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
