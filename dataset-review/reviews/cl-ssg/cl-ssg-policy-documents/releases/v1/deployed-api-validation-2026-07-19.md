# Chile policy-signal development API validation — 2026-07-19

> **Follow-up:** The lookup CSV contained ten incorrect LOCODEs. See `deployed-api-validation-corrected-locodes-2026-07-19.md` for the corrected-route retest. Nine corrected routes now work; La Pintana remains 404 and Valdivia receives the wrong regional plan.

## Conclusion

**Not ready.** The API contract is sound for successful responses, but the requested test matrix exposes deployment/city-identity failures: 7 of 20 routes return 404, and 3 additional routes resolve their LOCODE to a different Chilean municipality. Only 10 of 20 routes return scores for the intended city. The deployed results also do not match the current local scored artifact.

Validation was read-only. Requests were made to release `761236b5-4e6d-5af1-e1a2-b50eb3780fe1` with `top_evidence_limit=5` and again with the documented maximum `20`. Response generation timestamps were around `2026-07-19T19:33:49Z`.

## Per-city route and coverage results

Counts and timings below are from the limit-5 request. Every successful limit-5 response returned 102 scores and 510 evidence items. The limit-20 requests returned the same 102 scores and 1,859–2,013 evidence items. Coverage conclusions use limit 20 plus `meta.spatial_document_coverage`; absence from a top-20 evidence list alone is not treated as proof that a document is absent.

`N`, `R`, and `M` mean national, regional, and municipal. `✓` means the intended scope/document was observed or confirmed by response metadata; `—` means not expected; `wrong` means evidence belongs to a different region/municipality.

| Intended city | LOCODE | HTTP | Time (ms) | Scores | Evidence | Expected N/R/M | Observed N/R/M | Result |
|---|---:|---:|---:|---:|---:|---|---|---|
| Santiago | CL SCL | 200 | 1,867.1 | 102 | 510 | ✓/✓/✓ | ✓/✓/✓ | Pass |
| Providencia | CL PRO | 200 | 1,478.6 | 102 | 510 | ✓/✓/✓ | ✓/✓/✓ | Pass |
| Maipú | CL MAI | 200 | 1,370.3 | 102 | 510 | ✓/✓/✓ | ✓/✓/✓ | Pass |
| Puente Alto | CL PTA | 200 | 1,073.5 | 102 | 510 | ✓/✓/— | ✓/✓/— | Pass |
| Renca | CL REN | 200 | 1,135.4 | 102 | 510 | ✓/✓/✓ | ✓/✓/✓ | Pass |
| La Pintana | CL LPN | 404 | 485.8 | — | — | ✓/✓/— | —/—/— | Fail |
| Quilicura | CL QUI | 200 | 1,206.3 | 102 | 510 | ✓/✓/✓ | ✓/✓/✓ | Pass |
| Peñalolén | CL PEN | 200 | 1,233.6 | 102 | 510 | ✓/Metropolitana/Peñalolén | ✓/**Maule**/— | Fail: resolves to Pencahue |
| Valparaíso | CL VAP | 200 | 1,089.2 | 102 | 510 | ✓/—/✓ | ✓/—/✓ | Pass; regional placeholder correctly not required |
| Concepción | CL CON | 200 | 1,043.5 | 102 | 510 | ✓/Biobío/Concepción | ✓/—/— | Fail: resolves to Concón |
| Temuco | CL TEM | 404 | 507.9 | — | — | ✓/Araucanía/Temuco | —/—/— | Fail |
| Puerto Montt | CL PMT | 404 | 465.6 | — | — | ✓/Los Lagos/— | —/—/— | Fail |
| Antofagasta | CL ANF | 200 | 1,174.8 | 102 | 510 | ✓/Antofagasta/— | ✓/Antofagasta/— | Pass |
| Valdivia | CL VAD | 404 | 496.3 | — | — | ✓/Los Ríos/Valdivia | —/—/— | Fail |
| Paillaco | CL PAL | 200 | 1,065.7 | 102 | 510 | ✓/Los Ríos/Paillaco | ✓/**Los Lagos**/— | Fail: resolves to Palena |
| Lago Ranco | CL LRN | 404 | 478.6 | — | — | ✓/Los Ríos/Lago Ranco | —/—/— | Fail |
| Panguipulli | CL PNG | 404 | 495.1 | — | — | ✓/Los Ríos/Panguipulli | —/—/— | Fail |
| Frutillar | CL FRU | 404 | 504.3 | — | — | ✓/Los Lagos/Frutillar | —/—/— | Fail |
| San Nicolás | CL SNI | 200 | 1,150.2 | 102 | 510 | ✓/Ñuble/— | ✓/Ñuble/— | Pass |
| Canela | CL CAN | 200 | 1,106.9 | 102 | 510 | ✓/Coquimbo/— | ✓/Coquimbo/— | Pass |

At limit 20, evidence from eight national documents was directly observed for every successful route. Four applicable national documents were not visible within the top-20 cap (the draft mining plan and three national territorial plans); this is not classified as a coverage failure because the endpoint cannot return more than 20 evidence items per action.

## Findings by severity

### Critical — test-city LOCODEs do not reliably identify the intended municipality

