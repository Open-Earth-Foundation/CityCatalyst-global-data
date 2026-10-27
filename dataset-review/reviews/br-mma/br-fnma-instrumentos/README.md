# Ministério do Meio Ambiente e Mudança do Clima — Instrumentos de repasse FNMA 1990 a 2025

This review covers the public table of transfer instruments signed by the Fundo Nacional do Meio Ambiente (FNMA), the environmental fund run by the Ministério do Meio Ambiente e Mudança do Clima (MMA). The canonical file retrieved on 24 September 2026 contains 1,495 records for 1990–2024, despite the catalogue title saying 1990–2025. **Status: provenance, licence, profiling, methodology, fit assessment, a reproducible cleaned release, all call-description translations and an audited subset of project-title translations are complete. The 1,421 singleton project titles, medium-confidence mapping adjudication and publisher clarification of one amount defect remain pending.** Nothing here is production-approved.

## Canonical downloads

The canonical source is the FNMA record on the MMA open-data portal, a CKAN catalogue maintained by the Departamento de Gestão de Fundos e de Recursos Externos. The record contains the agreements CSV and a one-page data dictionary. The portal record was created on 12 June 2018 and last updated on 29 January 2026; no update cadence is stated (**verified**, 24 September 2026).

The CSV resource is titled “Instrumentos de repasse FNMA 1990 a 2025” and described as instruments signed from 1990 through March 2025. The downloaded file itself contains 1,495 rows whose year field ends in 2024, so the title and description overstate the observed temporal coverage (**verified**). The file name also says 1990–2024. Release `2025-03` follows the publisher's claimed cut-off but the cleaned data preserves the observed 1990–2024 coverage.

Scripted retrieval from the fixed resource URL succeeded on 24 September 2026. The 464,959-byte CSV has SHA-256 `7346517659194703df3bd3d9c6784b62af512b992caeaa2fd32a6e4cadaddfb0`; it is UTF-8 with a byte-order mark, semicolon-delimited and uses CRLF line endings. The 97,362-byte dictionary has SHA-256 `b0c11e7d3690bd5327a1528548975dbc0d2aedfe7cf1acd75e5561d49d904330` (**verified**).

References:

- Dataset record → https://dados.mma.gov.br/dataset/fundo-nacional-do-meio-ambiente
- Agreements CSV → https://dados.mma.gov.br/dataset/1eac548e-b245-4126-9a9f-259441aeebd6/resource/4e117582-ce72-4e5e-934c-bafb463ebe4c/download/projetos-fnma-1990-a-2024-dados-abertos-2025.csv
- Data dictionary → https://dados.mma.gov.br/dataset/1eac548e-b245-4126-9a9f-259441aeebd6/resource/2339001c-b810-4888-88a6-b604da18fda2/download/dicionario-dados-abertos-fnma.pdf
- FNMA execution guidance → https://www.gov.br/mma/pt-br/composicao/secex/dfre/fundo-nacional-do-meio-ambiente/execucao-de-projetos
- Retrieval inputs → `releases/2025-03/sample/`

## Why we use it

The table provides long-run, project-level evidence for Brazil's domestic environmental-grant pathway. It preserves a project title, executor and executor sphere, state, planned FNMA contribution, planned counterpart and the publisher's selection route. The source is broad environmental finance rather than an adaptation portfolio, so relevance is assessed record by record and is never assumed from FNMA funding alone.

The closest sibling is the FNMC projects dataset, which covers the climate fund's non-reimbursable arm with more explicit climate categories. Transferegov is the operational complement for recent execution and payment history where identifiers can be joined; this FNMA file remains useful because it reaches back to 1990.

References:

- Originating need → `dataset-discovery/needs/2026-09-br-finance-pathways-review/search.yaml`
- FNMC sibling review → `dataset-review/reviews/br-mma/br-fnmc-projetos/`
- Transferegov sibling review → `dataset-review/reviews/br-mgi/br-transferegov-discricionarias-legais/`

## License

The dataset record and both resources state “Creative Commons Atribuição (CC-BY)” and link to the Open Definition entry for CC BY (**verified**, 24 September 2026). CC BY permits copying, redistribution, adaptation and commercial use with attribution. The cleaned data can therefore be redistributed and translated if MMA/FNMA is credited and changes are indicated.

The licence version is not stated (**unanswered**). The portal links to a generic entry covering multiple CC BY versions, so the release follows the conservative CC BY 4.0 attribution practice: identify MMA/FNMA and the dataset, link the source and licence, and state that fields were cleaned and controlled labels translated. No prescribed citation appears in the record, resources, dictionary or CSV (**verified absent**).

