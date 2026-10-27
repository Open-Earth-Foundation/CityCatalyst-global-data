# Review — cl-city-action-fundability, release v3 (city profile)

## Scope and status

Research, not production-approved. This release replaces **both inputs to the model's city profile** while keeping the model contract unchanged:

- `capacity` is consumed from `cl-municipal-capacity-tier`, derived from INE Censo 2024 population and the published MEED bands;
- `autonomy` is consumed from `cl-subdere-sim-bep`, recalculated from SUBDERE's public 2025 municipal-income workbook; and
- `city_archetype` is recomputed from the same 0.5 thresholds and the same four labels used by v1.

The release number remains v3 because this is the same unpromoted city-profile change, completed with the replacement autonomy source. The notebook no longer loads SINIM, reproduces its staffing baseline or retains the consultant FCM extract. The old data is not relabelled: both axes are read from their reviewed replacement outputs.

The route logic, score bands, finance inventory and database schema are out of scope and unchanged.

| Check | Result | Status |
| ----- | ----- | ----- |
| Capacity rows | 345 unique CUT codes | verified |
| SIM/BEP autonomy rows | 345 unique CUT codes | verified |
| Join coverage | exact 345-to-345 key match | verified |
| Null or out-of-range axes | none | verified |
| Capacity consumed unchanged | exact match to source release | verified |
| Autonomy consumed unchanged | exact match to source release | verified |
| SIM/BEP source vintage | 2026-06-14 | verified |
| Archetype counts | 65 Self-sufficient / 105 Delivery-ready / 25 Well-resourced / 150 Support-ready | verified |
| Archetype changes against the former profile | 4 of 345 | verified in the SIM/BEP source review |
| SINIM-derived data loaded or exported by v3 | none | verified |
| T4 score band | 0.10, provisional | unanswered |
| T1 evidence gate | not joined; assigned on population | unanswered |
| Padre Hurtado source conflict | 25.6 percentage points | unanswered |
| Natales threshold edge | eight parts per million below 0.5 in SIM/BEP | unanswered |

## What this data supports

The v3 city profile can be rebuilt for all 345 Chilean comunas from the two replacement reviews without a SINIM input or a median fill. Both axes preserve their existing meaning and scale, so the current database columns and downstream score function remain valid.

The four archetype names remain stable. Relative to the former city profile, only Rinconada, Frutillar, Natales and Padre Hurtado cross an autonomy threshold; the detailed substitution comparison lives in the SIM/BEP review, not as copied restricted-source data in this release.

The city layer is usable commercially, subject to its two actual licence bases. INE's capacity input is CC BY-SA 4.0, which permits commercial use with attribution and share-alike. The public SIM/BEP workbook displays no resource-specific terms; CC0 applies by default under Chile's Gobierno Digital open-data standard. The SIM/BEP CC0 position is therefore government-default/inferred, not an explicit licence label printed in the workbook.

The capacity tier determines which action types trigger a technical-assistance escalation. A T1 comuna escalates on none of the current action bands, T2 on infrastructure, T3 on anything beyond a regulation, and T4 on everything at the provisional 0.10 value.

## What this data does not support

Do not call the full fundability product commercially clear solely because this city profile is clear. Finance inputs retain their own terms, including CORFO `CC BY-NC-ND`, and any combined redistribution inherits the most restrictive applicable source terms.

Do not describe CC0 as a licence printed by SUBDERE on this workbook. It is the national default applied because no resource-specific or contrary terms are displayed. Obtain written confirmation from SUBDERE if a customer or counsel requires an explicit owner statement.

Do not treat the capacity tier as a direct measurement of a municipality's institution. It is a population proxy; every comuna in a tier receives the same value.

Do not report T4 = 0.10 as settled or infer that a T1 comuna has a SECPLA and recent public-investment execution. Those source-methodology conditions remain unresolved.

Do not treat the Padre Hurtado replacement value as settled. Its SIM/BEP dependency differs from the former source by 25.6 percentage points, far beyond ordinary drift. Do not present Natales as a substantive reclassification either: it lies effectively on the 0.5 threshold.

## Using it downstream

