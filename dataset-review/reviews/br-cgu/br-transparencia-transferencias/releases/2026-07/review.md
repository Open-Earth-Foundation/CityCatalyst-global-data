# Review — br-transparencia-transferencias, release 2026-07

## Scope and status

Research release, not production-approved. The release holds the federal civil-defence payments from the Portal da Transparência monthly transfer files for January–July 2026: 743 rows paid by MIDR's civil-defence secretariat (Sedec) under action 22BO (response and recovery, 740 rows) and action 8348 (emergency mitigation works, 3 rows), R$ 596.0 million in total. The extraction notebook filters them from 1,056,421 rows and reproduces every count and exact sum in the README profile; the release builder writes a bilingual payment table with English descriptions and paired source Portuguese `*_pt` fields. A second notebook maps the two budget actions conservatively to the adaptation action bank. Its charts are rendered inline; this review carries the figures as tables. Dataset-level facts (provenance, licence, parsing, methodology and the proposed fit verdict) sit in the README one level up. The payment table is not committed while its public-redistribution basis is unconfirmed. It is written to this release's `sample/` folder from the monthly export; the three-row budget-action crosswalk stays in `data/`.

### References

- Extraction notebook (also renders the charts) → `transferencias_extract_clean.ipynb`
- Bilingual release builder → `build_bilingual_release.py`
- Payment table → `sample/br_transparencia_transferencias_civil_defence_payments.csv`
- Adaptation mapping notebook → `map_adaptation_actions.ipynb`
- Crosswalk to the adaptation action bank → `data/br_transparencia_transferencias_to_adaptation_actions.csv`
- Monthly source ZIPs (not committed) → `sample/2026MM_Transferencias.zip`

## Visual summary

Monthly civil-defence payments ranged from R$ 34 million in January to R$ 149 million in May, and nearly all of it went through action 22BO; action 8348 shows up only in February, March and April. The money is concentrated: Rio Grande do Sul, Minas Gerais and Pará received about 62% of the total. Most payees appear once: 406 of 532 were paid in a single month, and only 9 in four or five months. Within 22BO, 77% of the amount sits under budget labels that combine response and recovery, and none names a single phase. Run the notebook for the charts.

## What this data supports

The claims below are about cash that actually left the federal budget for named public bodies, by month. The load-bearing caveat is that a row is a payment, not a project or a transfer decision.

"Between January and July 2026, the federal government paid R$ 574.6 million to states and municipalities under civil-defence action 22BO (response and recovery) and R$ 21.4 million under action 8348 (emergency mitigation works)."

"Municipality X received R$ Y in federal civil-defence payments between January and July 2026." This holds when the figure is summed from this table by payee CNPJ, and the claim names the payee, which is not always the municipality itself (some payees are state civil-defence bodies or disaster funds).

"Federal prevention-and-mitigation payments were small next to response and recovery in early 2026: three payments to two municipalities, about 4% of the civil-defence total." This holds for actions 8348 and 22BO only; other federal prevention money (for example action 14RL, coastal erosion) is outside this extract.

"In January–July 2026, civil-defence payments concentrated in Rio Grande do Sul, Minas Gerais and Pará, which together received about 62% of the total."

"Municipality X has a precedent of receiving federal disaster money under Lei 12.340." This is the route-level evidence the finance-pathway guidance needs: it shows that the legal-transfer route has reached that payee, not that it will again.

## Mapping to adaptation actions

The mapping links each budget action, not each payment, to the ICB × OEF adaptation action bank (V13), because no payment says what it financed. It retains only three source-supported component links, all at medium confidence and pending adjudication. Looser thematic links were excluded to prevent route-level evidence from becoming a payment-level claim.

| Budget action | Adaptation action | Match type | Evidence behind the link |
|---|---|---|---|
| 8348 | Stabilise, inspect and maintain slopes in landslide-prone areas | component | 3 payments, 2 municipalities, R$ 21.4 million |
| 8348 | Improve climate-resilient water and sanitation infrastructure | component | same 3 payments |
| 22BO | Climate-responsive social protection and post-disaster financial support programmes | component | 740 payments, 530 payees, R$ 574.6 million |

The evidence column is the whole budget action's evidence repeated on each link, never a share of it, so it must not be summed down the table. The 8348 links are specific but rest on three payments; the 22BO link rests on hundreds of payments but still cannot classify any single payment. A claim this supports is "the Lei 12.340 legal-transfer route can fund slope stabilisation and post-disaster support for municipalities". A claim it does not support is "municipality X financed slope stabilisation": the Boa Vista payments could equally have gone to drought water-supply works. The 34 unreached actions, including early warning, drainage and resettlement, reflect the strict mapping threshold and what these two budget actions fund, not evidence that cities cannot finance them.

## What this data does not support

The overclaim to watch for is treating payment rows as projects or as decisions. Every anti-claim below follows from that.

"Sedec financed 743 projects in 2026." No: 743 is a count of monthly payments. The same payee and budget classification recur across months, and there is no project, portaria or agreement identifier to group rows into projects.

"Municipality X was granted R$ Y for its recovery works." No: the authorised amount sits in the Sedec portaria, and the payments here may be one instalment of it or several authorisations added together.

"R$ Y went to response and R$ Z to recovery." No: no 22BO budget label names a single phase, and 10% of the 22BO amount is booked under `Múltiplo`. The expense group (current versus investment) is not a proxy for phase.