The gov.br FNMA pages and call documents carry CC BY-ND 3.0 in the site footer (**verified**, 24 September 2026). That no-derivatives notice does not govern the separately licensed CSV. Programme text from gov.br must not be copied or translated as though the CSV licence applied. No replacement source is required for the portfolio data because the CSV has a reuse-compatible licence; Transferegov is a complementary execution source, not a rights workaround.

| Finding | Status | Consequence |
|---|---|---|
| CSV and dictionary are labelled CC BY | **verified** | Commercial reuse, cleaning and translation are allowed with attribution. |
| CC BY version | **unanswered** | Apply CC BY 4.0-style attribution conservatively and seek MMA confirmation before production sign-off. |
| gov.br FNMA pages are CC BY-ND 3.0 | **verified** | Do not adapt call text copied from those pages without separate legal clearance. |
| Prescribed citation | **verified absent** | Use the working attribution documented above. |

## Data profile

The CSV contains 1,495 transfer-instrument rows and 19 columns. There are no empty or exact duplicate rows. Every row has at least one of the two publisher identifiers, but the identifiers are not uniformly populated: 1,398 rows lack a Transferegov/SIAFI instrument number and 11 lack the internal number (**verified**).

| Source field | Meaning from the dictionary | Observed issue |
|---|---|---|
| `Ano` | Year the transfer instrument was signed | Covers 1990–2024 with gaps; no 2025 row. |
| `Nº do Instrumento de Repasse` | SIAFI or Transferegov instrument number | Blank in 1,398 rows. |
| `Nº Interno` | Instrument number within MMA | Blank in 11 rows; generic values such as `CR/Caixa` repeat. |
| `Tema` | Project theme | Thirteen values; `ANULADO` is used as a status for 12 rows, overwriting the actual theme. |
| `Instituição Executora` | Project executor | Complete, but names are not normalized identifiers. |
| `Título do Projeto` | Executor-defined project title | Complete Portuguese free text; 66 rows participate in repeated-title groups. |
| `UF`, region and executor city | Place of execution and executor headquarters | State and region complete; city blank in 847 rows and is not necessarily the project location. |
| `Bioma` | Biome where executed | Blank in 10 rows; categories include broad and combined labels. |
| `Esfera Institucional` | Executor sphere | 717 civil-society, 446 municipal, 185 state and 147 federal records. |
| Signature, DOU and end dates | Instrument dates | Signature blank in 412 rows, DOU date blank in 28 raw rows, end date blank in 35 raw rows; eight populated values are invalid. |
| FNMA, counterpart and total values | Planned amounts in BRL | One record fails `FNMA + counterpart = total` by R$205,306.33. |
| Selection type and origin call | Unsolicited or call-based route and source call | Selection type complete; origin call blank in 964 rows. |

The planned FNMA amount totals R$313,760,048.78; planned counterpart totals R$97,742,203.92; and published planned project totals sum to R$411,707,559.03. These totals include thirteen records marked cancelled. The one internally inconsistent row is source line 1435, project “Fomentar a produção de sementes e mudas de espécies florestais nativas”: R$100,082.67 from FNMA plus R$5,210.00 counterpart does not equal the published R$310,599.00 total (**verified**). The cleaned release retains every source amount and records the R$−205,306.33 difference instead of choosing a correction.

## Spatial and temporal scope

Observed years run from 1990 to 2024, with no records for 2008, 2009, 2019, 2021 or 2022. Only 34 records are from 2020 onward. This is a long-run historical portfolio, not a current opportunity list (**verified**).

All rows have a state code and one of five regions, but the dictionary defines the city as the headquarters of the executing institution rather than necessarily the project location. The city is blank for 847 records and there is no IBGE municipality code or UN/LOCODE. State-level comparison is supported; municipal joins are conditional and need name-plus-state matching with manual review (**verified**).

## Methodology

The publisher describes the rows as transfer instruments signed by FNMA, and the dictionary defines `Ano` as the year of signing. The three money fields are planned values: the total FNMA amount intended for transfer, the executor's planned counterpart and their sum as the planned project total (**verified**). They are not disbursements, expenditure or project outcomes.

FNMA guidance says supported projects are executed through Transferegov, where proposal, physical and financial execution and accountability stages are managed (**verified**). This CSV does not expose those stages. A joined Transferegov record is therefore required before claiming an amount was paid or an activity delivered.

The source states no uncertainty model, inflation adjustment, price-year normalization or evaluation methodology (**verified absent**). Historical BRL values must not be compared as real purchasing power without an external deflator, and planned amounts must not be treated as achieved costs.

## Fit for the Brazil finance-pathway need

The source is usable as historical grant evidence with important conditions. It passes the reuse-rights constraint and supplies record-level amounts and recipients, but municipal geography, exact instrument type, execution status and adaptation relevance remain incomplete.

