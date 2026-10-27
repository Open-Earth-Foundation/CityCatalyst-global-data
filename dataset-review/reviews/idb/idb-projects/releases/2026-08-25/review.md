# Review — IDB Projects Dataset, Brazil adaptation release 2026-08-25

## Scope and status

This is a research release, not production-approved. It screens the 1,750 Brazil operations returned by the IDB Projects Dataset API into 63 adaptation or disaster-risk candidates and preserves their lifecycle status. The cleaned table has English source text, English column names and an explicit `source_english_no_portuguese_fields` translation status; the reviewed resource contains no Portuguese fields to pair as `_pt`. A separate crosswalk links only project text with action-level evidence and leaves unsupported projects explicitly unmapped.

### References

- Cleaned projects: `data/idb_brazil_adaptation_projects.csv`
- Extraction notebook: `idb_brazil_adaptation_extract.ipynb`
- Adaptation crosswalk: `data/idb_brazil_adaptation_projects_to_actions.csv`
- Mapping notebook: `idb_brazil_adaptation_mapping.ipynb`
- Reproducible builder: `build_brazil_adaptation_release.py`

## Visual summary

The candidate portfolio is split almost evenly between implementation (29) and closed operations (28), with four in preparation and two cancelled. Technical cooperation dominates the count (38 of 63), while a small number of large loan and container records dominate the amount. Environment and natural disasters and water and sanitation together account for 33 of the 63 candidates. Run the extraction notebook for the lifecycle charts.

| Public status | Operations | Original amount | Median operation |
|---|---:|---:|---:|
| Implementation | 29 | US$3.321 billion | US$1.60 million |
| Closed | 28 | US$699.873 million | US$261,500 |
| Preparation | 4 | US$303.875 million | US$30.30 million |
| Cancelled | 2 | US$35.250 million | US$17.63 million |

The table reports full operation envelopes exactly as the source provides them. It is not an adaptation-finance total.

## What this data supports

The release supports claims about identifiable IDB operations and the finance routes they demonstrate. Its load-bearing limitation is that an operation can be broader than adaptation and its amount is not an adaptation allocation.

"The IDB Projects Dataset contained 63 Brazil operations with explicit climate-adaptation, resilience, disaster-risk or hazard evidence in the reviewed 25 August 2026 resource." This is a reproducible analytical screen, not an official IDB portfolio count.

"IDB has used loans and technical cooperation for Brazil operations involving urban drainage, disaster response, resilient water systems, rural adaptation, climate-risk insurance and climate governance." This is supported at route level by project objectives and instrument fields.

"Project BR-X was in implementation, closed, preparation or cancelled status in the reviewed resource." The status and retrieval date must remain attached because the source is live.

"Project BR-X had an original IDB amount of US$Y." This is valid when the claim says original operation amount and does not call it disbursed, spent, received by a city or attributable wholly to adaptation.

## Mapping to adaptation actions

The mapping reaches 36 of 63 projects and 13 of the 37 action-bank entries. Twenty-seven projects retain `none` rows because climate relevance does not identify a concrete action. The 51 proposed links are 13 direct, 29 component and 9 related links, all medium confidence and pending human adjudication.

| Judgment cluster | Downstream rule |
|---|---|
| Drainage and flood-control works | Direct only when the objective or title names drainage, macrodrainage, DRENURBS or flood control |
| Early warning | Component when the objective explicitly names early-warning capacity |
| Emergency and humanitarian support | Related to preparedness planning, never treated as proof that a plan was developed |
| Rural and agricultural resilience | Component only when agriculture, farmers or productive value chains are explicitly connected to adaptation or resilience |
| Resilient water or public infrastructure | Component because the wider operation includes non-adaptation activities |
| Climate governance and finance | Component when the operation strengthens planning, mainstreaming or adaptation-finance capacity |

No amount is apportioned to an action. A project with several links keeps one undivided source amount, so mapped rows cannot be summed.

## What this data does not support

The main overclaim is converting a screened operation envelope into delivered adaptation finance.

"IDB invested US$4.36 billion in Brazilian adaptation projects." No: US$4.36 billion is the sum of whole original envelopes across all four lifecycle statuses, including preparation and cancelled records, without an adaptation share.

