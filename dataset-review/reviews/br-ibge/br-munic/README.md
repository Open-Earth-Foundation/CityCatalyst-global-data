# IBGE — Pesquisa de Informações Básicas Municipais (MUNIC)

MUNIC is IBGE's annual census of municipal administrations: the prefecture of every Brazilian municipality reports on its own structures, instruments and policies. This entry covers the two editions that carry the finance-push capacity variables for the Brazil finance-feasibility method: 2020 (environment and risk-and-disaster-management blocks, base published 2021-11-10) and 2021 (legislation and planning instruments, base republished 2024-04-25). The 2024 edition (base of 2025-11-07) was checked and contributes nothing to this use: its governance block is transparency and data-protection content, and its climate-events block covers only Rio Grande do Sul. MUNIC's thematic blocks rotate between editions, so no single year carries all components; the release `2020-2021` combines the latest edition that carries each one.

## Canonical downloads

Bulk data lives on IBGE's public FTP, one folder per edition, each holding a base workbook (data plus dictionary) and result tables. There is no row-level API; retrieval is direct file download. Base dos Dados republishes harmonised copies, but the FTP is canonical.

- 2020 base: https://ftp.ibge.gov.br/Perfil_Municipios/2020/Base_de_Dados/Base_MUNIC_2020.xlsx
- 2021 base: https://ftp.ibge.gov.br/Perfil_Municipios/2021/Base_de_Dados/Base_MUNIC_2021_20240425.xlsx
- 2024 base (checked, not used): https://ftp.ibge.gov.br/Perfil_Municipios/2024/Base_de_Dados/Base_MUNIC_2024_20251107.xlsx
- Edition index: https://ftp.ibge.gov.br/Perfil_Municipios/
- 2020 publication (notas técnicas): https://biblioteca.ibge.gov.br/visualizacao/livros/liv101871.pdf
- 2021 publication (notas técnicas): https://biblioteca.ibge.gov.br/visualizacao/livros/liv101985.pdf

Retrieved files, pinned by hash:

| File | Size (bytes) | SHA-256 |
|---|---|---|
| Base_MUNIC_2020.xlsx | 14,204,953 | 8b89371dfdff43e32e8f6faa1950c95300eba6cd301d7a5f53f15f199b62ced1 |
| Base_MUNIC_2021_20240425.xlsx | 18,796,622 | cc3b942c2885798e767100766c3b2888e31d1eca42b796538af2cfc3e76edb4e |
| Base_MUNIC_2024_20251107.xlsx | 25,535,974 | 93d9f836e4435df6429c642fa6897640a0f0e67b7946cf354bb04eded342bf01 |

The 2021 filename encodes a republication date. IBGE's erratum confirms the 2024-04-25 replacement changed only variable MCUL42 in the Cultura sheet (empty cells filled with "Não"), so it does not affect the legislation block used here (**verified**: https://www.ibge.gov.br/novo-portal-erramos/39851-substituicao-da-base-de-dados-da-munic-2021.html).

## Why we use it

- Supplies the `finance_push` institutional capacity layer of the Brazil finance-feasibility method: whether a municipality has the bodies, funds, plans and staff signals needed to formulate and pursue climate finance.
- Direct complement to the CAPAG fiscal gate: CAPAG screens the Union-guaranteed credit routes, MUNIC covers the capacity to reach the other routes; both join on the seven-digit IBGE municipality code.
- Deliberately disjoint from the Impact side of the method: the blocks used here contain no poverty, income or vulnerability variables, so there is no double counting against AdaptaBrasil.

## License

