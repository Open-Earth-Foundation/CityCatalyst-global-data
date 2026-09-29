# BNDES — Operações de financiamento: operações não automáticas

This review covers the Banco Nacional de Desenvolvimento Econômico e Social (BNDES) open-data table of direct and non-automatic indirect financing operations contracted since 2002. It is the relevant resource for examining named projects, clients, financing instruments, contracted amounts and disbursements; the much larger automatic indirect-operations resource is a separate dataset. The working release is the resource snapshot dated 1 September 2026. **Status: provenance, access, licence, profiling, methodology, bilingual extraction, draft adaptation mapping and the release review are complete. Medium-confidence mapping adjudication and reviewer sign-off remain pending. Nothing is production-approved.**

## Review gates

Both gates pass. The dataset is applicable because it is a national BNDES portfolio with municipality name and IBGE municipality-code fields, project descriptions, client type, repayable/non-repayable modality, financing instrument, contracted amount, disbursed amount and contract status **(verified from the official resource metadata and data dictionary)**. Those fields can evidence Brazilian domestic climate and infrastructure credit and non-repayable BNDES support, although adaptation relevance still has to be established record by record **(inferred)**.

The dataset is profilable now because BNDES publishes a live national CSV of contracted operations and a matching data dictionary, and the complete current CSV was successfully retrieved on 24 September 2026 **(verified)**. It is an operating portfolio, not an eligible-in-principle programme with no records.

## Canonical downloads

The canonical source is the BNDES open-data dataset "Operações de Financiamento". The package contains separate resources for automatic indirect operations and non-automatic operations; this review uses only "Operações não automáticas" because it is the resource named by the catalogue item and includes direct and non-automatic indirect contracts **(verified)**. The accompanying non-automatic-operations dictionary is the canonical field definition **(verified)**.

The source is a living dataset without a publisher version number. BNDES reports monthly automatic updates for the package; the non-automatic CSV was last updated on 1 September 2026, while the package metadata was last updated on 23 September 2026 **(verified on 24 September 2026)**. The working release therefore uses `2026-09-01`, the publisher's resource date, rather than the later package-metadata date. A later resource update will supersede this snapshot **(inferred from the fixed resource identifier and automatic monthly cadence)**. Whether BNDES retains downloadable historical snapshots is **unanswered**; the current package exposes one live non-automatic CSV resource.

Direct retrieval from the fixed resource URL succeeded on 24 September 2026. The downloaded file is 20,011,334 bytes, exactly the size reported by BNDES, and its MD5 `b0b8902e33d3057403a6507ab0f4e7ab` exactly matches the publisher's resource hash **(verified)**. The local SHA-256 is `960fcf16d404cee16c41229cd563d8e951b26f673b20966384e7a5d788068a06`. This resolves the catalogue note that the earlier local download was truncated. The file is held in the release's gitignored `sample/` directory and was profiled in full for this review.

The two-page data dictionary was also retrieved on 24 September 2026. Its 83,457-byte file matches the publisher's MD5 `9b7843bb2193a4f06b1210e3246adce5`; the local SHA-256 is `af26c65a988585f982b6fd17d5ff251a0d0530cb0613938205d8652e193c2dea` **(verified)**. The PDF metadata says it was created on 2 June 2020, while the portal resource metadata dates it to 14 February 2025. The live CSV and dictionary differ in one field, discussed in the parsing notes.

References:

- Dataset record: https://dadosabertos.bndes.gov.br/dataset/operacoes-financiamento
- Non-automatic-operations resource metadata: https://dadosabertos.bndes.gov.br/dataset/operacoes-financiamento/resource/6f56b78c-510f-44b6-8274-78a5b7e931f4
- Non-automatic-operations CSV: https://dadosabertos.bndes.gov.br/dataset/10e21ad1-568e-45e5-a8af-43f2c05ef1a2/resource/6f56b78c-510f-44b6-8274-78a5b7e931f4/download/operacoes-financiamento-operacoes-nao-automaticas.csv
- Non-automatic-operations data dictionary: https://dadosabertos.bndes.gov.br/dataset/10e21ad1-568e-45e5-a8af-43f2c05ef1a2/resource/9dcdee83-de84-4547-946b-bff5335428db/download/dicionario-de-dados-operacoes-contratadas-na-forma-indireta-direta-nao-automatica.pdf
- Local raw copy: `releases/2026-09-01/sample/operacoes-financiamento-operacoes-nao-automaticas.csv`
- Local data dictionary: `releases/2026-09-01/sample/dicionario-de-dados-operacoes-nao-automaticas.pdf`

