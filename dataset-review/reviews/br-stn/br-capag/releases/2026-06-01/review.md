# Review — STN CAPAG Municípios, release 2026-06-01

What this release's data can and cannot support. Dataset-level facts (license, provenance, methodology, parsing) live in the review README one level up.

## Scope and status

This release contains one committed table and the notebook that produced it. The table covers all 5,568 published municipalities with the published CAPAG and ICF grades, the three fiscal indicators with their grades and status columns, the Treasury's explanatory observation text, and a derived credit screen stamped with the rule version `capag-icf-2026-06`. Status: research release; no production approval; promotion to the catalog is pending.

References:

- clean table → `data/br_capag_municipios_clean.csv`
- extraction and fit evidence → `capag_extract_clean.ipynb`
- raw workbook (gitignored, re-download steps in the review README) → `sample/capag-municipios-posicao-2026-jun.xlsx`

## Visual summary

Under the versioned screen, 2,358 municipalities (42.3%) pass, 1,984 (35.6%) fail on the published fiscal grade, 674 (12.1%) fail on information quality regardless of their displayed letter, and 552 (9.9%) are unknown. The geography is sharply uneven: pass rates run from 87% in Rondônia and about 81% in Espírito Santo and Santa Catarina down to 13% in Roraima and 0 of 16 municipalities in Amapá, with the South and parts of the Centre-West well above the national rate and most of the North and Northeast well below it. Run the notebook for the rendered charts; the precise figures are in the tables and sections below.

## What this data supports

The claims are mostly about a preliminary, dated screen for one family of finance routes, and the load-bearing caveat is that the screen is derived from CAPAG and ICF together under a versioned rule, never from the published letter alone.

"As of the June 2026 CAPAG snapshot (fiscal base year 2025), municipality X passes the preliminary CAPAG/ICF screen for credit routes that require a Union guarantee." This is valid when `credit_screen` is `credit_screen_pass`, and only with the date attached: the source is aligned with the Treasury's preliminary calculation and is republished during the year.

"Municipality X's published CAPAG grade is B+ in the June 2026 snapshot." Quoting the published grade, the published ICF, an indicator value or the observation text is supported at any time, provided the snapshot date travels with the value.

"2,358 of 5,568 municipalities (42.3%) pass the preliminary CAPAG/ICF screen in this release." National and by-state counts and shares of the four derived states are supported as descriptive statistics of the snapshot; the notebook's fit section is the evidence.

"A Union-guaranteed credit route is unlikely to be open to municipality X at present." This is supported as a negative screening statement when the derived state is a fail, subject to the documented regulatory exceptions noted in the review README.

## What this data does not support

The overclaim to watch for is treating a screening category as a credit decision, or treating the published letter as the decision variable.

"Municipality X is credit-eligible" or "municipality X can borrow" is not supported in any form. Formal approval considers the specific operation, counter-guarantees, limits and other legal conditions; the derived state is deliberately named `credit_screen_*` and not `credit_eligible`.

Any use of the published CAPAG column alone as an eligibility flag is not supported: 186 municipalities display `A` or `B` while graded `Dicf`, which the rule effective in 2026 makes ineligible. The screen must come from `credit_screen` or an equivalent CAPAG-and-ICF derivation.

A numeric fiscal-capacity score is not supported. Converting `A+` through `D` to evenly spaced numbers invents a scale the methodology does not define; the grades are regulatory categories.

Recomputing grades from the displayed indicators is not supported. The savings grade cannot be reproduced from the displayed savings indicator (1,026 of 5,126 checkable rows mismatch the published thresholds because the grade uses a three-exercise weighted value), so any re-derivation would silently disagree with the published result.

Averages, rankings or scores built on the raw indicator values are not supported without filtering: seven municipalities carry reporting-artifact savings ratios (from −1.77 up to 28,123), which would dominate any unfiltered aggregate.

Statements about grant, transfer, intermediated or other non-guaranteed finance routes are not supported; the dataset informs only routes subject to a Union guarantee, and a failing screen must not lower those other routes.

A complete-national-coverage claim is not supported: one code present in the workbook's internal sheet is absent from the published result, and Calçoene's row is entirely the `#N/A` error token.

## Using it downstream

Join on `municipality_code` read as a seven-character string; municipality names are not unique nationally and are never join keys. Keep the four derived states separate — `credit_screen_unknown` is an absence of evidence, not a fail — and preserve `n.d.`, `n.e.` and `#N/A` rather than collapsing them. Apply the screen only to the guaranteed-credit arms of the feasibility routes; leave grant and transfer routes untouched by it. When a new snapshot is ingested, derive the screen again under an explicitly named rule version, since both the data and the eligibility rule change over time. For the finance-push capacity axis, pair with the IBGE MUNIC complement named in the review README rather than stretching CAPAG beyond fiscal screening.

## Notes on non-obvious fields

- `indicator_*_status`: `ok` means a numeric value is present; `n.d.` is the source's not-calculated sentinel; `#N/A` is a literal Excel error token published in the source, not a parsing failure.
- `grade_savings` is not a function of `indicator_savings` (three-exercise weighting; see above). `grade_debt` and `grade_liquidity` do reproduce exactly from their indicators.
- `capag` keeps the literal string `#N/A` for Calçoene (`1600204`) on purpose.
- `observation`: original Treasury wording with embedded line breaks flattened to ` | `; 810 municipalities carry text, 673 of them multi-issue.
- `credit_screen_rule`: the rule version stamped on every row; a future release may carry a different rule without ambiguity.

## Traceability

- Source resource, SHA-256 of the retrieved workbook, regulatory references and the licence are recorded in the review README one level up.
- Extraction, validation assertions and fit evidence: `capag_extract_clean.ipynb` (restart-and-run-all passes against the workbook in `sample/`).
- Review and derivation rules drafted 2026-07-30 from the June 2026 workbook; the derived-state definitions match the review README's fit section.
