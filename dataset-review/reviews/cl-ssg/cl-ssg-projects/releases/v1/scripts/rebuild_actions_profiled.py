"""
Rebuild actions_profiled.csv to use authoritative fields from actions.json.

Replaces LLM-derived intervention values with the hand-curated `intervention_type`
from actions.json, and adds two new columns:
- `action_role` — "intervention" (action describes a lever) vs "outcome"
  (action describes a goal). Outcome-actions get matched separately in the
  matcher because they're not specific levers.
- `description_es` — Spanish translation of the action description. Used by the
  matcher's TF-IDF tiebreaker, which previously failed on language mismatch.

The LLM-derived `primary_outcome` / `secondary_outcome` stays — actions.json
doesn't have a categorical outcome field (only free-text outcome_summary).

Mapping from actions.json `intervention_type` to a 5-value vocabulary:
    infrastructure  -> infrastructure
    program         -> program
    regulatory      -> regulatory
    planning        -> planning
    financial       -> financial
    None            -> empty (action_role=outcome)

The LLM's 7-value intervention vocab is remapped to the same 5-value scheme
for any secondary_intervention values:
    infrastructure_build, infrastructure_retrofit, tech_deployment -> infrastructure
    program_capacity                                               -> program
    policy_regulation                                              -> regulatory
    planning_assessment                                            -> planning
    financial_incentive                                            -> financial

Usage
-----
    python scripts/rebuild_actions_profiled.py

Writes a .bak next to the existing file before overwriting.
"""

from __future__ import annotations

import csv
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / "data" / "inputs"
DERIVED = ROOT / "data" / "derived"

ACTIONS_JSON = INPUTS / "actions.json"
ACTIONS_PROFILED = DERIVED / "actions_profiled.csv"


# Remap LLM 7-value intervention vocab to actions.json 5-value vocab
LLM_TO_CANONICAL = {
    "infrastructure_build":    "infrastructure",
    "infrastructure_retrofit": "infrastructure",
    "tech_deployment":         "infrastructure",
    "program_capacity":        "program",
    "policy_regulation":       "regulatory",
    "planning_assessment":     "planning",
    "financial_incentive":     "financial",
}


def canonical(value: str) -> str:
    """Map any intervention value to the 5-value canonical vocab."""
    v = (value or "").strip()
    if not v:
        return ""
    return LLM_TO_CANONICAL.get(v, v)  # if it's already canonical, return as-is


def main() -> int:
    if not ACTIONS_JSON.exists():
        print(f"error: {ACTIONS_JSON} not found", file=sys.stderr)
        return 1
    if not ACTIONS_PROFILED.exists():
        print(f"error: {ACTIONS_PROFILED} not found", file=sys.stderr)
        return 1

    # Load actions.json — index by actionId
    actions_json = json.loads(ACTIONS_JSON.read_text(encoding="utf-8"))
    by_id = {a["actionId"]: a for a in actions_json}
    print(f"loaded {len(by_id)} actions from {ACTIONS_JSON.name}")

    # Load existing profiled CSV
    with open(ACTIONS_PROFILED, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        in_fields = list(reader.fieldnames or [])
        rows = list(reader)
    print(f"loaded {len(rows)} rows from {ACTIONS_PROFILED.name}")

    # New columns
    NEW_COLS = ["action_role", "description_es", "outcome_summary",
                "intervention_source"]
    out_fields = list(in_fields)
    for c in NEW_COLS:
        if c not in out_fields:
            out_fields.append(c)

    stats = {
        "from_actions_json": 0,
        "kept_from_llm": 0,
        "outcome_actions": 0,
        "no_match_in_json": 0,
        "secondary_cleared": 0,
    }

    for r in rows:
        aid = (r.get("action_id") or "").strip()
        a = by_id.get(aid)
        if a is None:
            r["intervention_source"] = "llm_only"
            r["primary_intervention"] = canonical(r.get("primary_intervention"))
            r["secondary_intervention"] = ""  # dropped universally
            stats["no_match_in_json"] += 1
            continue

        # Pull authoritative intervention_type from actions.json
        it_json = (a.get("intervention_type") or "").strip()
        role = (a.get("action_role") or "").strip()
        r["action_role"] = role
        r["description_es"] = (a.get("description_i18n", {}) or {}).get("es", "") or ""
        r["outcome_summary"] = a.get("outcome_summary") or ""

        if it_json:
            r["primary_intervention"] = it_json  # already canonical (5-value vocab)
            r["intervention_source"] = "actions_json"
            stats["from_actions_json"] += 1
        elif role == "outcome":
            # Outcome-actions describe a goal, not a lever. Empty intervention.
            r["primary_intervention"] = ""
            r["intervention_source"] = "outcome_action_no_intervention"
            stats["outcome_actions"] += 1
        else:
            # Fall back to LLM value, remapped
            r["primary_intervention"] = canonical(r.get("primary_intervention"))
            r["intervention_source"] = "llm_fallback"
            stats["kept_from_llm"] += 1

        # Drop secondary_intervention on actions. actions.json's intervention_type
        # is meant to be a single authoritative primary; LLM-added secondaries
        # (often "infrastructure") inflate match rates without adding signal.
        # See task: ipcc_0001 winning 664 top-1 matches because of this.
        r["secondary_intervention"] = ""

    # Backup + write
    bak = ACTIONS_PROFILED.with_suffix(ACTIONS_PROFILED.suffix + ".bak")
    shutil.copy2(ACTIONS_PROFILED, bak)
    print(f"backup: {bak}")

    with open(ACTIONS_PROFILED, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote: {ACTIONS_PROFILED}\n")

    print("Summary:")
    print(f"  Actions with intervention from actions.json: {stats['from_actions_json']}")
    print(f"  Outcome-actions (no intervention):           {stats['outcome_actions']}")
    print(f"  Actions kept LLM intervention (fallback):    {stats['kept_from_llm']}")
    print(f"  Actions not found in actions.json:           {stats['no_match_in_json']}")
    sec_cleared = sum(1 for r in rows if not r.get("secondary_intervention"))
    print(f"  Secondary interventions cleared (all actions): {sec_cleared}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
