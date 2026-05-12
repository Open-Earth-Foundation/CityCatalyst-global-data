"""
Deterministic post-processing for data/derived/projects_profiled.csv.

Applies two corrections that the LLM profiler doesn't reliably handle:

1.  **Confidence demote.** Projects with ``has_ficha_data=False`` only have
    nombre + sector + climate_classification_es as input — no narrative. The
    profiler tends to mark these ``confidence=high`` regardless. We demote
    any such row to ``confidence=low`` deterministically and append a note
    to ``reasoning`` so the override is auditable.

2.  **Intervention fill.** Projects with ``climate_relevance`` in
    {mitigation, adaptation, mixed} but an empty ``primary_intervention``
    get filled with ``infrastructure`` (the dominant intervention for these
    projects) and tagged. Projects with ``climate_relevance`` in
    {not_climate, unclear} are left unchanged — empty interventions are
    correct there.

Writes a ``.bak`` before overwriting.

Usage
-----
    python scripts/post_process_projects_profiled.py
    python scripts/post_process_projects_profiled.py --dry-run
"""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_PROFILED = ROOT / "data" / "derived" / "projects_profiled.csv"

DEMOTE_TAG = "[auto-demoted: no ficha narrative]"
FILL_TAG = "[auto-filled: intervention defaulted]"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true",
                    help="Report counts without writing.")
    args = ap.parse_args()

    if not PROJECTS_PROFILED.exists():
        print(f"error: {PROJECTS_PROFILED} not found", file=sys.stderr)
        return 1

    with open(PROJECTS_PROFILED, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    print(f"loaded {len(rows)} rows from {PROJECTS_PROFILED.name}\n")

    stats = {
        "confidence_demoted": 0,
        "intervention_filled": 0,
        "already_correct": 0,
    }
    pre_conf = Counter(r.get("confidence", "") for r in rows)
    pre_int = Counter(r.get("primary_intervention", "") for r in rows)

    for r in rows:
        has_ficha = (r.get("has_ficha_data") or "").strip()
        conf = (r.get("confidence") or "").strip()
        cr = (r.get("climate_relevance") or "").strip()
        pi = (r.get("primary_intervention") or "").strip()

        # Rule 1: demote confidence for no-narrative rows.
        if has_ficha == "False" and conf == "high":
            r["confidence"] = "low"
            existing = r.get("reasoning") or ""
            if DEMOTE_TAG not in existing:
                r["reasoning"] = (existing + " " + DEMOTE_TAG).strip()
            stats["confidence_demoted"] += 1

        # Rule 2: fill empty intervention for projects that should have one.
        if not pi and cr in ("mitigation", "adaptation", "mixed"):
            r["primary_intervention"] = "infrastructure"
            existing = r.get("reasoning") or ""
            if FILL_TAG not in existing:
                r["reasoning"] = (existing + " " + FILL_TAG).strip()
            stats["intervention_filled"] += 1

    print("=== Rule 1: confidence demote (has_ficha_data=False AND confidence=high) ===")
    print(f"  rows demoted: {stats['confidence_demoted']}\n")

    print("=== Rule 2: intervention fill (climate_relevance in {mit, adp, mixed} AND empty intervention) ===")
    print(f"  rows filled with 'infrastructure': {stats['intervention_filled']}\n")

    print("=== Confidence distribution BEFORE / AFTER ===")
    post_conf = Counter(r.get("confidence", "") for r in rows)
    for k in sorted(set(pre_conf) | set(post_conf)):
        print(f"  {k or '<empty>':<10} {pre_conf.get(k,0):>5}  ->  {post_conf.get(k,0):>5}")

    print("\n=== Intervention distribution BEFORE / AFTER ===")
    post_int = Counter(r.get("primary_intervention", "") for r in rows)
    for k in sorted(set(pre_int) | set(post_int)):
        print(f"  {k or '<empty>':<18} {pre_int.get(k,0):>5}  ->  {post_int.get(k,0):>5}")

    if args.dry_run:
        print("\n(dry-run; no output written)")
        return 0

    bak = PROJECTS_PROFILED.with_suffix(PROJECTS_PROFILED.suffix + ".bak")
    shutil.copy2(PROJECTS_PROFILED, bak)
    print(f"\nbackup: {bak}")

    with open(PROJECTS_PROFILED, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote: {PROJECTS_PROFILED}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
