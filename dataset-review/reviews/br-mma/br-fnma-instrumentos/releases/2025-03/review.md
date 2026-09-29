# Review — FNMA transfer instruments, release 2025-03

## Scope and status

This research release contains a cleaned, bilingual-schema table of 1,495 FNMA transfer instruments, a restartable extraction notebook, a standard-library build script and a draft mapping to the held adaptation-action bank. Controlled labels are translated into English and preserved in Portuguese. All 46 distinct non-empty origin-call descriptions and all 27 project titles that repeat in the release have reviewed English translations. The 1,421 singleton project titles remain blank in English with an explicit pending status. The release is not production-approved.

| Check | Result |
|---|---:|
| Source records | 1,495 |
| Observed years | 1990–2024 |
| Explicitly cancelled records | 13 |
| Planned FNMA amount | R$313,760,048.78 |
| Planned counterpart | R$97,742,203.92 |
| Published planned project total | R$411,707,559.03 |
| High-confidence action links | 106 |
| Medium-confidence links pending adjudication | 756 |
| Explicitly unmapped records | 633 |
| Distinct origin-call descriptions translated | 46 of 46 (531 rows) |
| Distinct project titles translated | 27 of 1,448 (74 rows) |
| Distinct project titles pending | 1,421 (1,421 rows) |

## Visual summary

The notebook's year chart shows that this is primarily a historical portfolio: 1,461 of 1,495 records predate 2020, and no records appear for 2021 or 2022. Civil-society organisations account for 717 records and municipalities for 446. Environmental education is the largest theme by count, while water and forests carries the largest planned FNMA amount. The notebook should be rerun for the rendered chart after any source refresh.

## What this data supports

The release supports the statement: “FNMA recorded 1,495 signed transfer instruments from 1990 through 2024 with planned FNMA contributions totalling R$313.76 million.” This claim must retain “planned” and must note that the total includes thirteen cancelled records.

The release supports the statement: “Municipal governments appear as the executing institution in 446 historical FNMA records.” This describes the publisher's executor sphere, not proof that every named municipality was the sole beneficiary or project location.

The release supports state-level searches for potentially comparable environmental projects because every row has a UF, title, executor, planned BRL values and at least one publisher identifier. Municipality-level use is conditional because the city field is the executor's headquarters, is blank in 847 rows and has no IBGE code.

The release supports using 106 high-confidence links as candidates for adaptation-project review because the project title explicitly names restoration, watershed protection or urban tree planting. The action match remains an OEF interpretation, not a classification supplied by FNMA.

## What this data does not support

The sentence “FNMA disbursed R$313.76 million” is not supported. The dictionary defines the amount as planned for transfer, and this file has no disbursement or payment field.

The sentence “These projects were completed successfully” is not supported. The source has no comprehensive execution or outcome status, and an end-of-validity date does not establish completion.

The sentence “All rows are adaptation projects” is not supported. FNMA is a broad environmental fund, its themes do not state adaptation relevance, and 633 records have no defensible current action match.

The sentence “The portfolio covers projects signed through March 2025” is not supported by the downloaded file. Its latest year is 2024 even though the catalogue title and description mention 2025.

The sentence “The published project total always equals FNMA plus counterpart” is not supported. Source line 1435 differs by R$205,306.33, and the release preserves that defect rather than selecting a corrected value.

## Using it downstream

Downstream use should treat each row as one source-reported transfer instrument and should keep the internal identifier separate from the SIAFI/Transferegov identifier. The latter is present in only 97 rows but is the preferred bridge to more detailed execution evidence.

Planned FNMA, planned counterpart and planned total must remain separate measures. Historical nominal BRL values should not be ranked across decades without a documented deflator and reference date. Cancelled rows should be retained for traceability and excluded explicitly from analyses of non-cancelled portfolios.

