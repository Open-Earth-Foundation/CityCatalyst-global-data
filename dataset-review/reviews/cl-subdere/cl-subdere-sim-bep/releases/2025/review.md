# Review — cl-subdere-sim-bep, release 2025

## Scope and status

Research, not production-approved and not in a pipeline. The release extracts SUBDERE's public 2025 SIM/BEP municipal-income workbook, recalculates FCM dependency and autonomy from its cash-received budget components, and exports one complete row for each of the project's 345 comunas.

The workbook is the sole financial data input. The notebook does not load or retain the retired SINIM baseline. The capacity-tier CUT list is used only to assert the expected commercially reusable comuna universe.

| Check | Result | Status |
| ----- | ----- | ----- |
| Workbook data rows | 346 | verified |
| Non-reporting Antarctic territory rows removed | 1 | verified |
| Cleaned comunas | 345 unique CUT codes | verified |
| Match to capacity-tier CUT universe | exact | verified |
| Null autonomy values | 0 | verified |
| `IP = IPP + FCM` | all rows | verified |
| Recalculation reproduces workbook ratio | 344 of 345 exactly | verified |
| Maximum workbook-ratio discrepancy | 0.045 percentage points | verified |
| Source vintage | 2026-06-14 | verified |
| Licence | commercial reuse supported; CC0 applies by national default, not by a resource-specific notice | verified with qualification |
| Upstream chain beyond `Fuente: CGR` | not stated by the workbook | unanswered |
| Padre Hurtado migration conflict | 25.6 percentage points in the pre-removal audit | unanswered |
| Natales threshold treatment | 0.500008 dependency | unanswered |

## What this data supports

The release supports a per-comuna financial-autonomy axis calculated entirely from the public SIM/BEP workbook. `fcm_dependency` is FCM received divided by permanent own income including FCM, on the *percibido* basis; `autonomy` is one minus that ratio.

Coverage is complete for the project's 345-comuna universe. No median or other imputation is needed, and no former-source value is copied into the output.

The indicator can be used commercially. The public workbook and landing page display no contrary terms, so Chile's Gobierno Digital open-data standard applies CC0 1.0 by default. This is a government-wide default applied to the resource, not an explicit licence printed inside it.

The workbook's own displayed ratio is a useful cross-check but not the calculation input. The budget components reproduce it exactly for 344 comunas; the one small mismatch demonstrates why the release calculates rather than relabels the stored percentage.

## What this data does not support

Do not call SIM/BEP an independent corroborating source for the retired publication. Both were SUBDERE surfaces grounded in municipal budget-execution reporting. This release stands on its own workbook components.

Do not describe `fcm_dependency` as FCM's share of total municipal revenue. That is the separate `fcm_share_total_income` field and is materially lower.

Do not compare years without deflating. The monetary fields are nominal thousands of pesos, and the workbook is revised in place.

Do not use the *devengado* columns as interchangeable alternatives to *percibido*. They are a different accounting basis; the model uses cash received.

Do not attribute the data to SICOGEN II. The workbook states `Fuente: CGR` but does not name a system below the Comptroller.

Do not describe CC0 as a resource-specific SUBDERE notice. If an explicit owner statement is contractually required, request confirmation from `sim@subdere.gov.cl`.

## Using it downstream

Join on `comuna_cut` as a zero-padded five-character string. The release carries no locode; consumers resolve `actor_id` through the administrative-boundary lookup and must not use `city_id` as the primary city key.

Read `autonomy` directly. The consuming transformer should remove its SINIM read and median fill rather than recalculating the same value from a second publication. Preserve `source_vintage` in staging or pipeline metadata so an in-place workbook revision is detectable.

Pair this release with `cl-municipal-capacity-tier` for the v3 city profile. Together those two inputs permit commercial use, subject to SIM/BEP's CC0 default position and INE's CC BY-SA 4.0 attribution/share-alike conditions.

The modelled table does not need a new column: its established `autonomy`, `capacity` and `city_archetype` contract remains sufficient. Upstream vintage and basis fields can remain in the release/staging audit trail if the current modelled schema is intentionally kept narrow.

## Migration cautions

The pre-removal substitution audit recorded four archetype changes. That comparison dataset has been hard-removed and is not required to build this release. Two decisions remain material:

- Padre Hurtado was recorded with a 25.6 percentage-point difference in dependency. Spot-check the CGR/SUBDERE components or explicitly accept SIM/BEP as authoritative before promotion.
- Natales has SIM/BEP dependency 0.500008, effectively on the model's 0.5 boundary. Define a tolerance or indeterminate treatment instead of presenting the change as substantive.

These are migration/adjudication questions, not licence blockers and not missing values in the SIM/BEP output.

## Notes on non-obvious fields

`fcm_dependency` is FCM over permanent own income including FCM. `fcm_share_total_income` is FCM over total income. They are not interchangeable.

`autonomy` is `1 − fcm_dependency`, clipped to the unit interval and rounded to six decimal places in the output.

The `_percibido_` and `_devengado_` pairs are cash-received and accrued accounting bases.

`fcm_contribution_ratio` and `operational_autonomy` are carried unused. Neither is validated as a model input in this release.

`source_vintage` is the revision stamp in the workbook banner, not the download date.

## Traceability

The workbook is anonymously downloadable from the direct SUBDERE URL; the public SIM Ciudadano landing page and placement instructions are in the README. Cell A1 and the compliance sheet establish the `Fuente: CGR` attribution. The licence position rests on the Gobierno Digital standard, Ley 20.285 Article 19 and the absence of contrary terms on the page and workbook.

**References**

- extraction, recalculation and validation: `01_sim_bep_extract.ipynb`
- cleaned output: `data/sim_municipal_income_2025.csv`
- source workbook (gitignored): `sample/indicadores-ingresos-municipales-2025.xlsx`
- public landing page: `https://ciudadano.subdere.gob.cl/indicadores-presupuestarios/`
- capacity pairing: `reviews/oef/cl-municipal-capacity-tier/releases/v1`
- consuming model: `reviews/oef/cl-city-action-fundability/releases/v3`
- consuming transformer: `cc-mage/transformers/transform_city_finance_profile.py`
- licence basis: `https://wikiguias.digital.gob.cl/Est%C3%A1ndares/Datos-Abiertos`
