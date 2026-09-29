# World Bank — Projects & Operations (`world-bank-projects`)

Project-level metadata for World Bank lending operations, sourced from the official Projects & Operations API. Release `v3` is a Brazil adaptation-relevance research slice; it does not replace the preserved Chile mitigation-oriented `v2` release and is not production-approved.

## Why this dataset matters

The source offers a long-run view of World Bank operations and their published commitments, instruments, sectors, themes, approval dates, closing dates and lifecycle statuses. For Brazilian adaptation research it can identify comparable projects and routes to project documents. It cannot by itself establish that a whole project or commitment is adaptation finance.

## Access

- Official catalog record: `https://datacatalog.worldbank.org/search/dataset/0037800/world-bank-projects-operations`
- Official Projects API: `https://search.worldbank.org/api/v2/projects`
- Brazil request: `https://search.worldbank.org/api/v2/projects?format=json&rows=1000&os=0&countrycode=BR`
- Access: public, no API key observed.
- Format: JSON; the `projects` member is a map keyed by project identifier.
- API stability: public but not version-pinned. The release retains dated raw responses and SHA-256 checksums in its review.

## Licensing and attribution

The catalog labels World Bank Projects & Operations **Creative Commons Attribution 4.0 International (CC BY 4.0)**. The World Bank licensing page says users may copy, modify and distribute the data for any purpose, including commercially, provided they give appropriate attribution and indicate changes, including translations. World Bank datasets under CC BY 4.0 also carry the publisher's mandatory mediation/arbitration terms; downstream users should retain a link to `https://datacatalog.worldbank.org/public-licenses` rather than representing the license as bare CC BY 4.0 without those terms.

Suggested attribution: “World Bank Projects & Operations, World Bank, used under CC BY 4.0 with World Bank mandatory terms; filtered, translated and classified by CityCatalyst. Changes were made.”

## Coverage and grain

The canonical source covers project-level records from 1947 to the present. The retained Brazil API response retrieved on 2026-09-25 contains 566 records. Release `v3` includes 55 records selected by an explicit-title or multiple-query screen for adaptation relevance. One row is one World Bank project identifier, not a contract, disbursement, project component or city award.

## Brazil adaptation screen

The release keeps a project when its title explicitly contains an adaptation/resilience/hazard term, or when it appears in at least two official Brazil Projects API full-text result sets among `adaptation`, `climate resilience`, `disaster risk`, `flood`, `drought`, `landslide` and `early warning`. Full-text matches may come from project-associated documents not exposed in the project row, so non-title matches are candidates for follow-up, not confirmed classifications.

`total_commitment_amount_usd` is the published project commitment field. It is not copied to `adaptation_finance_amount_usd`; that field remains blank because the API response supplies neither a climate/adaptation percentage nor a component allocation. The project endpoint also supplies no disbursement field.

## Language convention

Column names and controlled release fields are English. The API is overwhelmingly English for this slice. The single Portuguese project title is translated in `project_name`, retained verbatim in `project_name_pt`, and labelled `human_translated_from_portuguese_source`. English source titles have an empty `project_name_pt` and `source_english` status. Borrower and implementing-agency legal names are preserved as source identifiers rather than translated; source encoding defects are not silently repaired.

## Lifecycle interpretation

`board_approval_date` records Board approval where published. `closing_date` is a planned or recorded closing date and is not completion evidence. `Active`, `Closed`, `Pipeline` and `Dropped` are kept distinct. Pipeline operations are proposals, dropped operations were not carried forward, and neither an Active nor Closed status reports disbursement or proves delivery of adaptation components.

## Mapping to adaptation actions

The mapping is intentionally sparse. Explicit early-warning and climate-smart-agriculture titles can support direct links; water-security, flood-prevention and resilient-road titles support only component links. All mappings are medium confidence and pending human adjudication. Every unmatched project has an explicit `none` row. No project amount is allocated to an action.

## Release files

- `releases/v3/build_brazil_adaptation_release.py` — restartable API/evidence build.
- `releases/v3/world_bank_brazil_adaptation.ipynb` — restartable notebook wrapper with validations.
- `releases/v3/data/world_bank_brazil_adaptation_projects.csv` — cleaned project table.
- `releases/v3/data/world_bank_brazil_adaptation_projects_to_actions.csv` — draft action crosswalk.
- `releases/v3/review.md` — evidence, caveats and validation results.
- `releases/v3/sample/*.json` — retained official API evidence (locally present; ignored by repository rules).

Release `v2` remains the earlier Chile notebook/review and was not overwritten.