"Municipality X had no mitigation project in 2026." No: the only defensible statement is that no payment under action 8348 was found for that payee in January–July 2026. Mitigation money can come through other actions, other ministries or later months.

"This is the municipality where the money was spent." Not always: the payee can be a state civil-defence body, a fire brigade or a disaster fund, so the geography is the payee's, not necessarily the affected area's.

"These figures are final." Not established: whether CGU revises published months is unanswered, so a figure should cite the release month and download date.

## Using it downstream

Five rules keep downstream use inside what the data can carry.

Keep rows at the monthly grain until a grouping rule exists, and sum only by payee, month, action or UF. Any rollup to "transfers" or "projects" waits for a link to the Sedec portarias, and that link will be probabilistic (payee, amount, timing), so it must carry a match confidence.

Use the action as the only phase field: 8348 means prevention and mitigation; 22BO means response and/or recovery, undivided.

Keep the payee identity and the SIAFI municipality side by side. Converting to IBGE codes needs a name-plus-UF join (523 of 526 match directly; three need spelling aliases).

Present amounts as payments in a named month, citing the release, and keep the raw amount string for audit.

Show adaptation-action links only after adjudication, as route-level precedent ("this federal route has funded this kind of action"), never attached to an individual payment or payee.

## Benchmark values a city can use

These figures describe what a civil-defence payment under Lei 12.340 looked like in January–July 2026. They are comparator priors from seven months of a disaster-heavy year, not guarantees, and they describe payments, not authorised transfer sizes. Amounts are nominal BRL.

To understand the size of the route, the typical municipal payment and the typical total per municipal payee were:

| Measure (action 22BO, municipal payees) | Median | Interquartile range | Range |
|---|---:|---:|---:|
| One monthly payment (725 rows) | R$ 500,000 | R$ 234,000 – 873,000 | R$ 5,600 – 11.6 million |
| Total per payee, Jan–Jul (522 payees) | R$ 656,000 | R$ 299,000 – 1.16 million | R$ 5,600 – 33.2 million |

*Worked example: a municipality in the middle of the distribution received about R$ 0.5 million in one payment, and about R$ 0.66 million over the seven months; one in five municipal payments was R$ 1 million or more.*

To replicate the route, three features show up in the data:

- **Mostly current spending:** 60% of the 22BO amount is booked as current expenditure (contributions) and 33% as investment (grants for works), the rest aggregated. Money for response and recovery arrives mainly as operating money, not only capital.
- **Often staged:** 121 of 522 municipal payees received 22BO payments in two or more months, consistent with releases in instalments.
- **Prevention is rare:** the three 8348 payments were R$ 12.0 million and R$ 9.2 million to Boa Vista/RR and R$ 0.28 million to Vera Mendes/PI. Three payments are too few for a benchmark; they show the route exists, not its typical size.

To generalise, the route is proven where disasters hit: Rio Grande do Sul (116 municipal payees), Minas Gerais (102) and Pará (84) account for most payees, and 25 UFs appear at least once. The learning for a city is that this is reactive money that follows a recognised disaster, so it is evidence of a route a city can use after an event, not of a prevention budget it can plan against.

## Notes on non-obvious fields

- `amount_transferred_brl`: cash paid in the month, never an authorised or project amount. `amount_transferred_raw` keeps the published string.
- `is_multiple_classification`: true on 38 rows booked across more than one budget classification (codes `MU` or `-14`, names `Múltiplo`); their classification fields cannot be read as single values.
- `beneficiary_code` and `beneficiary_name_pt`: the payee, which can be a state body or a disaster fund; `municipality_name` is empty on the 12 state-level rows.
- `siafi_municipality_code`: a SIAFI code, not an IBGE code; kept as text with leading zeros.
- `budget_plan_name_pt`, `subtitle_name_pt` and `localizer_name_pt`: published with truncation, the `REPOSTA` typo and placeholder Medida Provisória numbers; do not correct them.
- `transfer_type_pt`: the source merges legal, voluntary and specific transfers into one value, so the instrument comes from the action, not this field.
- `translation_status`: `complete_exact_release_dictionary` means every descriptive Portuguese value observed in this release has an explicit English dictionary entry; it does not mean proper names were translated.
- `proper_name_translation_status`: `not_translated_source_proper_name_preserved` means municipality and beneficiary legal names remain source identifiers in both paired name fields.

## Traceability

Source: CGU Portal da Transparência, Recursos transferidos, monthly files 2026-01 to 2026-07, downloaded 24 September 2026 (July ZIP MD5 `14cc4c826bb836ff16aec4f33c3c1ab6`). The bilingual release builder asserts the file hash, 743-row count, exact R$596,018,315.06 total, action counts and sums, 14-digit CNPJs, complete translation-dictionary coverage, paired Portuguese fields and preservation of known source defects. The extraction notebook contains the broader per-month, source-wide and geography checks; its code was checked sequentially after the bilingual update, but the stored rendered outputs predate that update because no Jupyter runtime was available in this environment. The IBGE join test uses the IBGE municipality list from the br-munic review; no IBGE crosswalk is committed. The adaptation crosswalk was drafted against the V13 action bank (local-only export), narrowed to three source-supported component links on 24 September 2026, and remains pending human adjudication. Extracted 24 September 2026.

### References

- Review README → `../../README.md`
- IBGE municipality list (join test only) → `dataset-review/reviews/br-ibge/br-munic/releases/2020-2021/data/br_munic_finance_push.csv`
