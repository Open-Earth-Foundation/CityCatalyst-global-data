# Review — Transferegov discricionárias e legais, release 2026-07-17

## Scope and status

This release is one table: every proposal in the 17 July 2026 Transferegov snapshot (about 1.15 million), each with its programme, recipient, instrument, the first date of each administrative stage, and each stage's amount in its own column. The extraction and fit notebook produces it and holds every figure quoted here. The table is too large to commit and is regenerated in the gitignored sample folder. **Status: research only, not production-approved.** The proposed fit verdict (conditional fit for tracing federal transfers, weak fit for adaptation evidence) and the unresolved licence are recorded in the review README.

Most claims below are about city applicants: municipal governments and public consortia with a valid IBGE code, 791,928 of whom submitted a proposal for analysis.

### References

- Extraction and fit notebook → `transferegov_extract_fit.ipynb`
- Release table (gitignored) → `sample/br_transferegov_proposals_2026-07-17.csv.gz`
- Fit verdict, licence, parsing notes → `../../README.md`
- Stage definitions and analytical rules → `../../methodology.md`

## Visual summary

The notebook's charts show three things. First, a steep funnel: in each submission year, roughly one city proposal in five is signed and about one in six receives federal cash, with no steady trend across 2010–2022. Second, two different clocks: signature almost always comes within a year of submission, while first cash comes one to three years after signature. Third, the content: federal cash to cities runs mainly through the Ministry of Cities and the regional development ministry, road paving dwarfs every adaptation theme, and water supply is the only adaptation theme above R$1 billion disbursed. Run the notebook for the rendered charts.

## What this data supports

The claims are mostly about how federal transfers to cities move from request to cash, and how long that takes. The load-bearing caveat is follow-up time: recent proposals have not had the chance to reach later stages.

A city's proposal can be followed from submission to signed agreement, federal disbursement and onward payment, with the date and amount of each stage, as long as it was submitted after April 2010. For example: "Proposal X was submitted in March 2018, signed in October 2018, and received R$1.2 million of federal cash between 2019 and 2021."

Historical conversion rates can be stated for cohorts with enough follow-up. For example: "Of city proposals submitted for analysis in 2015–2019, about 20% were signed and about 16% received federal cash by July 2026." This holds only for cohorts with at least 12 months of follow-up for signature and 36 months for disbursement, and it describes what happened, not the odds for a new application.

Stage timing can be quoted from fully observed cohorts. For example: "Half of signed city agreements are signed within about 4 months of submission; half receive their first federal cash about 17 months after signature."

A funded project in some adaptation themes can serve as a comparable past case when the match has been checked. For example: "In the July 2026 Transferegov snapshot, 1,292 city water-supply agreements have received federal cash, with a median federal share of about R$0.5 million." This holds for themes where the screen is reliable (water supply, and slope stabilisation after a check), and the match is OEF's classification, not the source's.

A Novo PAC formalisation proposal can be traced to its agreement and payments. For example: "Of 5,323 Novo PAC formalisation proposals, 5,161 are signed, 2,631 have received federal cash and 1,329 show payments to suppliers."

## What this data does not support

The overclaim to watch for is turning an administrative record into a statement about finance access or adaptation. The data records what happened to applications in one federal system, not what a city could get or what worked.

"Drainage projects are easier to finance than slope projects" is not supported. Conversion differences between themes also reflect the programme, applicant capacity, project quality, place, year and instrument, and the theme labels themselves are unadjudicated.

"This city never received federal money for flood control" is not supported. Proposals before April 2010 lack submission events, disaster response and much Novo PAC work may sit outside this module, and the theme screen misses projects described in other words. The honest form is "no matching record found in the reviewed sources and period".

"R$193.6 billion was committed to these cities" is not a statement of secured money. Commitments are budget reservations that are regularly cancelled and reversed (69,715 negative commitment events), and 12,474 agreements hold a positive net commitment without a signature.

"The project was completed" is not supported. Payment shows money leaving the agreement account, not physical delivery, service quality or any climate outcome.

"The 2019 or 2023 change of federal government led to more cancellations" is not supported. The share of signed agreements later annulled, rescinded or cancelled falls for recent signing years mainly because cancellations build up over time.

"About 4% of federal transfers to cities are for adaptation" is not supported. The 4% is a keyword-and-programme screen of proposal counts with uneven precision, not a classified share of money.

