# Brazilian Federal Government — national climate policy documents

This review covers ten federal climate-policy documents selected for adaptation analysis. All ten have reproducible extraction outputs, but the corpus is still a research release: human adjudication and AdaptaBrasil mapping are pending.

## At a glance

The collection provides national direction and sector-level policy detail. It does not demonstrate implementation by a state or municipality.

| Measure | Result |
| --- | ---: |
| Canonical documents | 10 |
| Official English companion | 1 |
| Canonical PDF pages | 897 |
| Pages including the companion | 1,008 |
| Extracted document records | 553 |
| Included sector-plan targets | 107 |
| Included sector-plan actions | 370 |
| Schema errors | 0 |

The 553 total is a document-record count, not a count of distinct policies. The Strategy and executive summary both publish the same twelve national targets.

The human-review CSV places Portuguese and English descriptive columns next to each other. Portuguese remains the evidence source except for the English-language NDC. English translation is a required review phase: a record is not ready for English-language review while any non-empty Portuguese descriptive value lacks its English companion.

The 2026 review table is English-complete. It uses official companion wording for twelve Strategy targets, original English for four NDC records, and local machine translation for the remaining Portuguese records. Machine-translated wording supports meaning review but is not official English and should not be quoted as publisher text.

## Scope and use

The analytical scope is adaptation. The extraction preserves source objectives, targets, actions, deadlines, resources, institutions, indicators, and page evidence. AdaptaBrasil is the only planned external classification; TEF, mitigation, GPC, and general climate-action mappings are out of scope.

The selected seven sectoral and thematic plans cover biodiversity, cities, energy, water resources, disaster risk, health, and food and nutrition security. The official framework contains sixteen plans, so this collection is not complete.

National policy relevance does not establish local adoption, funding, implementation, or results. Any later city-level analysis must keep the source level explicit.

## Canonical sources

MMA is the authoritative source for the Climate Plan documents. UNFCCC is the authoritative source for the NDC.

| Document | Canonical source |
| --- | --- |
| Brazil's Second Nationally Determined Contribution | [UNFCCC PDF](https://unfccc.int/sites/default/files/2024-11/Brazil_Second%20Nationally%20Determined%20Contribution%20(NDC)_November2024.pdf) |
| Climate Plan 2024–2035 | [MMA executive summary](https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/sumario-executivo-plano-clima.pdf) |
| National Adaptation Strategy | [Portuguese strategy](https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/estrategia-nacional-de-adaptacao.pdf); [English companion](https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/climate-adaptation-plan-national-adaptation-strategy.pdf) |
| Biodiversity | [MMA plan](https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/plano-tematico-biodiversidade.pdf) |
| Cities | [MMA plan](https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-cidades.pdf) |
| Energy | [MMA plan](https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-energia.pdf) |
| Water resources | [MMA plan](https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planotematico-recursos-hidricos.pdf) |
| Disaster risk | [MMA plan](https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-reducao-gestao-riscos-desastres.pdf) |
| Health | [MMA plan](https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-saude.pdf) |
| Food and nutrition security | [MMA plan](https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima/planosetorial-seguranca-alimentar-nutricional.pdf) |

## License

Nine MMA documents permit partial or complete reproduction for non-profit purposes when the ministries or source URL are cited [verified]. The NDC PDF and UNFCCC record do not state a reuse licence [unanswered]. The collection therefore has no single verified licence, and modified redistribution of the NDC must not be assumed to be permitted.

## Extraction coverage

The extraction follows each document's native structure. Sector plans use objective–target–action records; the Strategy adds guidelines and national objectives; the NDC uses narrative records because it has no native `O/M/A` identifiers.

| Document | Objectives | Targets | Actions | Other | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Cities | 3 | 8 | 19 | 0 | 30 |
| Biodiversity | 3 | 6 | 31 | 0 | 40 |
| Energy | 3 | 16 | 38 | 0 | 57 |
| Water resources | 3 | 6 | 40 | 0 | 49 |
| Disaster risk | 3 | 10 | 89 | 0 | 102 |
| Health | 4 | 27 | 93 | 0 | 124 |
| Food and nutrition security | 5 | 34 | 60 | 0 | 99 |
| National Adaptation Strategy | 10 | 12 | 0 | 14 | 36 |
| NDC | 0 | 0 | 2 | 2 | 4 |
| Climate Plan executive summary | 0 | 12 | 0 | 0 | 12 |

The seven included sector plans contain 107 targets and 370 actions. The Strategy reports 312 targets and 810 actions across the full sixteen-plan framework, so the extracted subset must not be presented as national completeness.

## Interpretation warnings

These rules are the minimum needed for safe downstream use.

| Issue | Downstream rule |
| --- | --- |
| Policy versus implementation | Treat records as commitments, not evidence of funding, delivery, or results. |
| Resources | Preserve the source text. Programme names, possible funds, and sources still to be defined are not equivalent to committed budgets. |
| Duplicate national targets | Deduplicate the Strategy and executive summary by instrument and native target number. |
| Strategy hierarchy | Do not assign the twelve national targets to individual national objectives; the Strategy provides no explicit crosswalk [verified]. |
| English companion | Use English for analysis only. Portuguese remains the evidence source, and alignment uses identifiers and content rather than page number. |
| AdaptaBrasil | Action `A3.M5` in the Biodiversity plan names AdaptaBrasil/MCTI [verified], but this does not provide a sector mapping for every record or prove implementation. |
| Cities indicators | The plan states 23 indicators, while its monitoring cells contain 31 separately punctuated statements [verified]. Retain the discrepancy. |
| Monitoring cells | In five plans, preserve the complete cell rather than inferring a formal sub-indicator count from punctuation. |
| Human review | Records are source-grounded and schema-valid, but not yet fully adjudicated against rendered pages. |

## Parsing notes

The PDFs are born-digital and do not require OCR [verified]. Their main risk is layout, not missing text.

| Hazard | Handling |
| --- | --- |
| Merged target cells | Inherit a target only within the same visible table block. |
| Repeated continuation targets | Reconcile by native identifier instead of emitting duplicates. |
| Multi-page action | Energy action `A2.M10` remains one record with a two-page evidence range. |
| Irregular identifiers | Normalize spacing and punctuation to forms such as `A4.M1`; retain source text and page evidence. |
| Narrow-column hyphenation | Join verified visual word breaks while preserving genuine compounds such as `áreas-chave` and `pós-eventos`. |
| Objectives outside table grids | Recover headings from visible page text, then parse targets and actions from the table. |
| Diagram-like tables | Require recognized policy headers and identifiers. The Climate Plan diagram negative control emits zero records. |
| Page labels | Store the one-based physical PDF page; printed page labels may differ. |

## Current release

Release 2026 is a research release. No production-approved release is registered.

### References

- Methodology and testing brief → `releases/2026/external-testing-pack/methodology-and-testing-brief.md`
- Release contract → `releases/2026/review.md`
- Extraction notebook → `releases/2026/policy_extraction.ipynb`
- Record schema → `releases/2026/schemas/policy_record.schema.json`
- Complete bilingual review table → `releases/2026/data/policy_records_combined.csv`
- Source inventory → `releases/2026/data/policy_documents.csv`
- Preserved PDFs → `releases/2026/data/raw/`