## Why we use it

The dataset supplies past contract and disbursement evidence for financing pathways rather than an estimate of how easy an action is to finance. Its project description and financing-instrument fields make it a stronger action-matching source than programme-level totals, while the separate contracted and disbursed fields can preserve funding stage **(inferred from the verified dictionary)**. Approval rates and comparative financeability remain unsupported because this is a contracted-operations portfolio, not the full universe of applications **(inferred)**.

## License

The BNDES dataset and non-automatic resource assign the Open Data Commons Open Database License (ODbL); the portal's licence record links to the ODbL 1.0 legal text **(verified)**. ODbL 1.0 permits worldwide, royalty-free commercial use, extraction, modification, creation of derivative databases and redistribution, subject to its conditions **(verified from sections 3 and 4)**.

Redistribution is permitted, but ODbL is not an attribution-only licence. Publicly conveying the database or a derivative database requires the ODbL licence or URI to accompany it and existing copyright, database-right and licence notices to remain intact. Publicly used outputs must identify the source database and state that it is available under ODbL. Publicly used derivative databases must use ODbL or a compatible licence, and the whole derivative database or a machine-readable alterations file must be offered under the conditions in sections 4.4 and 4.6 **(verified)**.

BNDES provides no additional prescribed citation wording on the dataset record, resource page or dictionary **(verified absent)**. A working notice that follows the ODbL example is: "Contains information from BNDES, Operações de Financiamento, available under the Open Database License (ODbL)." The notice should link the dataset name to the canonical record and the licence name to the ODbL 1.0 text **(inferred implementation)**.

ODbL governs database and contract rights but does not automatically license independent rights that may subsist in individual contents, and it does not cover BNDES trademarks **(verified from sections 2.3 and 2.4)**. Whether any free-text project description carries separate third-party rights is **unanswered**; this does not block factual record extraction, but verbatim republication of descriptions should be reviewed before a public release.

References:

- ODbL 1.0 legal text: https://opendatacommons.org/licenses/odbl/1-0/
- BNDES licence record: https://opendefinition.org/licenses/odc-odbl/

## Data profile

The file is a 34-column table with 23,815 subcredit rows. The dictionary defines a subcredit as one component of a BNDES contract with its own financial conditions; one contract can contain multiple subcredits and the contracted subcredit values sum to the contract total **(verified)**. There are 8,388 distinct contract numbers; 4,188 occur more than once and one has 99 subcredits.

| Measure | Observed value | Consequence |
|---|---:|---|
| Subcredit rows | 23,815 | This is the source grain and must remain the auditable financial-detail layer. |
| Distinct contract numbers | 8,388 | This is the publisher-defined rollup for summing contracted subcredits, not automatically a unique project or recipient. |
| Contract numbers spanning multiple values | 172 span client CNPJs; 367 span dates; 122 span project descriptions; 249 span places | A contract-level record needs child parties, dates, descriptions and locations rather than a single arbitrarily selected value. |
| Byte-equivalent subcredit rows | 654 rows in 277 identical groups; 377 are extra copies | The export has no subcredit identifier, so distinct subcredits with identical published attributes cannot be separated from accidental duplicates. They must not be dropped silently. |
| Brazilian municipality codes | 1,140 valid seven-digit codes | The dataset provides useful but non-census municipal coverage. |
| Rows without a usable municipality | 7,766 | 2,599 `IE` rows plus 5,167 rows in Brazilian UFs coded `0` or `9999999` (`SEM MUNICÍPIO` or `DIVERSOS`). Valid codes cover 16,049 rows (67.4%). |
| Contract dates | 2 January 2002 to 31 July 2026 | All 23,815 values parse as ISO dates and none postdate the working release. |
| Support modality | 22,207 repayable; 1,608 non-repayable | The file covers both credit and grants; they must remain separate in route analysis. |
| Client nature | 21,818 private; 1,997 public | Most records are not municipal borrowers, although public direct and indirect entities are represented. |
| Contract status | 14,139 settled; 9,408 active; 268 `-` | The hyphen is an unknown source value, not a fourth interpreted status. |

