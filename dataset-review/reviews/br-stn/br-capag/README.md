# Secretaria do Tesouro Nacional — Capacidade de Pagamento de Municípios

This review covers the municipal Capacidade de Pagamento (CAPAG) dataset published by Brazil's Secretaria do Tesouro Nacional (STN). The current review release is the snapshot dated 1 June 2026, generated from Siconfi data and accounting-quality information with fiscal base year 2025 for municipalities. Provenance, access, licence, workbook structure, methodology and fit for the finance-feasibility use case have been reviewed, and the release's extraction notebook, cleaned table and release review are complete. Promotion to the catalog remains.

## Canonical downloads

The canonical source is the municipal CAPAG dataset on Tesouro Transparente. The selected release is `Capag Municípios 2026 - 01/06/2026`, the latest published municipal snapshot when this review began. The publisher also retains earlier snapshots from 2018 onward.

- Dataset page: https://www.tesourotransparente.gov.br/ckan/dataset/capag-municipios
- CKAN metadata API: https://www.tesourotransparente.gov.br/ckan/api/3/action/package_show?id=capag-municipios
- Selected release: https://www.tesourotransparente.gov.br/ckan/dataset/capag-municipios/resource/f117161f-44c4-4ada-9cfe-0d5da8c5b10e
- Direct XLSX: https://www.tesourotransparente.gov.br/ckan/dataset/9ff93162-409e-48b5-91d9-cf645a47fdfc/resource/f117161f-44c4-4ada-9cfe-0d5da8c5b10e/download/capag-municipios-posicao-2026-jun.xlsx
- Publisher metadata: https://www.tesourotransparente.gov.br/ckan/dataset/9ff93162-409e-48b5-91d9-cf645a47fdfc/resource/f3d005e7-97fb-4c9c-aefd-0d0288d54dfb/download/metadadoscapagmunicipios.pdf

The retrieved XLSX is 24,023,822 bytes with SHA-256 `86305234feee719b8098fc183bd6aa4c924d5df1737235de73867563be331b53`. The file opens as a valid Office Open XML workbook and passes compressed-file integrity validation.

Tesouro's CKAN API provides dataset and resource metadata, including the current resource URL, but not municipality records. The CAPAG XLSX is an uploaded CKAN resource rather than a CKAN DataStore table: `resource_show` succeeds, while the portal does not expose the `datastore_search` action. A refresh can therefore be automated as API discovery followed by file download, but cannot currently query CAPAG rows as JSON from the official catalog.

A re-check of the Treasury's other programmatic channels (July 2026) found no row-level CAPAG API anywhere official. The Tesouro Data Lake APIs carry no CAPAG endpoint: the Siconfi module serves the fiscal statements CAPAG is computed from (RREO, RGF, DCA, FINBRA, MSC, entes), so it can supply inputs but not the published grades or ICF, and the SADIPEM module serves credit-operation (PVL) records, not the quadrimestral snapshot. Third-party mirrors exist but do not substitute for the source: Base dos Dados republishes CAPAG only through 2020, and commercial lookup services (e.g. Infosimples) are paid scrapers of the same Treasury data. The XLSX download therefore remains the only official row-level channel.

References:

- Data Lake API documentation: https://apidatalake.tesouro.gov.br/docs/siconfi/
- Siconfi open-data API page: https://www.tesourotransparente.gov.br/consultas/consultas-siconfi/siconfi-api-de-dados-abertos
- SADIPEM API catalog entry: https://www.gov.br/conecta/catalogo/apis/sadipem-sistema-de-analise-da-divida-publica-operacoes-de-credito-e-garantias-da-uniao-estados-e-municipios

## Why we use it

CAPAG provides a municipality-level fiscal assessment relevant to finance routes that require Union-guaranteed credit. It is being reviewed as a city-side input to the Brazil finance-feasibility method, where the intended use is a categorical credit-access signal rather than a general measure of climate vulnerability or implementation capacity.

## License

The dataset page assigns the Open Data Commons Open Database License (ODbL). Tesouro Transparente additionally permits use for any purpose, including commercial use, reproduction, modification and distribution, provided the Secretaria do Tesouro Nacional and the portal URL are cited. Public redistribution of a derivative database must retain the ODbL attribution and share-alike conditions.

