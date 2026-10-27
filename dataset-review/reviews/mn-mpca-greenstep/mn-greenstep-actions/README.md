# Minnesota Pollution Control Agency — GreenStep Cities completed actions

What each Minnesota GreenStep community has *done*: the best-practice actions it has completed and the program step (1–5) it has reached. This is the implementation side of the GreenStep program, as opposed to the plans and inventories a community *has* (the Minnesota Sustainability Index) or its emissions values (the Regional Indicators Initiative). It is published by the Minnesota Pollution Control Agency (MPCA) as part of GreenStep Cities & Tribal Nations, a voluntary program in which communities work through a checklist of 29 best practices across five categories and are recognised at steps 1 through 5. This entry covers a dated snapshot retrieved 2026-07-05: the program site is a live directory with no versioned releases, so what we hold is a moving snapshot. Two extracts exist so far — per-community step ratings and total completed-action counts for 156 communities; the per-city detail of *which* actions each community completed is available on the site but is not yet extracted, because there is no bulk export (see Canonical downloads).

## Canonical downloads

There is no bulk data file or API. The program exposes its data across three HTML surfaces plus a set of dashboards, and the review's two extracts come from the first two.

The all-communities list gives, per community, the steps reached (1–5) with their certification dates and whether the community is a city or a tribal nation; it also carries a `city-detail` link per community whose numeric id is the only stable key. This is the source of the step-ratings extract **verified**. A separate action-statistics page gives the total number of completed actions per community, which is the source of the action-counts extract **verified**.

The per-community detail — *which* of the 29 best practices a community completed, at what depth (a 1-, 2-, or 3-star rating per action), with dates, narrative descriptions, and occasional attached PDFs — lives only on the individual `city-detail/<id>` pages, one per community, rendered as HTML with no download button **verified**. This is where "all the actions a city has" actually lives, and it is the reason the review stalled: getting it means fetching and parsing roughly 156 detail pages keyed by the numeric ids harvested from the all-communities list, not downloading a file. It is available and profilable, just not yet extracted — the documented gap of this release, not a dead end. A worked single-city sample (Rochester) demonstrating the exact fields available per action is in `releases/2026-07/greenstep_actions_extract_sample.ipynb` (see References).

The program's data page links only dashboards, none of which is an action-level bulk export: the Step 4 & 5 metrics dashboard (a Tableau workbook on `data.pca.state.mn.us`, the outcomes/metrics side of the program), B3 Benchmarking, the Minnesota Sustainability Index, the Regional Indicators Initiative, and the Twin Cities (Metropolitan Council) GHG inventory **verified**.

- All communities (steps + dates + type): https://greenstep.pca.state.mn.us/all-cities
- Total completed actions per community: https://greenstep.pca.state.mn.us/action-stats
- Per-community action detail (one page each): https://greenstep.pca.state.mn.us/city-detail/<id> — e.g. Rochester is `/city-detail/12396`
- Data & dashboards index: https://greenstep.pca.state.mn.us/page/data

## Why we use it

- It is the implementation-and-engagement signal for Minnesota city context: the step a community has reached and how many best-practice actions it has completed give a fast read on institutional capacity and momentum, which is exactly the kind of signal cohort selection needs alongside a city's emissions (need: `2026-07-mn-city-ghgi`).
- It completes the GreenStep picture under one publisher: the Sustainability Index says which plans and inventories a community *has*, this says what it has *done*, and the Regional Indicators Initiative supplies the emissions values. Pairs with the Sustainability Index for the has-versus-done split.

## License

No explicit reuse license is stated on the program site **unanswered**. As MPCA state-government data it is presumptively public under the Minnesota Government Data Practices Act **inferred**, but explicit redistribution and attribution terms have not been verified from a primary source — the same open item that gates the Sustainability Index and RII entries. Confirm before registering in the catalog.

## Spatial and temporal scope

Geography is Minnesota communities that have voluntarily joined GreenStep — 156 in this snapshot, of which 151 are cities and 5 are tribal nations; the type is carried per community so city-only analysis can filter it **verified**. Participation is self-selected, not a complete enumeration of Minnesota. The values are a live directory of what each community has reported, not a modelled prior. Coverage is a moving snapshot rather than a frozen release: communities log actions and advance steps continuously, and the certification dates in this snapshot span 2010 to 2026. Three communities are marked inactive, and step attainment is uneven — 23 communities at step 1, 58 at step 2, 31 at step 3, and 44 at steps 4–5 (steps 4 and 5 recognise outcome tracking and are usually awarded together, which is why almost no community sits at step 4 alone) **verified**.

