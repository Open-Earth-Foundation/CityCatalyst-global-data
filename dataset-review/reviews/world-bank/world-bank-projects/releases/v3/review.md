# Review — World Bank Brazil adaptation-screened projects, release v3

## Scope and status

This research release contains 55 Brazil project records selected from 566 official World Bank Projects API records retrieved on 2026-09-25. It provides a cleaned English-column project table, one paired Portuguese title field where Portuguese source text exists, a restartable build and notebook, and a complete draft action crosswalk. It is **not production-approved**.

## Source and license evidence

**[verified]** The official World Bank Data Catalog describes Projects & Operations as basic information on World Bank lending projects from 1947 onward and identifies project as the dataset granularity. The catalog classifies the dataset Public and labels it Creative Commons Attribution 4.0.

**[verified]** The World Bank public-licenses page states that CC BY 4.0 permits copying, modification and distribution for any purpose, including commercial use, with attribution and indication of changes and translations. It adds mandatory World Bank dispute-resolution terms: non-binding mediation followed, if unresolved and elected, by arbitration under the stated rules. This release records both CC BY 4.0 and those additional terms.

**[verified]** The build uses the official endpoint `https://search.worldbank.org/api/v2/projects` with `countrycode=BR`. It retains the full Brazil response and the query responses used for the screen. Raw evidence is ignored by repository rules but present in the release workspace.

## Selection method

**[verified]** The full Brazil response contains 566 unique project identifiers. The release includes records whose project title explicitly names adaptation, climate/resilience, flood, drought, disaster, landslide, early warning, water security, drainage, forest fire or climate-smart activity, or that occur in at least two of seven official full-text query result sets: adaptation, climate resilience, disaster risk, flood, drought, landslide and early warning.

**[inferred]** A repeated full-text hit is a defensible research lead because it is reproducible through the official API. It is not necessarily visible in the project-level fields and may reflect associated document text. Accordingly, records selected only through query overlap are not asserted to be adaptation projects.

**[unanswered]** The Projects API does not expose the text fragment responsible for a full-text match. Project documents must be reviewed before non-title candidates receive a substantive adaptation classification.

## Cleaned output

The cleaned table has 55 rows and 43 columns, with 55 distinct non-null `project_id` values. Lifecycle distribution is 22 Active, 26 Closed, 5 Pipeline and 2 Dropped. The derived `has_board_approval_evidence` flag is true only for 47 Active/Closed records that also have a published Board approval date; one old Closed record lacks that date and remains false rather than its approval history being inferred.

The sum of `total_commitment_amount_usd` across all 55 candidates is USD 8,679,030,000. This is a mechanical validation total only. It mixes lifecycle states and is **not an adaptation-finance total, disbursement total, or delivered-investment total**.

The API project slice has no disbursement field. `has_disbursement_data` is therefore false for every row, `adaptation_finance_amount_usd` is blank, and `adaptation_finance_amount_status` warns against inferring it from total commitment. Board approval, implementation status, recorded/planned closing, project commitments and disbursements remain separate concepts.

## Language handling

The API returned 54 included project titles in English and one in Portuguese. `P170682`, “Linha de Crédito para Resiliência Urbana no Sul do Brasil,” is retained in `project_name_pt` and translated as “Urban Resilience Credit Line in Southern Brazil” in `project_name`, with explicit translation status. No `_pt` value is invented for English source records. Legal entity names are kept as source identifiers and explicitly labelled `source_legal_names_not_translated`. Apparent replacement-character encoding in some agency names is retained and noted as a source/API quality issue.

## Adaptation-action mapping

Nine projects receive a draft action link and 46 retain an explicit none result. The nine links comprise two direct title matches and seven component relationships:

- early-warning/forest-fire warning title → `icare_0183`;
- climate-smart agriculture title → `ipcc_0096`;
- flood prevention/reduction title → possible drainage component `c40_0048`;
- water-security title → possible resilient water/sanitation component `ipcc_0101`;
- resilient-road title → public-infrastructure component `ipcc_0087`.

**[inferred]** These are semantic links from project titles to an action bank, not claims that the action was financed at the full project value or implemented. All nine links are medium confidence and pending human adjudication. No amounts are allocated.

## Validation results

- Full Brazil source: 566 records and 566 unique IDs.
- Cleaned release: 55 rows, 55 unique IDs, no missing IDs.
- Lifecycle counts: Active 22; Closed 26; Pipeline 5; Dropped 2.
- Board-approved derivation: 47 true; 8 false.
- Translation status: 54 source-English; 1 human translation with non-empty `_pt` source.
- Crosswalk: 55 rows, exactly one per released project; 9 mapped and 46 none.
- Action resolution: every non-empty action identifier resolves in the held adaptation action bank.
- Amount allocation: 0 mappings have an allocated amount.
- Cleaned commitment checksum total: USD 8,679,030,000.
- Repeat build from retained evidence reproduces the row counts, status counts and mapping counts.

SHA-256 evidence checksums:

- `world_bank_projects_brazil_api.json`: `147a966f6d631f33d91576c40521e68831af41e956db712e636b87f11752e66d`
- `query_adaptation.json`: `d2d735a63b4f49b14d3f0106396c6f505ebdc4022deb25b06977832fe9b8ebca`
- `query_climate_resilience.json`: `6074e07acc89ce3e787490720c519f72f652da639e07fd7305b463fe96065b17`
- `query_disaster_risk.json`: `8d64ea056c717a4e498ff4a9bf8e10d0e6228b8e0694721fd949a32fabeb54af`
- `query_flood.json`: `8cad16f16d437b185bff87dceb241771dd85f887ed75e69aff524a88d5f56b60`
- `query_drought.json`: `530f0e0c52f2a59a955a9ba236428df7f68e23196945d69fc85fe854150dcc69`
- `query_landslide.json`: `e5cbfad5eab68e975b0456f44cc3cc505d746d7202f2110f6ed91526e86f17eb`
- `query_early_warning.json`: `8f089eff02c1324d92f02efd9383eaf7125dc76694cc3c81124d9dc2735afff4`

The locally retained exploratory `drainage` and `water security` responses are not used by the final multiple-query criterion.

## What this data supports

The release supports statements that the World Bank published the named Brazil project, lifecycle status, approval/closing metadata, commitment and sector/theme fields on the retrieval date. It supports finding adaptation-relevant project candidates and routing users to the official project profile and documents.

## What this data does not support

It does not support treating USD 8.679 billion, or any whole project commitment, as adaptation finance. It does not report disbursement, expenditure, component-level amounts, implementation progress or benefits to a particular city. A Closed status does not prove every activity was delivered; an Active status does not quantify execution; Pipeline and Dropped records must not be treated as approved finance.

## Decision and blockers

Decision: keep as a non-production research release pending human adjudication and document review.

Before production consideration: review associated project documents for the 55 candidates; replace the full-text screen with an official climate/adaptation tagging field if one becomes available; resolve API encoding defects; confirm date semantics against source documentation; adjudicate the nine mappings; and decide whether raw API evidence should be explicitly force-added or stored in an approved archival location. The locally held action bank is also a review input, not independently licensed by this release.
