"""
Build a stratified QA evaluation sample for the faceted matcher's output.

Stratifies across the matcher's top-label tiers and produces a wide-format CSV
with project info + facets + EN narrative + top-3 candidates per row, plus
empty QA columns for human grading.

Strata and default counts (total 60)
-------------------------------------
- strong                              : 15
- compatible_context                  : 10  (full population is small)
- library_gap_adaptation              : 10
- library_gap_transport_continuity    : 10
- skip_not_climate                    :  5
- goal_aligned + wrong_scope + unrelated + unmatched_taxonomy (other) : 10

Outputs
-------
- data/qa/matching_eval_sample_v2.csv        the eval CSV
- data/qa/actions_reference.csv              action_id lookup for annotators

Usage
-----
    python scripts/build_qa_eval.py
    python scripts/build_qa_eval.py --size 120
    python scripts/build_qa_eval.py --seed 7
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
INPUTS = DATA / "inputs"
DERIVED = DATA / "derived"
QA = DATA / "qa"

PROJECTS_PROFILED = DERIVED / "projects_profiled.csv"
ACTIONS_PROFILED  = DERIVED / "actions_profiled.csv"
MATCHES           = DERIVED / "project_action_matches.csv"
TRANSLATED        = DERIVED / "ficha_idi_table_translated.csv"

OUT_EVAL = QA / "matching_eval_sample_v2.csv"
OUT_REF  = QA / "actions_reference.csv"

# Stratification: strata in priority order, fall through to "other" if a
# stratum is empty.
DEFAULT_STRATA = [
    ("strong",                              15),
    ("compatible_context",                  10),
    ("library_gap_adaptation",              10),
    ("library_gap_transport_continuity",    10),
    ("skip_not_climate",                     5),
    ("other",                               10),  # goal_aligned / wrong_scope / unrelated / unmatched_taxonomy
]

OTHER_LABELS = {"goal_aligned", "wrong_scope", "unrelated", "unmatched_taxonomy"}

NARRATIVE_FIELDS = [
    "justification_en", "justification_es",
    "description_en",   "description_es",
    "purpose_en",       "purpose_es",
    "components_en",    "components_es",
    "conclusions_en",   "conclusions_es",
    "funding_breakdown",
]


def load_csv(p: Path) -> list[dict]:
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _narrative_score(r: dict) -> int:
    return sum(1 for f in NARRATIVE_FIELDS if (r.get(f) or "").strip())


def _parse_int(s: str) -> int:
    try:
        return int(s)
    except (TypeError, ValueError):
        return 0


def load_translated_lookup() -> dict[str, dict]:
    if not TRANSLATED.exists():
        return {}
    by_bip: dict[str, list[dict]] = defaultdict(list)
    for r in load_csv(TRANSLATED):
        code = (r.get("bip_code") or "").strip()
        if code:
            by_bip[code].append(r)
    chosen = {}
    for code, cands in by_bip.items():
        ranked = sorted(cands, key=lambda r: (
            r.get("template_variant") != "STUB",
            _narrative_score(r),
            _parse_int(r.get("budget_year", "")),
        ), reverse=True)
        chosen[code] = ranked[0]
    return chosen


def group_matches_by_project(rows: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        grouped[r["codigo_bip"]].append(r)
    for cb in grouped:
        grouped[cb].sort(key=lambda r: _parse_int(r["rank"]))
    return grouped


def top_label_for(rows: list[dict]) -> str:
    rank1 = [r for r in rows if r["rank"] == "1"]
    if rank1:
        return rank1[0]["label"]
    sentinel = [r for r in rows if r["rank"] == "0"]
    if sentinel:
        return sentinel[0]["label"]
    return ""


def stratify(projects_by_bip: dict[str, dict],
             matches_by_bip: dict[str, list[dict]],
             strata: list[tuple[str, int]],
             seed: int) -> list[str]:
    """Pick codigo_bip values, stratified by top-label tier."""
    rng = random.Random(seed)
    # Bucket every codigo_bip by its top label.
    buckets: dict[str, list[str]] = defaultdict(list)
    for cb in projects_by_bip:
        ms = matches_by_bip.get(cb, [])
        lbl = top_label_for(ms)
        if not lbl:
            continue
        if lbl in {s for s, _ in strata if s != "other"}:
            buckets[lbl].append(cb)
        elif lbl in OTHER_LABELS:
            buckets["other"].append(cb)
        else:
            # Unrecognised label, drop into other so it gets coverage
            buckets["other"].append(cb)

    picks: list[str] = []
    for stratum, n in strata:
        bucket = buckets.get(stratum, [])
        if not bucket:
            print(f"  warning: stratum '{stratum}' is empty; skipping", file=sys.stderr)
            continue
        take = min(n, len(bucket))
        if take < n:
            print(f"  note: stratum '{stratum}' has {len(bucket)} rows, sampling all", file=sys.stderr)
        picks.extend(rng.sample(bucket, take))
    return picks


def build_row(sample_id: str,
              project: dict,
              matches: list[dict],
              translated_row: dict) -> dict:
    rank1 = [r for r in matches if r["rank"] == "1"]
    rank2 = [r for r in matches if r["rank"] == "2"]
    rank3 = [r for r in matches if r["rank"] == "3"]
    sentinel = [r for r in matches if r["rank"] == "0"]

    top_label = (rank1[0]["label"] if rank1 else
                 sentinel[0]["label"] if sentinel else "")

    row = {
        "sample_id":                          sample_id,
        "codigo_bip":                         project["codigo_bip"],
        "nombre":                             project.get("nombre", ""),
        "project_sector":                     project.get("sector", ""),
        "project_subsector":                  project.get("subsector", ""),
        "project_has_ficha_data":             project.get("has_ficha_data", ""),
        "project_climate_classification_es":  project.get("climate_classification_es", ""),
        # Profile facets
        "project_climate_relevance":          project.get("climate_relevance", ""),
        "project_primary_outcome":            project.get("primary_outcome", ""),
        "project_secondary_outcome":          project.get("secondary_outcome", ""),
        "project_primary_intervention":       project.get("primary_intervention", ""),
        "project_secondary_intervention":     project.get("secondary_intervention", ""),
        "project_confidence":                 project.get("confidence", ""),
        "project_reasoning":                  project.get("reasoning", ""),
        # Narrative (ES + EN) from the translated table for the best etapa
        "project_justificacion_es":           (translated_row.get("justification_es") or "").strip(),
        "project_justificacion_en":           (translated_row.get("justification_en") or "").strip(),
        "project_descripcion_etapa_es":       (translated_row.get("description_es") or "").strip(),
        "project_descripcion_etapa_en":       (translated_row.get("description_en") or "").strip(),
        "project_componentes_text_es":        (translated_row.get("components_es") or "").strip(),
        "project_componentes_text_en":        (translated_row.get("components_en") or "").strip(),
        "project_proposito_es":               (translated_row.get("purpose_es") or "").strip(),
        "project_proposito_en":               (translated_row.get("purpose_en") or "").strip(),
        "project_conclusions_es":             (translated_row.get("conclusions_es") or "").strip(),
        "project_funding_breakdown":          (translated_row.get("funding_breakdown") or "").strip(),
        # Matcher-assigned top label per project (sentinel or rank-1)
        "matcher_top_label":                  top_label,
    }

    def fill_candidate(prefix: str, cand_list: list[dict]) -> None:
        c = cand_list[0] if cand_list else None
        row[f"{prefix}_action_id"]            = c["action_id"] if c else ""
        row[f"{prefix}_action_name"]          = c["action_name"] if c else ""
        row[f"{prefix}_action_role"]          = c["action_role"] if c else ""
        row[f"{prefix}_label"]                = c["label"] if c else ""
        row[f"{prefix}_outcome_overlap"]      = c["outcome_overlap"] if c else ""
        row[f"{prefix}_intervention_overlap"] = c["intervention_overlap"] if c else ""
        row[f"{prefix}_outcome_shared"]       = c["outcome_shared"] if c else ""
        row[f"{prefix}_intervention_shared"]  = c["intervention_shared"] if c else ""
        row[f"{prefix}_tfidf_score"]          = c["tfidf_score"] if c else ""

    fill_candidate("candidate_1", rank1)
    fill_candidate("candidate_2", rank2)
    fill_candidate("candidate_3", rank3)

    # QA columns (blank, to be filled by annotator)
    row["qa_climate_relevance_correct"]    = ""    # Y / N / partial
    row["qa_climate_relevance_correction"] = ""    # free text if wrong
    row["qa_project_outcome_correct"]      = ""    # Y / N
    row["qa_project_outcome_correction"]   = ""    # free text if wrong
    row["qa_project_intervention_correct"] = ""    # Y / N
    row["qa_project_intervention_correction"] = "" # free text if wrong
    row["qa_candidate_1_label_correct"]    = ""    # Y / N — is the auto-computed label right?
    row["qa_candidate_2_label_correct"]    = ""
    row["qa_candidate_3_label_correct"]    = ""
    row["qa_best_action_id"]               = ""    # the action_id you think is the best match (or blank if no good match)
    row["qa_notes"]                        = ""

    return row


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", type=int, default=60,
                    help="Total sample size (will scale strata proportionally). Default 60.")
    ap.add_argument("--seed", type=int, default=42,
                    help="Random seed for reproducibility.")
    ap.add_argument("--out", type=Path, default=OUT_EVAL,
                    help="Output eval CSV path.")
    ap.add_argument("--actions-ref-out", type=Path, default=OUT_REF,
                    help="Output actions reference CSV path.")
    args = ap.parse_args()

    # Scale strata proportionally if size != 60.
    scale = args.size / 60
    strata = [(s, max(1, round(n * scale))) for s, n in DEFAULT_STRATA]
    print(f"target sample size {sum(n for _, n in strata)} (strata: {strata})\n")

    # --- Load ---
    if not PROJECTS_PROFILED.exists():
        print(f"error: {PROJECTS_PROFILED} not found", file=sys.stderr); return 1
    if not MATCHES.exists():
        print(f"error: {MATCHES} not found — run scripts/06_match_to_actions.py first",
              file=sys.stderr); return 1

    projects = load_csv(PROJECTS_PROFILED)
    projects_by_bip = {p["codigo_bip"]: p for p in projects}
    print(f"loaded {len(projects)} projects")

    matches = load_csv(MATCHES)
    matches_by_bip = group_matches_by_project(matches)
    print(f"loaded {len(matches)} match rows for {len(matches_by_bip)} projects")

    translated = load_translated_lookup()
    print(f"loaded narrative for {len(translated)} projects\n")

    # --- Stratify & sample ---
    picks = stratify(projects_by_bip, matches_by_bip, strata, args.seed)
    print(f"sampled {len(picks)} projects\n")

    # --- Build rows ---
    out_rows = []
    for i, cb in enumerate(picks, start=1):
        sample_id = f"S{i:03d}"
        p = projects_by_bip[cb]
        ms = matches_by_bip.get(cb, [])
        t = translated.get(cb, {})
        out_rows.append(build_row(sample_id, p, ms, t))

    # --- Write eval CSV ---
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(out_rows[0].keys()) if out_rows else []
    with open(args.out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)
    print(f"wrote {args.out}")

    # --- Write actions reference CSV ---
    actions = load_csv(ACTIONS_PROFILED)
    ref_fields = ["action_id", "action_name", "action_role", "subsector_number",
                  "primary_outcome", "secondary_outcome",
                  "primary_intervention", "secondary_intervention",
                  "outcome_summary"]
    ref_rows = [{k: a.get(k, "") for k in ref_fields} for a in actions]
    with open(args.actions_ref_out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ref_fields)
        w.writeheader()
        w.writerows(ref_rows)
    print(f"wrote {args.actions_ref_out}")

    # --- Summary ---
    from collections import Counter
    print("\nFinal sample composition:")
    for lbl, n in Counter(r["matcher_top_label"] for r in out_rows).most_common():
        print(f"  {lbl}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
