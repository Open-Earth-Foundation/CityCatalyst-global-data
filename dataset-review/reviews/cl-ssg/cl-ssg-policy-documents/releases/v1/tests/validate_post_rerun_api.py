#!/usr/bin/env python3
"""Validate the full corrected 20-city matrix after the Mage rerun."""

from __future__ import annotations

import csv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from validate_corrected_locodes import CORRECTED
from validate_deployed_policy_api import ROOT, contract_errors, fetch


def main() -> None:
    with (ROOT / "data/registry/policy_documents_test.csv").open(newline="", encoding="utf-8-sig") as f:
        cities = list(csv.DictReader(f))
    for city in cities:
        city["locode"] = CORRECTED.get(city["Comuna"], city["locode"])

    results = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(fetch, city, limit) for city in cities for limit in (5, 20)]
        for future in as_completed(futures):
            results.append(future.result())
    order = [c["locode"] for c in cities]
    results.sort(key=lambda r: (order.index(r["locode"]), r["limit"]))

    out_dir = ROOT / "output/api-validation-post-rerun"
    out_dir.mkdir(parents=True, exist_ok=True)
    for result in results:
        result["contract_errors"] = contract_errors(result)
        if result.get("status") == 200:
            response = result.pop("response")
            response_path = out_dir / f"{result['locode'].replace(' ', '_')}-limit-{result['limit']}.json"
            response_path.write_text(json.dumps(response, ensure_ascii=False, indent=2) + "\n")
            scores = response["scores"]
            result.update(
                meta=response["meta"],
                score_count=len(scores),
                evidence_count=sum(len(s.get("policy_evidence", [])) for s in scores),
                response_file=str(response_path.relative_to(ROOT)),
            )
    (out_dir / "requests.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    for result in results:
        context = result.get("meta", {}).get("api_context", {})
        coverage = result.get("meta", {}).get("spatial_document_coverage", {})
        print(result["city"], result["locode"], result["limit"], result.get("status"),
              result["timing_ms"], result.get("score_count"), result.get("evidence_count"),
              context.get("city_name"), coverage.get("finest_location_scope"),
              len(result["contract_errors"]))


if __name__ == "__main__":
    main()
