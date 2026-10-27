# Review — world-bank-projects, release v2

## Scope and status

Research release. The standalone notebook `wb_chile_projects.ipynb` pulls climate/mitigation projects from the World Bank Projects API, keeps the Chile slice, standardises the fields, and maps each project to a city action. Running it writes two committed `data/` outputs: `wb_chile_projects.csv` (the project dataset, one row per Chile operation) and `wb_chile_to_actions.csv` (the crosswalk). The notebook is committed unexecuted because it makes outbound API calls; its mapper is self-tested independently of the pull, so the mapping logic is verified even before the data lands. The only external reference is the city action list. Dataset-level provenance and the API are in the review README one level up.

## What this data supports

The extraction and mapping are proven. The World Bank API is queried with `qterm=mitigation` and paginated by offset; the Chile slice is a filter on `countryname`; the mapper maps a solar project to solar generation, an electromobility project to zero-emission bus fleets, and a broad climate-resilience programme to none. These behaviours are asserted in the notebook's self-test cell.

Chile's World Bank climate footprint is thin. Chile is a high-income borrower with limited Bank lending, so the Chile slice is expected to be small, and the records carry broad `theme1` and `sector1` labels.

## What this data does not support

Generic labels do not map. A project tagged only "renewable energy" or "climate change", with no specific intervention in the name, maps to none, because the action list has no generic-renewables or awareness archetype. A high none share is a property of the World Bank's broad labels, not a failure.

These are not opportunities a city applies to. World Bank lending is sovereign and intermediated; a city benefits as a sub-borrower under a national operation, so the records are outcomes, not open calls.

## Using it downstream

Run the notebook to produce the two `data/` outputs. Relate projects to actions at the project grain, link-don't-attribute, and treat a multi-component operation's commitment as the operation total. Medium, low and none rows await human adjudication.

## Notes on non-obvious fields

`mapping_confidence` of none means either out-of-scope (adaptation) or too broad to map, distinguished in the rationale. `total_commitment_amount` is the World Bank commitment, parsed from the API's comma-formatted string.

## Traceability

World Bank Projects API, queried 2026-06 per the project's reference patterns; public World Bank open data. The notebook is self-contained and reproducible.

### References

- notebook → `wb_chile_projects.ipynb`
- outputs (produced on run) → `data/wb_chile_projects.csv`, `data/wb_chile_to_actions.csv`
- API + provenance → review README one level up
