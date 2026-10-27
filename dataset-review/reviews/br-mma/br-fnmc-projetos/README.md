# Ministério do Meio Ambiente e Mudança do Clima — Projetos FNMC 2011 a novembro/2025

This review covers the open-data table of projects supported by the Fundo Nacional sobre Mudança do Clima (FNMC, also called Fundo Clima) through its non-reimbursable arm, which the Ministério do Meio Ambiente e Mudança do Clima (MMA) runs directly as grants. BNDES runs the separate, repayable credit arm, which this table does not cover. The release reviewed is the file the publisher labels "2011 a novembro/2025". **Status: provenance, access, licence, profiling, a reproducible cleaned release, reviewed English translations for all 82 records and a draft adaptation mapping are complete. Human adjudication of medium-confidence mappings remains pending.** Nothing here is production-approved.

## Canonical downloads

The canonical source is the dataset record on the MMA open-data portal, a CKAN catalogue. It holds two resources: the projects CSV and a data dictionary PDF. The record was created on 9 August 2022 and last updated on 29 January 2026; the portal states an annual update cycle. The projects resource was created on 27 November 2024 and keeps a fixed resource identifier while its file is replaced, so each yearly file supersedes the previous one at the same address and older files are not kept by the publisher (inferred from the resource dates and the single live resource). The release name `2025-11` follows the publisher's own label for the data cut-off.

The copy used for this review was downloaded on 23 September 2026. It is 34,044 bytes, encoded cp1252, semicolon-separated, with SHA-256 `334118fafa9092403b93e744c672ee06f858ff29676c9e5b59123902ea0ba23a`. Because the portal's last update (29 January 2026) predates the download, this copy is very likely the live file (inferred; a fresh download to compare the hash is pending).

Retrieval is a manual or scripted download of a static file. The portal's metadata API is blocked to automated fetchers by the site's robots rules, and the file download is refused by the cloud environment's network policy, so a refresh currently needs a browser download.

The table also appears on the MMA's gov.br pages as a PDF. That copy sits under the gov.br site licence rather than the dataset licence (see License), so the CSV is the copy to use.

References:

- Dataset record → https://dados.mma.gov.br/dataset/32b154de-d5eb-43de-9a72-7da0dca3d259 (slug `fundo-nacional-sobre-mudanca-do-clima`)
- Projects CSV → https://dados.mma.gov.br/dataset/32b154de-d5eb-43de-9a72-7da0dca3d259/resource/5f0f6325-f45a-457d-9e94-fb44971c70a0/download/projetos-fnmc-2011-a-2025-dados-abertos.csv
- Data dictionary PDF → https://dados.mma.gov.br/dataset/32b154de-d5eb-43de-9a72-7da0dca3d259/resource/17b96c88-c397-4b07-ad28-8a49cbeb3bb4/download/dicionario_dados_abertos_fnmc_2026.pdf
- MMA FNMC page (control total) → https://www.gov.br/mma/pt-br/composicao/secex/dfre/fundo-nacional-sobre-mudanca-do-clima
- FNMC 2025 execution report (MMA) → https://www.gov.br/mma/pt-br/composicao/secex/dfre/fundo-nacional-sobre-mudanca-do-clima/Relatorio_FNMC_MMA_2025_Final.pdf
- Local copy → `releases/2025-11/sample/projetos-fnmc-2011-a-2025-dados-abertos.csv`

## License

The dataset record's licence field reads "Creative Commons Atribuição" and links to the Open Definition entry for CC BY; the portal adds that the dataset meets the Open Definition. Both resources show the same licence. Creative Commons Attribution allows copying, redistribution, adaptation and commercial use on condition of credit, so reuse in a commercial product is permitted (verified from the record). 

The licence **version is not stated**. The link target is a generic page covering CC BY 1.0 to 4.0, which is the default CKAN "cc-by" licence choice rather than a publisher decision about a version (inferred). Every CC BY version permits commercial reuse and derivatives, so the missing version does not change the go/no-go, but the attribution wording and the notice of changes depend on it. Until MMA confirms, the conservative reading is to follow CC BY 4.0's conditions (credit the creator, link the licence, indicate changes), which also satisfies the earlier versions' core terms (inferred; version is **unanswered**).

The publisher prescribes no citation wording, and the CSV itself carries no licence notice. The working attribution is "Ministério do Meio Ambiente e Mudança do Clima (MMA), Fundo Nacional sobre Mudança do Clima — Projetos FNMC 2011 a novembro/2025, dados.mma.gov.br, licença Creative Commons Atribuição", plus a note of changes made.