## Interpretation warnings

A completed-action count measures breadth of program engagement, not emissions outcomes. A community with 100 completed actions has done a lot of GreenStep best practices — which include education, ordinances, and planning steps as well as physical measures — but that is not the same as having reduced its emissions. The outcome side of the program lives separately in the Step 4 & 5 metrics dashboard, not in these action records; do not read a high action count as a low-emissions city.

The star rating on an action is implementation depth, not cross-city quality. A 3-star action means the community met the deeper tier of that specific best practice; it is not a score you can average across a city or compare between cities as an impact ranking.

Steps 1–5 are program recognition milestones, not a linear sustainability index. A step-5 community has been recognised for tracking outcomes, not certified as more sustainable than a step-3 community; the step reflects how far through the program's process a community has gone.

Absence is not zero effort. Nine communities have zero completed actions logged in this snapshot — registered but not yet reporting — and blanks throughout are "not recorded here", not confirmed inaction, because reporting is voluntary and periodic.

The set mixes cities and tribal nations. An unfiltered community count includes five tribal nations; filter on the type field for city-only statistics.

## Parsing notes

The all-communities page is an HTML list, not a table: each community is a link to `city-detail/<id>` followed by bold "Step N — date" lines, and the numeric `<id>` in that link is the only stable join key to the detail pages — the community name is not in the detail URL, so the ids must be harvested from this list first. Inactive communities carry an "Inactive — date" marker in place of or alongside their step lines.

At least one community is duplicated in the source: West Saint Paul appears with its Step 1, 2, and 3 lines each listed twice. Dedupe per community when parsing steps, or the step history double-counts.

The action-statistics page is a separate page keyed by community name (community → total completed actions); it joins one-to-one to the step-ratings by name, with all 156 communities present on both sides in this snapshot. Names are plain strings with no locode, so joins to our other Minnesota datasets are by name and need name-hygiene care, exactly as with the Sustainability Index.

Each `city-detail/<id>` page, when extracted, is structured as a header (GreenStep category A/B/C and current step/date) followed by a "Best Practice Actions Underway and Completed" section: a total and a per-star breakdown, then individual action blocks labelled "N star - Action M" grouped under the numbered best practices, each with a "Date action report first entered", an optional "Year action initially completed", a narrative, and sometimes a linked descriptive-file PDF. A future extraction notebook turns these blocks into one row per (community, best-practice action) with its star level and dates.

## Current approved release

**2026-07** — not catalog-registered. Two summary extracts are in hand (per-community step ratings and total action counts, 156 communities), plus a single-city sample of the per-city action detail (Rochester) that proves the detail parses cleanly into one row per action. The remaining gap is running that same parser across all ~156 `city-detail` pages, which needs a raw-HTML fetch of each page (a single text fetch truncates long pages). Two items gate promotion: confirming the redistribution license with MPCA, and deciding whether to build the full detail scraper (one row per community-action) or to ship only the step/count summary. Production approval is tracked in `catalog/index.yaml`.

## References

- Committed extracts: `releases/2026-07/data/greenstep_step_ratings.csv` (community, current_step, status, govt_type) and `greenstep_action_counts.csv` (community, completed_actions).
- Single-city action sample (demo of the per-city detail): `releases/2026-07/greenstep_actions_extract_sample.ipynb` → `data/greenstep_actions_sample_rochester_12396.csv` (25 of Rochester's 89 actions, one row per action with category, best practice, action number, star rating, dates, and descriptive-file link).
- Sibling under the same publisher (has-versus-done): `../mn-greenstep-sustainability-index/`.
- Emissions values for the same cities: the Regional Indicators Initiative review (`../../mn-rii/rii-city-indicators/`).
- Originating need: `../../../dataset-discovery/needs/2026-07-mn-city-ghgi/`.
- Per-city action detail (not yet extracted): `https://greenstep.pca.state.mn.us/city-detail/<id>`, ids from `https://greenstep.pca.state.mn.us/all-cities`.