Every amount and interest field parses as a non-negative decimal after replacing the decimal comma. Contracted subcredit values range from R$0.55 to R$9,889,997,969.99, and 1,340 rows have zero disbursed. Disbursed amount exceeds contracted amount in 6,090 rows and in 2,021 contract groups after summation **(verified)**. The dictionary explains that contracted value is converted at the contract date and disbursed value at the disbursement date; when a contractual indexer rises between those dates, the converted disbursement can exceed the original contracted-real amount **(verified)**. This is not evidence of overpayment.

Fundo Clima is materially better covered than the existing annual-report extract. An exact match on `PROGRAMA FUNDO CLIMA` or a funding-source label containing `FUNDO CLIMA` identifies 167 contract numbers and 434 rows once every row belonging to those contracts is retained. Of those contract numbers, 158 are private and nine involve public clients; dates run from 2013 to July 2026. The match is a reproducible source filter, but it is not yet a validated adaptation-project filter: the programme includes mitigation, industrial, energy and mobility investments as well as resilience projects **(verified fields; inferred use restriction)**.

## Methodology

The source has three levels that must remain distinct. A row is a subcredit with its own conditions; `numero_do_contrato` rolls one or more subcredits into the publisher's contract total; and the project description describes the supported investment but does not define a stable project identifier. Some contracts cover a complex with multiple legal entities, and some carry more than one description, date or place. The comparable-project database therefore needs a contract parent with one-to-many subcredits and one-to-many parties/locations, rather than flattening one value from each column into a project row **(verified source model; inferred implementation)**.

Contracted and disbursed values answer different questions. `valor_contratado_reais` is the contract-date real conversion and may be indexed under the contract; `valor_desembolsado_reais` is the amount released, converted at the disbursement date and indexer. Contracted subcredits can be added within the same contract to obtain the publisher-defined contract total, but a disbursement ratio should be described as nominal/indexed source values rather than physical completion **(verified definitions; inferred analytical consequence)**.

The Fundo Clima comparison demonstrates why instrument components and contract totals both matter. The annual reports' rounded approvals match the `PROGRAMA FUNDO CLIMA` subcredits for contracted examples such as Ceará (R$250 million), Espírito Santo (R$150 million), Acre (R$80 million) and Fortaleza (R$100 million), while their complete BNDES contract totals are R$622.606 million, R$150 million, R$120 million and R$250 million respectively because some contracts combine Fundo Clima with `BNDES Invest Impacto` or another instrument **(verified)**. The platform should expose the fund component as the route evidence and the full contract total as co-financed project context, never substitute one for the other.

The dataset describes support modality, access form and financial product separately. `modalidade_de_apoio` distinguishes repayable from non-repayable support. `forma_de_apoio` distinguishes a direct request to BNDES from an indirect request through an accredited institution. Products define general financing rules; instruments are the lines, programmes or funds with more specific objectives and conditions **(verified)**. These fields should remain separate pathway facets.

The published interest number is not always the borrower's full financing cost. For ordinary records, the dictionary says total cost is the financial-cost index plus `juros`; when financial cost is `TAXA FIXA`, `juros` itself represents total cost. Direct and indirect support also compose the rate differently **(verified)**. Any future affordability comparison must implement those cases rather than rank the numeric `juros` field alone.

## Spatial and temporal scope

