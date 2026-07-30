#!/usr/bin/env python3
"""Analyze saved API responses against the v1 release artifacts (no network or mutations)."""

from __future__ import annotations

import csv
import json
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/api-validation"


def norm(value: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", value.casefold()) if not unicodedata.combining(c))


def main() -> None:
    requests = json.loads((OUT / "requests.json").read_text())
    tests = list(csv.DictReader((ROOT / "data/registry/policy_documents_test.csv").open(encoding="utf-8-sig")))
    applicable = list(csv.DictReader((ROOT / "data/registry/city_applicable_policies.csv").open()))
    documents = json.loads((ROOT / "data/registry/source_documents.json").read_text())["source_documents"]
    doc_by_id = {d["source_document_id"]: d for d in documents}
    doc_id_by_name = {d["source_name"]: d["source_document_id"] for d in documents}
    city_code_by_name = {}
    for row in applicable:
        city_code_by_name.setdefault(norm(row["city_name"]), row["city_code"])

    artifact_rows = set()
    artifact_pages = defaultdict(set)
    with (ROOT / "output/action_policy_signals.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            key = (row["action_id"], row["document_name"], row["evidence_text"], int(row["page"]))
            artifact_rows.add(key)
            artifact_pages[(row["document_name"], row["evidence_text"])].add(int(row["page"]))

    result = {"cities": [], "evidence_exact_match": {}, "local_score_comparison": {}}
    successful_locodes = {r["locode"] for r in requests if r["limit"] == 20 and r["status"] == 200}
    response_by_locode = {}
    evidence_total = evidence_matched = 0
    unmatched = []
    for test in tests:
        req = next(r for r in requests if r["locode"] == test["locode"] and r["limit"] == 20)
        city = {k: req.get(k) for k in ("city", "locode", "url", "status", "timing_ms", "score_count", "evidence_count", "error")}
        code = city_code_by_name.get(norm(test["Comuna"]))
        expected_rows = [r for r in applicable if r["city_code"] == code]
        expected = defaultdict(list)
        for row in expected_rows:
            expected[row["source_level"]].append(row["source_document_id"])
        city["city_code"] = code
        city["expected_documents"] = dict(expected)
        city["contract_errors"] = req["contract_errors"]
        if req["status"] == 200:
            response = json.loads((ROOT / req["response_file"]).read_text())
            response_by_locode[req["locode"]] = response
            observed_names = sorted({e["document_name"] for s in response["scores"] for e in s["policy_evidence"]})
            observed_ids = sorted({doc_id_by_name.get(name, f"UNMAPPED:{name}") for name in observed_names})
            city["observed_documents"] = observed_ids
            city["unmapped_document_names"] = [n for n in observed_names if n not in doc_id_by_name]
            city["coverage"] = {
                level: {"expected": ids, "observed": sorted(set(ids) & set(observed_ids)),
                        "not_observed": sorted(set(ids) - set(observed_ids))}
                for level, ids in expected.items()
            }
            city["spatial_document_coverage"] = response["meta"]["spatial_document_coverage"]
            city["top_actions"] = [{k: s[k] for k in ("src_action_id", "policy_support_score", "policy_support_category", "n_findings", "n_docs")}
                                   | {"top_document": s["policy_evidence"][0]["document_name"],
                                      "top_evidence": s["policy_evidence"][0]["evidence_text"]}
                                   for s in sorted(response["scores"], key=lambda x: x["policy_support_score"], reverse=True)[:3]]
            duplicates = []
            for score in response["scores"]:
                seen = Counter((e["document_name"], e["page"], e["evidence_text"]) for e in score["policy_evidence"])
                duplicates.extend((score["src_action_id"], key, count) for key, count in seen.items() if count > 1)
                for e in score["policy_evidence"]:
                    evidence_total += 1
                    key = (score["src_action_id"], e["document_name"], e["evidence_text"], e["page"])
                    if key in artifact_rows:
                        evidence_matched += 1
                    else:
                        unmatched.append({"locode": req["locode"], "action": score["src_action_id"],
                                          "document": e["document_name"], "page": e["page"], "text": e["evidence_text"],
                                          "artifact_pages_for_same_text": sorted(artifact_pages[(e["document_name"], e["evidence_text"])])})
            city["duplicate_evidence_within_action"] = duplicates
        result["cities"].append(city)

    result["evidence_exact_match"] = {"checked": evidence_total, "matched": evidence_matched,
                                      "unmatched_count": len(unmatched), "unmatched_examples": unmatched[:20]}

    code_by_locode = {t["locode"]: city_code_by_name.get(norm(t["Comuna"])) for t in tests}
    api_scores = {locode: {s["src_action_id"]: s for s in response["scores"]}
                  for locode, response in response_by_locode.items()}
    comparisons = {locode: {"checked": 0, "mismatches": []} for locode in successful_locodes}
    with (ROOT / "data/policy_score/scores.jsonl").open() as f:
        for line in f:
            local = json.loads(line)
            for locode, code in code_by_locode.items():
                if locode not in api_scores or local["city_code"] != code:
                    continue
                api = api_scores[locode].get(local["action_id"])
                if not api:
                    comparisons[locode]["mismatches"].append({"action": local["action_id"], "issue": "missing in API"})
                    continue
                comparisons[locode]["checked"] += 1
                diffs = {}
                for api_key, local_key in (("policy_support_score", "score_raw"), ("n_findings", "findings_count"),
                                           ("n_docs", "docs_with_findings_count"), ("best_relevance", "best_relevance")):
                    if api[api_key] != local[local_key]:
                        diffs[api_key] = {"api": api[api_key], "local": local[local_key]}
                if diffs:
                    comparisons[locode]["mismatches"].append({"action": local["action_id"], "diffs": diffs})
    result["local_score_comparison"] = comparisons
    (OUT / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"evidence": result["evidence_exact_match"],
                      "cities": [{"locode": c["locode"], "status": c["status"], "coverage": c.get("coverage"),
                                  "duplicates": len(c.get("duplicate_evidence_within_action", []))} for c in result["cities"]],
                      "score_mismatches": {k: len(v["mismatches"]) for k,v in comparisons.items()}},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
