# mn-climate-awards — collection notes

Provenance and method for the compiled dataset in this folder. This is a **staging dataset**: manufactured from public funder award announcements, not ingested from a single publisher, and **not yet vetted** through `dataset-review/`. Read alongside `schema.json` (the contract) and `sources.yaml` (the source registry).

## What this is

Real awarded climate-finance projects in Minnesota, indexed by reaching-money **route** (rollup) and the four Concept Note Builder axes — **funder · category · region · instrument**. It exists to power the CNB's "show examples" / comparable-projects logic and to give evidence for which funding *path* a city should pursue. Routes A and B only in this pass.

## How it was collected

1. **Navigated by the landscape doc.** `knowledge-base/topics/climate-finance/us-mn-climate-finance.md` names the routes, the funders on each, and where each route's award lists live. That reference — not this data — was the map.
2. **Targeted web search** per funder to find the specific award-announcement pages.
3. **Fetched primary sources** (see `sources.yaml`): agency news releases and the project-level PDFs/lists they link.
4. **Extracted award lines** — recipient + amount read directly off those pages.
5. **Structured + enriched** into `schema.json`'s fields.
6. **Verified what could be verified** (see below).

## Provenance is a gradient — read this before trusting a field

Fields are marked `sourced` (read from source) or `derived` (assigned by judgment) in `schema.json`. The `derived` fields are lower-trust and are the main work remaining before this can become a proper dataset:

- **`route`** — computed from the funder/instrument via the six-route model; not stated on any award page.
- **`category`** — assigned from the program + project description; needs a deterministic mapping rule.

`region` was in this list but is now **derived-by-rule** (an improvement): it's assigned from the auditable positive-list lookup `references/mn-region-lookup.csv` — MN-metro if the recipient is in the 7-county Twin Cities metro (or Metropolitan Council/MCES), else MN-greater. One straddler (New Prague, Scott/Le Sueur) is flagged `review`. Correct the tier in one place (the lookup) rather than per row. Still not stated in the award source, but reproducible.

Everything else (recipient, amount, dates, program, source) is read from the source.

## Verification status

- **BWSR (18 rows)** — every amount read from the FY27 Projects & Practices awards PDF; the line items reconcile **exactly** to the two published subtotals ($4,703,729 Projects & Practices + $1,881,817 Drinking Water). High confidence.
- **DNR flood (8 rows)** — project names/recipients read from the Oct 2025 release; **per-project amounts not published** (only the $9M round total), so `amount_usd` is null. Cost-share is the program cap (up to 50%), not a realized figure.
- **Aurora / Appleton (Route B)** — read from reporting on the 2025 bonding package; Aurora's $5M-in-$33M is stated, Appleton's exact award is not (null, flagged).
- **CWSRF 2026 PPL (333 rows)** — the full ranked Project Priority List, extracted from Exhibit 4 of the IUP PDF (provided locally, OCR not even needed once the binary was in hand — `pdftotext -layout` read it cleanly). Each row carries `ppl_rank`, `priority_points`, `project_ref`, and estimated project cost, all read from source. The row costs sum to $4,017,336,062, reconciling to the IUP's stated PPL total ($4,258,335,161) once the ~21 non-ranked Part C projects (not in Exhibit 4) are accounted for. Note: `project_total_usd` here is the **estimated project cost, not the loan/award amount** — the loan amounts live in Exhibit 1 (fundable range) and are a separate pull.
- **CWSRF aggregate row** — retained as a summary alongside the 333 detail rows (amount null, so no double-count).
- **CWSRF 2026 IUP fundable list (135 rows)** — extracted from Exhibit 1 of the same PDF: the fundable-range (Parts A/B) and Part C projects with actual **Net SRF loan** amounts (→ `amount_usd`), total project cost, and grant/principal-forgiveness subsidy (in notes). Each row reconciles internally (total = subsidy + loan), and every part total (A/B/C-1/C-2/C-3) ties **exactly** — TPC *and* Net SRF — to the IUP's own totals-by-part table ($1,528,710,169 TPC / $1,228,950,084 Net SRF across 135 projects, after the two documented "max SFY cashflow" portfolio adjustments). Highest-confidence Route B financial data in the set. These rows overlap the PPL rows by project (finer granularity, per project ID) and are distinguished by `status` = on-IUP-fundable / on-IUP-nonfundable.

## Insights — what the data says (Routes A & B)

Computed from the 498 rows (SFY2026 / FY27). Directional, one cycle, Routes A and B only.

- **Two routes, two orders of magnitude.** Median Route A grant $299K vs. median Route B SRF loan $4.73M — ~15×. The whole Route A sample totals ~$10M; fundable Route B loans total $1.2B in one year. "Climate finance" here is a small-grant world and a large-loan world that barely overlap in scale, and the route sets the size of the prize.

- **Route B is a queue, and it's long.** 333 projects sit ranked on the 2026 PPL requesting $4.0B, but only 108 (32%) reached the fundable range this cycle. Confirms the landscape claim that being *on the list* is necessary but not sufficient — the Route B concept note is a ranking exercise (priority points + facility plan), not a one-shot pitch.

- **The deep water money is wastewater, not climate resilience.** Of the $4.0B on the PPL, $3.9B (97%) is wastewater collection/treatment — aging-infrastructure renewal. Stormwater / green infrastructure — where a *climate-resilience* concept note actually lives — is $108M (2.7%) across 21 projects (median $1.8M). The giant, stable MN water pipeline is largely not adaptation money; it just shares the funds.

