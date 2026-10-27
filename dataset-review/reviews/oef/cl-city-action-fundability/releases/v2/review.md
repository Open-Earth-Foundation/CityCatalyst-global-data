# Review — oef/cl-city-action-fundability, release v2

## Scope and status

**Research, not production-approved, and nothing in it is safe for default display today.** This release refreshes the Chile opportunity inventory and replaces v1's sector-level action matching with a derived scheme: how specifically a fund matches an action follows from how specific the fund is. A targeted route can support a specific match, a general route can only support a general one, and a route that buys readiness can never support a capital claim. All 100 opportunities currently fail the separate availability gate, so the release ships zero displayable links by design. The v1 release remains the one implemented in production.

Most of the matching is computed rather than asserted. Of the 200 links, 180 derive from the route profile carried by the opportunity compile and the delivery mode of the action; only 20 come from human judgement, recorded in a 21-row crosswalk. Coverage therefore grows by verifying funds in the compile rather than by adjudicating pairs, which is the opposite of how v1 grew.

The release holds one notebook, two hand-maintained inputs, and two pipeline-ready tables. The action summary is rendered in the notebook rather than exported, as it is an aggregate of the links.

### References

- build, validation and charts → `01_opportunity_action_links.ipynb`
- opportunity inventory → `data/chile_finance_inventory.csv`
- action delivery modes, hand-adjudicated → `data/action_delivery_mode.csv`
- curated crosswalk, the only stored judgement → `data/action_opportunity_mapping.csv`
- resolved links → `data/finance_opportunity_action.csv`
- matching contract → `../../methodology.md` → *Action-to-opportunity matching*

## Visual summary

Of 102 climate actions, 11 are covered by a targeted fund a municipality can apply to, 18 have only a general municipal route, and 48 are territory-only: money for them exists in Chile but goes to a firm, a farmer, a utility or a transport operator rather than the city. The remaining 25 have nothing, and all of them are regulations, programmes or plans rather than capital projects.

| Sector | Actions | Covered | General route only | Territory only | Nothing |
|---|---:|---:|---:|---:|---:|
| Stationary energy | 30 | 1 | 10 | 9 | 10 |
| Industry | 28 | 0 | 0 | 21 | 7 |
| AFOLU | 26 | 5 | 4 | 15 | 2 |
| Waste | 10 | 4 | 3 | 0 | 3 |
| Transportation | 8 | 1 | 1 | 3 | 3 |

## What this data supports

The claims are about what the reviewed evidence establishes and, equally, about who the money is for. The load-bearing caveat is that coverage claims hold only for the 14 records the compile has reverified.

Across ten Chilean public and firm-facing sources there are 100 catalogued climate-relevant funding opportunities, of which 27 are routes a municipality can itself receive.

For 11 of the 102 climate actions, a named Chilean fund that a municipality can apply to finances the whole of the action or a material part of it, with a stated rationale a reviewer can argue with.

For a further 18 actions a general municipal works fund exists that could plausibly pay, subject to the project qualifying under that programme's operating rules. The release says which funds and what would have to be confirmed.

For 48 actions the money exists but the city is not the applicant. This is the actor gap stated as data rather than as a caveat, and it is the most decision-relevant thing in the release: for these actions a city's lever is convening, permitting or regulating, not applying for a grant.

For every opportunity the release states what the money buys, how targeted the route is, and whether a municipality can receive it, so a downstream consumer can reproduce any link without re-reading the sources.

## What this data does not support

The overclaim to watch for is reading any link as money a city can go and get. Two thirds of the links are general routes whose eligibility nobody has checked, and none of them passes the availability gate.

"These are the funds available for this action." No. Zero links pass the current-use gate, because the compile marks every opportunity as not yet ready for production display. A link is a relationship, not an open call.

"25 actions have no Chilean funding." No, and the composition matters more than the count: all 25 are regulations, city-run programmes or plans. Sixteen need authority rather than capital, and the rest are operating cost that capital funds do not cover anyway. None of the 25 needs capital investment.

That is not the same as saying every capital action is funded. Two do have a genuine capital gap: adopting zero-emission bus fleets and electrifying the municipal vehicle fleet are the only actions in the catalogue that carry no link of any kind. Both are equipment purchases, and the only Chilean vehicle-renewal money in the inventory is directed at transport operators. Municipal fleet electrification in particular is a capital purchase a city would make itself, with no city-receivable route on record.