Seven exact routes return `404 {"detail":"No policy scores found for this city and release"}` at both evidence limits:

- `https://ccglobal.openearth.dev/api/v1/cities/CL%20LPN/action-policy-scores?top_evidence_limit=5`
- `https://ccglobal.openearth.dev/api/v1/cities/CL%20TEM/action-policy-scores?top_evidence_limit=5`
- `https://ccglobal.openearth.dev/api/v1/cities/CL%20PMT/action-policy-scores?top_evidence_limit=5`
- `https://ccglobal.openearth.dev/api/v1/cities/CL%20VAD/action-policy-scores?top_evidence_limit=5`
- `https://ccglobal.openearth.dev/api/v1/cities/CL%20LRN/action-policy-scores?top_evidence_limit=5`
- `https://ccglobal.openearth.dev/api/v1/cities/CL%20PNG/action-policy-scores?top_evidence_limit=5`
- `https://ccglobal.openearth.dev/api/v1/cities/CL%20FRU/action-policy-scores?top_evidence_limit=5`
- `https://ccglobal.openearth.dev/api/v1/cities/CL%20LPN/action-policy-scores?top_evidence_limit=20` (representative larger-limit retry; all seven behaved identically)

Three nominally successful routes echo the requested LOCODE but identify a different city in `meta.api_context.city_name`, producing demonstrably wrong geography:

```json
// https://ccglobal.openearth.dev/api/v1/cities/CL%20PEN/action-policy-scores?top_evidence_limit=20
{"locode":"CL PEN","city_name":"Pencahue"}
// top evidence: "Plan de Acción Regional de Cambio Climático Maule"
```

```json
// https://ccglobal.openearth.dev/api/v1/cities/CL%20CON/action-policy-scores?top_evidence_limit=20
{"locode":"CL CON","city_name":"Concón"}
// spatial_document_coverage.finest_location_scope: "national"
```

```json
// https://ccglobal.openearth.dev/api/v1/cities/CL%20PAL/action-policy-scores?top_evidence_limit=20
{"locode":"CL PAL","city_name":"Palena"}
// top evidence: "Plan de Acción Regional de Cambio Climático Los Lagos"
```

This explains the apparent Maule evidence for Peñalolén, Los Lagos evidence for Paillaco, and missing Biobío/municipal evidence for Concepción. It is an identity-resolution issue, not merely evidence truncation.

### High — deployment differs from the current scored release artifacts

For all 13 HTTP-200 routes, at least 101 of 102 action records differed from `v1/data/policy_score/scores.jsonl` in score, finding count, document count, or best relevance. Even intended-city routes differ systematically. Examples:

- Santiago `c40_0010`: API score `0.9572`, 40 findings, 9 docs; local score `0.996`, 70 findings, 8 docs.
- Antofagasta `c40_0010`: API score `0.9504`, 44 findings, 8 docs; local score `0.9926`, 71 findings, 7 docs.
- Renca `c40_0010`: API score `0.9615`, 40 findings, 9 docs; local score `0.9978`, 73 findings, 8 docs.

Among correctly identified successful routes, 40–53 action scores differ numerically per city, with maximum absolute differences of `0.2137–0.3009`. This is consistent with a stale or otherwise different deployed ingestion state. The API release UUID alone is insufficient to reconcile it with the local artifacts.

### Medium — documentation and observed route behavior disagree

`v1/policy-api.md` says `scores` contains one object per action “that has policy support.” In practice, every successful route returns all 102 canonical actions. This appears intentional in the deployed implementation because it is uniform across all 13 successful routes and `meta.total_records` is consistently 102, but the contract prose should state that all canonical actions are returned (including how zero/none actions are represented).

## Contract and data-quality checks that passed

- All 13 HTTP-200 responses contain `meta` and `scores`; `meta.api_context.locode` matches the requested LOCODE.
- Every successful response returns all 102 canonical action IDs with no duplicate action IDs.
- All score records contain the documented required fields. Scores are numeric and within 0–1; score categories match the documented thresholds; relevance/category vocabularies are valid.
- Evidence ranks are contiguous and ordered. Required document, type, page, relation, strength, explicitness, relevance, and verbatim text fields are populated; all checked page numbers are positive integers.
- Across all limit-20 successful responses, all **25,462 of 25,462** returned evidence records exactly match `v1/output/action_policy_signals.csv` on action ID, document name, page, and evidence text. No invented summaries or page mismatches were found.
- No duplicate `(document, page, evidence_text)` tuples occurred within an action's returned top-20 evidence.
- For the 10 correctly resolved cities, the highest-scoring themes are broadly reasonable: public-transport/modal-shift, industrial emissions targets, fleet electrification, and circular-economy actions are backed by explicit high-strength commitments/targets from applicable national, regional, or municipal plans.

## Release recommendation

Do not approve this deployment for the intended Chile test-city workflow until the LOCODE-to-city identity issue is resolved, the seven missing routes return data for the intended municipalities, and the deployed ingestion is reconciled with the current `action_policy_signals.csv` / `scores.jsonl` artifacts. Re-run this same 20-city matrix afterward; successful acceptance should require 20/20 intended city-name matches, no cross-region evidence, expected municipal coverage metadata, and explained score parity.