"Programme 1027 funded disaster prevention in this city" needs a check of the object text. The prevention programmes also paid for rural roads, bridges and fords.

## Using it downstream

Count at proposal grain. A proposal linked to several programmes is counted once, and amounts from different stages are never added together because they are the same money at different points.

Show only matches that have been adjudicated. The theme screen in the notebook is a candidate list for the Phase C mapping; water-supply matches are near-clean, slope and flood matches about five in eight, drainage and disaster-risk matches about three in eight on a sample of eight each. Paving projects that mention drainage (18,643 proposals) are kept apart and should not count as drainage without review.

Take commitment from the event file, not from the agreement's own total, which disagrees for 7,833 agreements. Keep payments back to the recipient out of onward payment. Keep the stage-order exceptions (12,474 committed but unsigned, 7,211 disbursed without net commitment, 246 paid without disbursement) as flags rather than repairing them.

Always show the proposal or agreement number with any record, so it can be matched against Novo PAC lists, SADIPEM or the Transparency Portal and never counted twice. Until the licence is resolved, use the data for internal analysis and guidance design only, not for records displayed in the product.

## Benchmark values a city can use

These are comparator priors from funded city agreements (those with federal cash disbursed), not guarantees. Amounts are nominal reais across 2008–2026 with no deflator, so they understate recent costs, and theme membership comes from the unadjudicated screen.

To understand the typical scale, a funded city agreement carries a median federal share of about R$0.3 million (middle half R$0.24 to 0.53 million). Adaptation-theme agreements are larger:

| Theme | Funded agreements | Federal share, median | Middle half | Counterpart, median | Signature to first cash, median |
|---|---:|---:|---:|---:|---:|
| Water supply and drought | 1,292 | R$0.51 m | R$0.29–1.50 m | 1.0% | 22.7 months |
| Drainage and stormwater | 426 | R$0.61 m | R$0.29–1.88 m | 2.9% | 18.9 months |
| Disaster risk and response | 319 | R$1.00 m | R$0.39–4.69 m | 3.0% | 12.9 months |
| Slope stabilisation | 147 | R$1.18 m | R$0.41–4.96 m | 2.2% | 17.6 months |
| Green and nature-based | 116 | R$0.48 m | R$0.25–0.81 m | 3.7% | 19.4 months |
| Erosion control | 46 | R$0.80 m | R$0.50–1.20 m | 3.0% | 21.0 months |
| Flood control | 28 | R$1.09 m | R$0.46–7.27 m | 3.8% | 18.1 months |
| All funded city agreements | 118,545 | R$0.30 m | R$0.24–0.53 m | 3.2% | 17.1 months |

To replicate a funded project, the counterpart a city puts in is small, typically 1 to 4% of the agreement value, and the federal share carries the project. Planning should allow about 18 months to two years from signature to the first federal cash, and longer for water supply.

To generalise, the route is proven at volume for water supply and at modest volume for drainage, disaster risk and slope works. Flood control, erosion and nature-based projects have too few funded agreements (under 150 each) to treat these figures as more than indicative.

## Notes on non-obvious fields

`is_submitted` is False for proposals that were never sent for analysis and for 2008–2009 proposals whose submission was never recorded; the two cannot be told apart, so it is not a draft flag for early years.

`vl_pago_net_cent` is onward payment to suppliers and other creditors; `vl_pago_convenente_net_cent` is money moved back to the recipient itself and is not spending on the project.

`vl_empenho_net_cent` can be zero or negative on disbursed agreements, because commitments are later cancelled even after cash has moved.

All amount fields are integer centavos, so divide by 100 for reais.

`qf_` columns flag the named stage-order exceptions; they mark records to show with care, not errors to drop.

## Traceability

The source is the Transferegov.br open-data export of Discricionárias e Legais, downloaded as the 17 July 2026 snapshot; file hashes and re-download steps are in the review README. The raw files are local-only in the gitignored sample folder, and a fresh download will not match this snapshot's pinned counts because the publisher replaces the files continuously. The theme screen's precision read (eight sampled matches per theme) was done during the notebook build on 24 September 2026 and has not been adjudicated; Phase C will record the adjudicator and date.

### References

- Publisher open-data portal → https://api-publica.transferegov.gestao.gov.br/
- Snapshot hashes and re-download → `../../README.md` (Profile section)
- Originating need → `dataset-discovery/needs/2026-09-br-finance-pathways-review/search.yaml`
