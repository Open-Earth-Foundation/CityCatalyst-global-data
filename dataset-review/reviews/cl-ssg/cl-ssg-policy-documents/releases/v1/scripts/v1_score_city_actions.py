#!/usr/bin/env python3
"""Phase 4: score (city, action) pairs from policy_action_signals + applicability.

Implements releases/v1/design/scoring_rubric.md (rubric_version 0.3.0).

v0.2.0 changes from v0.1.0:
  - SATURATION_K raised from 2.0 to 4.0 (less aggressive saturation)
  - Relevance cap: best_relevance across applicable docs caps score_raw.
    none -> 0.0, low -> 0.32, medium -> 0.65, high -> uncapped.

Usage:
  # Pilot: all actions for Aysén communes (region 11), all applicable docs with findings
  python v1_score_city_actions.py --region-code 11

  # PARCC-only slice (regional doc contribution only; same score for every city in region)
  python v1_score_city_actions.py --region-code 11 --doc-filter chl_parcc_aysen_2025

  # One city, one action
  python v1_score_city_actions.py --city-code 11101 --action ipcc_0053
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

RUBRIC_VERSION = "0.3.0"
SATURATION_K = 4.0
TOP_EVIDENCE_N = 5

CONFIDENCE_WEIGHT = {"high": 1.00, "medium": 0.60, "low": 0.30}
RELATION_WEIGHT = {
    "commits": 1.00,
    "targets": 1.00,
    "funds": 1.00,
    "monitors": 0.80,
    "governs": 0.80,
    "prioritizes": 0.70,
    "identifies": 0.50,
    "references": 0.40,
    "contextualizes": 0.40,
    "restates": 0.30,
}
EXPLICITNESS_WEIGHT = {"explicit": 1.00, "inferred": 0.60}
MATCH_TYPE_WEIGHT = {"direct": 1.00, "indirect": 0.25, "contextual": 0.05}
DIRECT_STRONG_RELATIONS = {"commits", "targets", "funds", "monitors", "governs"}

BUCKET_STRONG = 0.66
BUCKET_MEDIUM = 0.33

# v0.2.0 relevance cap: best_relevance across applicable docs caps score_raw.
RELEVANCE_RANK = {"none": 0, "low": 1, "medium": 2, "high": 3}
RELEVANCE_CAP = {"none": 0.00, "low": 0.32, "medium": 0.65, "high": 1.00}

V1 = Path(__file__).resolve().parents[1]
DEFAULT_APPLICABILITY = V1 / "data" / "registry" / "city_applicable_policies.csv"
DEFAULT_FINDINGS_DIR = V1 / "data" / "policy_action_signals"
DEFAULT_OUTPUT_DIR = V1 / "data" / "policy_score"


def load_applicability(path: Path) -> dict[str, dict[str, float]]:
    """city_code -> {source_document_id: proximity_weight}.

    The applicability registry's rubric_version stamp is informational only;
    we accept any version because proximity_weight and applicability rules
    did not change between rubric v0.1.0 and v0.2.0 (only K and the cap did).
    """
    by_city: dict[str, dict[str, float]] = defaultdict(dict)
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            city = row["city_code"].strip()
            doc = row["source_document_id"].strip()
            w = float(row["proximity_weight"])
            by_city[city][doc] = w
    return dict(by_city)


def load_findings_index(findings_dir: Path) -> dict[tuple[str, str], dict]:
    """(action_id, source_document_id) -> findings payload."""
    index: dict[tuple[str, str], dict] = {}
    for path in findings_dir.rglob("*.json"):
        if path.name.startswith("_") or path.name == "failed.jsonl":
            continue
        doc_id = path.parent.name
        action_id = path.stem
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if payload.get("source_document_id") and payload["source_document_id"] != doc_id:
            doc_id = payload["source_document_id"]
        index[(action_id, doc_id)] = payload
    return index


def finding_passes_validation(payload: dict, finding: dict) -> bool:
    run = payload.get("search_run") or {}
    if run.get("schema_check_passed") is False:
        return False
    ev = (finding.get("evidence_text") or "").strip()
    return len(ev) >= 5


def dedupe_key(finding: dict, doc_id: str) -> tuple:
    return (
        doc_id,
        finding.get("page"),
        (finding.get("evidence_text") or "").strip(),
        finding.get("primitive_type"),
        finding.get("primitive_relation"),
    )


def explicitness_weight(finding: dict) -> float:
    exp = (finding.get("explicitness") or "explicit").strip().lower()
    return EXPLICITNESS_WEIGHT.get(exp, EXPLICITNESS_WEIGHT["explicit"])


def finding_strength(finding: dict, proximity: float) -> float:
    conf = CONFIDENCE_WEIGHT.get(finding.get("signal_confidence"), 0.0)
    rel = RELATION_WEIGHT.get(finding.get("primitive_relation"), 0.0)
    if conf == 0.0 or rel == 0.0:
        return 0.0
    match_weight = MATCH_TYPE_WEIGHT.get(finding.get("match_type"), 0.0)
    if match_weight == 0.0:
        return 0.0
    return proximity * conf * rel * explicitness_weight(finding) * match_weight


def is_direct_strong_evidence(finding: dict) -> bool:
    return (
        finding.get("match_type") == "direct"
        and finding.get("signal_confidence") == "high"
        and (finding.get("explicitness") or "explicit") == "explicit"
        and finding.get("primitive_relation") in DIRECT_STRONG_RELATIONS
    )


def score_raw(sum_strength: float, k: float = SATURATION_K) -> float:
    if sum_strength <= 0:
        return 0.0
    return 1.0 - math.exp(-sum_strength / k)


def score_bucket(raw: float) -> str:
    if raw >= BUCKET_STRONG:
        return "strong"
    if raw >= BUCKET_MEDIUM:
        return "medium"
    if raw > 0.0:
        return "weak"
    return "none"


def collect_scored_findings(
    city_code: str,
    action_id: str,
    applicable: dict[str, float],
    findings_index: dict[tuple[str, str], dict],
    doc_filter: str | None,
) -> tuple[list[dict], dict[str, str]]:
    """Return (scored_findings, doc_relevance_map).

    doc_relevance_map: source_document_id -> relevance grade ("high"/"medium"/"low"/"none")
    Only includes docs that returned at least one finding (or relevance=none with a payload).
    """
    seen: set[tuple] = set()
    scored: list[dict] = []
    doc_relevance: dict[str, str] = {}

    for doc_id, proximity in applicable.items():
        if doc_filter and doc_id != doc_filter:
            continue
        payload = findings_index.get((action_id, doc_id))
        if not payload:
            continue
        rel = payload.get("relevance")
        if rel in RELEVANCE_RANK:
            doc_relevance[doc_id] = rel
        if rel == "none" and not (payload.get("findings") or []):
            continue
        for finding in payload.get("findings") or []:
            if not finding_passes_validation(payload, finding):
                continue
            key = dedupe_key(finding, doc_id)
            if key in seen:
                continue
            seen.add(key)
            strength = finding_strength(finding, proximity)
            if strength <= 0:
                continue
            scored.append({
                "source_document_id": doc_id,
                "page": finding.get("page"),
                "section": finding.get("section"),
                "evidence_text": finding.get("evidence_text"),
                "primitive_type": finding.get("primitive_type"),
                "primitive_relation": finding.get("primitive_relation"),
                "match_type": finding.get("match_type"),
                "policy_subject": finding.get("policy_subject"),
                "subject_match_reason": finding.get("subject_match_reason"),
                "signal_confidence": finding.get("signal_confidence"),
                "explicitness": finding.get("explicitness") or "explicit",
                "finding_strength": round(strength, 4),
                "proximity_weight": proximity,
                "atom_id": finding.get("atom_id"),
            })
    scored.sort(key=lambda x: x["finding_strength"], reverse=True)
    return scored, doc_relevance


def best_relevance_for(doc_relevance: dict[str, str]) -> str:
    """Return the highest relevance across applicable docs that returned findings."""
    if not doc_relevance:
        return "none"
    return max(doc_relevance.values(), key=lambda r: RELEVANCE_RANK.get(r, 0))


def score_city_action(
    city_code: str,
    region_code: str,
    city_name: str,
    action_id: str,
    action_gpc: str,
    applicable: dict[str, float],
    findings_index: dict[tuple[str, str], dict],
    doc_filter: str | None,
) -> dict:
    scored, doc_relevance = collect_scored_findings(
        city_code, action_id, applicable, findings_index, doc_filter,
    )
    sum_s = sum(f["finding_strength"] for f in scored)
    raw_uncapped = score_raw(sum_s)

    # v0.2.0 relevance cap: best relevance across docs that produced findings
    # (or relevance=none decisions) becomes a hard ceiling on score_raw.
    best_rel = best_relevance_for(doc_relevance)
    cap = RELEVANCE_CAP.get(best_rel, 1.00)
    raw = min(raw_uncapped, cap)
    direct_strong_evidence_count = sum(is_direct_strong_evidence(f) for f in scored)
    direct_evidence_gate_applied = raw >= BUCKET_STRONG and direct_strong_evidence_count == 0
    if direct_evidence_gate_applied:
        raw = min(raw, RELEVANCE_CAP["medium"])
    bucket = score_bucket(raw)
    rel_counts = Counter(f["primitive_relation"] for f in scored)
    docs_with_findings = {f["source_document_id"] for f in scored}

    return {
        "rubric_version": RUBRIC_VERSION,
        "city_code": city_code,
        "region_code": region_code,
        "city_name": city_name,
        "action_id": action_id,
        "action_gpc_reference": action_gpc,
        "score_raw": round(raw, 4),
        "score_raw_uncapped": round(raw_uncapped, 4),
        "score_bucket": bucket,
        "sum_finding_strength": round(sum_s, 4),
        "best_relevance": best_rel,
        "relevance_cap_applied": round(cap, 2),
        "direct_strong_evidence_count": direct_strong_evidence_count,
        "direct_evidence_gate_applied": direct_evidence_gate_applied,
        "doc_relevance_map": dict(sorted(doc_relevance.items())),
        "findings_count": len(scored),
        "applicable_doc_count": len(applicable) if not doc_filter else (1 if doc_filter in applicable else 0),
        "docs_with_findings_count": len(docs_with_findings),
        "findings_count_by_relation": dict(sorted(rel_counts.items())),
        "doc_filter": doc_filter,
        "top_evidence": scored[:TOP_EVIDENCE_N],
        "score_run": {
            "rubric_version": RUBRIC_VERSION,
            "saturation_k": SATURATION_K,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "doc_filter": doc_filter,
        },
    }


def load_city_names(applicability_path: Path) -> dict[str, tuple[str, str]]:
    """city_code -> (region_code, city_name)."""
    names: dict[str, tuple[str, str]] = {}
    with applicability_path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            cc = row["city_code"].strip()
            if cc not in names:
                names[cc] = (row["region_code"].strip(), row["city_name"].strip())
    return names


def main() -> int:
    ap = argparse.ArgumentParser(description="Score city x action from v2 findings")
    ap.add_argument("--applicability", type=Path, default=DEFAULT_APPLICABILITY)
    ap.add_argument("--findings-dir", type=Path, default=DEFAULT_FINDINGS_DIR)
    ap.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    ap.add_argument("--region-code", help="limit to communes in this region (e.g. 11 for Aysén)")
    ap.add_argument("--city-code", help="single commune code (e.g. 11101)")
    ap.add_argument("--action", help="single action_id")
    ap.add_argument(
        "--doc-filter",
        help="only count findings from this source_document_id (pilot: one PARCC)",
    )
    ap.add_argument("--min-bucket", choices=["weak", "medium", "strong"],
                    help="only write scores at or above this bucket")
    args = ap.parse_args()

    if not args.applicability.exists():
        print(f"missing applicability: {args.applicability}", file=sys.stderr)
        print("run: python v2_derive_applicability.py", file=sys.stderr)
        return 1

    by_city = load_applicability(args.applicability)
    city_names = load_city_names(args.applicability)
    findings_index = load_findings_index(args.findings_dir)

    action_ids = sorted({aid for aid, _ in findings_index})
    if args.action:
        if args.action not in action_ids:
            print(f"no findings for action {args.action}", file=sys.stderr)
            return 1
        action_ids = [args.action]

    cities = sorted(by_city)
    if args.city_code:
        if args.city_code not in by_city:
            print(f"unknown city_code {args.city_code}", file=sys.stderr)
            return 1
        cities = [args.city_code]
    elif args.region_code:
        cities = [c for c in cities if city_names.get(c, ("", ""))[0] == args.region_code]

    bucket_rank = {"none": 0, "weak": 1, "medium": 2, "strong": 3}
    min_rank = bucket_rank.get(args.min_bucket, 0)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"_doc_{args.doc_filter}" if args.doc_filter else ""
    out_path = args.output_dir / f"scores{suffix}.jsonl"
    summary_path = args.output_dir / f"summary{suffix}.json"

    rows: list[dict] = []
    bucket_dist: Counter[str] = Counter()

    for city_code in cities:
        region_code, city_name = city_names.get(city_code, ("", ""))
        applicable = by_city[city_code]
        for action_id in action_ids:
            # GPC from any findings file for this action
            gpc = ""
            for (aid, _), payload in findings_index.items():
                if aid == action_id:
                    gpc = payload.get("action_gpc_reference", "")
                    break
            row = score_city_action(
                city_code, region_code, city_name, action_id, gpc,
                applicable, findings_index, args.doc_filter,
            )
            if bucket_rank[row["score_bucket"]] < min_rank:
                continue
            rows.append(row)
            bucket_dist[row["score_bucket"]] += 1

    with out_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Action-level summary (collapse cities — identical for regional-only doc filter)
    by_action: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_action[row["action_id"]].append(row)

    action_summary = []
    for aid, city_rows in sorted(by_action.items()):
        sample = city_rows[0]
        action_summary.append({
            "action_id": aid,
            "action_gpc_reference": sample.get("action_gpc_reference"),
            "score_raw": sample["score_raw"],
            "score_bucket": sample["score_bucket"],
            "findings_count": sample["findings_count"],
            "sum_finding_strength": sample["sum_finding_strength"],
            "cities_scored": len(city_rows),
            "top_evidence": sample["top_evidence"],
        })
    action_summary.sort(key=lambda x: x["score_raw"], reverse=True)

    summary = {
        "rubric_version": RUBRIC_VERSION,
        "region_code": args.region_code,
        "city_code": args.city_code,
        "doc_filter": args.doc_filter,
        "cities_scored": len(cities),
        "actions_scored": len(action_ids),
        "pairs_written": len(rows),
        "bucket_distribution": dict(bucket_dist),
        "top_actions_by_score_raw": action_summary[:20],
        "output": str(out_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"wrote {len(rows)} scores -> {out_path}", file=sys.stderr)
    print(f"summary -> {summary_path}", file=sys.stderr)
    print(f"buckets: {dict(bucket_dist)}", file=sys.stderr)
    if action_summary:
        top = action_summary[0]
        print(
            f"top action: {top['action_id']} raw={top['score_raw']} bucket={top['score_bucket']} "
            f"findings={top['findings_count']}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