Required attribution: `Secretaria do Tesouro Nacional - disponível em: www.tesourotransparente.gov.br`.

## Spatial and temporal scope

The selected release contains 5,568 unique municipality codes across 26 states. Every published row identifies a municipality with a seven-digit IBGE code, name and UF. The workbook states that the final score originates from fiscal base year 2025 for every row.

The publisher labels the dataset quadrimestral. Multiple dated snapshots can occur within one publication year, so the release date and fiscal base year are separate fields and both must be preserved.

## Methodology

CAPAG measures the fiscal risk to the National Treasury of a state or municipality taking on new debt backed by a Union guarantee. It is a deterministic regulatory classification built from fiscal accounts reported through Siconfi; it is not a probability of default, a statistical credit score or a measure of whether a climate intervention is financially viable.

The June 2026 workbook calculates three ratios. The indicator values are fractions in the workbook and should be formatted as percentages for display:

| Component | Measure and baseline | Partial grades in the June 2026 workbook |
|---|---|---|
| Debt (`DC`) | Consolidated debt divided by net current revenue, using the latest fiscal exercise | `A` below 60%; `B` from 60% to below 100%; `C` at or above 100% |
| Current savings (`PC`) | Adjusted committed current expenditure divided by adjusted current revenue over the latest three fiscal exercises, weighted 20% oldest, 30% middle and 50% latest | `A` below 85%; `B` from 85% to below 95%; `C` at or above 95% |
| Relative liquidity (`LR`) | Gross cash availability, adjusted for cash insufficiency, minus financial obligations, divided by net current revenue for the latest fiscal exercise | `A` at or above 5%; `B` above 0% and below 5%; `C` at or below 0% |

The three partial grades produce an unadjusted CAPAG. It is `A` when debt is `A` and the savings/liquidity pair is `A/A`, `A/B` or `B/A`; `D` when all three grades are `C`; `C` when either savings or liquidity is `C`; and `B` for the remaining valid combinations. If any component cannot be calculated, the combined result is `n.d.`.

The workbook then applies the Siconfi accounting and fiscal information quality grade (`ICF`). `Aicf` upgrades `A` to `A+` and `B` to `B+`; these plus grades are a data-quality/governance bonus, not evidence of a better fiscal ratio. The workbook converts `Eicf` to `n.e.`. Current Treasury rules also make municipalities with `Dicf` ineligible from 2026, but the June 2026 workbook does not apply that rule to its final CAPAG column: 537 records retain a letter grade or `n.d.`, including 186 records with displayed `A` or `B`. This is a verified conflict between the published workbook logic and the effective eligibility rule. A finance-feasibility indicator must use the ICF column alongside CAPAG and must not classify those 186 `Dicf` records as eligible merely because the workbook displays `A` or `B`.

There is no modelled confidence interval or quantified uncertainty. The important uncertainty is administrative: the result depends on the completeness, quality and timing of reported fiscal statements and can change after republication or formal verification. The preliminary dataset therefore supports a dated screening signal, not a forecast or permanent municipal attribute.

For the proposed finance-feasibility method, `A`, `A+`, `B` and `B+` may indicate a potentially available Union-guaranteed credit route only when the applicable ICF and other legal conditions are satisfied. `C`, `D`, `n.d.`, `n.e.` and spreadsheet errors do not all mean the same thing and must remain separate. CAPAG does not assess project cash flow, capital cost, climate impact, municipal delivery capacity, access to grants, borrowing without a Union guarantee or final approval of a credit operation. Some fiscal programmes and operation types also have regulatory exceptions, so an unfavourable CAPAG must not be interpreted as a universal prohibition on all finance routes.

Evidence status for this methodology is:

| Finding | Status | Evidence |
|---|---|---|
| Purpose, three-indicator design and preliminary/non-binding status | **verified** | Current Treasury CAPAG page and municipal dataset page |
| Indicator formulas, thresholds, three-year weights and grade-combination logic | **verified** | Effective regulations and formulas in the June 2026 workbook |
| `Aicf` upgrades and workbook treatment of `Eicf` | **verified** | June 2026 workbook formulas and observed results |
| `Dicf` is ineligible from 2026, while the workbook retains displayed grades | **verified** | Effective rule, Treasury explanation and cross-tabulation of the June 2026 workbook |
| Why the June 2026 workbook does not apply the `Dicf` rule to its final column | **unanswered** | No publisher explanation was found in the dataset metadata or current CAPAG guidance |
| Code `5101837` appears internally but not in the result sheet | **unanswered** | Workbook comparison; no publisher explanation found |

