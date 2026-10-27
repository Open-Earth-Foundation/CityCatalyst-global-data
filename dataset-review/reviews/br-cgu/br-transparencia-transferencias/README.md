# Controladoria-Geral da União — Portal da Transparência, Recursos transferidos

This review covers the monthly "Recursos transferidos" downloads of the Portal da Transparência do Governo Federal, published by the Controladoria-Geral da União (CGU) from SIAFI, the federal financial-administration system. The use here is narrow: federal civil-defence transfers from the Ministério da Integração e do Desenvolvimento Regional (MIDR, órgão 53000) to states and municípios under budget ações 22BO (response and recovery) and 8348 (emergency mitigation works). The working release is July 2026, profiled together with January–June to observe the sparse 8348 activity. **Status: all review steps are drafted: provenance, licence, profile, methodology, bilingual extraction, a conservative route-level adaptation mapping and release review.md. The proposed fit verdict is conditional fit as payment-stage evidence for civil-defence finance, not fit as project records, and awaits reviewer sign-off. A research-only catalog entry has been made; nothing is production-approved.**

## Canonical downloads

The canonical source is the portal's bulk download section, one ZIP per month of transfer payments. Each monthly URL on the portal redirects to a ZIP on CGU's download server. The January–July 2026 files were retrieved successfully on 24 September 2026 and each contains one CSV; their MD5 hashes match the server ETags observed before download **(verified)**. The July ZIP is 3,094,982 bytes, MD5 `14cc4c826bb836ff16aec4f33c3c1ab6`, SHA-256 `5c5071a6f9a2b3fe42bade8010a6c104a61f93a15c8c29c6ef1d60fc3e59630a`, and expands to a 108,951,223-byte CSV. The data dictionary page lists the same 36 fields found in every file **(verified)**.

According to the portal's data-origin page, the transfers data come from SIAFI, are updated monthly, and were current to July 2026 on 24 September 2026, with August 2026 scheduled for 30 September 2026 (verified). The August URL already redirects, so a redirect alone does not prove a month is published (inferred; confirm by opening the file). Whether published months are later revised in place is unanswered; keep the download date and file hash for every month.

The portal also offers an API returning the same data as the web screens, which needs a free e-mail-registered token (verified). The portal itself recommends the bulk files for complete datasets (verified), so the API is not the extraction route here. Its only transfers endpoint is a COVID-era monthly view; the rest of what it offers for this use sits at the expense-document level (empenho, liquidação, payment), per payee or per document (verified from the API specification). The same document level exists as bulk files in the "Despesas – Execução" download, whose empenho records carry `Processo`, `Observação` and `Código Convênio` (verified from the data dictionary). Those fields are the likely route to the Sedec portaria link this dataset lacks; whether `Observação` actually quotes portaria numbers is unanswered until those files are profiled.

References:

- Download page: https://portaldatransparencia.gov.br/download-de-dados/transferencias
- Monthly file: https://portaldatransparencia.gov.br/download-de-dados/transferencias/YYYYMM → https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/transferencias/YYYYMM_Transferencias.zip
- Data dictionary: https://portaldatransparencia.gov.br/pagina-interna/603420-dicionario-de-dados-recursos-transferidos
- Data origin and update schedule: https://portaldatransparencia.gov.br/origem-dos-dados
- API: https://portaldatransparencia.gov.br/api-de-dados
- Local monthly files: `releases/2026-07/sample/202601_Transferencias.zip` through `202607_Transferencias.zip`

## Why we use it

Civil-defence and disaster finance (Route E) has no evidence records yet in the Brazil finance-pathway work. These files are the most complete public view of what the Union actually paid, month by month, to each recipient under the civil-defence ações. They record the payment stage only, so they complement rather than replace the transfer-authorisation portarias published in the Diário Oficial, which carry the per-transfer purpose and amount.

References:

- Originating need: `dataset-discovery/needs/2026-09-br-finance-pathways-review/`
- Sibling candidate (authorisations): `br-dou-sedec-portarias` in `dataset-discovery/needs/2026-09-br-finance-pathways-review/candidates.yaml`