BNDES describes the package as detailed financing operations contracted from 2002 onward, and the file covers contract dates from 2 January 2002 through 31 July 2026 **(verified)**. It contains every Brazilian UF plus `IE`, a non-UF code used on 2,599 rows. The `IE` rows are labelled `SEM MUNICÍPIO` or `DIVERSOS` and use municipality codes `0` or `9999999`; they must be excluded from Brazilian municipality joins **(verified)**.

Within Brazilian UFs, 5,167 rows also lack a municipality: 3,066 use code `0` and 1,958 use code `9999999`, both labelled `SEM MUNICÍPIO`, and 143 use `9999999` labelled `DIVERSOS` **(verified in the extraction notebook, which corrected an earlier count of 5,619 that missed the `9999999` rows)**. The remaining data contain 1,140 distinct valid seven-digit municipality codes, far fewer than Brazil's municipality count. The table therefore provides the location attached to an operation when BNDES publishes one, not complete city coverage and not proof that the named municipality is the sole project-benefit area **(verified structure; inferred scope consequence)**.

## Interpretation warnings

The dataset establishes that BNDES records an operation as contracted and supplies contracted and disbursed amounts, but a source row is one subcredit rather than one contract or project. The contract number is the documented financial rollup, yet some contract numbers span clients, dates, descriptions and locations. Counts of past projects must therefore state whether they count contract groups, legal recipients or separately described investments.

The two money fields are real-denominated conversions made at different dates and may use contractual indexers. A disbursed value above the original contracted-real value is allowed by the documented method and is not an anomaly by itself. The data still do not measure implementation progress: money released, an active financial obligation and a completed physical asset are different states.

`situacao_do_contrato` distinguishes active, settled and unknown records; it does not report whether the financed asset was completed, operating or successful. A settled contract can be a repaid or otherwise closed financial relationship, not a completed adaptation outcome **(verified field; inferred consequence)**.

The project description is useful for action matching but contains source wording, abbreviations and broad programme descriptions. Keyword hits are candidate records, not verified adaptation classifications. For example, `clima` appears across thousands of rows because Fundo Clima and climate-related phrases occur in multiple fields, while one contract can span both Fundo Clima and another instrument.

An annual-report approval is not a contract. Of the 23 Fundo Clima approvals from the 2024 and 2025 BNDES reports already in the compile, 7 appear in this resource as contracts by 31 July 2026 when matched on client, client type and the Fundo Clima component; the other 16 have no matching record in this resource and period **(verified in the extraction notebook, §6.5)**. The three matched 2024 approvals were contracted between September 2025 and June 2026. Unmatched approvals may be contracted later, under a different client such as an operator, or through the automatic-operations resource, so the absence is not evidence that the operation failed.

Municipal direct borrowing in this resource is mostly historical. Municipal governments hold 528 contracts, but only 31 are dated 2020 or later, led by public-administration modernisation and Fundo Clima; the PMAT line that dominates 2002–2016 has no contracts after 2019 **(verified in the extraction notebook, §6.6)**. Past use of a route does not establish that it is open to cities now.

English values are machine translations made with Claude on 24 September 2026 and have not been reviewed by a Portuguese speaker. They are for reading and matching; the `_pt` value is authoritative. Where BNDES truncated a description mid-sentence, the English stops at the same point and ends with "…" rather than guessing the rest. Programme and fund names such as Fundo Clima, PMAT and FINEM are kept in their Portuguese form.

Private companies account for 21,818 rows and 158 of the 167 Fundo Clima contract matches. These records can demonstrate domestic climate-finance precedents, but they do not by themselves demonstrate that a municipality can borrow through the same route. Route guidance must retain borrower nature, instrument and access role separately.

## Parsing notes

The source is a CP1252, semicolon-delimited CSV with a quoted header and 34 fields. It has 23,816 physical lines, no embedded line breaks, no ragged rows and no blank cells **(verified)**. Blank-looking values are encoded with sentinels instead: `----------` appears in intermediary and exception fields, while `-` appears in funding source and contract status. These must become explicit nulls only through field-specific rules.