References:

- Current CAPAG guidance: https://www.tesourotransparente.gov.br/temas/estados-e-municipios/capacidade-de-pagamento-capag
- Portaria Normativa MF nº 1.583/2023: https://www.ba.gov.br/seplan/sites/site-seplan/files/migracao_2024/arquivos/wp-content/uploads/PORTARIA-NORMATIVA-MF-No-1.583-DE-13-DE-DEZEMBRO-DE-20230-PORTARIA-NORMATIVA-MF-No-1.583-DE-13.12.2024.pdf
- Portaria STN/MF nº 857/2026: https://legislacaofinanceira.fazenda.sp.gov.br/Federal/PORTARIA%20STN-MF%20N%C2%BA%20857%20DE%2027%20DE%20MAR%C3%87O%20DE%202026.pdf
- Treasury explanation of the 2026 `Dicf` rule: https://www.gov.br/tesouronacional/pt-br/noticias/ministerio-da-fazenda-altera-metodologia-para-calculo-da-analise-da-capacidade-de-pagamento-capag/

## Fit for purpose

The verdict is **conditional pass**. CAPAG is fit as the minimum city-side fiscal signal and as a regulatory screen for finance routes that require a Union guarantee. It is not fit as a standalone financial-feasibility score, a smooth fiscal-capacity axis or a gate on grants, transfers and other non-guaranteed routes.

The originating feasibility method asks whether an intervention's cost and type can be matched to a city's fiscal capacity and reachable funding routes. Against that need:

| Requirement | Result | Implication |
|---|---|---|
| National, municipality-level city signal | **conditional** | The result sheet has 5,568 unique IBGE-coded municipalities. It omits the newly installed Boa Esperança do Norte/MT from the final result despite carrying its code internally, and Calçoene/AP has spreadsheet errors rather than a usable assessment. |
| Clean join to city profile | **pass** | The seven-digit IBGE municipality code is a stable join field once emitted as a string. Names must not be used as keys. |
| Current fiscal-capacity evidence distinct from climate vulnerability | **pass** | The ratios measure reported debt, current savings and liquidity and do not reuse AdaptaBrasil's impact or vulnerability variables. |
| Hard gate for Union-guaranteed credit | **conditional** | CAPAG is directly relevant, but the final grade must be combined with ICF and a versioned rule. The displayed CAPAG column alone misclassifies 186 `Dicf` municipalities under the rule effective in 2026. |
| Distinguish favourable, unfavourable and unknown cases | **pass** | The source supports separate raw grades, partial indicators, ICF and explanatory observations. The extraction must preserve `n.d.`, `n.e.` and error states rather than forcing a binary value. |
| Estimate the intervention funding gap | **fail alone** | CAPAG contains no intervention cost, type, sector, OPEX or revenue information. It must be joined to the intervention profile. |
| Determine whether all finance routes are open | **fail alone** | It directly informs only credit routes subject to a Union guarantee. Grant, transfer, intermediated, emergency and political routes require programme eligibility, institutional capacity, emergency and other evidence. |
| Produce a smooth 0–1 finance score | **fail alone** | Regulatory categories are not equal numerical intervals. Converting `A+` through `D` into evenly spaced numbers would invent a scale not present in the methodology. |
| Support reproducible refreshes | **conditional** | CKAN metadata discovery and XLSX download can be automated, but the resource is formula-heavy, publication timing is quadrimestral and the eligibility interpretation must be versioned alongside regulatory changes. |
| Permit reuse | **pass** | ODbL terms and the required STN attribution are explicit. |

The June 2026 distribution also changes how the feasibility method should describe the gate. The workbook contains 2,544 raw favourable grades (`A`, `A+`, `B` or `B+`), or 45.7% of rows. Removing the 186 favourable-looking `Dicf` records leaves 2,358 municipalities, or 42.3%, that pass this preliminary CAPAG/ICF screen. With information-quality failure taking precedence over the displayed fiscal result, the remaining derived states are 674 information-quality failures (12.1%), 1,984 fiscal failures (35.6%) and 552 unknown results (9.9%). These are screening groups, not final credit approvals.

