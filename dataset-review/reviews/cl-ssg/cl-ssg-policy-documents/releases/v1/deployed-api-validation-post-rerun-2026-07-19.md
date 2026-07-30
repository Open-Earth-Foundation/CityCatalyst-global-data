# Chile policy-signal API validation after Mage rerun — 2026-07-19

## Conclusion

**Ready with one material caveat.** The LOCODE, city identity, and spatial applicability failures are fixed across the complete corrected 20-city matrix. However, deployed finding counts and many calculated scores still differ from the current local scoring artifact, so the deployment is not fully release-identical.

## Results

- 20/20 corrected routes returned HTTP 200 at `top_evidence_limit=5` and `20`.
- 20/20 responses echoed the intended LOCODE and municipality name.
- Every response returned all 102 canonical actions.
- No API contract failures were found.
- La Pintana (`CL LPI`) now returns 102 actions with national and Metropolitana regional coverage, correctly reporting no municipal plan.
- Valdivia (`CL ZAL`) now returns its municipal PACCC and the **Los Ríos** PARCC; no Los Lagos regional evidence was observed.
- Expected municipal plans are present for all municipalities where one is expected.
- No cross-region or wrong-municipality documents were found.
- All 39,184 limit-20 evidence records exactly match `action_policy_signals.csv` on action ID, document name, page, and verbatim evidence text.
- No duplicate evidence occurred within an action.

## Per-city route status

| City | LOCODE | HTTP | Scores | Finest scope |
|---|---:|---:|---:|---|
| Santiago | CL SCL | 200 | 102 | municipal |
| Providencia | CL PRO | 200 | 102 | municipal |
| Maipú | CL MAI | 200 | 102 | municipal |
| Puente Alto | CL PTA | 200 | 102 | regional |
| Renca | CL REN | 200 | 102 | municipal |
| La Pintana | CL LPI | 200 | 102 | regional |
| Quilicura | CL QUI | 200 | 102 | municipal |
| Peñalolén | CL PLN | 200 | 102 | municipal |
| Valparaíso | CL VAP | 200 | 102 | municipal |
| Concepción | CL CCP | 200 | 102 | municipal |
| Temuco | CL ZCO | 200 | 102 | municipal |
| Puerto Montt | CL PMC | 200 | 102 | regional |
| Antofagasta | CL ANF | 200 | 102 | regional |
| Valdivia | CL ZAL | 200 | 102 | municipal |
| Paillaco | CL PAO | 200 | 102 | municipal |
| Lago Ranco | CL RNC | 200 | 102 | municipal |
| Panguipulli | CL PAN | 200 | 102 | municipal |
| Frutillar | CL FRT | 200 | 102 | municipal |
| San Nicolás | CL SNI | 200 | 102 | regional |
| Canela | CL CAN | 200 | 102 | regional |

## Remaining caveat: deployed score state differs from local artifact

All 102 records in every city differ from `v1/data/policy_score/scores.jsonl` in at least one of score, `n_findings`, `n_docs`, or `best_relevance`. Numeric scores differ for 40–62 actions per city, with maximum absolute per-city differences from `0.2137` to `0.3385`.

Representative example for Santiago `c40_0010`:

| Field | API | Local score artifact |
|---|---:|---:|
| `policy_support_score` | 0.9572 | 0.9960 |
| `n_findings` | 40 | 70 |
| `n_docs` | 9 | 8 |
| `best_relevance` | high | high |

Because every returned evidence item is genuine and present in the current CSV, this looks like a deployed ingestion-version/finding-set mismatch rather than fabricated or corrupted evidence. Reconcile or rerun the `cl_ssg_action_policy_signals_to_modelled` pipeline with the current `action_policy_signals.csv`, then repeat the score-parity check.

