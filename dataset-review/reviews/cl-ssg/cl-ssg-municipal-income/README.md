# SSG municipal income line items (cl-ssg-municipal-income)

Comuna-level municipal income for 2025, broken down by every line of the national municipal budget classifier (`115.xx…`), as supplied by SSG for the MEED programme. It holds the detail behind SUBDERE's published totals: where SIM/BEP gives one IPP figure per comuna, this sheet shows the 182 budget lines that IPP, FCM and everything else are built from.

**At a glance**

- **Status:** research. Not production-approved, not in a pipeline, not catalog-registered.
- **Coverage:** 345 comunas, accounting year 2025, fourth quarter (full year), municipal sector only, cash received (*percibido*). 340 report income; 5 report nothing.
- **Licence:** **programme-internal, not verified.** Supplied by SSG; the line items most likely come from SINIM, whose terms exclude commercial use.
- **Headline:** the only line-item source we hold that separates "other permanent income" from IPP and FCM, which the SSG review of the financial-feasibility model asks for.

## Why we use it

SSG's review of the fundability model (MEED consolidated methodology, annex section 5.3) asks for a city's own money to include **other permanent income**: recurring income that is neither a municipal tax or fee (IPP) nor the Fondo Común Municipal (FCM). SUBDERE's public SIM/BEP workbook publishes only the IPP, FCM and total figures, so that income cannot be separated from it. This sheet can.

It is consumed by `reviews/oef/cl-city-action-fundability/releases/v4`, which reads only the other-permanent-income lines from it and keeps IPP and FCM from SIM/BEP.

## Canonical source

Internal working data, no public URL. The sheet `BEP INGRESOS MUNICIPALES 2025` sits inside SSG's `Analisis Version 2.xlsx`, shared in the MEED project drive under *08 Law and Regulations Analysis* (file dated 6 July 2026). The workbook's second sheet, `ANALISIS`, is SSG's own summary with an IPP / FCM / OI tag per code; it is not read here, because the consuming release classifies the codes itself at a finer level.

**Re-download:** copy `Analisis Version 2.xlsx` from the project drive into `releases/2025/sample/` as `Analisis_Version_2.xlsx` (gitignored) and run the notebook.

**Where the figures come from upstream is unanswered.** The sheet carries no banner or source line. Its layout (region banner rows, `Sector`, `Trimestre`, one column per classifier line) matches SINIM's BEP income report, and its totals match SUBDERE's CGR-based SIM/BEP figures wherever the two snapshots agree. *[inferred]*

## Licence

> **Programme-internal; not cleared for commercial use.** No licence travels with the file. Like the other `cl-ssg` reviews, this is SSG working data supplied for the SSG / OpenEarth programme and usable within it. *[decided here, not verified]*

Being SSG's file does not clear the underlying figures. If they are a SINIM export, SINIM's portal terms (*sin fines comerciales*) are the most restrictive upstream condition, and anything built on this sheet inherits them. This is why `cl-subdere-sim-bep` replaced SINIM for the v3 autonomy axis. Two routes would clear it: SSG confirming a different, open source for the line items, or SUBDERE publishing the line-item breakdown on SIM. *(Not legal advice.)*

## Spatial and temporal scope

345 comunas keyed on the five-digit CUT (leading zeros significant), accounting year 2025, Q4 cumulative. Money is in thousands of nominal pesos (M$). The sheet covers the **municipal sector only**: the separate education and health sectors that some municipalities run are not in it, although some transfers for those services still pass through municipal accounts (see the classification in the consuming release).

## Interpretation warnings

**This is a different download from the SIM/BEP release.** FCM and total income agree with `cl-subdere-sim-bep` for 298 of the 340 reporting comunas. For the other 42 the figures differ, sometimes a lot (Antofagasta's total income is 192.5 bn here against 149.6 bn in SIM/BEP; Padre Hurtado's FCM is 15.9 bn against 8.2 bn). Do not mix the two for the same measure without saying so.

**Five comunas report nothing.** San Pedro de Atacama, Rinconada, Lota, Curacautín and Frutillar have zero on every line. They have `reported = false`. This is missing data, not zero income.

**Parent and child codes are both present.** `115.03.00.000.000.000` is the sum of its children, which are also columns. Sum only codes that do not nest inside each other, or totals double.

**Some lines are collected for someone else.** Lines marked *de beneficio Fondo Común Municipal*, *de beneficio servicios de salud* or *de beneficio otras municipalidades* are collected by the municipality and passed on. They are not its money.

## Parsing notes

**Header is rows 4 and 5.** Row 4 holds the budget codes, row 5 the labels. Data rows have a comuna code in column B; the region banner rows between them do not.

**Codes carry trailing spaces** in the workbook. They are stripped in the output.

**The `Total` column sits after the last code**, not in the last column of the sheet; the sheet reports more used columns than it has data. Find it by label.

**CUT is an integer in the workbook.** Pad to five characters.

## Current approved release

**2025**: research, not in `catalog/index.yaml`. Output `releases/2025/data/bep_income_lines_2025.csv`, 345 rows × 185 columns (`comuna_cut`, `comuna`, `reported`, then one column per budget code). Contract in `releases/2025/review.md`.
