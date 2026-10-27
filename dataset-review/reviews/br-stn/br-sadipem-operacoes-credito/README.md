# Secretaria do Tesouro Nacional — SADIPEM credit-operation requests (Consulta Pública Geral)

This review covers the public list of credit-operation requests that Brazilian states, the Federal District, municipalities and some state companies file with the National Treasury (STN) through SADIPEM, the Treasury's credit and debt analysis system. Each row is one PVL (pedido de verificação de limites e condições, the request for the Treasury or the lending bank to check legal borrowing limits and conditions) and shows the stage the request has reached. The release under review is the daily batch of 20 September 2026. **Status: provenance, access, licence, profiling, a complete 28,402-row cleaned release, controlled-vocabulary translation and a draft purpose-level adaptation mapping are complete. Translation of uncatalogued purpose text and human mapping adjudication remain pending. Not production-approved.**

## Canonical downloads

The canonical source is the Tesouro Transparente dataset "Análises de operações de crédito de estados e municípios", maintained by COPEM (the Treasury unit that analyses subnational credit operations). It publishes one CSV, "Consulta Pública Geral", which is replaced in place: the resource keeps its identifier but the file name carries the batch date and changes with each batch. The publisher labels the update frequency daily and the field-list document states "atualização diária, com defasagem de dois dias". The batch reviewed here is `sadipemconsultapublicageralbatch20092026.csv`; its latest status date is 18 September 2026, consistent with a two-day lag behind 20 September **(verified)**.

The local copy was downloaded on 23 September 2026. It is 6,381,183 bytes with SHA-256 `2a3659a6e02330544439e4dc4fa5750f1ed6376f93bde6155c6bd6188654c050`, and matches the byte size and file name that the catalog metadata still reported on 24 September 2026 (resource last modified 21 September 2026). The publisher gives no checksum, so identity with the live file is **inferred** from name and size. Although labelled daily, the resource had not been replaced between 21 and 24 September **(verified observation)**; refreshes should read the current URL from the catalog API rather than assume a new file every day.

Earlier batches are not retained on the portal; each batch overwrites the last, so a release can only be reproduced from the stored copy **(verified: the dataset has a single CSV resource)**. Records also change retroactively: the API field-list document states that data may be revised to reflect the state of analysis, back to the start of the series **(verified)**.

The file is a plain semicolon-separated CSV in Latin-1 encoding with 14 columns and 28,402 data rows, every row with 14 fields; status dates run from 19 March 2002 to 18 September 2026 **(verified)**. The detailed profile and downstream handling implications are recorded below.

The same records are also served by an official JSON API (Tesouro Data Lake, SADIPEM module) with no login or key **(verified: a request for one state returned records)**. The API carries fields the CSV lacks, most importantly a flag showing whether the lender has reported that the operation was contracted, a flag showing whether a debt record in the Treasury's debt register is linked to the PVL, the internal request id and the protocol date **(verified in the API field-list document and in a live response)**. This matters for the stage question: the CSV alone can show a Treasury clearance but never a signature, while the API can indicate a lender-reported contract. Whether the API covers the same set of records as the CSV is **unanswered**: a one-state query returned fewer records than the CSV holds for that state, and the summarising fetch tool used here is not reliable enough for counts. A full API pull is needed to settle it.

References:

- Dataset page: https://www.tesourotransparente.gov.br/ckan/dataset/operacoes-copem
- Catalog metadata API: https://www.tesourotransparente.gov.br/ckan/api/3/action/package_show?id=operacoes-copem
- CSV resource metadata: https://www.tesourotransparente.gov.br/ckan/api/3/action/resource_show?id=c9cbf4d5-8c68-4fa6-9224-afc34c006d11
- Reviewed batch (URL changes with each batch): https://www.tesourotransparente.gov.br/ckan/dataset/25a770df-920e-4519-a172-65b84b14e643/resource/c9cbf4d5-8c68-4fa6-9224-afc34c006d11/download/sadipemconsultapublicageralbatch20092026.csv
- CSV field list (PDF): https://www.tesourotransparente.gov.br/ckan/dataset/25a770df-920e-4519-a172-65b84b14e643/resource/7ed51c18-5610-4e1f-b7de-888dd17c6b66/download/metadados-pvl-consulta-publica.pdf
- API field list (PDF): https://www.tesourotransparente.gov.br/ckan/dataset/25a770df-920e-4519-a172-65b84b14e643/resource/b6c61ce2-a369-439f-8ff1-ef25975693cc/download/metadados-pvl-api.pdf
- API documentation: https://apidatalake.tesouro.gov.br/docs/sadipem/
- API endpoint (paged, 5,000 rows per page): https://apidatalake.tesouro.gov.br/ords/sadipem/tt/pvl
- Public PVL query in SADIPEM (the system of record): https://sadipem.tesouro.gov.br
- Local raw copy → `releases/2026-09-20/sample/sadipemconsultapublicageralbatch20092026.csv` (gitignored; re-download from the batch URL above, or from the current URL in the resource metadata)