"Industry has no climate finance in Chile." No. Industry has 21 territory-only actions, which means the finance exists through CORFO guarantees, Innova Chile and regional productivity funds and is directed at firms. A city cannot apply for it. Reading zero coverage as zero finance inverts the finding.

"A general route means the city can fund this." No. A general route means a municipal works fund covers this class of activity, not that this project qualifies. Every general link carries the check that remains outstanding.

"Coverage fell from 86 actions to 11, so v2 is a regression." No. The v1 figure came from a sector join that generated links nobody reviewed, including a taxi renewal programme matched to an electric bike-share action. The fall is the removal of unreviewed links and of funds a city cannot apply to.

## Using it downstream

Filter on the display recommendation, never on match type alone. Match type describes the relationship; the recommendation is the conjunction of coverage and availability, and it is the only field safe to serve.

Read the four coverage states as different actions for the reader, not as a ranking. Covered means pursue the named fund. General route means check eligibility. Territory-only means the city's lever is not funding. Nothing means the action needs authority or operating budget.

Treat the general routes as a starting list rather than an answer. The median routed action returns eight of them, because the release currently models all municipal capital works as one class; buildings, public space, paving and basic services behave differently and that distinction is not yet in the data.

Do not join to the action catalogue on action name. Source-side spelling errors and trailing spaces are preserved as published; join on action id.

For anything a city will act on today, the v1 production model and the finance API built on it remain the live path.

## Notes on non-obvious fields

The link table separates three questions that a single relevance score would blur: what the relationship is, how it was arrived at, and whether the city can act on it. Reading any one alone will mislead.

- `match_type`: `whole` and `part` are reviewed judgements about a targeted fund. `prepares` is derived from the fund buying preparation and never implies capital. `general_route` is derived and means a general municipal fund covers this class of activity.
- `match_basis`: `reviewed` means a person chose this pair; `rule` means the pair itself was computed. A `prepares` row is `reviewed`, because someone decided which actions that fund prepares even though the type is forced by what the fund buys. Counts of coverage never mix the two bases.
- `city_can_apply`: whether a municipality can receive the money. A reviewed link can be `no`, which is deliberate; those links record funding that exists for someone else and are what make the territory-only state visible.
- `counts_as_coverage`: true only when the match type is `whole` or `part` *and* the city can apply. This is why 16 reviewed coverage links yield 12 counted ones.
- `funds_what` and `route_scope`: carried from the compile so the derivation is auditable on the row itself.
- `current_display_eligible`: whether the compile has evidenced the call, dates, geography and applicant. Currently false for every record.
- `status` (inventory): normalised where the compile reverified the record, otherwise the seed's own claim from v1. Not uniformly a current status.

## Traceability

The opportunity records, the route profile and all availability evidence come from the Chile climate-finance opportunities compile, which remains authoritative for per-record verification notes. Actions come from the ClimateView transition-elements release of 2026-02-23. Lossless retention of the v1 inventory is asserted in the notebook against the v1 file itself.

Two inputs are hand-maintained and adjudicated by amanda@openearth.org on 2026-08-16: the 102 action delivery modes and the 21 crosswalk judgements. The delivery mode is a property of the action catalogue rather than of this dataset and should move upstream to the ClimateView review when that entry next changes.

The v1-to-v2 comparison quoted in discussion of this release, 504 draft links falling to a reviewed handful, is **unverified and not reproducible**: the v1 draft files were never committed and are not in git history. The one v1 defect that is verified is the taxi-colectivo to bike-share link, which the notebook asserts is absent.

Three limitations are open in the compile and bound what this release can say. Forty-six opportunities still carry a `cross_sector` theme tag and are read permissively as covering every sector. Twenty-nine have no recorded applicant, all of them historic environmental-fund calls, so their city eligibility is unknown and they emit no links either way. And general municipal works are modelled as a single class, which is what inflates the number of general routes per action.

### References

- compile, route profile and verification record → `dataset-compile/cl-climate-finance-opportunities/`
- action catalogue → `reviews/climateview/climateview-transition-elements/releases/2026-02-23/data/current_actions.csv`
- v1 inventory → `../v1/data/chile_finance_inventory.csv`