The 2020-created dictionary lists 35 fields and ends with a derived `Ano` column, while the September 2026 CSV has 34 fields and omits `Ano` **(verified)**. The extraction must derive year from `data_da_contratacao` and test the live header rather than treat the dictionary's field count as current. The dictionary also labels CNPJ, municipality code and contract number as integers, but the CSV supplies formatted CNPJs and sentinel municipality codes; all identifiers must remain strings.

Whitespace is data noise throughout the export. Project descriptions have leading or trailing spaces in 22,375 rows, the source sector field is padded in every row, the detailed CNAE name is padded in 23,548 rows, and client nature is padded in 21,818 rows. Trimming outer whitespace is safe for comparison; collapsing internal spaces in project descriptions should produce a cleaned field while preserving the raw text for audit.

Contracted value, disbursed value and interest use a comma as the decimal separator without thousands separators. Decimal precision varies, including one contracted value with eight decimal places, so these fields must be parsed as exact decimals rather than binary floats. Contract dates use ISO `YYYY-MM-DD` consistently.

`municipio_codigo` is text, not an integer. Valid Brazilian municipality values are seven digits, while `0` and `9999999` are non-municipal sentinels. The `uf` value `IE` is also not a Brazilian federative unit. Geographic joins must validate both fields before using a municipality code.

The source is in Portuguese; the cleaned table uses English column names. Each descriptive or categorical field carries its English value under the English name and the Portuguese source value under the same name with a `_pt` suffix (for example `financing_instrument` and `financing_instrument_pt`). Client, place and financial-institution names are proper nouns and are not translated; `inovacao` becomes the boolean `is_innovation`. English values come from a committed lookup keyed by source field and distinct Portuguese value, so a new snapshot with an untranslated value stops the notebook until the lookup is extended.

The raw table contains 277 groups of byte-identical rows, 654 rows in total, of which 377 are extra copies beyond the first in each group. The dictionary says every published row is a different subcredit, but the export exposes no subcredit identifier. Identical legitimate subcredits and accidental duplication are therefore observationally indistinguishable **(verified structure; unanswered cause)**. Retain a raw-row identifier, flag identical rows, include them in source-faithful contract totals, and publish a sensitivity total with identical extras removed so reviewers can see the maximum duplication effect.

## Current approved release

No release is approved. Working release: **2026-09-01** (`releases/2026-09-01/`). The extraction notebook implements each parsing note as one cleaning block, asserts the profile figures above, and exports one typed subcredit table that keeps every source row, adds geography-validity and identical-row flags, and holds amounts as exact decimal text.

A second notebook maps the release to the ICB × OEF adaptation action bank (V13). The crosswalk has one row per distinct project description and linked action, with a match type (`direct`, `component`, `enabling`, `related` or `none`), a confidence and a one-line rationale; contract amounts are never split across actions. Links were drafted with Claude on 24 September 2026. The 352 medium-confidence links are pending adjudication, grouped into judgment clusters in the notebook, and should not be shown to cities until they are decided. The action bank export is a local-only input; re-export it from the V13 workbook to re-run the notebook.

References:

- Extraction notebook: `releases/2026-09-01/extract_clean.ipynb`
- Cleaned subcredit table: `releases/2026-09-01/data/br_bndes_operacoes_financiamento_subcredits.csv.gz`
- English translation lookup: `releases/2026-09-01/data/br_bndes_operacoes_financiamento_translations_en.csv`
- Adaptation mapping notebook: `releases/2026-09-01/map_adaptation_actions.ipynb`
- Crosswalk to the adaptation action bank: `releases/2026-09-01/data/br_bndes_operacoes_financiamento_to_adaptation_actions.csv`
- Action bank input (local only, gitignored): `releases/2026-09-01/sample/adaptation_action_bank_icb_oef_v13.csv`, exported from the ICB × OEF V13 workbook, sheet "Final Action Bank"
- Annual-report approvals used in the reconciliation: `releases/2026-09-01/sample/bndes_fundoclima_relatorios.tsv` (local; transcribed from the BNDES Fundo Clima annual reports)
