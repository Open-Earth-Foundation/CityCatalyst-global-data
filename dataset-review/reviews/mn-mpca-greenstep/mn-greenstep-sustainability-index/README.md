# Minnesota Pollution Control Agency — Minnesota Sustainability Index (GreenStep)

A directory of what climate work each Minnesota community has on record: which have a Climate Action Plan, an Energy Action Plan, an adaptation or resiliency plan, a community-wide GHG inventory, a GHG reduction goal, a vulnerability or vulnerable-population assessment, formal climate commitments, and green teams or commissions, each with a website link and, for plans and goals, a year. It is a directory of what exists and where, not the underlying plans or emissions numbers. The Minnesota Pollution Control Agency (MPCA) publishes it as part of GreenStep Cities & Tribal Nations, downloadable as five thematic worksheet exports. This entry covers the dated snapshot retrieved 2026-07-05, because the Index is a live, voluntarily-reported directory with no versioned releases.

## Canonical downloads

The source is the Minnesota Sustainability Index page, exported as five thematic worksheets: Planning; GHG & Climate Mitigation; Vulnerability & Equity; Formal Commitments; Green Teams & Commissions. The files were retrieved and opened (user-provided download, 2026-07-05) **verified**. There is no versioned release or archival permalink: the page is regenerated as reporting is updated, so what we hold is a snapshot, and re-retrieval will return a moving target rather than this exact set of rows. Re-download by exporting each of the five worksheets from the Index page; the raw exports and the built documents table are committed under the release `data/` folder because they are small (single-digit MB total).

- Index page: https://greenstep.pca.state.mn.us/page/minnesota-sustainability-index

## Why we use it

- It answers the CNB's city-context question directly for Minnesota: which cities already have a CAP, a GHG inventory, and a vulnerability assessment, with links to each, so the agent can seed a cohort city from what the city has already published rather than from nothing.
- It is the inventory-availability directory for the MN city-GHGI need: it tells us which communities have a community-wide inventory and links to it, complementing the Regional Indicators Initiative, which holds the inventory values themselves. Pairs with RII for that reason.
- Its breadth (73–119 communities per theme) replaces the retired hand-built `mn-city-climate-docs` index, which covered only a handful of cities and is now superseded.

## License

No explicit reuse license is stated on the Index page **unanswered**. As MPCA state-government data it is presumptively public under the Minnesota Government Data Practices Act **inferred**, but explicit redistribution and attribution terms have not been verified from a primary source. This is the one open item blocking promotion: the license must be confirmed **verified** before the dataset is registered in the catalog.

## Spatial and temporal scope

Geography is Minnesota communities, self-selected through voluntary reporting rather than a complete enumeration of the state. "Community" is broader than "city": across the worksheets the `Type of Community` field carries city, county, region, state, township, tribal nation, and watershed district, and the set includes the Metropolitan Council (a `Region` row) and state-level rows. For city-only analysis, filter on `type`. The values are a local-truth directory: each entry is what that community reported to MPCA, not a modelled or imputed prior. Coverage is a moving snapshot, not a frozen release: logging is voluntary and periodic, and plan years run from the 1990s to the 2020s. There is no supersedes chain because there are no discrete versions, only the live page.

## Interpretation warnings

The single most important caveat is that this is a directory, not the data. The GHG worksheet tells you which communities have a community-wide inventory and links to it; it does not carry the emissions values. For actual community GHG numbers use the Regional Indicators Initiative, not this Index.

Absence of a flag means "not recorded here", not confirmed absence. Because reporting is voluntary and periodic, a blank cell means the community has not logged that item, which is not the same as the community not having it.

The Index lags on recency. It logs Minneapolis's Climate Action Plan as 2013 rather than the 2023 Climate Equity Plan, shows no CAP for Mankato (which adopted one in 2025) or Rochester (2021 work plan), and similar gaps exist elsewhere. It is authoritative for breadth and for links, but it can trail the newest plans, so cross-check the city's own site or the 100% Campaign's November-2025 LCAPS report when currency matters.

The row population is uneven by theme. A community carries an Energy Action Plan link and year without the named-plan flag being set (Minneapolis is the one such case here), so a count of "communities with an Energy Action Plan" is 44 by the named-plan flag but 45 if any energy field counts. The documents table ships the flag-based count (44); the discrepancy is a real data quirk, not a parsing error.

"Community" mixes administrative types, so an unfiltered count double-counts a metro area as its city, its county, its region, and the Met Council. Filter by `type` before any city-level statistic.

## Parsing notes

The five worksheets carry a `.csv` extension but are **UTF-16 little-endian, tab-separated, with CRLF line endings** — an export of a spreadsheet tool, not comma-delimited CSV. Read them as UTF-16 with a tab delimiter; a naive `read_csv` will fail or return a single garbled column.

Each community appears as several duplicate rows within a worksheet — four rows each in Planning and GHG, three in Vulnerability, five in Commitments and Green Teams — a denormalization artifact in which different attributes are populated on different rows for the same community. Dedupe by taking the first non-blank value per field across that community's rows before reshaping.

The presence columns are not `Yes`/`No`: a populated cell holds the resource's label (for the GHG inventory, values such as "Twin Cities GHG Inventory" or "RII"), and blank means "not logged". Treat non-blank as presence and blank as "not recorded", never as a confirmed "no".

The committed output is a tidy long documents table, not a wide one-column-per-artifact table: one row per community-document, with a controlled `document_type`, the source-side name in `document_label`, the adoption year in `document_year`, and the link in `document_url`. Absence of a document is the absence of a row. The familiar one-row-per-community presence matrix is a single `pivot_table` away and is shown in the notebook; the reshape trades twenty-two columns for six and makes commitments (one row per named commitment) and green-team bodies (one row per specific body) separable rather than collapsed.

The `Type of Community` value can sit on only some of a community's duplicate rows, so the type is recovered with the same first-non-blank rule across all five worksheets and carried on every document row. The hand-built table delivered earlier left `type` blank for 23 communities whose type is in fact present in the worksheets; the extraction notebook repairs this so every row carries a type.

Community names are plain strings with no locode or other code, so joins to our other Minnesota datasets are by name and need name-hygiene care.

## Current approved release

**2026-07** — not yet catalog-registered; production approval is tracked in `catalog/index.yaml` and is pending license confirmation.

## References

- Release data: `releases/2026-07/data/` — `mn_sustainability_index_documents_2026-07.csv` (tidy long table, 498 document rows across 172 communities) and the five source worksheets.
- Extraction notebook: `releases/2026-07/mn_sustainability_index_extract_clean.ipynb`.
- Release contract: `releases/2026-07/review.md`.
- Sibling under the same publisher: `../mn-greenstep-actions/` (implementation side — what a community has done, not what it has).
- Originating need: `../../../dataset-discovery/needs/2026-07-mn-city-ghgi/`.
- Inventory values to pair with: Regional Indicators Initiative (see the GHGI need).