"Brazilian cities received US$Y from these operations." No: the dataset has no structured recipient, municipality allocation or disbursement field. A city name in a title does not establish the final beneficiary or amount received.

"IDB completed 28 adaptation projects." No: `Closed` is an operation lifecycle status, not proof that every planned activity or adaptation result was delivered.

"The four preparation operations are approved finance." No: they have no approval date and show the publisher's preparation stage, even when an amount field is populated.

"Every mapped operation financed every linked adaptation action." No: component and related mappings identify plausible project-level relationships; they do not classify each expenditure or beneficiary.

"Environmental classification measures adaptation benefit." No: it describes potential negative environmental and social impacts.

## Using it downstream

Keep the stable `project_id` as the operation key and retain lifecycle status in every aggregate. Use `Implementation` and `Closed` only for statements that require an approved operation; keep preparation and cancelled rows for route discovery but exclude them from approved-portfolio sums.

Treat technical cooperation, loans, grant products and containers separately. Similar project names can represent support operations and financing operations for the same programme. They should be linked through document research rather than collapsed automatically.

Use the crosswalk as a discovery index after adjudication. Join action IDs back to unique projects, never sum the fanned-out mapping rows, and label all amounts as whole operation envelopes.

The correct next join is to IDB project documents using `project_id`. Those documents are needed to establish implementing entities, subnational geography, components, adaptation shares, approval conditions and delivery evidence.

## Benchmark values a city can use

The figures below describe operation envelopes for the 57 screened records in implementation or closed status. They are comparator priors for navigating IDB instruments, not promises of city funding or typical adaptation component costs.

| Comparator | Value |
|---|---:|
| Median original operation amount | US$800,000 |
| Interquartile range | US$223,000–58.223 million |
| Full range | US$9,000–2.000 billion |
| Total whole-operation envelope | US$4.021 billion |

The distribution spans small technical cooperation and very large financing envelopes, so the overall median should not be used to size a loan. For replication, the more useful precedent is the instrument route and project document: technical cooperation can prepare capacity, studies or designs, while loans and containers carry much larger programme envelopes.

For generalisation, the dataset shows repeated routes for urban drainage, resilient sanitation, rural adaptation, disaster response and climate governance. A city can use those records to locate comparable operation designs and responsible national or state counterparts, then read the linked project documents before estimating a finance request.

## Notes on non-obvious fields

- `public_status`: publisher lifecycle label; `Closed` does not certify outcome delivery, and `Preparation` is not approval.
- `original_approved_amount_usd`: whole original IDB operation amount; preparation rows can still carry a value.
- `adaptation_screen_confidence`: strength of inclusion evidence in this analytical release, not an IDB quality score or adaptation percentage.
- `adaptation_screen_terms`: evidence family that triggered inclusion; several families may apply.
- `translation_status`: the English resource contained no Portuguese fields, so no `_pt` pairing was applicable.
- `environmental_classification_name`: potential adverse-impact classification, not adaptation relevance.

## Traceability

Source: Inter-American Development Bank, IDB Projects Dataset, DOI `10.60966/ihisavwe`, English resource `814b7b54-477a-4c25-b3bf-6be05412069d`, retrieved 24 September 2026 under CC BY 4.0. The retained API response has SHA-256 `85573a16161be62e49784a50c85a2560c53b9a5ea92f4d8a66c709ebcaa4dcc8` and declares 1,750 Brazil records. The builder asserts the hash, raw shape, 63-row screen, unique IDs, lifecycle counts, language status, non-negative amounts and mapping coverage before export.

The action mapping uses the local V13 ICB × OEF action-bank export, which is not committed here. Thirty-six projects map to 13 actions, 27 retain none rows, and all 51 proposed links remain pending human adjudication. The notebooks are restartable, but their output cells are unexecuted because the available environment lacks Jupyter and matplotlib; the underlying builder and non-visual mapping logic were executed directly.

### References

- Review README: `../../README.md`
- Raw API response (local only): `sample/idb_projects_brazil_api.json`
- Action bank (local only): `dataset-review/reviews/br-bndes/br-bndes-operacoes-financiamento/releases/2026-09-01/sample/adaptation_action_bank_icb_oef_v13.csv`
