#!/usr/bin/env python3
"""Evaluate a findings corpus against the manually reviewed specificity fixture."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


V1 = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = V1 / "tests" / "fixtures" / "matching_specificity_regression.json"
DEFAULT_FINDINGS = V1 / "data" / "policy_action_signals"


def evaluate(fixture_path: Path, findings_dir: Path) -> dict:
    cases = json.loads(fixture_path.read_text(encoding="utf-8"))["cases"]
    relevance_correct = 0
    missing_pairs = 0
    accepted_total = accepted_found = accepted_type_correct = 0
    rejected_total = rejected_found = 0
    by_expected_type: dict[str, Counter] = defaultdict(Counter)

    for case in cases:
        path = findings_dir / case["source_document_id"] / f"{case['action_id']}.json"
        expected_type = case["strongest_match_type"]
        by_expected_type[expected_type]["total"] += 1
        if not path.exists():
            missing_pairs += 1
            by_expected_type[expected_type]["missing"] += 1
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("relevance") == case["expected_relevance"]:
            relevance_correct += 1
            by_expected_type[expected_type]["relevance_correct"] += 1
        findings = {row.get("atom_id"): row for row in payload.get("findings", [])}
        for expected in case["accepted"]:
            accepted_total += 1
            finding = findings.get(expected["atom_id"])
            if finding:
                accepted_found += 1
                if finding.get("match_type") == expected["match_type"]:
                    accepted_type_correct += 1
        for atom_id in case["rejected"]:
            rejected_total += 1
            if atom_id in findings:
                rejected_found += 1

    evaluated = len(cases) - missing_pairs
    return {
        "fixture_cases": len(cases),
        "evaluated_pairs": evaluated,
        "missing_pairs": missing_pairs,
        "relevance_exact": relevance_correct,
        "relevance_accuracy": round(relevance_correct / evaluated, 4) if evaluated else 0.0,
        "accepted_atoms": accepted_total,
        "accepted_atom_recall": round(accepted_found / accepted_total, 4) if accepted_total else 0.0,
        "accepted_match_type_accuracy": (
            round(accepted_type_correct / accepted_found, 4) if accepted_found else 0.0
        ),
        "rejected_atoms": rejected_total,
        "rejected_atoms_retained": rejected_found,
        "rejected_atom_retention_rate": (
            round(rejected_found / rejected_total, 4) if rejected_total else 0.0
        ),
        "by_expected_match_type": {
            key: dict(sorted(counts.items())) for key, counts in sorted(by_expected_type.items())
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--findings-dir", type=Path, default=DEFAULT_FINDINGS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate(args.fixture, args.findings_dir)
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