Join on `comuna_cut` as a zero-padded five-character string. The release carries no `actor_id`; the existing transformer should continue resolving `actor_id`/locode through the administrative-boundary lookup. Do not use `city_id` as the city key.

The output is `data/city_finance_profile.csv`. The modelled contract remains:

`actor_id`, `autonomy`, `capacity`, `city_archetype`, `country_code`, `source_dataset`, `release_id`.

The pipeline uses `oef/cl-city-action-fundability` as the consolidated `source_dataset` and v3 is registered in the catalog. The combined profile is not labelled as SIM/BEP alone because each row also contains the INE-derived capacity tier.

No database migration or table alteration is required. The implemented **data and pipeline change**:

1. reads the consolidated reviewed v3 CSV from S3;
2. performs no axis recalculation or imputation in Mage;
3. stages the joined v3 rows and resolves locodes as before;
4. explicitly deletes the retired SINIM-backed rows and any prior OEF city-profile rows inside the insert transaction; and
5. raises if inserted row counts differ or any retired row remains.

The exporter includes an explicit cleanup set for both the retired SINIM identity and any prior OEF city-profile rows. That cleanup and the v3 insert run in one transaction, so a failed insert cannot leave the table partially replaced. This is a data/pipeline change rather than a table-schema migration.

Mage run 170 completed on 31 August 2026 using the checked-in v3 trigger parameters and the reviewed CSV at `s3://test-global-api/raw_data/oef/cl_city_action_fundability/release/v3/cl_city_action_fundability.csv`. Post-load verification found 341 locode-resolved rows under `oef/cl-city-action-fundability`, release `v3`, and zero rows under the retired `cl-subdere/cl-subdere-sinim` identity. The archetype counts were Support-ready 149, Delivery-ready 105, Self-sufficient 65 and Well-resourced 22. Catalog promotion remains separate from this successful pipeline/database verification.

The pipeline's deletion scope is the modelled database table. S3 retention or deletion is a separate storage-lifecycle decision and is not required for the database replacement to succeed.

The two axes run on different clocks: capacity is based on the 2024 census; autonomy is the 2025 accounting year from a workbook revised on 14 June 2026. Preserve both upstream release identities in pipeline configuration even though the modelled table stores the consolidated product release.

## Notes on non-obvious fields

`capacity` and `gl_technical_capacity` are the same tier value on 0–1 and 0–100 scales. They are consumed unchanged from the capacity-tier review.

`autonomy` is already calculated by the SIM/BEP release as `1 − fcm_dependency`, where dependency is FCM received divided by permanent own income including FCM on the *percibido* basis. v3 reads that value and does not recalculate it from another publication.

`capacity_basis` identifies the population-tramo rule. `autonomy_basis` identifies the SIM/BEP cash-received calculation. `autonomy_source_vintage` is the workbook's internal revision stamp, not the download date.

`t4_provisional` marks rows whose capacity depends on the undecided T4 band. It is not a missing-data flag.

## Open decisions before promotion

1. Decide the T4 capacity value left undefined by the source methodology.
2. Decide whether T1 remains population-assigned or is evidence-gated on SECPLA and public-investment execution.
3. Resolve or explicitly accept Padre Hurtado's 25.6 percentage-point source disagreement.
4. Define threshold handling for Natales and other values effectively equal to 0.5, for example a documented tolerance or an indeterminate flag.

The licence confirmation is no longer a normal promotion blocker: commercial reuse is supported by the national default. It remains a legal/commercial escalation only if an explicit owner statement is required.

## Traceability

The notebook reads only the two reviewed cleaned outputs and exports their joined city profile. It contains no former-source baseline or copied consultant financial values. The detailed source extraction, definitions, caveats and licence evidence remain authoritative in the upstream reviews.

**References**

- join, assertions and export: `01_city_profile_v3.ipynb`
- city profile output: `data/city_finance_profile.csv`
- capacity source: `reviews/oef/cl-municipal-capacity-tier/releases/v1`
- autonomy source: `reviews/cl-subdere/cl-subdere-sim-bep/releases/2025`
- population source: `reviews/cl-ine/cl-ine-censo/releases/2024`
- model methodology: `../../methodology.md`
- consuming transformer: `cc-mage/transformers/transform_city_finance_profile.py`