The recommended use is therefore a versioned categorical feature rather than a single numeric CAPAG score:

| Derived state | Rule for the June 2026 release | Permitted claim |
|---|---|---|
| `credit_screen_pass` | Published CAPAG in `A`, `A+`, `B`, `B+` and ICF not `Dicf` or `Eicf` | The municipality passes the preliminary CAPAG/ICF screen for a route requiring a Union guarantee. |
| `credit_screen_fail_information_quality` | ICF in `Dicf` or `Eicf` under the 2026 rule | The municipality does not pass the information-quality requirement, regardless of a displayed favourable letter. |
| `credit_screen_fail_fiscal` | ICF passes the information-quality rule and published CAPAG is `C` or `D`, unless a documented regulatory exception applies | The published fiscal classification does not pass the ordinary CAPAG screen. |
| `credit_screen_unknown` | ICF is not `Dicf` or `Eicf` and CAPAG is `n.d.`, an error or absent | This release cannot establish a passing CAPAG screen. |

The derived state must not be named simply `credit_eligible`. CAPAG is necessary but not sufficient: formal approval also considers the specific operation, counter-guarantees, costs, credit limits and other legal conditions. A route-specific model should apply this signal only to the guaranteed-credit arms of Route A and Route C. It should not lower grant or transfer routes because a city fails this screen, and it should retain documented programme exceptions rather than treating CAPAG as a universal borrowing prohibition.

No production catalog dataset currently supplies an equivalent Brazil municipal fiscal-capacity signal. The Brazil geography collection contains AdaptaBrasil and SEEG, which answer impact and emissions questions rather than financing capacity. The climate-finance collection contains global lender portfolios and a Chilean city-action fundability model; the latter is a useful structural precedent but its Chilean fiscal inputs cannot substitute for CAPAG. The local Brazil climate-awards compile supplies revealed examples for Routes A–C and is a direct complement for testing route matching, but it is still a staging compilation rather than a vetted catalog dataset. IBGE MUNIC remains the priority complement for finance-push capacity, while Siconfi/FINBRA or IFEM would be extended fiscal complements rather than replacements for the regulatory gate.

Evidence status for this fit assessment is:

| Finding | Status | Evidence |
|---|---|---|
| CAPAG is suitable as a city fiscal signal and guaranteed-credit screen | **verified** | Feasibility-method requirements matched to the current CAPAG rules and workbook fields |
| CAPAG is insufficient for intervention-level or all-route feasibility | **verified** | CAPAG scope compared with the cost, type, sector, finance-push and six-route inputs required by the method |
| The June 2026 preliminary screen yields 2,358 passing municipalities after applying the `Dicf` rule | **verified** | Workbook cross-tabulation using published CAPAG and ICF fields |
| The Brazil climate-awards compile can supply sample interventions and revealed route evidence | **verified** | Local compile schema, collection notes and source registry |
| A later combined model will improve predictive validity or ranking quality | **unanswered** | Requires sample-city/intervention testing and sensitivity analysis; CAPAG alone cannot establish this |

References:

- Feasibility methodology draft: https://docs.google.com/document/d/1TyCqsRmjyqFGu3gwL4JEjCWWGPoaf1p377QZPnbkiUk/edit?tab=t.0
- Brazil climate-finance reference: `knowledge-base/topics/climate-finance/br-climate-finance.md`
- Brazil awards staging compile: `dataset-compile/br-climate-awards/`
- Catalog theme view: `dataset-review/collections/by-theme.yaml`
- Catalog geography view: `dataset-review/collections/by-geography.yaml`

## Interpretation warnings

The published score is a snapshot aligned with the Treasury's `Prévia Fiscal`, not a binding decision by the Treasury. Definitive CAPAG is calculated during formal verification for a specific credit operation, so this dataset can support a preliminary credit-route eligibility signal but cannot establish that a municipality has approval to borrow or will receive a Union guarantee.

The final CAPAG field is categorical but contains nine observed values: `A`, `A+`, `B`, `B+`, `C`, `D`, `n.d.`, `n.e.` and one literal `#N/A`. Missing or exceptional values therefore cannot be collapsed into a single low grade.

