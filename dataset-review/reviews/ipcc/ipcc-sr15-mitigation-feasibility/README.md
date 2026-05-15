# IPCC SR1.5 — Chapter 4 Supplementary Material (mitigation feasibility)

Dataset review entry for the **approval-version** supplementary material to *Global Warming of 1.5°C* (IPCC SR1.5), **Chapter 4** — *Strengthening and Implementing the Global Response*. The PDF is the canonical source for **multidimensional feasibility** assessments of **mitigation options** (economic, technological, institutional, socio-cultural, environmental, and geophysical dimensions), including the SM tables (e.g. 4.SM.5–4.SM.6 methodology, 4.SM.7–4.SM.15 option-level matrices) and evidence/agreement annotations.

## Canonical download

- **SR15_Approval_Chapter_4_SM.pdf** (IPCC, 2019 approval layout):  
  [https://www.ipcc.ch/site/assets/uploads/sites/2/2019/05/SR15_Approval_Chapter_4_SM.pdf](https://www.ipcc.ch/site/assets/uploads/sites/2/2019/05/SR15_Approval_Chapter_4_SM.pdf)

Landing context for the full Special Report: [https://www.ipcc.ch/sr15/](https://www.ipcc.ch/sr15/)

## Why we use it

- **Authoritative** global synthesis of feasibility for discrete mitigation options (as of the SR1.5 cycle), with per-indicator **A / B / C** (and related) codings traceable to the published tables.
- **Stable priors** for action- and city-level workflows that need a literature-backed baseline before local data are applied (see `dataset-review/reviews/oef/oef-action-indicators/sr15_priors/`).
- **Explicit provenance** for HIAP / MEED–style scoring: every derived cell should map back to a table and row in this document.

## Spatial and temporal scope

- **Geography:** global assessment (not city-specific); use as **prior**, then adjust with local indicators where methodology allows.
- **Temporal reference:** SR1.5 assessment period (published 2018; approval PDF dated 2019 on the IPCC site). Treat as a **2018-vintage** evidence base when comparing to AR6 products.

## Repository layout

| Path | Purpose |
|------|---------|
| `releases/2018/` | Release folder for the 2018 SR1.5 cycle; may hold a **local copy** of the PDF (same filename as the IPCC asset above) for offline review, plus `review.md` describing how extracted priors relate to the SM tables. |
| `releases/2018/review.md` | Internal methodology and design notes (feasibility dimensions, aggregation formula, bridge rules, limitations). |

Structured CSV extracts and notebooks built from this PDF live under **`oef-action-indicators/sr15_priors/`** (separate dataset review) so they can evolve with the action catalogue without duplicating the IPCC source file.

## Citation

When citing the underlying assessment, follow IPCC guidance for SR1.5 Chapter 4 and its Supplementary Material. Example (adapt to your house style):

> IPCC (2018). *Global Warming of 1.5°C. An IPCC Special Report on the impacts of global warming of 1.5°C above pre-industrial levels and related global greenhouse gas emission pathways, in the context of strengthening the global response to the threat of climate change, sustainable development, and efforts to eradicate poverty* — Chapter 4 Supplementary Material. World Meteorological Organization, Geneva, Switzerland.

## Reuse

Copyright and reuse conditions are set by the **IPCC** and may differ between figures, tables, and full report text. Before redistributing or adapting content, confirm the current terms on [ipcc.ch](https://www.ipcc.ch/) and cite the SR1.5 report and chapter accordingly.
