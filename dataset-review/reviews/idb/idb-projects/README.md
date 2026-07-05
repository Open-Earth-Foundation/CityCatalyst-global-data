# IDB — projects (idb-projects)

Project-level records from the **Inter-American Development Bank (IDB) open-data datastore**, the IDB slice of the multilateral climate-finance picture. Strong Latin America / Caribbean coverage, one row per operation, with country, sector/subsector, instrument, commitment and approval date. Like the GCF and World Bank project reviews, this is the **awards/projects layer** (what got funded), at the **multilateral level**, accessed **intermediated** (a city benefits via national programmes, it does not apply). See `knowledge-base/topics/climate-finance/cl-climate-finance.md` ("Funder levels").

## Access (verified 2026-06)

CKAN-style datastore API: `https://data.iadb.org/api/action/datastore_search` with `resource_id = 814b7b54-477a-4c25-b3bf-6be05412069d`, paginated by `limit` and `offset` (read `result.total`); the Chile slice uses the CKAN `filters={"cntry_cd":"CL"}` parameter so only Chile records are returned. The full resource is about **27,500 operations**. Records use short field codes; the notebook renames them, the useful ones being `oper_num`→`project_id`, `oper_nm`→`project_name`, `objtv`→`objective`, `cntry_cd`/`cntry_nm`→country, `sector_nm`→`sector`, `subsector_nm`→`subsector`, `apprvl_dt`→`approval_date`, `publc_sts_nm`→`status`, `orig_apprvd_useq_amnt`→`total_commitment_amount`, `lending_instrmnt_nm`→`instrument_type`. License: public IDB open data (confirm reuse terms before redistribution).

## Scope and Chile filter

IDB has no climate query parameter, so mitigation relevance is scored client-side: the notebook keyword-scores `project_name` + `objective` + `sector` + `subsector` (renewable energy, efficiency, electromobility, recycling, forests, etc.) and keeps the matches. We cover **mitigation** only, so adaptation/disaster operations are dropped. The Chile slice is the `cntry_cd=CL` filter. Note FP189 e-mobility and similar GCF programmes are delivered by IDB as the accredited entity, so some IDB and GCF records describe the same money from different sides — relate at the (country, sector) level, do not double-count.

## Mapping to actions

IDB projects map at a **classification grain**: `sector` + `subsector` plus the objective text to the city action list, link-don't-attribute, with the keyword-scored mitigation flag carried through. The objective text is decisive — it carries the intervention detail the broad sector label lacks. Self-contained in the review notebook (extract → score → map), not a shared step.

## Extraction and status

This review is **self-contained**: `releases/v1/idb_chile_projects.ipynb` pulls the IDB datastore (Chile filter), keeps the mitigation operations, standardises the fields, maps to actions, and writes both `data/idb_chile_projects.csv` (the project dataset) and `data/idb_chile_to_actions.csv` (the crosswalk). It is committed unexecuted (it makes outbound API calls); running it produces the data. The mapper is self-tested independently of the pull. Production: **pending validation** (run the notebook, then add a `catalog/index.yaml` entry). Release detail in `releases/v1/review.md`.

## Main sources

- IDB datastore search → `https://data.iadb.org/api/action/datastore_search` (`resource_id=814b7b54-477a-4c25-b3bf-6be05412069d`)
- review notebook → `releases/v1/idb_chile_projects.ipynb`