The FTP states all files are public (**verified**: "Todos os arquivos aqui disponíveis são públicos"). No named license instrument (Creative Commons, ODbL or similar) appears on the dataset pages, the library records or the publication front matter (**verified absence**; unlike CAPAG's explicit ODbL). Reuse with attribution to IBGE is standard practice under the federal open-data regime (**inferred**). Attribution used by IBGE's own tables: "Fonte: IBGE, Pesquisa de Informações Básicas Municipais". Confirm terms with IBGE before redistributing raw extracts commercially.

## Spatial and temporal scope

All 5,570 municipalities, one row each, national coverage with no duplicates. Values are local truth as declared by each prefecture, not modelled priors. Answers refer to the interview date unless a question states otherwise. Fieldwork windows matter: the 2020 edition was collected September 2020 to March 2021, straddling the November 2020 municipal elections and January 2021 inaugurations, so a declared structure may belong to an outgoing or incoming administration; the 2021 edition was collected September 2021 to March 2022, mid-term. The survey is annual but blocks rotate: the environment and risk blocks last ran in 2020, the planning-instruments block in 2021, and whether either returns in the 2025 edition is **unanswered** (no announced theme list; settled when IBGE publishes the 2025 questionnaire or results, expected late 2026).

## The finance_push component map

Each component is one block of the extraction notebook and one or two status columns in the release table, categorical and per-municipality. National counts are from the profiled 2020/2021 bases (**verified** by notebook assertions).

| Component | Edition | Variables | Municipalities passing |
|---|---|---|---|
| Environment governance body | 2020 | MMAM01 | 1,658 dedicated; 3,522 shared; 288 none |
| Environment council | 2020 | MMAM10, MMAM15/MMAM1518 | 4,375 exist; 366 with own budget line |
| Environment fund | 2020 | MMAM17, MMAM18 | 3,274 exist; 1,467 used in 2019 |
| Earmarked environment resources | 2020 | MMAM16 | 2,578 |
| Climate adaptation/mitigation legislation | 2020 | MMAM2011 + year | 390 |
| Federal climate training of staff | 2020 | MMAM08 root, MMAM098 topic | 193 |
| Civil-defence structure | 2020 | MGRD212, MGRD225, MGRD226, MGRD2212 | 4,236 body; 968 with budget-law line; 1,326 staffed |
| Planning instruments | 2021 | MLEG01 + MLEG02–MLEG22 battery | 2,960 plano diretor; instrument count 0–21 |

One component from the method's wish list is deliberately absent: intermunicipal consortium participation. MUNIC last surveyed consortia by policy area in the 2015 edition, and an eleven-year-old flag would degrade a current capacity score, so the component was dropped and the gap recorded (see Interpretation warnings).

## Methodology

MUNIC is a self-completed administrative survey: the prefecture is the informant, answering through its department heads, via web system or emailed questionnaire (**verified**, notas técnicas). Every variable is therefore a declaration by the body being assessed, not an audited fact. IBGE's own caveat for the planning block generalises to the whole survey: the existence of an instrument "não garante, necessariamente, o cumprimento da função social da Cidade" (**verified**). Non-response has four distinct forms and the bases keep them distinct: `Recusa` (refusal), `Não informou` (did not answer), `Não soube informar` (knows it exists but no details, an existence-positive answer), and `-` (question skipped by filter logic). In 2020, 90 municipalities refused the entire survey and carry `Recusa` across all blocks; in 2021 only two did (Porto de Moz/PA, São José/SC) (**verified**).

| Finding | Status | Evidence |
|---|---|---|
| Prefecture self-report, web/email collection, interview-date reference | **verified** | 2020 and 2021 notas técnicas |
| 2020 fieldwork Sep 2020–Mar 2021; 2021 fieldwork Sep 2021–Mar 2022 | **verified** | Notas técnicas of each edition |
| Block-to-edition mapping (environment/risks 2020, planning 2021) | **verified** | Sheet and dictionary inspection of the three bases |
| MMAM098 measures federal training on climate, not a management area | **verified** | Skip-logic crosstab: its `-` count exactly matches MMAM08 = Não |
| MUNIC has no direct "climate plan" question in any recent edition | **verified** | 2020/2021/2024 dictionaries searched |
| Consortia by policy area last surveyed 2015 | **verified** | IBGE MUNIC 2015 release; only a health-consortium pair remains in 2021 |
| Reuse-with-attribution licensing | **inferred** | Public-files statement plus federal open-data practice; no named instrument found |
| Whether environment/risk blocks return in the 2025 edition | **unanswered** | No announced theme list at review time |

## Fit for purpose

The verdict is **conditional pass**. MUNIC is fit as the institutional finance-push capacity layer: categorical, per-municipality, nationally complete, cleanly joinable, and free of Impact-side variables. It is not fit as a climate-plan register (only a legislation proxy exists), a consortium signal (dropped), or any measure of capacity quality (self-reported existence only). The component-level detail and the claims/anti-claims live in the release review; the headline conditions are the naming discipline (`climate_legislation`, not `climate_plan`; `planning_instruments`, not project-formulation capacity) and the unknown-handling rule (refusals are unknown, never "no").

## Interpretation warnings

Declared existence collapses when the survey asks about activity or money, and the collapse is large: 3,274 municipalities declare an environment fund but only 1,467 report using it in 2019; 4,375 declare a council but only 366 report it having its own budget line; 4,236 declare a civil-defence body but only 968 report a civil-defence line in the annual budget law. A finance-push score built on bare existence flags roughly doubles apparent capacity; score the activity variables where they exist.

The 90 whole-survey refusals of 2020 are the same municipalities in every 2020 block. Their components are unknown, not absent; treating them as "no" silently zeroes about 1.6% of the country, and the release table flags them explicitly.

There is no climate-plan variable anywhere in recent MUNIC. The nearest instrument is municipal legislation on climate adaptation and mitigation (390 municipalities), which may be an article in another law rather than a plan. Any downstream field must be named for what it is.

Climate-specific capacity is rare and size-graded: climate legislation rises from 3.7% of municipalities under 5,000 people to 37.5% of those above 500,000. A finance-push component built on it mostly separates large cities from the rest; interpret small-municipality zeros accordingly.

The 2020 answers straddle a municipal administration change and are five-plus years old at review time, spanning a further election (2024). Structures (secretariats, councils) decay faster than legislation (a plano diretor persists); weight component confidence accordingly.

The intermunicipal-consortium gap: MUNIC cannot currently support a consortium component. The 2015 edition was the last to measure consortia by policy area (environment 25.2%, solid waste 35.2% of municipalities then); the 2021 base retains only a health-consortium pair and the 2020 base an indirect signal (whether the solid-waste plan is single-municipality). If a future edition revives the block, add the component then.

## Parsing notes

Each base is one sheet per thematic block plus a `Dicionário` sheet; data starts at row 2 with variable codes as headers. Dictionary codes are upper-case (`MMAM01`) but data headers are title-case (`Mmam01`).

`CodMun` is stored as a number but is an identifier: emit as a seven-character string. Municipality names are not join keys twice over: they are not unique nationally, and the 2020 base strips apostrophes entirely ("Alta Floresta DOeste" for D'Oeste).

The answer vocabulary is `Sim`, `Não`, `Recusa`, `Não informou`, `Não soube informar`, and `-` for filter skips; some 2021 instrument questions answer `Sim, com legislação específica` or `Sim, como parte integrante do Plano Diretor`, and one 2020 council question answers `Não foi instalado ou está inativo`. Map the full vocabulary explicitly and fail on anything unmapped; collapsing any of these to "Não" corrupts the unknowns.

Skip logic (`-`) must be resolved per battery, not globally. Verified filters: the MMAM09x training-topic battery is asked only where MMAM08 = Sim; the MGRD22x civil-defence battery only where a COMPDEC or similar exists (MGRD212 = Sim); the MMAM1518 council-infrastructure item only where a council exists and infrastructure is provided; MMAM18 (fund used) only where MMAM17 = Sim.

The 2021 legislation sheet carries 7 trailing all-blank rows; drop all-blank rows before use. The 2024 base renames identity columns (`Cod Munic`, `Desc Mun` versus `CodMun`, `Mun`) and drops accents from some sheet names (`Governanca`, `Habitacao`); sheet names also drift across editions (`Agropecuário` 2020 versus `Agropecuária` 2024). The 2024 climate-events sheet covers only the 497 Rio Grande do Sul municipalities.

The 2020 block sheets carry no population column (population estimates sit in the separate `Variáveis externa` sheet); the 2021 sheets carry `Pop` inline.

## Current approved release

No release is production-approved. Review work is underway for **2020-2021**.

### References

- Extraction notebook → `releases/2020-2021/munic_finance_push_extract.ipynb`
- Release table → `releases/2020-2021/data/br_munic_finance_push.csv`
- Release review → `releases/2020-2021/review.md`
- Fiscal-gate sibling → `dataset-review/reviews/br-stn/br-capag/`
- Brazil finance routes reference → `knowledge-base/topics/climate-finance/br-climate-finance.md`
