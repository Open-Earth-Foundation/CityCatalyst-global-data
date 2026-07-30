#!/usr/bin/env python3
"""Analyze corrected-LOCODE API responses against current v1 artifacts."""

from __future__ import annotations

import csv
import json
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from validate_corrected_locodes import CORRECTED
from validate_deployed_policy_api import ROOT

OUT = ROOT / "output/api-validation-corrected"


def norm(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", value.casefold()) if not unicodedata.combining(c))


def main() -> None:
    requests = json.loads((OUT / "requests.json").read_text())
    applicable = list(csv.DictReader((ROOT / "data/registry/city_applicable_policies.csv").open()))
    documents = json.loads((ROOT / "data/registry/source_documents.json").read_text())["source_documents"]
    doc_id_by_name = {d["source_name"]: d["source_document_id"] for d in documents}
    city_code = {norm(r["city_name"]): r["city_code"] for r in applicable}

    artifact = set()
    with (ROOT / "output/action_policy_signals.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            artifact.add((r["action_id"], r["document_name"], r["evidence_text"], int(r["page"])))

    result = {"cities": [], "evidence": {}, "local_score_comparison": {}}
    api_scores = {}
    checked = matched = 0
    for intended, locode in CORRECTED.items():
        request = next(r for r in requests if r["locode"] == locode and r["limit"] == 20)
        row = {"city": intended, "locode": locode, "url": request["url"], "status": request["status"],
               "timing_ms": request["timing_ms"], "score_count": request.get("score_count"),
               "evidence_count": request.get("evidence_count"), "error": request.get("error"),
               "contract_errors": request["contract_errors"]}
        code = city_code[norm(intended)]
        expected_rows = [r for r in applicable if r["city_code"] == code]
        expected = defaultdict(list)
        for r in expected_rows:
            expected[r["source_level"]].append(r["source_document_id"])
        row["expected_documents"] = dict(expected)
        if request["status"] == 200:
            response = json.loads((ROOT / request["response_file"]).read_text())
            row["api_city_name"] = response["meta"]["api_context"]["city_name"]
            row["spatial_document_coverage"] = response["meta"]["spatial_document_coverage"]
            observed = {doc_id_by_name[e["document_name"]] for s in response["scores"] for e in s["policy_evidence"]}
            row["coverage"] = {level: {"expected": ids, "observed": sorted(set(ids) & observed),
                                               "not_observed": sorted(set(ids) - observed)}
                               for level, ids in expected.items()}
            row["unexpected_documents"] = sorted(observed - {d for ids in expected.values() for d in ids})
            duplicates = []
            for score in response["scores"]:
                counts = Counter((e["document_name"], e["page"], e["evidence_text"]) for e in score["policy_evidence"])
                duplicates.extend((score["src_action_id"], key, count) for key, count in counts.items() if count > 1)
                for e in score["policy_evidence"]:
                    checked += 1
                    if (score["src_action_id"], e["document_name"], e["evidence_text"], e["page"]) in artifact:
                        matched += 1
            row["duplicate_evidence_count"] = len(duplicates)
            api_scores[code] = {s["src_action_id"]: s for s in response["scores"]}
        result["cities"].append(row)

    comparisons = {code: {"checked": 0, "mismatches": 0, "score_mismatches": 0, "max_score_delta": 0}
                   for code in api_scores}
    with (ROOT / "data/policy_score/scores.jsonl").open() as f:
        for line in f:
            local = json.loads(line)
            code = local["city_code"]
            if code not in api_scores:
                continue
            api = api_scores[code].get(local["action_id"])
            if not api:
                continue
            c = comparisons[code]
            c["checked"] += 1
            fields = (("policy_support_score", "score_raw"), ("n_findings", "findings_count"),
                      ("n_docs", "docs_with_findings_count"), ("best_relevance", "best_relevance"))
            if any(api[a] != local[b] for a, b in fields):
                c["mismatches"] += 1
            if api["policy_support_score"] != local["score_raw"]:
                c["score_mismatches"] += 1
                c["max_score_delta"] = max(c["max_score_delta"],
                                           abs(api["policy_support_score"] - local["score_raw"]))
    result["evidence"] = {"checked": checked, "matched": matched, "unmatched": checked - matched}
    result["local_score_comparison"] = comparisons
    (OUT / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
