# Inter-American Development Bank — Projects Dataset

The IDB Projects Dataset is the Bank's operation-level register for projects and programmes in preparation or approved across its borrowing member countries. This review now has a Brazil/adaptation research release based on the English API resource modified 25 August 2026, alongside the earlier Chile/mitigation `v1` release. **Status: the Brazil source, screen, cleaned table, extraction notebook, conservative adaptation mapping and release review are complete as a draft. Human adjudication of mapping rows and production engineering remain outstanding; nothing is production-approved.**

## Canonical downloads

The canonical dataset page and DOI identify the current Projects Dataset, published 22 October 2025 and modified 25 August 2026 **(verified)**. The page offers separate English and Spanish CSV resources. The release uses the English DataStore resource because its fields and descriptive values are English and the API supports an exact `cntry_cd=BR` filter **(verified)**.

The API returned 1,750 Brazil records on 24 September 2026. The response is retained locally with SHA-256 `85573a16161be62e49784a50c85a2560c53b9a5ea92f4d8a66c709ebcaa4dcc8` **(verified)**. The resource changes in place, so the retrieval date, response hash and publisher modification date together define this review release **(inferred handling rule)**.

Re-download the reviewed input with:

```bash
curl --fail --silent --show-error --max-time 60 --output releases/2026-08-25/sample/idb_projects_brazil_api.json 'https://data.iadb.org/api/action/datastore_search?resource_id=814b7b54-477a-4c25-b3bf-6be05412069d&limit=2000&filters=%7B%22cntry_cd%22%3A%22BR%22%7D'
```

### References

- Canonical dataset page: https://data.iadb.org/dataset/idb-projects-dataset
- DOI: https://doi.org/10.60966/ihisavwe
- DataStore API: https://data.iadb.org/api/action/datastore_search
- English resource identifier: `814b7b54-477a-4c25-b3bf-6be05412069d`
- Reviewed raw response: `releases/2026-08-25/sample/idb_projects_brazil_api.json`

## Why we use it

This is operation-level evidence that IDB routes have financed or prepared climate adaptation, resilient infrastructure and disaster-risk work in Brazil. It supplies stable project identifiers, lifecycle status, objectives, sectors, instruments and original financial envelopes. These fields make it useful for identifying precedent and following an operation into its project documents.

It is not a city-finance transaction table. The resource has no structured recipient municipality, implementing entity, component budget, disbursement or adaptation-finance share. City relevance must be established from project documents or explicit place names in the title and objective, not inferred from the Brazil country code.

### References

- Finance-pathways need: `dataset-discovery/needs/2026-09-br-finance-pathways-review/`
- Brazil release: `releases/2026-08-25/`

## License

The dataset page states Creative Commons Attribution 4.0 International (CC BY 4.0) **(verified)**. Redistribution and adaptation are allowed, including commercially, provided appropriate credit, a licence link and an indication of changes are supplied. No share-alike or no-derivatives condition applies **(verified from the named licence)**.

Use the publisher's citation: `Inter-American Development Bank (2026). IDB Projects Dataset. IDB Open Data. https://doi.org/10.60966/ihisavwe`. For the cleaned derivative, add: `Brazil adaptation screen and English field renaming by Open Earth Foundation; source retrieved 24 September 2026; not endorsed by IDB.`

### References

- Dataset licence and citation: https://data.iadb.org/dataset/idb-projects-dataset
- CC BY 4.0 legal code: https://creativecommons.org/licenses/by/4.0/legalcode

## Data profile

The API response contains 1,750 Brazil operations and 29 source fields **(verified)**. It spans 1961–2026, although 38 preparation records in the full source lack an approval date. Project IDs are unique in the Brazil slice. All project names, objectives and classifications in the reviewed resource are English; no Portuguese source-text fields are present **(verified)**.

The release screen retains 63 candidate adaptation or disaster-risk operations. Thirty-three have explicit climate adaptation/resilience wording or the dedicated climate-adaptation subsector, and 30 rely on explicit hazard/risk-reduction evidence or a disaster/urban-drainage subsector **(verified by builder assertions)**.