| Requirement | Result | Evidence |
|---|---|---|
| Native record ID | **pass** | Every row has an internal or SIAFI/Transferegov identifier; neither field is complete alone. |
| Recipient name and type | **pass** | Executor and four publisher-defined spheres are complete. |
| Recipient geography | **conditional** | UF is complete, but city is executor headquarters, 847 cities are blank and no IBGE code is supplied. |
| Funder or programme | **pass** | The dataset is explicitly the FNMA portfolio. |
| Instrument | **conditional** | Every row is a signed transfer instrument, but agreement subtype is not separately normalized. |
| Amount with meaning | **pass** | Planned FNMA, counterpart and total BRL values are explicit; one defect is flagged. |
| Stage and date | **conditional** | The dataset asserts signed instruments, but 412 signature dates are blank and post-signature stage is absent. |
| Project description | **pass** | All rows have an executor-defined title. |
| Disbursement or payment | **fail** | No paid or executed amount is supplied. |
| Source-stated adaptation relevance | **fail** | Themes are environmental and do not assert adaptation relevance. |
| Link to other sources | **conditional** | Only 97 rows carry the SIAFI/Transferegov identifier intended for an operational join. |
| Commercial reuse | **pass** | The CSV is labelled CC BY; the missing version remains a sign-off question. |

The main surprise is the mismatch between the advertised 2025 cut-off and the file's 2024 maximum. The second is that a supposedly thematic field contains cancellation status, while another cancellation is encoded only as an end-date value. These defects make separate source-preserving status and theme handling necessary (**verified**).

## Interpretation warnings

The values are planned amounts attached to signed instruments, not money demonstrably disbursed or spent. A row supports the statement that FNMA recorded a transfer instrument with those planned values; it does not support a delivery, impact or current-eligibility claim.

Thirteen records are explicitly cancelled. Twelve place `ANULADO` in the theme field and one places `Anulado` only in the end-date field. These records remain in the release with `record_status=cancelled`; excluding only the theme value would miss one cancellation (**verified**).

The remaining 1,482 rows have `record_status=not_stated`, not “active” or “completed”. End dates may be historical, future or missing, and the file supplies no comprehensive status field. Expired validity is not proof of successful completion (**verified**).

The adaptation crosswalk is analytical, not publisher evidence. High-confidence links require an explicit action in the project title; medium links use broader themes or enabling instruments and require human adjudication. Unmapped rows remain in the mapping with `mapping_confidence=none` so the absence of a defensible match is auditable.

## Parsing notes

The file is UTF-8 with a byte-order mark, semicolon-delimited and contains embedded newlines in quoted text. It must be opened with a CSV-aware parser and `utf-8-sig`; line splitting or comma-delimited defaults will corrupt the structure (**verified**).

- Whitespace is inconsistent: several fields include leading spaces, trailing spaces or non-breaking spaces. Trim Unicode whitespace and collapse embedded whitespace in descriptions while preserving the source meaning.
- Portuguese currency uses periods for thousands and commas for decimals. Parse into decimal BRL values, not binary floating-point numbers.
- Dates mix numeric formats with Portuguese month abbreviations. Seven DOU values are malformed (`22/12/20004`, `XX-Dez-05`, `291-DEZ-05` or `230-DEZ-05`) and one end date is impossible (`31/11/2014`). Preserve the source text and leave the ISO field blank for those values.
- `Tema=ANULADO` is status contamination, not a legitimate environmental theme. Preserve the source field and derive status separately.
- Repeated titles and repeated generic internal identifiers are not duplicate rows. The cleaned `record_id` hashes year, internal identifier, executor, title and FNMA amount, while the source identifiers remain separate.
- Portuguese project titles and origin-call names are preserved in `*_pt`. All 46 distinct non-empty call descriptions have reviewed exact English translations, covering 531 rows; 964 rows have no source call and are labelled not applicable. The audited project-title subset covers all 27 titles that occur more than once, representing 74 rows. The remaining 1,421 distinct singleton titles remain blank in English with `translation_status=pending_free_text_translation`. Proper project and legal names are preserved rather than mechanically translated. Controlled themes, regions, spheres, selection types and common biome labels are translated.
- The restartable build contains the exact reviewed dictionaries and asserts their full frozen-release coverage. A source refresh that changes a translated call or repeated-title set fails validation rather than silently copying Portuguese into an English field.
- The source-amount inconsistency at line 1435 is a named exception. Validation requires exactly one mismatch and blocks export if that count or location changes.

## Current approved release

No release is approved. Working release: **2025-03** (`releases/2025-03/`). The cleaned table contains 1,495 records, and the draft mapping contains one auditable mapping decision for every record. Of those decisions, 106 are high-confidence, 756 are medium-confidence pending human review and 633 are explicitly unmapped.
