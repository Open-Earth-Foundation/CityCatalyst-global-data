# Review — cl-ssg-municipal-income, release 2025

## Scope and status

Research, not production-approved and not in a pipeline. The release extracts the BEP income sheet from SSG's `Analisis_Version_2.xlsx` into one row per comuna and one column per budget code. It does no classification or summing; that is the consuming model's job.

| Check | Result | Status |
| ----- | ----- | ----- |
| Comuna rows | 345 unique CUT codes | verified |
| Sector and period | municipal, Q4 (full year), every row | verified |
| Budget codes | 182 | verified |
| Subtitle lines add up to the workbook `Total` | all 345 rows | verified |
| Comunas reporting income | 340 | verified |
| Comunas reporting nothing | 5 (San Pedro de Atacama, Rinconada, Lota, Curacautín, Frutillar) | verified |
| FCM and total income match SIM/BEP | 298 of 340 | verified |
| Upstream source of the line items | likely SINIM; not stated in the file | inferred |
| Licence | programme-internal; commercial use not cleared | decided here, not verified |

## What this data supports

Line-by-line municipal income for 2025, for building measures that SUBDERE's published totals cannot give, such as other permanent income. The budget lines nest cleanly: the classification in `oef/cl-city-action-fundability/releases/v4` splits every reporting comuna's total income into IPP, other permanent income, FCM and excluded lines with no remainder.

The lines that make up SUBDERE's IPP can be identified. Fifteen codes reproduce SIM/BEP's published IPP to within 3 M$ for 286 of the 298 comunas where the snapshots agree.

## What this data does not support

Do not use it for commercial outputs. The upstream source is most likely SINIM, and nothing in the file says otherwise.

Do not treat it as the same snapshot as `cl-subdere-sim-bep`. 42 reporting comunas differ on FCM or total income.

Do not read the five non-reporting comunas as having zero income.

Do not sum parent and child codes together.

## Using it downstream

Join on `comuna_cut` as a zero-padded five-character string. Filter on `reported` before summing anything. Pick codes that do not nest inside one another; the v4 fundability notebook shows how to test for that.

## Traceability

**References**

- extraction and checks: `01_extract_income_lines.ipynb`
- output: `data/bep_income_lines_2025.csv`
- source workbook (gitignored): `sample/Analisis_Version_2.xlsx`
- the SSG methodology that asks for this measure: `MEED_Metodologia_Consolidada_y_Anexo_HIAP VF Consolidado.docx`, section 5.3 (project drive, *08 Law and Regulations Analysis*)
- consuming release: `reviews/oef/cl-city-action-fundability/releases/v4`
- public totals it is checked against: `reviews/cl-subdere/cl-subdere-sim-bep/releases/2025`
