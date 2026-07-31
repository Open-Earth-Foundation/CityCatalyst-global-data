# How Brazil city finance feasibility works — working methodology

**Status: working draft.** The pillar design is owned by the Feasibility pre-read (References); this document records how OEF implements its Financing component with the data actually reviewed, what is held, and what remains to build. It will change as the open decisions in the pre-read are confirmed.

## In one paragraph

Feasibility rests on two components: Legal (a per-intervention verdict, owned by I Care) and Financing. Financing compares what an intervention needs (cost band, preparation type) with what the city has (fiscal capacity, finance-push capacity), reads the shortfall as a funding gap on an effort ladder, and checks which of six Brazilian finance routes are open to that city. The result is an outcome bucket from self-deliverable down to a no-path hard stop, with the route annotation carrying the explanation. Delivery capacity is not scored separately: the finance-push signal folds into Financing as the know-how axis, socio-economic capacity stays in Impact, and implementation capacity moves to project design.

## The city profile (held)

Two signals, both from vetted reviews, joined on the seven-digit IBGE code:

| Signal | Reads as | Source | Coverage |
|---|---|---|---|
| CAPAG + ICF, with the versioned credit screen | fiscal capacity; the hard gate on Union-guaranteed credit | br-capag release 2026-06-01 | national; all 50 pilots |
| finance_push components | ability to formulate and win a funded project | br-munic release 2020-2021 | national; all 50 pilots, no refusals |

The finance-push breakdown stays componentwise in every output, and the scoring is itself a dataset: every point comes from one row of the scoring-rules table, points subtotal into five families (environment governance 0–4, environment finance 0–3, climate-specific 0–2, civil defence 0–3, planning 0–2), the 0–14 total maps to a named bucket via the bucket table, and the per-city working-through is exported as the step-1 scores dataset. The rules give extra weight to a dedicated environment body (2 points) and prefer activity over existence where MUNIC asks both (fund used, council budget, civil-defence budget and staff). Buckets are grounded in the national distribution of all 5,570 municipalities: minimal 0–3 (bottom quartile), developing 4–6 (to the median), established 7–9, extensive 10–14 (top decile). The gap ladder's binary reads established and extensive as push-strong.

One calibration note, flagged open: the pilot cities sit in the national top half almost uniformly (49 of 50 land established or extensive), so the national cut differentiates the country well but the pilot set weakly — if the working group wants sharper separation among pilots, the binary can move to extensive-only or the ladder can consume the 0–14 score directly. Two source caveats travel with the profile: MUNIC components are prefecture self-declarations from 2020–2021 fieldwork, and CAPAG is a preliminary screen, not a credit approval.

The vulnerability boundary is structural: nothing in the city profile reads poverty, income or vulnerability. Those belong to Impact (AdaptaBrasil), and grant windows that target vulnerability enter through funder criteria in the route model, never by re-reading the vulnerability index.

## The intervention profile (to build)

Cost band and type come from the intervention catalog (I Care / C40); the sector and adaptation-eligibility tag that matches an intervention to funds is not yet built. Until it exists, route eligibility can only be read at the city level, not matched fund-by-fund.

## The gap and the routes

The funding gap reads the two axes against the intervention's needs, ordered as an effort ladder (a money gap sits below a know-how gap because know-how can be bought in). Route eligibility then determines whether a gap has a path:

| Route | Gate held in the profile | Gate still to build |
|---|---|---|
| A — programmatic funds and credit lines | credit arm: `credit_screen`; grant arm: open | adaptation-eligibility of each fund |
| B — federal transfers (Transferegov, Novo PAC) | finance-push (formulation capacity) | programme-level matching |
| C — direct external borrowing (MDB + Union guarantee) | `credit_screen` pass required | COFIEX practice, size threshold |
| D — international grant facilities (GCF, GEF, AF) | none (intermediated, not an open application) | accredited-entity pathway map |
| E — disaster and civil-defence transfers | civil-defence components as readiness proxy | emergency-declaration trigger data |
| F — politically-allocated windfalls | not scored; context only | — |

The adaptation inversion lives inside route eligibility: for grant windows that deliberately target low-capacity, high-vulnerability cities, low fiscal capacity widens access rather than narrowing it, so the credit channel and the grant channel partly cancel and are modelled separately.

## Pilot scope

Release v1 profiles the 50 pilot cities from the CityCatalyst export. The pilot list arrived with two quirks, resolved and asserted in the notebook: Altamira carries no state and was matched by nationally-unique name to the Pará municipality, and Cruzeiro do Sul is the Rio Grande do Sul municipality, not the larger Acre namesake. The June 2026 snapshot splits the pilots 29 credit-screen pass to 21 fail-or-unknown, and the fiscally-gated cities span the full finance-push range, which is the premise of modelling the two axes separately.

## Build order

The city profile is done for the pilot. The next builds, in dependency order: the intervention sector / adaptation-eligibility tag (unblocks route matching); the fund-supply inventory with instrument, route and adaptation-eligibility per fund, including the non-climate-badged sanitation and disaster flows; the awards / revealed-fundability compile promoted from staging (evidence beside the score); and the per-intervention legal classification (I Care). Route-eligibility-only scoring can start on the held profile before fund-by-fund matching exists, mirroring the pre-read's recommendation.

### References

- Feasibility pillar pre-read (design authority) → https://docs.google.com/document/d/1TyCqsRmjyqFGu3gwL4JEjCWWGPoaf1p377QZPnbkiUk/edit
- City fiscal signal → `dataset-review/reviews/br-stn/br-capag/` (release 2026-06-01)
- Finance-push components → `dataset-review/reviews/br-ibge/br-munic/` (release 2020-2021)
- Brazil finance routes reference → `knowledge-base/topics/climate-finance/br-climate-finance.md`
- Awards staging compile → `dataset-compile/br-climate-awards/`
- Chile precedent (structure and lessons) → `dataset-review/reviews/oef/cl-city-action-fundability/methodology.md`
