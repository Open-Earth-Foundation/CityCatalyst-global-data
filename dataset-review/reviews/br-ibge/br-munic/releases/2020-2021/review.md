# Review — br-munic, release 2020-2021

## Scope and status

This release contains one extraction notebook, one committed component table (one row per municipality, 22 columns), and the two raw bases in `sample/` with re-download URLs in the README. The notebook runs clean end to end (restart-and-run-all, all validation assertions passing, national counts pinned to the profiling pass). Status: research, not production-approved; promotion to the catalog is pending sign-off.

## Visual summary

The notebook's charts show three shapes. Declared institutional existence collapses to a much smaller active core when the survey asks about money or activity (roughly half for funds, a tenth for council budgets, a quarter for civil-defence budget lines). Component pass rates differ by region, with the South and Southeast leading on planning instruments and the North and Northeast on neither axis. The count of cleared core components forms a broad middle (most municipalities clear 2–4 of 6) with a thin top: only 54 municipalities clear all six. Run the notebook for the rendered charts; the exact figures are in the tables below and in the README's component map.

## What this data supports

The claims below are mostly about declared institutional presence, and the load-bearing caveat is that the prefecture reports on itself. Each claim is written to be liftable.

A municipality-level statement of the form "the prefecture of X declared, in the 2020 MUNIC survey, that it has an environment fund, and that the fund was used in 2019" is supported, at national coverage, joinable to CAPAG and other city data by the seven-digit IBGE code.

A transparent finance_push component breakdown is supported: eight named components, each traceable to specific MUNIC variables, each categorical per municipality, with unknowns carried explicitly. Ranking or grouping municipalities by how many core components they clear is supported provided refused municipalities are excluded rather than zeroed.

Comparative statements across regions or population bands are supported for any component, and the size gradient is steep enough to be a finding in itself: climate legislation runs from 3.7% of the smallest municipalities to 37.5% of the largest.

A dated capacity signal for the finance-feasibility method is supported with the reference window stated: 2020 for environment and civil defence, 2021 for planning instruments.

## What this data does not support

The overclaim to watch for is quietly upgrading a self-declared existence flag into functioning capacity.

"Municipality X has the capacity to formulate and manage climate-finance projects" is not supported; the data records declared structures, not their quality, staffing depth or track record.

"Municipality X has a climate plan" is not supported by any field in this release; `climate_legislation_status` records legislation on adaptation and mitigation, which may be an article in another law. Name the field, not the wish.

"Municipality X has no environment fund" is not supported for the 90 municipalities flagged `is_survey_refusal_2020`; their 2020 components are unknown, and any aggregate that counts them as "no" understates the country by construction.

"Municipality X participates in an intermunicipal consortium" is not supported at all in this release; MUNIC last measured it in 2015 and the component was deliberately dropped.

A smooth 0–1 finance_push score is not supported by the source's semantics; the components are categorical declarations, and any numeric composite is a methodology-owner decision layered on top, to be documented there rather than attributed to MUNIC.

Current-year statements are not supported: the environment and civil-defence declarations are from the 2020 edition (fieldwork September 2020 to March 2021) and cross two municipal administration changes by 2026.

## Using it downstream

Join on `cod_mun` as a seven-character string; never on names (non-unique, and the 2020 base strips apostrophes). Pair with the CAPAG review for the fiscal gate: CAPAG covers Union-guaranteed credit routes, this table covers the capacity to reach the rest; the two are disjoint by construction and complementary by design. Keep the Impact separation: nothing in this table measures poverty, income or vulnerability, and AdaptaBrasil variables must not be mixed into finance_push. Prefer activity over existence when scoring (`env_fund_used_status` over `env_fund_status`, `civil_defence_budget_status` over `civil_defence_body_status`); the existence flags remain in the table for transparency, not for scoring. Treat every `unknown` as missing, propagate it, and surface unknown counts in anything user-facing.

## Notes on non-obvious fields

`env_fund_used_status = "no_fund"` and `civil_defence_*_status = "no_body"` are skip-logic resolutions: the question was never asked because the parent structure is absent. They are semantically "no" for scoring but kept distinct so the filter is auditable.

`climate_training_status` has four states: `yes` (federal training on climate in the last four years), `env_training_other_topics`, `no_env_training`, `unknown`. It measures training received, not staff counts.

`env_council_budget_status = "council_inactive"` marks councils declared as never installed or inactive, a distinct state from having no council.

`planning_instrument_count` counts `Sim` answers across the 21-instrument battery of the 2021 legislation block (plano diretor excluded, held in its own column); it is null, not zero, for whole-block refusals. Compound answers ("Sim, com legislação específica") count as yes.

`climate_legislation_year` and `plano_diretor_year` are the declared years of the creating law, absent where the answer was no or unknown.

## Traceability

Inputs are the two pinned raw bases (SHA-256 in the README): `Base_MUNIC_2020.xlsx` and `Base_MUNIC_2021_20240425.xlsx`, retrieved from IBGE's FTP on 2026-07-30 via user download (direct container fetch is blocked). The component table is produced solely by `munic_finance_push_extract.ipynb`; every derivation rule is one notebook block citing one README parsing note. The consortium-drop decision was taken by the methodology owner on 2026-07-30 during this review. No taxonomy mapping (Phase C) applies: the release links to cities by IBGE code, and locode linkage is handled by the method's existing city reference, not duplicated here.