- **So stormwater's real home is Route A.** 15 of the 21 stormwater PPL projects are metro (Minneapolis greenways, Minnehaha Creek & Capitol Region watershed districts), and stormwater/flood/water-quality is exactly what the Route A grants (BWSR CWF, Met Council, DNR flood) name as their focus. A climate-resilience concept note is a Route A object in a Route B–dominated landscape.

- **Subsidy is means-tested.** Across fundable projects only 16% of cost is grant/principal-forgiveness subsidy; 84% is repayable loans. But 32% of projects get *some* subsidy, and the fully/heavily-forgiven ones are all tiny cities (Sandstone 100%, Braham 100%, Appleton 84%). Large cities borrow; small low-income cities get cost written off. A small city's "fundability" therefore includes qualifying for affordability subsidy (population + median-income), a different lever than rank.

- **Money concentrates in one metro entity, then scatters.** The Metropolitan Council (MCES) alone takes $385M of $1.2B fundable loans (~⅓). After that, a long tail of small greater-MN cities: 85 greater-MN fundable projects ($762M) vs. 23 metro ($438M). Metro dollars are dense and centralized; greater-MN dollars are numerous and small.

- **The through-line for the routes model:** the route determines the instrument (grant vs. loan), the document (competitive narrative + BCA vs. priority ranking + facility plan), the ceiling (hundreds of thousands vs. tens of millions), *and* the category fit. The CNB has to steer category→funder fit, not just chase the biggest pool.

- **Scoping is funder-first (per PRD §1, §7, §8).** Project category isn't narrowed independently — it falls out of the still-open funder choice (TBC at M1, NLC). This dataset covers the water routes richly, which is enough to *inform* a water-funder pick.

- **Energy/buildings finance is program-heavy and award-thin — the predicted lopsidedness, confirmed.** Where water Routes A/B yielded ~470 enumerable award rows, the energy side yields almost none. The one real enumerable award set is **MnCIFA** (Route D, the state green bank): 10 closed loans (solar, geothermal, net-zero affordable housing, resiliency hubs), portfolio $37M across 14 loans, $500k–$5M, avg $2.6M — new (2024–26), small, and per-project amounts aren't public. Everything else is a *mechanism*, not an award list: EECBG is a formula block grant ($2k–$20k re-granted to small cities); CERTs are tiny seed grants ($5–10k); and the workhorses — utility CIP/ECO rebates and IRA elective/direct pay — are program participation and tax filings, not competitive awards. So for an energy/buildings concept note, "fundable" means **assembling a stack** (green-bank loan + rebates + elective pay + PACE), not winning one grant — a fundamentally different shape from the water routes, and the binding constraint is timing (tax-credit sunsets), not a ranking or a competition.

## Coverage readiness

Strong where the pilot is most likely to land (MN water/stormwater/wastewater funder), thin elsewhere. Depth by category:

| Category | Depth | Usable as "show examples"? |
|---|---|---|
| wastewater / SRF | deep, amount-level, verified | yes |
| stormwater / water-quality | good (grants + SRF slice) | yes |
| drinking water | good (BWSR + SRF) | yes |
| flood | 8 named projects, no amounts | partial |
| energy / buildings | first slice (MnCIFA 10 + aggregates), no per-project $ | thin |
| extreme heat / adaptation | essentially absent | no |

Verdict: enough to power examples **and** inform the funder pick for a water-focused pilot; deepen energy/heat only if a cohort city needs it. Confidence hinges on the still-open decisions (which funder, which 3 cities). This is the examples layer, not the funder profile.

## Known gaps (the to-proper checklist)

- **Per-column subsidy split** — for IUP rows the grant subsidy is captured as one aggregate figure (total − loan). The source splits it into PSIG / GPR (principal forgiveness) / affordability grant; those per-column values aren't broken out per row (they shift column position per page). Part-level totals for each are in the IUP totals table if needed.
- **Drinking Water SRF PPL/IUP** — only Clean Water SRF pulled; the DWSRF list (MDH) is separate.
- **Region — mostly done.** All rows now carry a metro/greater/statewide tier via `references/mn-region-lookup.csv` (81 metro, 416 greater, 1 statewide). Remaining: confirm the one `review` entry (New Prague) and, if a finer split than metro/greater is ever needed, add per-county detail to the lookup.
- **Standalone PSIG award list** — program terms captured; individual PSIG-only awards not enumerated.
- **PSIG award list** — program terms captured in the landscape doc; individual awards not enumerated.
- **DNR per-project amounts** — only the round total is public in the release; need the grant detail.
- **Met Council** — current row is a TBRA placeholder (contaminated-land redevelopment, adjacent to stormwater); swap for stormwater-relevant Livable Communities Demonstration Account awards.
- **Derived-field rules** — replace the hand-assigned `region` and `category` with deterministic lookups.
- **Routes C–F** — deliberately absent (thin or non-enumerable award history).

## Refresh model

There is no feed to poll. "Refresh" = re-run the compile against the pages in `sources.yaml` and diff. Each source carries a `last_fetched` date there.

## Promotion

When scope is locked, derived fields are computed by rule, amount gaps are filled from primary sources, and provenance is complete, this graduates into `dataset-review/` — which creates the catalog entry and, downstream, the pipeline into `modelled.*` / the CA microservice `get_projects()` service.