| Public lifecycle status | Operations | Original amount |
|---|---:|---:|
| Implementation | 29 | US$3.321 billion |
| Closed | 28 | US$699.873 million |
| Preparation | 4 | US$303.875 million |
| Cancelled | 2 | US$35.250 million |

These amounts are complete as source values but not additive as adaptation finance. The screen selects whole operations, not climate components, and the preparation and cancelled rows are not approved active awards. One `Container` record is also a financing envelope that can relate to later operations, so adding it to child operations can double-count **(verified operation types; inferred aggregation consequence)**.

The 63 candidates comprise 38 technical cooperations, 23 loan operations, one grant-financing product and one container. Environment and natural disasters (19), water and sanitation (14), urban development and housing (7), agriculture and rural development (6), financial markets (5) and transport (4) dominate the screen **(verified)**.

## Spatial and temporal scope

All output rows have `country_code=BR`. The selected approval dates run from 31 May 1985 to 17 September 2026, and four preparation records have no approval date **(verified)**. A project can be federal, state, municipal, regional or private-sector; the API does not provide a structured subnational geography or recipient. Place names in titles are useful search evidence, not a complete spatial field.

The source is a live administrative register. `Preparation` means the operation is not yet shown as approved; `Implementation` and `Closed` establish an approved operation but do not show money disbursed or work completed; `Cancelled` must remain visible and must not be counted as delivered finance **(verified status values; inferred downstream rules)**.

## Adaptation screen

The release is a reproducible candidate screen, not an official IDB climate-finance classification. A record is retained when the title, objective or subsector contains one of three evidence families: a dedicated adaptation/disaster/urban-drainage subsector; explicit climate adaptation, resilience, risk or vulnerability language; or explicit flood, landslide, drought, early-warning, stormwater, drainage, erosion-control or resilient-reconstruction language.

The screen deliberately excludes `BR-G1006`. Its objective mentions adaptation only inside the name of a general IDB strategy, while the intervention itself is low-carbon mobility. This named exception prevents a mitigation operation from becoming adaptation evidence **(verified text; analytical decision)**.

Thirty-three `high` rows have explicit climate wording or the dedicated climate-adaptation subsector. Thirty `medium` rows have hazard/disaster evidence without explicit climate language. Confidence describes the screen evidence, not project quality, delivery or the share of finance attributable to adaptation.

## Adaptation-action mapping

The project-to-action crosswalk is intentionally narrower than the screen. Rules read project names and objectives, not broad subsector labels, and every screened project appears. Thirty-six of 63 projects link to 13 of the 37 action-bank entries; 27 retain an explicit `none` row because the text does not identify a concrete city action **(verified)**.

The 51 judgment links are 13 direct, 29 component and 9 related links. All carry medium confidence and await human adjudication. Emergency and humanitarian operations are only `related` to an extreme-weather preparedness plan because cash or relief after an event does not prove that a plan was developed. No project amount is split or attached to a mapped action.

The action-bank export is a local-only input held in the BNDES review's ignored `sample/` directory. The mapping may retain stable action IDs, but the target descriptions cannot be treated as publisher content or redistributed independently until their own licensing is resolved.

### References

- Mapping notebook: `releases/2026-08-25/idb_brazil_adaptation_mapping.ipynb`
- Crosswalk: `releases/2026-08-25/data/idb_brazil_adaptation_projects_to_actions.csv`
- Local action-bank input: `dataset-review/reviews/br-bndes/br-bndes-operacoes-financiamento/releases/2026-09-01/sample/adaptation_action_bank_icb_oef_v13.csv`

## Interpretation warnings

`original_approved_amount_usd` is the operation's original IDB-approved amount or, for preparation-stage records, a populated source envelope. It is not a disbursement, current balance, total adaptation cost or amount reaching a city. Local counterpart and total-cost fields are separate source measures and must not be added to the approved amount without defining the intended financial concept.