## License

No named licence applies. The portal publishes a free-use statement, and the federal open-data decree makes federal executive data free to use; record this as a free-use statement, not a licence, and flag it for legal review (the need's "acceptable" licence tier).

The API page says the API "é de livre utilização, conforme previsto no DECRETO Nº 8.777, DE 11 DE MAIO DE 2016" (verified). That sentence names only the API. The bulk downloads are covered by two other sources rather than by that sentence. The portal's "O que é e como funciona" page says any citizen may "visualizar e utilizar os dados disponíveis da forma que melhor lhe convier" (verified). Decreto 8.777/2016, article 4, as amended by Decreto 9.903/2019, says "Os dados disponibilizados pelo Poder Executivo federal e as informações de transparência ativa são de livre utilização pelos Poderes Públicos e pela sociedade", and its §1º authorises free use of Union-owned databases (verified text). CGU is a federal executive body, so the downloads fall under article 4 (inferred, strong). The Termos de Uso name no licence and say nothing on reuse, attribution or commercial use (verified).

Commercial use is not restricted anywhere found; "livre utilização" by "a sociedade" places no purpose limit (inferred). No share-alike or no-derivatives condition exists (verified absence in the pages read). Attribution is not required in any text found for this portal. The decree's definition of open data limits conditions to crediting the author or source (art. 2º III, verified), so credit the source as good practice.

Suggested attribution: `Fonte: Controladoria-Geral da União, Portal da Transparência do Governo Federal (portaldatransparencia.gov.br), Recursos transferidos, AAAA/MM`.

The Diário Oficial da União (DOU) is the lower-constraint alternative for authorisation facts, but it is not a substitute for this payment table. Article 8(IV) of Lei 9.610/1998 excludes laws, regulations and other official acts from copyright protection, and the Imprensa Nacional describes DOU data as open data available for free use with source credit (verified). Sedec portarias can therefore provide the legal act, authorised amount and stated purpose without relying on CGU's unnamed free-use terms. They cannot show the monthly cash actually paid, so a complete route needs both sources. The DOU mobile app's separate no-commercial-use term was not used as evidence for the official acts or open-data feed (verified distinction).

References:

- API free-use statement: https://portaldatransparencia.gov.br/api-de-dados
- Portal use statement: https://portaldatransparencia.gov.br/sobre/o-que-e-e-como-funciona
- Termos de Uso: https://portaldatransparencia.gov.br/termos-de-uso
- Decreto 8.777/2016: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/decreto/d8777.htm
- Lei 9.610/1998, article 8(IV): https://www.planalto.gov.br/ccivil_03/leis/l9610.htm
- Imprensa Nacional open-data page: https://www.gov.br/imprensanacional/pt-br/acesso-a-informacao/dados-abertos

## Data profile

The seven monthly files contain 1,056,421 rectangular data rows with an identical 36-column header and no ragged records **(verified)**. Applying `CÓDIGO ÓRGÃO SIAFI = 53000` and `AÇÃO IN (22BO, 8348)` produces 743 civil-defence payment rows. These are payment evidence, not 743 projects: the same beneficiary and budget classification can recur in several months, and the files carry no project, agreement, portaria or transfer-authorisation identifier.

| Month | All rows | 22BO rows | 22BO paid | 8348 rows | 8348 paid |
|---|---:|---:|---:|---:|---:|
| 2026-01 | 122,527 | 42 | R$34,298,173.35 | 0 | R$0.00 |
| 2026-02 | 106,663 | 93 | R$68,971,029.13 | 1 | R$11,994,567.84 |
| 2026-03 | 119,844 | 67 | R$53,044,667.73 | 1 | R$277,793.49 |
| 2026-04 | 180,836 | 113 | R$106,240,748.58 | 1 | R$9,175,511.98 |
| 2026-05 | 241,393 | 192 | R$148,900,511.33 | 0 | R$0.00 |
| 2026-06 | 142,514 | 120 | R$76,941,943.40 | 0 | R$0.00 |
| 2026-07 | 142,644 | 113 | R$86,173,368.23 | 0 | R$0.00 |
| **Total** | **1,056,421** | **740** | **R$574,570,441.75** | **3** | **R$21,447,873.31** |

The 740 action-22BO rows cover 530 beneficiary codes, 528 beneficiary-name strings and 25 UFs. Municipal public administrations account for 725 rows, state or Federal District administrations for 11, and the generic type `Administração Pública` for four. Twelve rows have no municipality because the recipient is a state-level or other public body. Action 8348 appears only for Boa Vista/RR in February and April and Vera Mendes/PI in March; its three rows are all municipal payments for prevention or mitigation **(verified)**.

The observed row grain is one monthly transferred amount for a beneficiary and a full combination of budget classifications. No target row is an exact duplicate, and within each file the 35 non-value fields are unique. Across months, 57 action-22BO classification-and-beneficiary combinations recur, producing 65 additional monthly observations; Boa Vista's action-8348 combination recurs once. Monthly rows must therefore remain separate before any beneficiary or project-like rollup **(verified structure; inferred handling rule)**.

The budget fields add broad purpose but not a project object. For action 22BO, plan names refer to response, recovery, disaster-protection measures or emergency appropriations; they do not separate response from recovery into reliable row-level categories. Thirty-seven rows use `Múltiplo` instead of a single budget plan. Action 8348 cleanly identifies prevention/mitigation, but its three rows still do not state the specific work financed.

## Spatial and temporal scope

National coverage of federal transfers. The recipient is identified by UF, SIAFI municipality code and name, plus the favorecido code and name (verified from the dictionary). SIAFI municipality codes are not IBGE codes. Joining on accent-folded name + UF to the IBGE municipality list matches 523 of the 526 SIAFI municipalities in the target slice; the three misses are spelling variants (`PARATI`/Paraty, `ELDORADO DOS CARAJAS`/Eldorado do Carajás, `SANTA ISABEL DO PARA`/Santa Izabel do Pará), and each SIAFI code carries one name **(verified, notebook §6.5)**. An official SIAFI–IBGE crosswalk would remove the name step; whether one is published is unanswered. Time is the transfer month only, with no day (verified from the dictionary). Monthly files run to July 2026 at review time.

Budget scope for this use: ação 22BO finances emergency measures "durante ou após desastre" (relief, humanitarian assistance, restoring essential services and rebuilding damaged infrastructure), and ação 8348 finances mitigation works done before a disaster, such as slope and dam stabilisation, erosion control and support to the Operação Carro-Pipa (verified, MIDR 2024 portfolio). Both are transferências legais under Lei 12.340/2010 (verified). Prevention therefore separates from response and recovery at the level of the ação. The profile confirms that `plano orçamentário` does not reliably split response from recovery inside 22BO: most labels combine the two and 37 rows are aggregated as `Múltiplo` **(verified)**. MIDR also lists ação 14RL (coastal-erosion prevention) as prevention; it is outside the requested filter and appears twice in July 2026.

References:

- MIDR portfolio of ações 2024: https://www.gov.br/mdr/pt-br/acesso-a-informacao/portfolio-de-acoes-2024.pdf
- Ação 8348 page: https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil/solicitacao-de-recursos-1/acao-8348-apoio-a-obras-emergenciais-de-mitigacao-para-reducao-de-desastres
- Ação 22BO on the portal: https://portaldatransparencia.gov.br/programas-e-acoes/acao/22BO-acoes-de-protecao-e-defesa-civil

## Interpretation warnings

`VALOR TRANSFERIDO` is the amount recorded as transferred in that month and budget classification. It is not the authorising portaria amount, the total project budget or evidence that a work was completed. Summing months can describe observed cash transfers to a beneficiary under an action, but it cannot produce a defensible project count or project total without a separate instrument-level link.

The files cannot be joined deterministically to Sedec portarias. They provide beneficiary CNPJ, SIAFI municipality code, month, action and budget classifications, but no portaria number, process number, agreement identifier, payment document or exact payment date. A later match on recipient, amount and timing will be probabilistic and must retain match confidence; repeated payments such as Boa Vista's action-8348 rows may belong to one authorization or several **(verified fields; inferred consequence)**.

Action 22BO is suitable for a combined response-and-recovery route but not for distinguishing those stages. No 22BO budget-plan label names a single phase: 77% of the 22BO amount sits under combined response-and-recovery labels, 14% under labels that name only a Medida Provisória, and 10% under `Múltiplo` **(verified, notebook §6.4)**. `LINGUAGEM CIDADÃ` is `Sem informação` in all 743 target rows. Do not assign a more specific disaster phase from expenditure group, element or recipient name.

The data identify the payee, which is not always the geographic beneficiary or implementing municipality. Most rows name municipalities, but some name a state government, civil-defence directorate, fire brigade or municipal assistance fund. Geographic presentation must retain both payee identity and the SIAFI municipality field rather than replacing one with the other.

Action 8348 is sparse in the reviewed period. Its absence in four of seven months means no payment row was published under the filter for those months; it does not mean no mitigation project existed, no authorization was active or no spending occurred elsewhere in the federal budget.

## Parsing notes

Each ZIP contains one CP1252, semicolon-delimited, fully quoted CSV with CRLF line endings and 36 columns. All identifiers must remain text. SIAFI municipality codes can start with zero, beneficiary codes are 14-digit CNPJs with leading zeros, action and programme codes are alphanumeric, and sentinel codes include `-1`, `-14` and `MU`.

Amounts use a comma decimal separator and no thousands separator. Parse them as signed exact decimals: the seven complete files contain 706 negative and 67 zero values (July alone: 9 and 12), mostly constitutional transfers and all outside the target slice, so a generic loader must preserve reversals and zero-value records **(verified, notebook §3)**. The 743 target rows are all positive.

Missingness is encoded inconsistently. Empty strings occur for municipality fields on state-level recipients; `Sem informação` appears in descriptive fields; `-1` and `-14` appear in code fields; and `Múltiplo`/`MU` marks rows aggregated across more than one budget classification. Normalize these only with field-specific rules and preserve the raw values. The extract keeps every sentinel as published and adds one boolean, `is_multiple_classification`, true where any budget-classification code is `MU` or `-14` or any name is `Múltiplo`. It marks 38 rows: the 37 `Múltiplo` budget-plan rows plus Vera Mendes/PI (action 8348, March), which has a single plan but `MU` expense group, modality and element.

Several labels are publisher-truncated. Target `NOME SUBTÍTULO` values stop at 57 characters and end mid-word, while `NOME LOCALIZADOR` stops at 45 characters; examples include `NACIONAL (CREDITO EX` and `NO ESTAD`. Other source-quality issues include `REPOSTA` in place of `RESPOSTA` and placeholder legal references such as `MEDIDA PROVISORIA N. XXXXX, DE XX DE MAIO DE 2026`. These strings are evidence of the source export and must not be silently completed or corrected.

Source headers carry accents, spaces and a slash. The extract uses snake_case English names and pairs every translated description with the source Portuguese in a `_pt` field. The release-scoped dictionary translates every observed controlled or descriptive value exactly; its assertions fail if a new Portuguese value appears without a translation. Known source truncation, placeholder numbers and the `REPOSTA` typo remain visible in the Portuguese fields and are called out in bracketed notes in the English translations rather than silently repaired. Municipality and beneficiary legal names are proper names, not descriptions: they are preserved unchanged in both paired fields and marked `not_translated_source_proper_name_preserved`. The row-level `translation_status` is `complete_exact_release_dictionary` for all 743 rows. Codes, amounts, dates, UF and provenance fields carry no language suffix.

The extraction filter should use the codes, not names: `CÓDIGO ÓRGÃO SIAFI = 53000` and `AÇÃO IN (22BO, 8348)`. Names vary in accents, casing, truncation and typographical quality. The unit `530012`, `SECRETARIA NACIONAL PROTECAO E DEFESA CIVIL`, is constant across all target rows in the reviewed months and can be asserted as a structural check for this release.

## Methodology

These are SIAFI payment records, not estimates, so there is no model, baseline or uncertainty band to assess. What matters for this use is what stage and date each amount records, and which legal route produces a civil-defence payment.

Each value is cash paid in the month, in nominal BRL. The data dictionary defines `VALOR TRANSFERIDO` only as "Valor da Transferência" and the payee as the "favorecido do pagamento realizado", and the portal's transfers page says it shows amounts "efetivamente pagos (gastos ou transferidos)" separately from committed and liquidated amounts **(verified)**. The month is defined only as "Mês/Ano da transferência"; whether it is the payment-order date or the accounting month is **unanswered**. The 706 negative amounts in the full files behave like reversals of earlier payments, but no document says so **(inferred)**.

The legal route is Lei 12.340/2010. Its transfers are obligatory and reach the recipient either by deposit into a specific account held by the recipient or fund-to-fund, from the national disaster fund (Funcap) to a state or municipal civil-defence fund (art. 1-A, verified). They cover prevention in risk areas and response and recovery in affected areas (art. 4, verified). Response and recovery support goes to recipients whose emergency or calamity the federal executive has recognised, and response money may be released before that recognition is complete (arts. 3–4, verified). Recovery requires a work plan submitted within 90 days of the disaster (art. 4, verified), and the ministry can suspend payments on misuse (art. 5, verified). Three consequences follow for this use: a 22BO payment points to a recognised or pending disaster at the payee **(inferred)**; the state and municipal civil-defence funds among the payees are the fund-to-fund channel **(inferred)**; and repeated monthly payments to one payee are consistent with staged releases under one work plan, but nothing in the file confirms it **(inferred)**.

The publisher states no caveats specific to civil defence on the dictionary, data-origin or transfers pages **(verified absence)**. The one structural caveat it does state is that payment is shown apart from commitment (empenho) and liquidation, which sit in the separate expense-execution data **(verified)**; this file therefore cannot show money committed but not yet paid. Whether CGU revises published months in place is **unanswered**; re-downloading July after the August release and comparing hashes would answer it.

References:

- Transfers overview page: https://portaldatransparencia.gov.br/transferencias
- Lei 12.340/2010: https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2010/lei/l12340.htm

## Fit for purpose (proposed)

Scored against the finance-pathways need, the proposed verdict is **conditional fit as payment-stage evidence for civil-defence finance, not fit as project records**. It is the only reviewed source that shows civil-defence cash actually reaching named municipalities, month by month, with bulk access and a verified free-use statement. It fails the need's identifier and linkage must-haves: a row is a monthly payment, not a transfer decision, and nothing joins it deterministically to the Sedec portaria that authorised it. The verdict awaits reviewer sign-off.

| Criterion | Result | Evidence |
|---|---|---|
| Native record ID | Fail | No portaria, process, agreement or payment-document number; 58 payee-and-classification keys recur across months (notebook §6.3) |
| Recipient name and type | Pass | Payee CNPJ, name and type on every row; 725 municipal, 15 state-level payee rows under 22BO |
| Recipient geography | Conditional | UF and SIAFI municipality code, not IBGE; 523 of 526 municipalities join to IBGE by folded name + UF (notebook §6.5); 12 state-level rows have no municipality |
| Funder or programme | Pass | Órgão 53000, managing unit 530012 (Sedec), programme and action on every row |
| Instrument | Pass | Legal transfer under Lei 12.340, identified by the action; the transfer-type field itself merges legal and voluntary transfers |
| Amount with meaning | Pass | Cash paid in the month, nominal BRL, exact to the centavo |
| Stage and date | Conditional | Payment stage only; month, no day |
| Project description | Fail | Budget labels only; `LINGUAGEM CIDADÃ` is empty on all target rows |
| Disbursement or payment | Pass | This is the payment record |
| Adaptation relevance stated by source | Conditional | Prevention (8348) vs response and recovery (22BO) is stated at action level; no finer phase and no adaptation tag (notebook §6.4) |
| Links to other sources | Fail | Only CNPJ and municipality; any portaria match is probabilistic |
| Licence | Acceptable tier | Free-use statement under Decreto 8.777, no named licence; flag for legal review |
| Access | Pass | Monthly bulk CSV without login |
| Temporal coverage | Pass | Monthly since January 2013 per the data-origin page; January–July 2026 reviewed |

Three sibling sources shape how this one is used. The Sedec transfer portarias in the Diário Oficial (a discovery candidate, not yet reviewed) carry the authorisation stage this file lacks: one act per transfer, with purpose, phase and amount; they are the natural pair, matched on CNPJ or municipality, amount and timing with a recorded match confidence. The Transferegov review does not overlap for current years: its 17 July 2026 snapshot holds programmes under actions 8348 and 22BO only for voluntary agreements from 2010 to 2019, and none for the 2026 legal transfers **(verified)**. The Portal da Transparência expense-execution files are the likely route to a document-level link (see Canonical downloads). This release now has a research-only catalog entry under the `disaster_risk` theme.

Four things were surprising. The negative and zero amounts in the full files were undercounted in the first profile (the July count had been read as the seven-month count). No 22BO budget plan names a single phase, so a response-versus-recovery split is impossible in this source, not merely hard. Action 8348 appears only three times in seven months, all to two municipalities. And official budget-plan labels still carry placeholder Medida Provisória numbers (`N. XXXXX, DE XX DE MAIO DE 2026`).

References:

- Fit criteria: `dataset-discovery/needs/2026-09-br-finance-pathways-review/search.yaml`
- Sedec portarias candidate: `br-dou-sedec-portarias` in `dataset-discovery/needs/2026-09-br-finance-pathways-review/candidates.yaml`
- Transferegov review: `dataset-review/reviews/br-mgi/br-transferegov-discricionarias-legais/`

## Current approved release

No release is approved. Working release: **2026-07** (`releases/2026-07/`). The extraction notebook reproduces every count and sum in the data-profile table and writes one table of the 743 target rows; the release review states what that table can and cannot support.

A second notebook maps the release to the ICB × OEF adaptation action bank (V13). The source has no per-payment description, so the mapping unit is the budget action and the crosswalk is route-level evidence only. It retains three medium-confidence component links pending adjudication: 8348 to slope stabilisation and climate-resilient water supply (its two eligible categories on the MIDR action page, verified), and 22BO to post-disaster financial support. Looser links to emergency planning, resilient retrofits and shelters were excluded to prevent a budget classification from becoming an unsupported payment-level claim. Payment amounts are never split across actions or assigned to an individual mapped activity. The action bank export is a local-only input held in the BNDES review's `sample/`.

References:

- Notebook: `releases/2026-07/transferencias_extract_clean.ipynb`
- Bilingual release builder: `releases/2026-07/build_bilingual_release.py`
- Release review: `releases/2026-07/review.md`
- Adaptation mapping notebook: `releases/2026-07/map_adaptation_actions.ipynb`
- Crosswalk to the adaptation action bank: `releases/2026-07/data/br_transparencia_transferencias_to_adaptation_actions.csv`
- Action bank input (local only, gitignored): `dataset-review/reviews/br-bndes/br-bndes-operacoes-financiamento/releases/2026-09-01/sample/adaptation_action_bank_icb_oef_v13.csv`
- MIDR action 8348 page: https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil/solicitacao-de-recursos-1/acao-8348-apoio-a-obras-emergenciais-de-mitigacao-para-reducao-de-desastres
- Extract: `releases/2026-07/sample/br_transparencia_transferencias_civil_defence_payments.csv`
- IBGE municipality list used for the join test: `dataset-review/reviews/br-ibge/br-munic/releases/2020-2021/data/br_munic_finance_push.csv`
- Despesas – Execução data dictionary (empenho): https://portaldatransparencia.gov.br/pagina-interna/605513-dicionario-de-dados-despesas-pagamento
