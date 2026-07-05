# World Bank — projects (world-bank-projects)

Project-level records from the **World Bank Projects API**, the World Bank slice of the multilateral climate-finance picture. Global coverage, one row per operation, with country, commitment, sector/theme, instrument and approval date. Like the GCF and IDB project reviews, this is the **awards/projects layer** (what got funded), at the **multilateral level**, accessed **intermediated** (sovereign lending; a city benefits as a sub-borrower, it does not apply). See `knowledge-base/topics/climate-finance/cl-climate-finance.md` ("Funder levels").

## Access

Public JSON API: `https://search.worldbank.org/api/v2/projects?format=json&rows=50&os={offset}&qterm={term}`. The `projects` key is a `{project_id: record}` map (convert values to rows); paginate with `os` in steps of `rows`. Climate relevance is filtered at the query with `qterm`: `qterm=climate` returns about 6,200 projects, `qterm=mitigation` about 4,500. Useful fields: `id`, `project_name`, `countryname`/`countrycode`/`countryshortname`, `regionname`, `boardapprovaldate`, `closingdate`, `status`, `totalcommamt`/`curr_total_commitment`, `lendprojectcost`, `sector1`, `theme1`, `lendinginstr`, `url`. License: public World Bank open data (confirm reuse terms before redistribution).

## Scope and Chile filter

We cover **mitigation** only, so pull with `qterm=mitigation` (or filter `theme`/`sector` and drop adaptation-only operations). The Chile slice is a filter on `countryname` / `countrycode` (Chile / CL). As with GCF, multi-country operations carry programme totals, not a Chile figure.

## Mapping to actions

Like the FPA awards and the GCF Chile slice, World Bank projects map at a **classification grain**: `theme1` + `sector1` plus the project name (energy, transport, urban, forestry, waste) to the city action list, link-don't-attribute, medium or none where a project is broad or adaptation. This is self-contained in the review notebook (extract → standardise → map), not a shared step. Expect a larger `none` share than the domestic award sets — World Bank sector/theme labels are broad, and a generic "renewable energy" or "climate change" operation has no single action.

## Extraction and status

This review is **self-contained**: `releases/v2/wb_chile_projects.ipynb` pulls the World Bank API, keeps the Chile slice, standardises the fields, maps to actions, and writes both `data/wb_chile_projects.csv` (the project dataset) and `data/wb_chile_to_actions.csv` (the crosswalk). It is committed unexecuted (it makes outbound API calls); running it produces the data. The mapper is self-tested independently of the pull. Production: **pending validation** (run the notebook, then add a `catalog/index.yaml` entry). Release detail in `releases/v2/review.md`.

## Main sources

- World Bank Projects API → `https://search.worldbank.org/api/v2/projects`
- mitigation query → `https://search.worldbank.org/api/v2/projects?format=json&rows=100&os=0&qterm=mitigation`
- review notebook → `releases/v2/wb_chile_projects.ipynb`