An operation is not an independent project count in every analytical sense. Technical cooperation can prepare or support a loan, a container can frame later operations, and multiple IDs can describe different instruments for the same programme. The API carries no relationship field, so deduplication by similar title would destroy valid instrument records while raw counting can overstate programme count.

Lifecycle status is load-bearing. Preparation and cancelled records demonstrate a proposed route but not approved finance; closed records demonstrate an operation existed but not that every component or planned result was delivered; implementation records do not indicate execution percentage.

The adaptation screen operates on project-level text. It cannot determine an adaptation percentage, and broad operations may contain both mitigation, adaptation and general development components. The cleaned amount column must never be summed and labelled "adaptation investment" without component-level financial evidence.

## Parsing notes

The DataStore response is JSON with a `result.records` array. All source fields arrive as strings except `_id`; dates include nanosecond-style time suffixes, and three financial fields are numeric strings. The builder keeps identifiers as text, converts valid dates to ISO `YYYY-MM-DD`, converts financial fields to numbers and preserves blanks as missing values.

Short source headers are renamed to English snake_case. This release uses the English resource, so there are no Portuguese values to pair into `_pt` columns. Every row carries `source_language=English` and `translation_status=source_english_no_portuguese_fields`; generating artificial Portuguese duplicates would misrepresent provenance.

The API's `total` and returned record count are both asserted as 1,750. The raw response hash is also asserted. Any publisher update therefore fails the release build until the new content is reviewed and versioned in a new release folder.

## Methodology

The Projects Dataset is an administrative inventory of operations in preparation or approved by IDB, not an impact-evaluation dataset **(verified from publisher description)**. It covers sovereign- and non-sovereign-guaranteed instruments including loans, guarantees, grants, technical cooperation and equity **(verified)**. The API provides no uncertainty measure because the values are administrative attributes rather than modeled estimates.

The original approved amount is useful for comparing operation scale only within a clearly defined lifecycle and instrument context. It does not measure delivery, beneficiary receipt, climate additionality or adaptation effectiveness. Environmental classification describes potential negative environmental and social impacts; it is not an adaptation-benefit score **(verified field meaning from labels; inferred consequence)**.

## Fit for purpose (proposed)

The proposed verdict is **conditional fit for finding Brazil adaptation-finance precedents and tracing them to IDB project documents; not fit for city-level awards, disbursements or adaptation-spend totals**. It passes source identity, stable project ID, objective, sector, instrument, lifecycle and original envelope needs. It fails structured municipality, recipient, transaction and adaptation-share needs. Human review should decide whether medium screen rows and mapping clusters are retained.

| Criterion | Result | Evidence |
|---|---|---|
| Brazil coverage | Pass | 1,750 API records with `cntry_cd=BR` |
| Stable project identifier | Pass | Unique `project_id` on all 63 screened rows |
| Project objective and classifications | Pass | English objective, sector, subsector and operation type |
| Lifecycle stage | Pass | Preparation, Implementation, Closed and Cancelled retained |
| Amount with meaning | Conditional | Original IDB amount in USD; not disbursement or adaptation share |
| City or recipient geography | Fail | Country only; place names are unstructured and incomplete |
| Disbursement/execution | Fail | No transaction or execution fields |
| Official adaptation classification | Conditional | Dedicated subsector on some rows; documented analytical screen on others |
| Adaptation-action mapping | Conditional | 36 projects linked, all medium and pending adjudication; 27 explicit none rows |
| Licence | Pass | CC BY 4.0 with attribution |

## Current approved release

No release is production-approved. The Brazil/adaptation working release is **2026-08-25**. The older **v1** Chile/mitigation release remains preserved and should not be used as evidence for Brazil.

### References

- Brazil extraction notebook: `releases/2026-08-25/idb_brazil_adaptation_extract.ipynb`
- Reproducible builder: `releases/2026-08-25/build_brazil_adaptation_release.py`
- Cleaned project table: `releases/2026-08-25/data/idb_brazil_adaptation_projects.csv`
- Release review: `releases/2026-08-25/review.md`
- Preserved Chile release: `releases/v1/`
