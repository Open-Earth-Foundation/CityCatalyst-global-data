# Review — cl-municipal-capacity-tier, release v1

## Scope and status

Research, not production-approved and not in a pipeline. The release holds one derivation notebook and one classified table covering all 345 comunas. The notebook reads only the INE census release, applies the two methodology rules and validates their bracket boundaries directly. Restart-and-run-all passes.

Dataset-level facts, meaning the two rules, the licence position, the interpretation warnings and the parsing traps, live in the README one level up and are not repeated here. This document is the contract for what the classification can and cannot be used to say.

| Check | Result | Status |
| ----- | ----- | ----- |
| Comunas covered | 345 | verified |
| Tier split T1 / T2 / T3 / T4 | 57 / 113 / 133 / 42 | verified |
| Input datasets read | INE Censo 2024 only | verified |
| Rows outside their population bracket | none | verified |
| Population share in T3 and T4 | 10% | verified |
| T4 score band | 0.10, provisional | unanswered |
| T1 evidence gate on SECPLA and investment history | not joined, assigned on population | unanswered |

## Visual summary

The two charts in the notebook make one point between them: the shape of the country flips depending on whether comunas or people are counted. By comuna the distribution is bottom-heavy, with 133 comunas in T3 and 42 in T4. By population it inverts, with 57 T1 comunas holding 63% of Chileans and the whole of T4 holding 106,357 people, about 1%. Any national statement about municipal capacity has to say which of the two it is weighting by, because the honest answer differs. Run the notebook for the rendered charts.

## What this data supports

The claims here are about which of four capacity bands a comuna sits in, and the condition attached to nearly all of them is that the band is a proxy derived from population rather than a measurement of the municipality.

A comuna can be placed in one of four technical-capacity tiers, and the placement is fully reproducible by anyone holding a census population figure and the two published rules. There is no residual judgement inside the classification to replicate or dispute.

The classification can be stated as commercially reusable. Its only data input is the INE census under CC BY-SA 4.0, so attribution and share-alike apply where required, but there is no non-commercial term.

The tier is fully reproducible from the stated census population and bracket rules. No former-source comparison table is needed to build or validate it.

The tier can be quoted as what determines whether an action needs technical assistance in the consuming model. A T1 comuna escalates on nothing, T2 on infrastructure, T3 on anything beyond a regulation, and T4 on every action type. Stating the tier alongside that consequence is more useful to a reader than the bare number.

National statements about the prevalence of low capacity are supportable, with the weighting named. Just over half of Chilean comunas, 51%, sit in the two lowest tiers, and those comunas are home to 10% of the population.

## What this data does not support

The overclaim to watch for is any sentence in which the tier stands in for a fact about a municipality's actual institution. The classification knows one thing about each comuna, its population, and everything else is inference from a published rule.

Do not say that one comuna has more technical capacity than another comuna in the same tier. Every comuna inside a tier carries an identical score by construction, and the staffing data this replaced showed the genuine within-tier spread is large enough to reverse many such comparisons.

Do not say that a T1 comuna has a planning unit or a record of executing public investment. The published rule attaches that condition to the T1 score, but no SECPLA or investment-execution evidence is joined in this release, so T1 is assigned on population alone.

Do not report the T4 score as decided. It is provisional at 0.10, flagged per row by `t4_provisional`, and the value is consequential rather than cosmetic: at 0.10 every action type escalates to technical assistance across all 42 T4 comunas.

Do not rank comunas, or read the gaps between bands as measured quantities. The bands are tunable settings chosen to express an ordering, in the same way the feasibility score bands are, and the distance from 0.25 to 0.50 encodes no estimated difference in capability.

Do not treat a low tier as a reason to score an action lower on impact or alignment. A low tier means harder to deliver locally, or needs an external route, and it belongs in a feasibility reading only.

Do not quote a figure of 346 comunas. The source methodology note uses that number throughout, but its own workbook and the census both hold 345, which is what this release covers.

Do not treat this as a time series. It is a single classification from a single census, and a comuna near a bracket edge can change tier on a small population revision without anything about the municipality having changed.

## Using it downstream

Join on `comuna_cut` as a string. This release deliberately carries no city locode: a consumer that needs city identity resolves it through the administrative-boundary lookup, which keeps the identity mapping in one place rather than duplicating it per dataset.

Consume `capacity` where a 0–1 axis is needed and `gl_technical_capacity` where the MEED's native 0 to 100 scale is expected. They are the same value and must never be treated as two measures. Carry `capacity_basis` through any derived table, because it is what lets a consumer tell this classification from the staffing blend that preceded it without inspecting the numbers.

Respect `t4_provisional`. A consumer building anything reportable should either exclude those rows or surface the flag, because the underlying band has not been adjudicated.

Pair this dataset with the census review for population provenance and vintage, and with the SIM/BEP review for the financial-autonomy axis if a full v3 city profile is being assembled. A two-by-two built from population-derived capacity and transfer dependency is a coarse partition rather than two fully independent readings.

The consuming model is the Chile city-action fundability review, whose v3 release reads this table for its capacity axis. Any change to the bands here changes routes and scores there, so the two releases move together.

## Notes on non-obvious fields

`tramo` follows the VEM numbering, where T1 is the largest comuna and T4 the smallest. The workbook that publishes this classification numbers its own raw column the opposite way. Anyone cross-checking by hand has to homologate first.

`gl_technical_capacity` and `capacity` are one value on two scales, not two independent measures.

`capacity_basis` records which rule produced the value. It exists so a stale row is identifiable in a downstream table without archaeology.

`t4_provisional` marks rows whose score depends on a band that has not been decided. It is not a data-quality flag: those rows are as well derived as any other, but the constant behind them is still open.

`population` is the INE Censo 2024 count. Cabildo sits at 19,983, just below the 20,000 boundary, and is therefore especially sensitive to a later population revision.

## Traceability

Population comes from the INE census review in this repo. The bracket definition and scoring band come from the MEED methodology documents of June 2026, whose copies are held with the consuming model's v3 release. The notebook reads no comparison dataset: it checks all rows against the bracket boundaries and score map directly.

**References**

- derivation and validation: `01_capacity_tier.ipynb`
- classified output: `data/municipal_capacity_tier.csv`
- population source: `reviews/cl-ine/cl-ine-censo/releases/2024`
- consuming model: `reviews/oef/cl-city-action-fundability/releases/v3`
- source methodology documents: `reviews/oef/cl-city-action-fundability/releases/v3/sample/`