The PDF copy on gov.br falls under the gov.br site notice, recorded earlier as Creative Commons Attribution-NoDerivatives 3.0; that notice was not re-checked in this review, and the CSV route makes it moot.

| Finding | Status | Evidence |
|---|---|---|
| Licence is Creative Commons Attribution, on the dataset and both resources | **verified** | Dataset and resource pages, 24 September 2026 |
| Commercial reuse and adaptation permitted with attribution | **verified** | Terms common to all CC BY versions |
| Licence version | **unanswered** | Not stated on any page; answerable only by MMA (fnma@mma.gov.br) |
| Prescribed citation wording | **verified absent** | None on the record, resource or CSV |
| gov.br PDF copy is CC BY-ND 3.0 | **inferred** | Earlier repository evidence; not re-fetched |

## Data profile

The CSV contains 82 project/instrument records, exactly matching the publisher's stated project count. It also contains one unlabelled control-total row and three empty rows. All 87 logical CSV records have 20 fields, but only the first 16 are named or populated. All findings in this section are **verified** from the local source file unless marked otherwise.

| # | Publisher field | Observed representation | Blank project rows |
|---:|---|---|---:|
| 1 | `Ano` | Four-digit year, 2011–2025 | 0 |
| 2 | `Nº do Instrumento de Repasse` | Text identifier or instrument description | 0 |
| 3 | `Nº Processo` | Text identifier | 2 |
| 4 | `Nome do Projeto` | Text | 0 |
| 5 | `Instituição Executora` | Text | 0 |
| 6 | `UF` | State code, state name, multi-state list or `Brasil` | 0 |
| 7 | `Bioma` | Publisher category, including multi-biome values and `Todos` | 0 |
| 8 | `Área de Atuação - art. 7º Decreto 9578/2018` | 11 publisher categories | 0 |
| 9 | `Tipo de Instituição` | `OSC`, `Federal`, `Municipal` or `Estadual` | 0 |
| 10 | `Data de início da da Vigência` | Date, `D/M/YYYY` or `DD/MM/YYYY` | 0 |
| 11 | `Data de Fim da Vigência` | Date, mostly two-digit year; 18 rows use four-digit year | 0 |
| 12 | `Valor FNMC` | BRL currency text | 0 |
| 13 | `Valor contrapartida` | BRL currency text | 0 |
| 14 | `Valor Total` | BRL currency text | 0 |
| 15 | `Valor repassado` | BRL currency text | 1 |
| 16 | `Valor não repassado` | BRL currency text | 1 |
| 17–20 | unnamed | Empty in every record, including the total and padding rows | 82 |

The five amount columns reconcile exactly to the unlabelled total row after Brazilian currency strings are parsed. `Valor Total` also equals `Valor FNMC + Valor contrapartida` for every project. Where both transfer fields are populated, `Valor não repassado` equals `Valor FNMC - Valor repassado` for every project.

| Amount field | Project-row sum |
|---|---:|
| `Valor FNMC` | R$ 152,850,266.43 |
| `Valor contrapartida` | R$ 2,368,254.76 |
| `Valor Total` | R$ 155,218,521.19 |
| `Valor repassado` | R$ 127,737,821.59 |
| `Valor não repassado` | R$ 22,873,444.84 |

The table has no exact duplicate rows. The instrument identifier is not unique: `TC 02/2012` occurs twice, and the descriptive value `Descentralização órgão MMA` also occurs twice. Two records have no process number. One project name occurs twice under different years and instruments, representing two records rather than a duplicate. No single native field is therefore a complete row key; a durable source key is **unanswered** and should be checked against the data dictionary or publisher system before a production pipeline assigns identity.

## Spatial and temporal scope

The year field covers 2011–2025 but contains no 2019 record. The 82 rows comprise 23 records for 2011, between one and nine records for each other represented year, and four records for 2025. The agreement-validity start dates run from 21 August 2011 to 10 December 2025, and end dates run through 8 December 2027. Four rows labelled 2025 start in December 2025, so the publisher title's stated cut-off of November 2025 does not describe the actual contents (**verified**).

Geography is only coarsely structured. The `UF` field has 26 raw values: single state codes, one spelled-out state (`Bahia`), comma-separated multi-state lists and 12 national records labelled `Brasil`. There is no municipality field, no municipality code and no UN/LOCODE. Municipalities appear only incidentally in executor or project names, so city-level matching would require a bespoke, reviewed extraction rather than a direct join (**verified**).

