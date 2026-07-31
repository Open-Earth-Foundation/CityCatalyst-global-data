# Review — br-city-finance-feasibility, release v1

## Scope and status

This release contains the pilot city profile (notebook 01, one row per pilot city), the pilot action finance profiles (notebook 02: the 53-action bank crossed with the 50 cities, 2,650 rows, funding-gap bucket and route annotation per pair), and the funding-options evidence table for an 8-city focus set (notebook 03: award evidence and options-available annotations from the br-climate-awards staging compile, 424 rows). All notebooks run clean end to end with all assertions passing, including the assertion that evidence never alters a bucket. Status: research. The scoring is route-eligibility-only on held data, per the methodology's build order; fund-by-fund matching waits on the sector tags and the fund-supply inventory, and the evidence layer inherits the compile's staging status.

## What this data supports

The claims are about city-side readiness, and the load-bearing caveat is inherited: CAPAG is a preliminary regulatory screen and MUNIC is prefecture self-declaration.

"All 50 pilot cities carry a complete city profile: CAPAG grade, ICF, versioned credit screen, and the full MUNIC finance-push component breakdown" is supported, with no missing records and no survey refusals in the set.

"29 of the 50 pilot cities pass the June 2026 CAPAG/ICF credit screen; 12 fail on the fiscal classification, 6 on information quality, and 3 are unknown" is supported and dated.

"A pilot city's locode and CityCatalyst id resolve to exactly one IBGE municipality" is supported; the two list quirks (Altamira's null state, the Cruzeiro do Sul homonym) are resolved and asserted in the notebook.

A statement of the form "in this pilot city, this action lands at needs-external-co-finance, with the grant arm of Route A and Route B open" is supported as a route-family reading under the documented tunables, dated to the June 2026 credit screen and 2020-2021 MUNIC components. Comparative readings across the bank are supported: low-cost actions are self-deliverable nearly everywhere, and cities diverge on the medium and high cost bands.

## What this data does not support

The overclaim to watch for is treating a bucket as a funding decision. The funding-gap bucket and routes string are rule outputs from two categorical city axes and two action fields under tunable cut points; they are not an award probability, not a fund match (no fund inventory or sector tags exist yet), and not a legal verdict (I Care's classification is pending, so a bucket says nothing about mandate). `finance_push_core_count` is a transparent convenience reading with a tunable threshold, not a capacity measurement; the components remain the evidence. A credit-screen pass is not borrowing approval, and a fail does not close grant or transfer routes. The adaptation inversion (grant windows favouring low-capacity cities) is carried only as the always-open A-grant annotation, not modelled from funder criteria yet.

## Using it downstream

Join on `cod_mun` or `locode`, both unique in this table. Carry `credit_screen_rule` and `capag_release_date` into any output so the screen stays versioned. Unknown statuses propagate as unknown. When the intervention profile and fund inventory land, this table is the city input to the gap ladder unchanged; nothing here should need rebuilding.

## Notes on non-obvious fields

`finance_push_core_count` counts six core components (dedicated environment body, council, fund used, civil-defence body, climate legislation, plano diretor); the rule and its status as a tunable summary live in methodology.md. Component status vocabularies (`no_fund`, `no_body`, `council_inactive`, `no_env_training`) are documented in the br-munic release review. `area` comes from the pilot export as delivered and is unvalidated; prefer IBGE geometries for any spatial use.

## Traceability

Inputs: the pilot export `sample/pilotcities.json` (CityCatalyst, received 2026-07-31); the CAPAG clean extract (br-capag release 2026-06-01); the finance-push table (br-munic release 2020-2021). All derivation is in `01_city_profile_pilot.ipynb`. The Altamira and Cruzeiro do Sul adjudications were made in-session on 2026-07-31 and are asserted in the notebook's validation block.
