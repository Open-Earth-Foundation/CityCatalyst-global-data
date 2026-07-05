# Review — mn-greenstep-sustainability-index, release 2026-07

## Scope and status

This release turns the five thematic worksheet exports of the Minnesota Sustainability Index, retrieved 2026-07-05, into one tidy long documents table: 498 rows, one per community-document, keyed by a controlled `document_type`. It is research / exploratory: not yet catalog-registered and not in a pipeline, with license confirmation the one blocker to promotion (see the README). Dataset-level facts (provenance, license, encoding, parsing) live in the README one level up and are not repeated here; this document is the contract for what the table can and cannot say once joined to our other Minnesota work.

The release contains the documents table (498 rows across all 172 communities), the five source worksheets it was built from, and the extraction notebook that produced it. The long shape replaces the earlier wide one-column-per-artifact table: six columns (`community`, `type`, `document_type`, `document_label`, `document_year`, `document_url`) instead of twenty-two, with the familiar one-row-per-community presence matrix a single `pivot_table` away (notebook block 5). The reshape also carries two corrections to the earlier hand-built table: it fills `type` for 23 communities left blank though their type is present in the worksheets, and it keeps every signal the wide table folded away — formal commitments as one row per named commitment, and the green-team/commission bodies as one row each rather than a single collapsed flag.

References — Documents table: `data/mn_sustainability_index_documents_2026-07.csv`. Notebook: `mn_sustainability_index_extract_clean.ipynb`. Source worksheets: `data/*.csv`.

## Visual summary

The notebook's charts show a directory that is broad on inventories and thin on plans. A community-wide GHG inventory is the most common document by far (113 of 172 communities, and 112 of the 147 cities), because the Metropolitan Council's Twin Cities inventory and the Regional Indicators Initiative each supply many communities at once. Named plans are much rarer: 17 communities carry a Climate Action Plan, 44 an Energy Action Plan, 37 an adaptation or resiliency plan. The set is city-heavy (147 of the 172 communities are cities; the rest are counties, regions, tribal nations, townships, watershed districts, and the state), so any headline count must be filtered to `type == "City"` first. The Climate Action Plan year histogram clusters before the current wave of adoptions, which is the visible evidence for the recency-lag warning below. Run the notebook to see the rendered charts; the precise figures are in the tables here.

## What this data supports

The claims this release backs are all of the form "community X has an artifact of type Y on record, here is the link" — availability and pointers, never the contents or the numbers inside those artifacts. The load-bearing caveat sits on the word "on record": the Index is voluntarily and periodically reported, so a claim is only ever about what has been logged.

"Of Minnesota communities that report to GreenStep, 113 have a community-wide GHG inventory with a link to it, including 112 of the 147 cities" is supported directly by the `ghg_inventory` rows. Read it as an inventory-availability directory, the companion to the Regional Indicators Initiative which holds the inventory values.

"City X has a Climate Action Plan on record, adopted in year Y" is supported by a `document_type == "climate_action_plan"` row for that city, with the year and link in `document_year` and `document_url`. This holds for 13 cities. The same pattern supports Energy Action Plans (40 cities), adaptation/resiliency plans (23 cities), GHG reduction goals (30 cities), and vulnerable-population assessments (21 cities).

"These eight cities carry the full CAP + GHG-inventory + vulnerability-assessment set the CNB seeds a cohort city from" is supported and enumerable: Albert Lea, Burnsville, Duluth, Edina, Minneapolis, Minnetonka, Saint Louis Park, and Saint Paul. This is the concrete cohort-seeding shortlist the originating need asked for.

## What this data does not support

The overclaim to watch for is treating the directory as the data, or treating a blank cell as a confirmed "no". Both turn an availability index into false factual claims.

"City X emitted N tonnes of CO2e" is not supported: the GHG worksheet records that a community has an inventory and links to it, not the emissions values. For numbers, follow the link or use the Regional Indicators Initiative.