## Why we use it

SADIPEM is the one national, record-level source for subnational borrowing requests, so it evidences the domestic credit pathway (CAIXA, including FGTS Saneamento para Todos; state development banks; BNDES), the loan arm of PAC sanitation programmes and the Union-guaranteed external loans that follow COFIEX approvals. It is reviewed for the Brazil finance-pathways need, where it supplies comparable past financing decisions rather than a ranking input.

## License

The dataset page assigns the Open Data Commons Open Database License (ODbL) **(verified: licence field on the dataset page and `odc-odbl` in the catalog metadata)**. The portal's terms of use add that the data may be used for any purpose, explicitly including profit-making activities, reproduction, adaptation and distribution, that users must also check each dataset's licence field for additional conditions, and that the Treasury disclaims any warranty on the data **(verified)**. The metadata links the licence to its Open Definition page without a version number; ODbL 1.0 is the only published version, so the operative version is **inferred** to be 1.0.

Required attribution: `Secretaria do Tesouro Nacional - disponível em: www.tesourotransparente.gov.br`. The STN logo may not be used in the citation or on any other site **(verified)**.

ODbL is not attribution-only. Any public display built from these records (a "produced work") must carry a notice that the content came from this database. If a derivative database, or a produced work made from one, is used publicly, a machine-readable copy of the whole derivative database or of a file of all alterations must be offered, and a publicly used derivative database must itself be under ODbL or a compatible licence (ODbL sections 4.3, 4.4 and 4.6) **(verified from the licence text)**. Commercial reuse in the City Climate Compass is therefore permitted, but the platform needs a plan for the share-alike and access duties; keeping SADIPEM-derived records separable by source is what makes the alterations file practical. How those duties apply to the specific platform design is a legal question and remains **unanswered** here.

References:

- Tesouro Transparente terms of use: https://www.tesourotransparente.gov.br/sobre/dados-abertos/termos-de-uso
- ODbL 1.0 text: https://opendatacommons.org/licenses/odbl/1-0/

## Data profile

The batch is one rectangular table with 28,402 records and 14 columns. Every row has exactly 14 fields, the native PVL/process identifier is complete and unique, and there are no exact duplicate rows **(verified from the local file)**.

| Column | Observed content | Missing or exceptional values |
|---|---|---|
| `Interessado` | Applicant or interested party name | Complete; 4,101 distinct labels |
| `UF` | Two-letter state abbreviation | Complete; all 27 federative units |
| `Tipo de interessado` | `Município`, `Estado` or `Empresa Estatal` | Complete |
| `Tipo de operação` | Six operation types, principally domestic contractual operations | Complete |
| `Finalidade` | One of 86 programme or broad-purpose labels | Complete; 11,659 rows (41.05%) are the generic `Infraestrutura` |
| `Tipo de credor` | One of seven lender types | Complete |
| `Credor` | Lender name | Complete; 142 distinct labels |
| `Moeda` | `Real`, US dollar, euro, yen or SDR | Complete |
| `Valor` | Nominal operation amount in the stated currency | Complete; six genuine `0,00` values |
| `Número do Processo/PVL` | Native request identifier | Complete and unique; 21,011 legacy process numbers and 7,391 `PVL` numbers |
| `Código IBGE` | Seven-digit municipality code or two-digit state code | Missing for all 15 state-company records; otherwise complete |
| `Status` | Current workflow/legal-review status | Complete; 28 distinct labels |
| `Data` | Date attached to the current status | Complete; day/month/year format |
| `Analisado por` | `STN` or `Instituição Financeira` | Complete |

The operation amount is not a common-currency measure. Values range from zero to BRL 223,539,966,235.09 within the real-denominated rows, while the other currencies retain their original nominal units; no exchange rate or converted-real field is supplied **(verified)**. The six zero values are source values rather than missing cells **(verified)**. Whether each amount reflects the latest amended request value throughout the historical series is **unanswered** and requires the methodology review.

