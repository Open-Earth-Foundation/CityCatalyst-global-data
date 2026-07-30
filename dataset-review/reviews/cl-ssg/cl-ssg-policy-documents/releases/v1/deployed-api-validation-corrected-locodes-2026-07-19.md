# Corrected-LOCODE API retest — 2026-07-19

## Conclusion

**Not ready, but substantially improved after correcting the lookup CSV.** Nine of the ten corrected routes now return the intended municipality, all 102 actions, and expected municipal coverage. Two deployment issues remain:

1. `CL LPI` (La Pintana) returns 404 despite being the correct UNECE UN/LOCODE.
2. `CL ZAL` correctly resolves to Valdivia and includes its municipal plan, but applies the **Los Lagos** regional plan instead of **Los Ríos**.

The previously identified deployed-versus-local score mismatch also remains. This retest was read-only and used `top_evidence_limit=5` and `20`.

## Corrected route results

Counts and timings are from the limit-5 request. Every successful limit-5 response returned 102 scores and 510 evidence items. Coverage was assessed using limit 20 and `meta.spatial_document_coverage`.

| Intended city | Correct LOCODE | HTTP | Time (ms) | Scores | Limit-20 evidence | Expected coverage | Observed coverage | Result |
|---|---:|---:|---:|---:|---:|---|---|---|
| La Pintana | CL LPI | 404 | 807.1 | — | — | National + Metropolitana | None | Fail |
| Peñalolén | CL PLN | 200 | 1,281.1 | 102 | 1,992 | N + Metropolitana + municipal | Exact | Pass |
| Concepción | CL CCP | 200 | 1,421.3 | 102 | 1,905 | N + Biobío + municipal | Exact | Pass |
| Temuco | CL ZCO | 200 | 1,074.9 | 102 | 1,870 | N + Araucanía + municipal | Exact | Pass |
| Puerto Montt | CL PMC | 200 | 1,335.0 | 102 | 1,937 | N + Los Lagos; no municipal | Exact | Pass |
| Valdivia | CL ZAL | 200 | 1,163.8 | 102 | 1,940 | N + Los Ríos + municipal | N + **Los Lagos** + municipal | Fail |
| Paillaco | CL PAO | 200 | 1,125.8 | 102 | 1,979 | N + Los Ríos + municipal | Exact | Pass |
| Lago Ranco | CL RNC | 200 | 1,093.4 | 102 | 1,974 | N + Los Ríos + municipal | Exact | Pass |
| Panguipulli | CL PAN | 200 | 1,165.7 | 102 | 1,970 | N + Los Ríos + municipal | Exact | Pass |
| Frutillar | CL FRT | 200 | 1,236.2 | 102 | 1,977 | N + Los Lagos + municipal | Exact | Pass |

Combining these corrected routes with the ten originally correct routes gives:

- 19/20 intended municipalities returning HTTP 200 and 102 actions.
- 18/20 with correct intended-city spatial coverage.
- 1 missing city (La Pintana).
- 1 cross-region applicability defect (Valdivia).

## Remaining findings

### Critical — Valdivia receives Los Lagos regional evidence

Exact failing request:

`https://ccglobal.openearth.dev/api/v1/cities/CL%20ZAL/action-policy-scores?top_evidence_limit=20`

The API correctly echoes Valdivia but ranks a Los Lagos PARCC passage first for `icare_0117`:

```json
{
  "api_context": {"locode": "CL ZAL", "city_name": "Valdivia"},
  "src_action_id": "icare_0117",
  "policy_support_score": 0.998,
  "policy_evidence": [{
    "evidence_rank": 1,
    "document_name": "Plan de Acción Regional de Cambio Climático Los Lagos",
    "document_type": "parcc",
    "page": 60,
    "evidence_strength": 0.7,
    "evidence_text": "... promover la peatonalidad ... en la región de Los Lagos."
  }]
}
```

The expected regional source is `chl_parcc_los_rios_2025`. The response does include `chl_paccc_valdivia_2023`, so municipal mapping is correct; the failure is specifically regional applicability. A likely cause to inspect is the legacy `LL` subdivision value attached to Valdivia in UN/LOCODE versus current Chilean region 14 / Los Ríos.

### High — La Pintana remains unavailable

Both corrected requests return the same error:

```http
GET https://ccglobal.openearth.dev/api/v1/cities/CL%20LPI/action-policy-scores?top_evidence_limit=5
GET https://ccglobal.openearth.dev/api/v1/cities/CL%20LPI/action-policy-scores?top_evidence_limit=20
```

```json
{"detail":"No policy scores found for this city and release"}
```

La Pintana has national and Metropolitana regional applicability in `city_applicable_policies.csv`, so lack of a municipal PACCC in this release does not explain the absence of all scores.

### High — deployed scores still differ from current local scores

For each of the nine corrected HTTP-200 cities, all 102 records differ from `v1/data/policy_score/scores.jsonl` in at least one of score, finding count, document count, or best relevance. Numeric scores differ for 50–62 actions per city; maximum absolute per-city score differences range from `0.2265` to `0.3385`.

This remains consistent with a stale or otherwise different deployed ingestion state and needs reconciliation before approval.

## Checks that passed

- All nine corrected HTTP-200 responses echo the intended LOCODE and municipality name.
- All successful corrected routes contain valid `meta` and `scores`, all 102 unique canonical actions, bounded numeric scores, valid categories, complete required fields, and ordered evidence ranks.
- Expected municipal documents are present for Peñalolén, Concepción, Temuco, Valdivia, Paillaco, Lago Ranco, Panguipulli, and Frutillar.
- Puerto Montt correctly reports regional coverage without a municipal plan.
- No unexpected document appears for eight of the nine successful corrected routes; Valdivia is the sole geography exception.
- All **17,544 of 17,544** limit-20 evidence records exactly match `v1/output/action_policy_signals.csv` on action ID, document name, page, and verbatim text. No duplicates were found within an action.
- Across the combined 19 intended-city HTTP-200 responses, **37,197** limit-20 evidence records were verified against the ingestion artifact.

## Recommendation

Correct the ten LOCODE values in the lookup CSV, then fix or ingest La Pintana (`CL LPI`) and change Valdivia's regional mapping to Los Ríos / region `14`. Reconcile the deployed finding set with the current scored artifact and rerun the full corrected 20-city matrix. Acceptance should require 20/20 HTTP 200 responses, 20/20 intended city-name matches, and no cross-region evidence.