"City X has no Climate Action Plan" is not supported by the absence of a `climate_action_plan` row. Absence means "not logged in this voluntary directory", not confirmed absence, and the Index is known to trail current documents. It logs Minneapolis's CAP as 2013 rather than the 2023 Climate Equity Plan, shows no CAP for Mankato (adopted 2025) or Rochester (2021 work plan), so a missing row or a stale year is a floor on what exists, not a ceiling.

"44 communities have an Energy Action Plan, exactly" overstates the precision: 44 have a named-plan row, but Minneapolis carries an Energy plan URL and 1996 year with no named plan, so an any-field count is 45. The table ships the flag-based 44; quote it as "about 44" or state the definition.

"There are 172 Minnesota cities with climate plans" misreads the counts: the table spans 172 communities of all types, only 147 of which are cities, and most carry documents other than plans. An unfiltered statistic also double-counts a metro as its city, its county, its region, and the Met Council.

## Using it downstream

Filter to `type == "City"` before any city-level statistic, and treat every row as availability, not attainment. For a one-row-per-community view, pivot on `document_type` (notebook block 5) — the long shape is the source of truth, the wide matrix a derived convenience. Join to our other Minnesota datasets by `community` name, since the Index carries no locode or other code, and budget for name-hygiene (spelling, "City of" prefixes, saint/st. variants) on the join.

Pair it with the Regional Indicators Initiative for inventory values, using this Index to know which communities have an inventory and RII for the numbers. For cohort selection, the CAP + inventory + vulnerability trio above is the ready shortlist; widen it with the `mn-greenstep-actions` sibling (what a community has implemented) and the `mn-climate-awards` funding footprint when a broader cohort is needed. When currency matters, cross-check the city's own site or the 100% Campaign's November-2025 LCAPS report, because this Index trails the newest plans.

## Notes on non-obvious fields

A row means the document is logged, never that it is the community's only one or a confirmed complete picture; the absence of a row means "not logged here", never a confirmed "the community has none". Presence is defined as a non-blank source cell.

`document_type` is a controlled vocabulary of fourteen values. Most are one-per-community (a community has at most one `climate_action_plan` row), with two intentional exceptions: `formal_commitment` repeats, one row per named commitment a community holds (91 rows across 60 communities), and the green-team/commission bodies are five separate types — `environmental_sustainability_commission` (40), `equity_human_rights_commission` (30), `green_team_community_led` (6), `green_team_internal_staff` (25), `green_team_joint` (14). The earlier wide table's single `green_team_or_commission` count (74) is now a group-by over the first four (the equity/human-rights commission was, and still is, kept separate).

`document_label` carries the source-side name only where the worksheet gives one: the GHG-inventory provider (e.g. "Twin Cities GHG Inventory", "RII") and the formal-commitment name. It is blank for plans and assessments, which the worksheets label only by column.

`document_year` is populated for the three dated types (`climate_action_plan`, `energy_action_plan`, `ghg_reduction_goal`) and null elsewhere. `energy_action_plan` has 44 rows by the named-plan flag; Minneapolis carries an energy URL and 1996 year with no named plan, so any-field coverage is 45 — the table ships the 44.

`type` distinguishes City, County, Region, State, Township, Tribal Nation, and Watershed. The `Region` set includes the Metropolitan Council. This value was blank for 23 communities in the earlier table and is repaired here so every row carries a type.

## Traceability

Inputs — the five worksheet exports in `data/` (Planning, GHG and Climate Mitigation, Vulnerability and Equity, Formal Commitments, Green Teams and Commissions), UTF-16 tab-separated, retrieved 2026-07-05 from the Index page. Derivation and validation — `mn_sustainability_index_extract_clean.ipynb` (restart-and-run-all passes; coverage counts and the type repair are asserted). Methodology — none published beyond the worksheet column headings; the Index is a self-reported directory. License — unverified (README open item). Sibling and need — `../../mn-greenstep-actions/` and `../../../../dataset-discovery/needs/2026-07-mn-city-ghgi/`.
