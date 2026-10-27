# How Brazil city finance feasibility works — working methodology

**Status: working draft.** The pillar design is owned by the Feasibility pre-read (References); this document records how OEF implements its Financing component with the data actually reviewed, what is held, and what remains to build. It will change as the open decisions in the pre-read are confirmed.

## In one paragraph

Feasibility rests on two components: Legal (a per-intervention verdict, owned by I Care) and Financing. Within Financing, cost band is the only action-level field used to order actions. Credit status, finance-push capacity, six Brazilian finance routes and comparable projects are explanatory context for the city and the project-preparation module. They do not change the action ranking. Socio-economic capacity stays in Impact, while detailed budgets, delivery capacity and due diligence belong to project design.

## The city profile (held)

Two signals, both from vetted reviews, joined on the seven-digit IBGE code:

| Signal | Reads as | Source | Coverage |
|---|---|---|---|
| CAPAG + ICF, with the versioned credit screen | fiscal capacity; the hard gate on Union-guaranteed credit | br-capag release 2026-06-01 | national; all 50 pilots |
| finance_push components | ability to formulate and win a funded project | br-munic release 2020-2021 | national; all 50 pilots, no refusals |

The finance-push breakdown stays componentwise in every output, and the scoring is itself a dataset: every point comes from one row of the scoring-rules table, points subtotal into five families (environment governance 0–4, environment finance 0–3, climate-specific 0–2, civil defence 0–3, planning 0–2), the 0–14 total maps to a named bucket via the bucket table, and the per-city working-through is exported as the step-1 scores dataset. The rules give extra weight to a dedicated environment body (2 points) and prefer activity over existence where MUNIC asks both (fund used, council budget, civil-defence budget and staff). Buckets are grounded in the national distribution of all 5,570 municipalities: minimal 0–3 (bottom quartile), developing 4–6 (to the median), established 7–9, extensive 10–14 (top decile). The gap ladder's binary reads established and extensive as push-strong.

One calibration note, flagged open: the pilot cities sit in the national top half almost uniformly (49 of 50 land established or extensive), so the national cut differentiates the country well but the pilot set weakly — if the working group wants sharper separation among pilots, the binary can move to extensive-only or the ladder can consume the 0–14 score directly. Two source caveats travel with the profile: MUNIC components are prefecture self-declarations from 2020–2021 fieldwork, and CAPAG is a preliminary screen, not a credit approval.

The vulnerability boundary is structural: nothing in the city profile reads poverty, income or vulnerability. Those belong to Impact (AdaptaBrasil), and grant windows that target vulnerability enter through funder criteria in the route model, never by re-reading the vulnerability index.

## The action profile

Release v2 replaces the former 53-action pilot input with the supplied V13 final action bank. Its source CSV contains 37 adaptation actions with implementation timeline, indicative investment need and co-requisite, prerequisite and synergistic relationships. The cleaned v2 input retains the 32 actions that have at least one component-level impact score in `br-action-adaptation-impact/v1`; five unscored rows remain outside the release until they are assessed. This filter prevents the broader mitigation action inventory from entering the adaptation finance model.

The action bank still does not provide the fund-specific actor, sector and call-eligibility tests needed for automatic pathway matching. Exact action identifiers shared with existing finance crosswalks are useful draft links, but their original confidence and adjudication status still apply.

## The six finance pathways

The pathway names and their two explanatory fields are the published methodology contract. Release v2 preserves this wording and adds stable identifiers only for machine use. Later versions may add evidence or refine operational tests, but should not silently redefine the shared pathway descriptions.

| Pathway | City access | Further considerations |
|---|---|---|
| Domestic climate and environmental grants | The city applies where eligible or enables a state, consortium or civil-society partner to apply. Includes national, regional and state programmes. | Potentially relevant until actor, geography, sector, adaptation eligibility and call conditions are checked. |
| Domestic climate and infrastructure credit | The city or relevant service provider seeks reimbursable finance from BNDES, CAIXA/FGTS, a regional fund, state bank or another operator. | Conditional on the preliminary credit screen and on product, borrower, project and lender requirements. |
| Federal transfers and public investment programmes | The city formulates and submits a project through the applicable programme, including Transferegov arrangements or a Novo PAC selection. | Potentially relevant; programme fit and proposal readiness must be checked. Preparation support may be highlighted. |
| Direct external development-bank borrowing | A municipality proposes a larger operation through COFIEX and seeks a loan from an MDB, normally with federal authorisation and a Union guarantee. | Conditional on the preliminary credit screen, COFIEX process, guarantee requirements and lender appraisal. |
| International grant facilities | The city develops a concept with Brazil's National Designated Authority and an accredited entity such as BNDES, FUNBIO or CAIXA; the city does not apply directly to the facility. | Intermediation requires a partner route and the concept-development questions to verify. |
| Civil-defence and disaster finance | The city follows the MIDR/Sedec and S2ID process for prevention, response or reconstruction, as applicable. | Conditional on the legal trigger, action type, documentation and civil-defence process; hazard exposure alone does not make the route available. |

