#!/usr/bin/env python3
"""Read-only validation of the deployed Chile action-policy score API."""

from __future__ import annotations

import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://ccglobal.openearth.dev/api/v1/cities"
REQUIRED_SCORE = {
    "src_action_id", "policy_support_score", "policy_support_category",
    "best_relevance", "n_findings", "n_docs", "policy_evidence",
}
REQUIRED_EVIDENCE = {
    "evidence_rank", "signal_relation", "signal_strength", "document_name",
    "document_type", "page", "evidence_strength", "evidence_text",
}


def fetch(city: dict[str, str], limit: int) -> dict:
    locode = city["locode"]
    url = f"{BASE}/{urllib.parse.quote(locode, safe='')}" \
          f"/action-policy-scores?top_evidence_limit={limit}"
    started = time.perf_counter()
    result = {"city": city["Comuna"], "locode": locode, "limit": limit, "url": url}
    try:
        with urllib.request.urlopen(url, timeout=90) as response:
            body = response.read()
            result.update(status=response.status, timing_ms=round((time.perf_counter()-started)*1000, 1))
        result["response"] = json.loads(body)
    except urllib.error.HTTPError as exc:
        result.update(status=exc.code, timing_ms=round((time.perf_counter()-started)*1000, 1),
                      error=exc.read().decode("utf-8", "replace")[:2000])
    except Exception as exc:  # diagnostic artifact should retain any transport/JSON error
        result.update(status=None, timing_ms=round((time.perf_counter()-started)*1000, 1),
                      error=f"{type(exc).__name__}: {exc}")
    return result


def contract_errors(result: dict) -> list[str]:
    if result.get("status") != 200:
        return [f"HTTP {result.get('status')}: {result.get('error', '')}"]
    root = result["response"]
    errors = []
    if not isinstance(root, dict):
        return ["response root is not an object"]
    for key in ("meta", "scores"):
        if key not in root:
            errors.append(f"missing root.{key}")
    if errors:
        return errors
    meta, scores = root["meta"], root["scores"]
    if meta.get("api_context", {}).get("locode") != result["locode"]:
        errors.append("meta.api_context.locode mismatch")
    if meta.get("total_records") != len(scores):
        errors.append("meta.total_records mismatch")
    evidence_total = sum(len(s.get("policy_evidence", [])) for s in scores)
    if meta.get("total_evidence_items") != evidence_total:
        errors.append("meta.total_evidence_items mismatch")
    seen_actions = set()
    for i, score in enumerate(scores):
        missing = REQUIRED_SCORE - score.keys()
        if missing:
            errors.append(f"scores[{i}] missing {sorted(missing)}")
        action = score.get("src_action_id")
        if action in seen_actions:
            errors.append(f"duplicate action {action}")
        seen_actions.add(action)
        value = score.get("policy_support_score")
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 1:
            errors.append(f"{action}: invalid score {value!r}")
        category = score.get("policy_support_category")
        if category not in {"strong", "medium", "weak", "none"}:
            errors.append(f"{action}: invalid category {category!r}")
        elif isinstance(value, (int, float)):
            expected = "strong" if value >= .66 else "medium" if value >= .33 else "weak" if value > 0 else "none"
            if category != expected:
                errors.append(f"{action}: score/category mismatch ({value}, {category})")
        if score.get("best_relevance") not in {"high", "medium", "low", "none"}:
            errors.append(f"{action}: invalid best_relevance")
        evidence = score.get("policy_evidence", [])
        ranks = [e.get("evidence_rank") for e in evidence]
        if ranks != list(range(1, len(evidence) + 1)):
            errors.append(f"{action}: evidence ranks not contiguous/ordered: {ranks}")
        for j, item in enumerate(evidence):
            missing_e = REQUIRED_EVIDENCE - item.keys()
            if missing_e:
                errors.append(f"{action}.policy_evidence[{j}] missing {sorted(missing_e)}")
            if not item.get("document_name") or not item.get("document_type") or not item.get("evidence_text"):
                errors.append(f"{action}.policy_evidence[{j}] has blank required content")
            if not isinstance(item.get("page"), int) or item.get("page", 0) < 1:
                errors.append(f"{action}.policy_evidence[{j}] invalid page {item.get('page')!r}")
            if item.get("signal_strength") not in {"high", "medium", "low"}:
                errors.append(f"{action}.policy_evidence[{j}] invalid signal_strength")
    return errors


def main() -> None:
    with (ROOT / "data/registry/policy_documents_test.csv").open(newline="", encoding="utf-8-sig") as f:
        cities = list(csv.DictReader(f))
    results = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(fetch, city, limit) for city in cities for limit in (5, 20)]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda r: ([c["locode"] for c in cities].index(r["locode"]), r["limit"]))
    (ROOT / "output/api-validation").mkdir(parents=True, exist_ok=True)
    for result in results:
        result["contract_errors"] = contract_errors(result)
        if result.get("status") == 200:
            response = result.pop("response")
            out = ROOT / "output/api-validation" / f"{result['locode'].replace(' ', '_')}-limit-{result['limit']}.json"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            meta, scores = response["meta"], response["scores"]
            result.update(meta=meta, score_count=len(scores),
                          evidence_count=sum(len(s.get("policy_evidence", [])) for s in scores),
                          response_file=str(out.relative_to(ROOT)))
    summary = ROOT / "output/api-validation/requests.json"
    summary.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(summary)
    for r in results:
        print(r["locode"], r["limit"], r.get("status"), r["timing_ms"],
              r.get("score_count"), r.get("evidence_count"), len(r["contract_errors"]))


if __name__ == "__main__":
    main()
