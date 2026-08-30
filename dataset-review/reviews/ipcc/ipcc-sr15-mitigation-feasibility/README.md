# IPCC SR1.5 — Chapter 4 Supplementary Material (mitigation feasibility)

Dataset review entry for the **approval-version** supplementary material to *Global Warming of 1.5°C* (IPCC SR1.5), **Chapter 4** — *Strengthening and Implementing the Global Response*. The PDF is the canonical source for **multidimensional feasibility** assessments of **mitigation options** (economic, technological, institutional, socio-cultural, environmental, and geophysical dimensions), including the SM tables (e.g. 4.SM.5–4.SM.6 methodology, 4.SM.7–4.SM.15 option-level matrices) and evidence/agreement annotations.

## Canonical download

- **SR15_Approval_Chapter_4_SM.pdf** (IPCC, 2019 approval layout):  
  [https://www.ipcc.ch/site/assets/uploads/sites/2/2019/05/SR15_Approval_Chapter_4_SM.pdf](https://www.ipcc.ch/site/assets/uploads/sites/2/2019/05/SR15_Approval_Chapter_4_SM.pdf)

Landing context for the full Special Report: [https://www.ipcc.ch/sr15/](https://www.ipcc.ch/sr15/)

## Why we use it

- **Authoritative** global synthesis of feasibility for discrete mitigation options (as of the SR1.5 cycle), with per-indicator **A / B / C** (and related) codings traceable to the published tables.
- **Stable priors** for action- and city-level workflows that need a literature-backed baseline before local data are applied (extracted CSVs and the scoring engine live in `releases/2018-v2/`).
- **Explicit provenance** for HIAP / MEED–style scoring: every derived cell should map back to a table and row in this document.

## Spatial and temporal scope

- **Geography:** global assessment (not city-specific); use as **prior**, then adjust with local indicators where methodology allows.
- **Temporal reference:** SR1.5 assessment period (published 2018; approval PDF dated 2019 on the IPCC site). Treat as a **2018-vintage** evidence base when comparing to AR6 products.

## Releases

Two releases sit side by side. The IPCC evidence base is identical in both — SR1.5 is a 2018 vintage and there is no newer per-option feasibility assessment — so the second release is a **scoring-methodology** version, not a new publisher vintage.

| Release | What it is |
|---|---|
| `releases/2018` | The original scorer, kept as the pre-change baseline. Do not extend it; it exists so the 2018-v2 comparison has something to be measured against. |
| `releases/2018-v2` | Current. Adopts **one city indicator, one channel** (CC-718): six bridge rows retired and one re-issued so no city measurement reaches an action score through more than one SR1.5 indicator. Also corrects the scoring formula published in `review.md`, splits the shrunk and unshrunk action scores in the API contract, and regenerates the sample payload from the notebook. |

Neither release is production-approved. The served scores come from a SQL function in `CityCatalyst/global-api` reading the chain table; until that table is reloaded from 2018-v2, the API returns `2018` behaviour. Required changes are listed in `releases/2018-v2/data/api/feasibility-api.md`.

2018-v2 is a re-ranking, not a refinement: it moves 492 of 1,032 sample (action × city) scores and changes the top ten in five of twelve sample comunas. It also leaves the Institutional dimension with no city-level discrimination, because its only bridged channel was the sector-employment group that the one-channel rule consolidated elsewhere. A governance-index bridge is the open work that would restore it.

## Repository layout

Paths below are relative to a release folder; both releases share the same shape.

| Path | Purpose |
|------|---------|
| `review.md` | Methodology and design notes — feasibility dimensions, the scoring formula, the A/C bridging rule, the repeated-indicator rule, known limitations. |
| `scorer_simple.ipynb` | Self-contained scoring engine. Reads canonical inputs from `data/` and a city-indicator file from `sample/`, regenerates every derived artifact, and (in 2018-v2) runs the CC-718 regression checks and renders the before/after sensitivity. |
| `data/` | Canonical inputs extracted from the SR1.5 SM PDF (`actions_to_sr15_mapping.csv`, `sr15_feasibility_per_cell.csv`, `sr15_indicator_to_city_indicator.csv`) plus notebook-regenerated artifacts (`sr15_cell_bridge.csv`, `scoring_chain.csv`). |
| `data/api/` | API contract — `feasibility-api.md` (endpoint spec) and `example_response.json` (full sample payload) for the city-action mitigation feasibility scores endpoint that hiap-meed consumes. |
| `sample/` | Sample city-indicator inputs (12 Chilean comunas in `test_cities_indicators.csv`) and the ranked-action outputs the notebook writes (`test_cities_ranked_actions_by_locode.csv`, `test_cities_ranked_actions_per_cell.csv`, `scoring_chain_full.csv`). Gitignored. |
| `releases/2018/archive/` | Snapshots of earlier mapping versions kept for diffing (e.g. `actions_to_sr15_mapping.pre_single_primary.csv`). Baseline release only. |

The PDF itself is not redistributed in this folder — fetch it from the IPCC link above. Bridge tables and the notebook live here (rather than in a separate `oef-action-indicators` review) so the action-catalogue mapping evolves alongside the IPCC extracts in one place.

## Citation

When citing the underlying assessment, follow IPCC guidance for SR1.5 Chapter 4 and its Supplementary Material. Example (adapt to your house style):

> IPCC (2018). *Global Warming of 1.5°C. An IPCC Special Report on the impacts of global warming of 1.5°C above pre-industrial levels and related global greenhouse gas emission pathways, in the context of strengthening the global response to the threat of climate change, sustainable development, and efforts to eradicate poverty* — Chapter 4 Supplementary Material. World Meteorological Organization, Geneva, Switzerland.

## Reuse

Copyright and reuse conditions are set by the **IPCC** and may differ between figures, tables, and full report text. Before redistributing or adapting content, confirm the current terms on [ipcc.ch](https://www.ipcc.ch/) and cite the SR1.5 report and chapter accordingly.
