#!/usr/bin/env python3
"""Analyze the full corrected post-rerun API response set."""

from __future__ import annotations

import csv
import json
import unicodedata
from collections import Counter, defaultdict

from validate_corrected_locodes import CORRECTED
from validate_deployed_policy_api import ROOT

OUT = ROOT / "output/api-validation-post-rerun"


def norm(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", value.casefold()) if not unicodedata.combining(c))


def main() -> None:
    requests = json.loads((OUT / "requests.json").read_text())
    with (ROOT / "data/registry/policy_documents_test.csv").open(encoding="utf-8-sig") as f:
        tests = list(csv.DictReader(f))
    for test in tests:
        test["locode"] = CORRECTED.get(test["Comuna"], test["locode"])
    applicable = list(csv.DictReader((ROOT / "data/registry/city_applicable_policies.csv").open()))
    docs = json.loads((ROOT / "data/registry/source_documents.json").read_text())["source_documents"]
    doc_id_by_name = {d["source_name"]: d["source_document_id"] for d in docs}
    code_by_name = {norm(r["city_name"]): r["city_code"] for r in applicable}

    artifact = set()
    with (ROOT / "output/action_policy_signals.csv").open(newline="") as f:
        for r in csv.DictReader(f):
            artifact.add((r["action_id"], r["document_name"], r["evidence_text"], int(r["page"])))

    result = {"cities": [], "evidence": {}, "score_comparison": {}}
    api_scores = {}
    evidence_checked = evidence_matched = 0
    for test in tests:
        req = next(r for r in requests if r["locode"] == test["locode"] and r["limit"] == 20)
        row = {"city": test["Comuna"], "locode": test["locode"], "status": req["status"],
               "timing_ms": req["timing_ms"], "score_count": req.get("score_count"),
               "evidence_count": req.get("evidence_count"), "contract_errors": req["contract_errors"]}
        if req["status"] != 200:
            result["cities"].append(row)
            continue
        response = json.loads((ROOT / req["response_file"]).read_text())
        code = code_by_name[norm(test["Comuna"])]
        expected_rows = [r for r in applicable if r["city_code"] == code]
        expected = defaultdict(list)
        for r in expected_rows:
            expected[r["source_level"]].append(r["source_document_id"])
        observed = {doc_id_by_name[e["document_name"]] for s in response["scores"] for e in s["policy_evidence"]}
        expected_all = {d for ids in expected.values() for d in ids}
        row.update(
            api_city_name=response["meta"]["api_context"]["city_name"],
            spatial_document_coverage=response["meta"]["spatial_document_coverage"],
            observed_documents=sorted(observed),
            unexpected_documents=sorted(observed - expected_all),
            coverage={level: {"expected": ids, "observed": sorted(set(ids) & observed),
                              "not_observed": sorted(set(ids) - observed)} for level, ids in expected.items()},
        )
        duplicates = 0
        for score in response["scores"]:
            counts = Counter((e["document_name"], e["page"], e["evidence_text"]) for e in score["policy_evidence"])
            duplicates += sum(1 for count in counts.values() if count > 1)
            for e in score["policy_evidence"]:
                evidence_checked += 1
                if (score["src_action_id"], e["document_name"], e["evidence_text"], e["page"]) in artifact:
                    evidence_matched += 1
        row["duplicate_evidence_count"] = duplicates
        api_scores[code] = {s["src_action_id"]: s for s in response["scores"]}
        result["cities"].append(row)

    comparisons = {code: {"checked": 0, "record_mismatches": 0, "score_mismatches": 0,
                          "max_score_delta": 0.0} for code in api_scores}
    with (ROOT / "data/policy_score/scores.jsonl").open() as f:
        for line in f:
            local = json.loads(line)
            code = local["city_code"]
            if code not in api_scores:
                continue
            api = api_scores[code].get(local["action_id"])
            if not api:
                continue
            comp = comparisons[code]
            comp["checked"] += 1
            fields = (("policy_support_score", "score_raw"), ("n_findings", "findings_count"),
                      ("n_docs", "docs_with_findings_count"), ("best_relevance", "best_relevance"))
            if any(api[a] != local[b] for a, b in fields):
                comp["record_mismatches"] += 1
            if api["policy_support_score"] != local["score_raw"]:
                comp["score_mismatches"] += 1
                comp["max_score_delta"] = max(comp["max_score_delta"],
                                               abs(api["policy_support_score"] - local["score_raw"]))
    result["evidence"] = {"checked": evidence_checked, "matched": evidence_matched,
                          "unmatched": evidence_checked - evidence_matched}
    result["score_comparison"] = comparisons
    (OUT / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "routes": {"total": len(result["cities"]), "http_200": sum(c["status"] == 200 for c in result["cities"]),
                   "identity_matches": sum(c.get("api_city_name") == c["city"] for c in result["cities"]),
                   "contract_failures": sum(bool(c["contract_errors"]) for c in result["cities"])},
        "evidence": result["evidence"],
        "coverage_issues": [{"city": c["city"], "unexpected": c.get("unexpected_documents"),
                             "scopes": c.get("spatial_document_coverage"), "coverage": c.get("coverage")}
                            for c in result["cities"] if c.get("unexpected_documents")],
        "duplicates": sum(c.get("duplicate_evidence_count", 0) for c in result["cities"]),
        "score_comparison": comparisons,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
