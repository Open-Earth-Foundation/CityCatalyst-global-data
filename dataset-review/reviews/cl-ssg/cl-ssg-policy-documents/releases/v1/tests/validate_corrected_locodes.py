#!/usr/bin/env python3
"""Rerun deployed API validation for corrected Chile UN/LOCODE mappings."""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from validate_deployed_policy_api import ROOT, contract_errors, fetch


CORRECTED = {
    "La Pintana": "CL LPI",
    "Peñalolén": "CL PLN",
    "Concepción": "CL CCP",
    "Temuco": "CL ZCO",
    "Puerto Montt": "CL PMC",
    "Valdivia": "CL ZAL",
    "Paillaco": "CL PAO",
    "Lago Ranco": "CL RNC",
    "Panguipulli": "CL PAN",
    "Frutillar": "CL FRT",
}


def main() -> None:
    cities = [{"Comuna": name, "locode": locode} for name, locode in CORRECTED.items()]
    results = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(fetch, city, limit) for city in cities for limit in (5, 20)]
        for future in as_completed(futures):
            results.append(future.result())
    order = list(CORRECTED.values())
    results.sort(key=lambda r: (order.index(r["locode"]), r["limit"]))
    out_dir = ROOT / "output/api-validation-corrected"
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
        print(result["city"], result["locode"], result["limit"], result.get("status"),
              result["timing_ms"], result.get("score_count"), result.get("evidence_count"),
              context.get("city_name"), len(result["contract_errors"]))


if __name__ == "__main__":
    main()