Portuguese free text is authoritative. Applications may display `project_title` only where `project_title_translation_status=reviewed_exact_translation`; otherwise they must display `project_title_pt` with a language label. Every non-empty origin call has a reviewed English value, while missing source calls remain blank and explicitly not applicable. The status fields prevent untranslated Portuguese from being mistaken for English, and proper names remain source identifiers.

Medium-confidence action links represent themes, components or enabling instruments rather than exact equivalence and require human adjudication. Mapping fan-out is not used, so no project amount should be attributed to an action solely through this crosswalk.

## Benchmark values a city can use

The figures below are historical comparator priors for understanding the scale and delivery channel of FNMA-supported instruments. They are not current grant limits, real-price estimates or guarantees of eligibility.

| Comparator | Records | Planned FNMA amount | Published planned project amount |
|---|---:|---:|---:|
| All instruments | 1,495 | median R$124,000; range R$1,515.45–R$12,040,350.64 | median R$175,970; range R$2,020.45–R$12,052,405 |
| Records not explicitly cancelled | 1,482 | total R$298,857,247.58 | total R$395,931,096.57 |
| Explicitly cancelled records | 13 | total R$14,902,801.20 | total R$15,776,462.46 |
| Municipal executors | 446 | total R$117,021,054.60 | Source-level planned values only |
| Civil-society executors | 717 | total R$131,280,326.26 | Source-level planned values only |

The strongest replicable lesson is the delivery mix: FNMA historically used both call-based selection (568 records) and unsolicited demand (927 records), with municipal, state, federal and civil-society executors. These counts show observed routes, not routes currently open to applications.

## Notes on non-obvious fields

`record_status=not_stated` means the CSV contains no explicit cancellation marker; it does not mean active, completed or paid. `funding_stage=signed_transfer_instrument` reflects the publisher's definition of the dataset and must not be promoted to a payment stage.

`amount_reconciliation_difference_brl` is FNMA planned amount plus planned counterpart minus the published planned total. It is zero for all but one source row and exists to preserve that defect visibly.

`date_parse_status` records separate signature, gazette and end-date outcomes. An empty ISO date can mean a missing source value, an invalid source value or the literal cancellation marker; the source text columns distinguish those cases.

The mapping's `none` rows are deliberate decisions, not missing work. `mapping_confidence=medium` and `adjudication_status=pending` identify the 756 links that require human review before production use.

## Traceability

The release was built from the official MMA CSV downloaded on 24 September 2026 and the accompanying official data dictionary. The raw inputs remain in the gitignored sample folder and can be re-downloaded from the canonical URLs in the review README. The build validates 46 distinct call translations, 27 distinct repeated-title translations, 1,421 distinct pending singleton titles and 531 call-bearing rows. The adaptation action bank is a local dependency held with the BNDES review; all referenced target identifiers were validated against that file. Translation work left the mapping byte-for-byte unchanged at SHA-256 `56e769ea1010484073599bfedadb3718b383b30456775d9c6bd3e69ed8f4b5c7`. No human mapping adjudication has occurred.

References:

- Review and canonical retrieval instructions → `dataset-review/reviews/br-mma/br-fnma-instrumentos/README.md`
- Build script → `dataset-review/reviews/br-mma/br-fnma-instrumentos/releases/2025-03/build_release.py`
- Extraction notebook → `dataset-review/reviews/br-mma/br-fnma-instrumentos/releases/2025-03/extract_clean.ipynb`
- Cleaned table → `dataset-review/reviews/br-mma/br-fnma-instrumentos/releases/2025-03/data/br_fnma_transfer_instruments.csv`
- Draft mapping → `dataset-review/reviews/br-mma/br-fnma-instrumentos/releases/2025-03/data/br_fnma_transfer_instruments_to_adaptation_actions.csv`
- Action-bank dependency → `dataset-review/reviews/br-bndes/br-bndes-operacoes-financiamento/releases/2026-09-01/sample/adaptation_action_bank_icb_oef_v13.csv`