## Interpretation warnings

The file shows funded project/instrument records and agreement-validity dates, but it does not supply a general status field, a signature date, approval date or accounting reference date. The administrative stage represented by an ordinary row is therefore **unanswered** until the data dictionary and programme methodology are read; the existence of an instrument number should not be converted automatically to `contracted` or `active`.

| Finding | Status | Consequence |
|---|---|---|
| Two instrument labels explicitly contain `ANULADO`; their combined `Valor FNMC` is R$ 12,511,712.91 and both have zero transferred | **verified** | The project's status is encoded inside a free-text identifier, not a status column. These rows must be retained and flagged, not counted as active awards. |
| The published control totals include the two annulled records | **verified** | R$ 152.85 million is a historical table total, not an active-portfolio or disbursed total. |
| `Valor FNMC` is the amount assigned to the project by the fund | **inferred** | The exact accounting stage (approved, committed or contracted) is not established by the CSV alone and must not be asserted before the methodology checkpoint. |
| `Valor repassado` and `Valor não repassado` describe transferred and not-transferred portions of `Valor FNMC` | **inferred** | Their arithmetic is internally consistent, but the as-of date and whether transfers are gross, net or cumulative remain unanswered. |
| One R$ 2,239,000 project has both transfer fields blank | **verified** | Blank does not mean zero. It must remain unknown; otherwise portfolio transfer totals and project status are misstated. |
| The year field differs from the validity-start year in four rows | **verified** | `Ano` cannot be assumed to be the award or agreement-start year without the data dictionary. |
| `Tipo de Instituição` is a publisher category, not a normalized legal-form field | **inferred** | Downstream recipient types need a documented mapping and review; names alone must not silently override the source category. |

## Parsing notes

The source is a CP1252, semicolon-separated export with mixed physical line endings and embedded newlines inside quoted cells. It must be opened with CSV-aware parsing and `newline=''`; line-by-line splitting, UTF-8 decoding or a physical `wc -l` count produces incorrect results (**verified**).

- The header for `Data de Fim da Vigência` contains a trailing embedded newline. Eight more embedded newlines occur across five project-name or executor cells, creating 96 physical lines for only 87 logical records.
- Four trailing delimiter fields create unnamed columns 17–20 in every logical record. Drop them only after verifying that they are empty.
- The unlabelled totals row has blank fields 1–11 and amounts in fields 12–16. Three fully empty padding records follow it. Select project rows by validated record structure, not merely by dropping the last four records.
- Leading tabs occur in several 2024–2025 identifiers, names and dates. Ordinary spaces, trailing spaces and one trailing non-breaking space also occur. Trim Unicode whitespace before key comparison or date parsing, and collapse embedded whitespace only in descriptive text.
- `UF` includes `Bahia`, `Brasil`, multi-value lists and inconsistent spaces around commas. `Bioma` includes multi-value strings with inconsistent internal spacing. Preserve the raw values and create normalized fields separately.
- Start dates always use four-digit years, but end dates mix two- and four-digit years. Parse both formats explicitly and retain the original text for audit.
- Currency values use `R$`, periods as thousands separators and commas as decimal separators. Parse them as decimal BRL values, not binary floats. Do not coerce the two blank transfer cells to zero.
- The two cancelled records are detectable only from `ANULADO` inside the instrument field. No other row carries an explicit status marker, so absence of that token is not proof of an active or contracted state.
- The existing compilation script converts blank currency cells to `0.0` and assigns `contratado` to every row without the `ANULADO` token. Both transformations are **verified** pipeline hazards: the first changes an unknown transfer value to zero, and the second asserts a stage the CSV does not establish.
- A literal question mark occurs in one indigenous place name (`Itax? Mirim`). It is present in the source bytes, not a decoding replacement, so preserve it and treat correction as a publisher-data issue.

The profile used the raw file exactly as downloaded. No cleaned release file has been created at this checkpoint.

## Current approved release

No release is approved. Working release: **2025-11** (`releases/2025-11/`). The cleaned table has English column names, preserves all 81 distinct source project titles in `project_name_pt`, and supplies a reviewed English project title for all 82 records with `translation_status=reviewed_english_translation`. The duplicate Portuguese title shared by two records has the same English translation. The mapping covers every record with a high, medium or explicit `none` decision.