The status is a snapshot of the legal/administrative stage, not a transaction history. The most common labels are `Deferido` (12,760), `Deferido (PVL-IF)` (7,021), `Arquivado` (1,937), `Devolvido` (1,805), `Encaminhado à PGFN com manifestação técnica favorável` (1,576) and `Arquivado por decurso de prazo` (1,285) **(verified)**. All 7,294 rows analysed by a financial institution use a PVL-IF-specific status; the remaining 21,108 were analysed by STN **(verified)**. No status states that the loan was contracted, paid or disbursed **(verified)**, so `Deferido` must not be converted into a financed-project flag **(inferred consequence)**.

## Spatial and temporal scope

The snapshot covers all 27 federative units and contains 27,036 municipal records, 1,351 state records and 15 state-company records. The municipal records represent 4,222 distinct IBGE municipality codes, so the file is national in reach but does not contain every Brazilian municipality **(verified)**. It records participation in the credit-request system, not a census of municipal financing needs **(inferred)**.

Status dates run from 19 March 2002 through 18 September 2026, with valid dates in every row **(verified)**. The file contains only the current row-level status and date, not prior status events, application dates, contract dates or disbursement dates **(verified from the available columns)**. Repeated daily batches would be needed to reconstruct changes over time, and even then changes before the first archived batch would remain unavailable **(inferred)**.

## Interpretation warnings

The data supports evidence that a government entity pursued a credit route for a stated broad purpose, with a named lender, currency, operation amount and observed legal-review outcome. It does not by itself prove that financing was signed, committed or disbursed **(verified from the available fields; inferred analytical consequence)**.

Action-level use is limited by the purpose taxonomy. The file has no project title, project object, expenditure description or free-text summary, and 41.05% of rows use the generic purpose `Infraestrutura` **(verified)**. Dedicated labels such as `Saneamento básico`, `Saneamento para Todos` and `Preservação e recuperação ambiental` can support coarse financing precedent, but assigning records to specific adaptation actions from `Finalidade` alone would be **inferred** and often underdetermined. A richer project description or a linked source is required for defensible action-level matching **(unanswered for this release)**.

Counts by status are not approval or finance-success rates. The labels represent different review routes and stages, archived and returned cases remain in the snapshot, and the file lacks a contract outcome **(verified)**. Comparing action financeability would additionally require a defensible action mapping, comparable applicant populations and a contracted or disbursed outcome **(inferred)**.

The 91 `Concessão de garantia` rows are guarantee requests rather than new loan proceeds **(verified from `Tipo de operação`)**. They must be separated from borrowing operations before amounts are aggregated; otherwise related legal requests may be counted as additional finance **(inferred)**. The file provides no explicit link between a guarantee PVL and the underlying borrowing PVL **(verified from the available columns)**.

## Parsing notes

The file is ISO-8859-1/Latin-1, semicolon-delimited, has no byte-order mark, uses LF line endings and contains one header plus 28,402 data lines. It has no quoted fields, embedded newlines, tabs, NUL bytes, leading or trailing field whitespace, or ragged rows **(verified)**.

`Valor` uses Brazilian formatting in every row: periods group thousands and a comma introduces exactly two decimal places. Parse it as a decimal only after removing grouping periods and replacing the decimal comma, and retain `Moeda`; summing across currencies is invalid **(verified format; inferred handling rule)**. Zero is not a null sentinel because six records explicitly contain `0,00` **(verified)**.

`Data` must be parsed as `%d/%m/%Y`. It is the date associated with `Status`, not evidence of contract signature or cash movement **(verified from the field combination; inferred analytical consequence)**.

`Código IBGE` is a mixed-level string: seven digits for municipalities, two digits for states and blank for state companies. A municipal join must first filter `Tipo de interessado = Município`; treating every non-null code as a municipality identifier would misjoin state records **(verified)**. `Número do Processo/PVL` should also remain text because it contains punctuation and two identifier formats **(verified)**.

No exact duplicates were found, but uniqueness is at the PVL/process level rather than necessarily at the underlying investment level **(verified / inferred)**. Do not deduplicate on applicant, lender, currency and amount: repeated round amounts are common, and separate guarantee and borrowing requests can describe related finance **(verified observation; inferred handling rule)**.

The cleaned release pairs every finite controlled label with its Portuguese source value: 3 applicant types, 6 operation types, 7 creditor types, 5 currencies, 28 statuses and 2 analysing-body values. All 28,402 rows carry `controlled_translation_status=complete_exact_release_dictionary`, and the restartable build fails if a new categorical value appears without an explicit translation. Applicant, creditor and place names remain source proper names rather than being translated.

Purpose remains a separate boundary. Seven reviewed broad purposes produce English purpose-derived descriptions for 12,770 rows; 15,632 rows across the remaining purpose labels stay blank in English with `translation_status=pending_free_text_translation`. This is intentional and does not reduce the completeness of the controlled categorical fields.