The final CAPAG column cannot be used as an eligibility flag by itself. In particular, the workbook retains `A` for 103 and `B` for 83 municipalities graded `Dicf`, even though the applicable rule makes `Dicf` municipalities ineligible from 2026. Downstream logic must preserve the published CAPAG, preserve ICF separately and derive any eligibility screen under an explicitly versioned rule.

The workbook publishes 5,568 final municipality rows although an internal `Datalake` sheet contains 5,569 unique entity identifiers. Code `5101837` appears in the internal sheet but not in the final result. The reason remains unanswered and must be resolved before making a complete-national-coverage claim.

Calçoene/AP (`1600204`) is the single final row whose CAPAG and all three indicator values and grades are literal `#N/A`. Downstream extraction must retain and flag this record rather than treating the Excel error token as a missing cell.

The current-savings grade cannot be reproduced from the displayed savings indicator: 1,026 of 5,126 checkable rows mismatch the published thresholds, while the debt and liquidity grades reproduce exactly from theirs (0 mismatches each). This is consistent with the displayed value being a single-exercise figure while the grade reflects the three-exercise weighted calculation held in the workbook's input sheets (inferred; the mismatch counts are verified in the extraction notebook). Downstream logic must use the published grade columns and never re-derive a grade from a displayed indicator.

Raw indicator values are not bounded and must not feed averages, rankings or scores unfiltered. Seven municipalities carry reporting-artifact savings ratios (from −1.77 up to 28,123, mostly from declared-negative items in the underlying fiscal statements); five of the seven carry an explanatory observation and all land on `n.d.` or `n.e.` rather than a letter grade.

## Parsing notes

The source is an 11-sheet calculation workbook, not a flat data export. The result sheet is `Prévia da CAPAG`; its headers are on row 3 and its 5,568 data rows begin on row 4. The first two rows contain lookup formulas and working labels and must not be parsed as records.

Do not interpret the portal's `URL de API` control as a row-level data endpoint. It returns CKAN package metadata. Extraction still requires downloading the resource URL returned by that metadata call and parsing the workbook.

The result sheet has 22 columns and 105,818 formula cells. Values must be read from Excel's cached results or reproduced from the documented methodology; loading the full workbook formatting and formula model exceeded 4 GB of memory in one inspection library, while read-only streaming completed successfully.

The 11 sheets are `Prévia da CAPAG`, `CAPAG Ano Base 2024`, `CAPAG Ano Base 2025`, `Datalake`, `DCA_Ultimo_Exercicio`, `DCA_Penultimo_Exercicio`, `RGF_Ultimo_Exercicio`, `RGF_Penultimo_Exercicio`, `RREO_Ultimo_Exercicio`, `ChavesBusca` and `Ranking`. The non-result sheets are calculation inputs, availability checks, lookup keys and prior-year components; they must not be unioned as additional municipality observations.

The municipality code is stored as a number in the workbook but is an identifier and should be emitted as a seven-character string. Municipality names are not unique nationally; joins must use the IBGE code rather than the name.

The final result has no duplicate municipality codes and no nulls in code, name, UF or CAPAG. The three numeric indicator columns mix numeric values with text sentinels such as `n.d.` and `#N/A`, so type coercion must explicitly separate numeric measurements from status values. Loading through pandas defaults silently converts the literal `#N/A` error tokens to blanks; the extraction reads cached values through openpyxl to preserve them.

The result sheet also carries workbook-internal working columns alongside the published result: availability checks (`Possui DCA 2025?`, `Possui DCA 2024?`, `Publicou RGF`, `Publicou RREO`), the prior-method `Indicador 3 Antigo`, diagnostic flags (`Dedução Negativa`, `DCB zerada ou negativa`, `OF negativa`) and a `CAPAG rebaixada` column that is entirely empty in this release. The extraction keeps the published result columns and drops the working columns.

`Observação` carries explanatory text for 810 municipalities and contains embedded line breaks where more than one issue applies (an earlier count of 811 included Calçoene's `#N/A` error token in this column). It should be preserved as explanatory source text or normalized into flags without losing the original wording.

## Current approved release

No release is production-approved. For **2026-06-01** the extraction notebook, cleaned table and release review are complete (`releases/2026-06-01/`); promotion to `catalog/index.yaml` is pending approval.