## The gap and the pathways

The funding gap reads the two axes against the intervention's needs, ordered as an effort ladder (a money gap sits below a know-how gap because know-how can be bought in). Route eligibility then determines whether a gap has a path:

| Pathway | Gate held in the profile | Gate still to build |
|---|---|---|
| Domestic climate and environmental grants | grant access is not closed by the credit screen | actor, geography, sector, adaptation eligibility and call conditions |
| Domestic climate and infrastructure credit | `credit_screen` is a preliminary city-side signal | product, borrower, project and lender requirements |
| Federal transfers and public investment programmes | finance-push components are a formulation-readiness proxy | programme fit, proposal readiness and programme-level matching |
| Direct external development-bank borrowing | `credit_screen` is a preliminary Union-guarantee signal | COFIEX practice, operation scale, guarantee requirements and lender appraisal |
| International grant facilities | none; the city cannot be treated as a direct applicant | National Designated Authority and accredited-entity partner route |
| Civil-defence and disaster finance | civil-defence components are a readiness proxy | legal trigger, S2ID process, documentation and action-type fit |

The adaptation inversion lives inside route eligibility: for grant windows that deliberately target low-capacity, high-vulnerability cities, low fiscal capacity widens access rather than narrowing it, so the credit channel and the grant channel partly cancel and are modelled separately.

## Pilot scope

Release v1 profiles the 50 pilot cities from the CityCatalyst export. The pilot list arrived with two quirks, resolved and asserted in the notebook: Altamira carries no state and was matched by nationally-unique name to the Pará municipality, and Cruzeiro do Sul is the Rio Grande do Sul municipality, not the larger Acre namesake. The June 2026 snapshot splits the pilots 29 credit-screen pass to 21 fail-or-unknown, and the fiscally-gated cities span the full finance-push range, which is the premise of modelling the two axes separately.

## Build order

The city profile is done for the pilot and the v2 finance context tables are built. The ranking implementation needs only the action cost band from this finance work. Future review can improve the contextual layer by adjudicating medium-confidence project-to-action matches, adding fund-specific actor and eligibility tests, and expanding the project record across programme cycles. Observed awards and execution records remain examples and preparation evidence, not inputs that silently change the ranking.

Release v2 publishes four small linked tables. `projects.csv` contains one row per observed project, proposal, financing operation or payment record. `project_action_matches.csv` contains the separate many-to-many links to adaptation actions. Each link records the matching approach, strength, review state and a fixed statement that it is illustrative rather than a final implementation recommendation. `datasets.csv` lists the ten publisher datasets that contribute records, with evidence stage, source URL and reuse conditions. `routes.csv` retains the six published route descriptions and names the contributing example datasets. A single notebook builds the record and match tables from the source reviews' clean tables and draft mappings, then validates schemas, joins and controlled matching terms. Only records from sources cleared for redistribution are committed; the full catalogue, including Novo PAC, COFIEX and CGU, stays in the gitignored `sample/` folder. The V13 action bank is held in the release data folder as the notebook's input.

### References

- Feasibility pillar pre-read (design authority) → https://docs.google.com/document/d/1TyCqsRmjyqFGu3gwL4JEjCWWGPoaf1p377QZPnbkiUk/edit
- City fiscal signal → `dataset-review/reviews/br-stn/br-capag/` (release 2026-06-01)
- Finance-push components → `dataset-review/reviews/br-ibge/br-munic/` (release 2020-2021)
- Brazil finance routes reference → `knowledge-base/topics/climate-finance/br-climate-finance.md`
- Brazil finance source reviews and candidates → `dataset-discovery/needs/2026-09-br-finance-pathways-review/candidates.yaml`
- Chile precedent (structure and lessons) → `dataset-review/reviews/oef/cl-city-action-fundability/methodology.md`
