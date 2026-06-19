# Review — idb-projects, release v1

## Scope and status

Research release. The standalone notebook `idb_chile_projects.ipynb` pulls Chile operations from the IDB open-data datastore, keeps the mitigation ones (keyword-scored), standardises the fields, and maps each to a city action. Running it writes two committed `data/` outputs: `idb_chile_projects.csv` (the project dataset, one row per Chile mitigation operation) and `idb_chile_to_actions.csv` (the crosswalk). The notebook is committed unexecuted because it makes outbound API calls; its mapper is self-tested independently of the pull, so the mapping logic is verified even before the data lands. The only external reference is the city action list. Dataset-level provenance and the API are in the review README one level up.

## What this data supports

The extraction and mapping are proven. The IDB datastore is queried with a Chile filter (`cntry_cd=CL`) and paginated; mitigation relevance is keyword-scored on name, objective, sector and subsector, then filtered; the mapper maps electromobility to zero-emission bus fleets, housing energy efficiency to building retrofit, and forest restoration to reduce deforestation, while a public-finance operation is dropped as non-climate before mapping. These behaviours are asserted in the notebook's self-test cell.

The objective text carries the signal. Broad IDB `sector` labels (for example "Urban Development and Housing") hide the intervention, so the project name and objective are folded into the mapping text; that is what lets an electric-bus operation map correctly.

## What this data does not support

A keyword-scored filter is approximate. It will miss climate operations described in unusual terms and may admit borderline ones; the mitigation flag is a screening aid, not a definitive classification, and is carried through for review.

IDB and GCF can describe the same money. IDB is a GCF accredited entity (for example the FP189 e-mobility programme), so an IDB operation and a GCF record may be two views of one programme; relate them at the (country, sector) level and do not double-count.

## Using it downstream

Run the notebook to produce the two `data/` outputs. Access is intermediated (a city benefits via a national operation), so carry that on every row, link-don't-attribute, and adjudicate the medium, low and none rows.

## Notes on non-obvious fields

`is_mitigation` is the keyword-screen flag, not a final classification. IDB field codes are renamed at load (for example `oper_nm` to `project_name`, `objtv` to `objective`); the rename map is in the notebook. `mapping_confidence` of none means out-of-scope or too broad to map, distinguished in the rationale.

## Traceability

IDB datastore resource `814b7b54-477a-4c25-b3bf-6be05412069d`, queried 2026-06 per the project's reference patterns; public IDB open data. The notebook is self-contained and reproducible.

### References

- notebook → `idb_chile_projects.ipynb`
- outputs (produced on run) → `data/idb_chile_projects.csv`, `data/idb_chile_to_actions.csv`
- API + provenance → review README one level up
