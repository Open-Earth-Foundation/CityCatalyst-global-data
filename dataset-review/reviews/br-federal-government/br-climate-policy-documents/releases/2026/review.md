# Review — Brazil national climate policy documents, release 2026

## Status

All ten canonical documents have validated adaptation extraction outputs. The release remains research-only because human adjudication, AdaptaBrasil mapping, cross-document deduplication, and production approval are pending.

| Measure | Result |
| --- | ---: |
| Canonical documents | 10 |
| Official companion editions | 1 |
| Extracted document records | 553 |
| Included sector-plan targets | 107 |
| Included sector-plan actions | 370 |
| Schema errors | 0 |

The source inventory and PDF structure are verified. Record wording is source-grounded and page-bound, but the full corpus has not been visually adjudicated record by record.

## Supported claims

The release supports a limited set of claims with explicit conditions.

| Claim | Condition |
| --- | --- |
| The selected corpus contains the NDC, Climate Plan executive summary, National Adaptation Strategy, and seven named sectoral or thematic plans. | This is an inventory claim, not national completeness. |
| The seven included plans contain 107 targets and 370 actions. | These are source-defined records in the selected subset. |
| The documents provide federal adaptation direction for biodiversity, cities, energy, water, disaster risk, health, and food security. | Direction does not prove local adoption or implementation. |
| Every canonical document has a reproducible adaptation extraction output. | Records are schema-valid and retain source pages. |
| Biodiversity action `A3.M5` names AdaptaBrasil/MCTI. | This shows an intended operational relationship, not completed implementation or a corpus-wide mapping. |

## Unsupported claims

The release does not support stronger conclusions about completeness, delivery, or comparative performance.

| Unsupported claim | Reason |
| --- | --- |
| These are all documents in Brazil's Climate Plan. | Nine adaptation plans and other cross-cutting instruments are outside the selected scope. |
| A municipality adopted or implemented an action because a federal plan mentions it. | National direction and local implementation are different evidence levels. |
| A named programme or fund is a committed budget. | Resource cells mix programmes, possible sources, and funding still to be defined. |
| One sector has stronger policy than another because it has more records. | Document purpose, granularity, and table design differ. |
| The 553 records are distinct policies. | The Strategy and executive summary repeat twelve national targets. |
| The Strategy assigns every national target to an objective. | No explicit target-to-objective crosswalk is published [verified]. |
| All monitoring-cell statements are formal indicators. | Several cells contain multiple statements whose publisher-defined grouping is unclear. |
| The extraction is production-ready. | Human adjudication and mapping remain pending. |

## Downstream rules

Safe use requires preserving evidence and uncertainty.

| Rule | Required handling |
| --- | --- |
| Source authority | Use Portuguese MMA documents as evidence; use the English Strategy only for analysis. |
| Traceability | Retain document, native identifier, source wording, and physical PDF page. |
| Duplicate targets | Deduplicate Strategy and executive-summary targets by instrument and native number. |
| Multi-objective targets | Do not force a single parent when several objectives are printed. |
| Resources | Keep source wording and distinguish named programmes from confirmed funding. |
| Monitoring | Preserve complete cells unless a formal indicator split is source-defined. |
| Implementation | Do not infer funded, initiated, completed, or monitored status. |
| Mapping | Keep AdaptaBrasil classification separate from source extraction and retain unmapped records. |

## Known issues

The remaining risks are explicit and reviewable.

| Issue | Current handling |
| --- | --- |
| Cities states 23 indicators, while 31 statements are visibly punctuated. | Preserve all statements and the discrepancy. |
| Energy action `A2.M10` spans two pages. | Join fragments in page order and retain the page range. |
| Narrow table columns break Portuguese words. | Apply controlled dehyphenation and preserve verified compounds. |
| NDC has no native adaptation identifiers. | Use four bounded narrative records; do not treat them as a sector action inventory. |
| Full visual adjudication is incomplete. | Keep `review_status: proposed` until reviewed against rendered pages. |
| NDC reuse licence is unstated. | Treat licence as unanswered; do not assume modified redistribution is permitted. |

## Traceability

The ten canonical PDFs total 897 pages. The official English Strategy companion raises the preserved total to 1,008 pages. MMA documents permit non-profit reproduction with source attribution [verified]; the NDC licence remains unanswered.

Official servers returned access-control pages during automated retrieval, so valid PDF bytes were obtained from exact Climate Policy Radar mirrors while official publisher URLs remain the canonical provenance. The incorrect news-article PDF initially retrieved for the Climate Plan record was replaced with the official 91-page executive summary.

### References

- Review overview → `../../README.md`
- Source inventory → `data/policy_documents.csv`
- Preserved PDFs → `data/raw/`
- Extraction notebook → `policy_extraction.ipynb`
- Record schema → `schemas/policy_record.schema.json`
- MMA publication collection → https://www.gov.br/mma/pt-br/centrais-de-conteudo/publicacoes/mudanca-do-clima
- UNFCCC NDC → https://unfccc.int/sites/default/files/2024-11/Brazil_Second%20Nationally%20Determined%20Contribution%20(NDC)_November2024.pdf
