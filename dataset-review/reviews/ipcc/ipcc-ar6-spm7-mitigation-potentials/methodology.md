# Methodology — ranking city climate actions on IPCC potentials (WORKING)

> **Status: working assumption, not landed.** This is the cross-cutting method for the Chile/Brazil action-ranking work, kept here in the SPM.7 review hub while it is still being revised across chapter reviews. It is deliberately *not* in `knowledge-base/topics/` (which is for settled reference) — promote a consolidated version there only once the method stabilises. Per-sector detail lives in the individual chapter reviews (`ipcc-ar6-ch9-buildings`, `ipcc-ar6-ch10-transport`).

## Purpose and constraints

- **Goal:** an *ordinal* ranking of candidate city actions by emissions-reduction potential — "which are likely biggest" — not target-setting or absolute tCO₂e.
- **Geography:** Chile and Brazil cities; method generic, inputs local.
- **Clean-room / commercial:** IPCC + openly-usable public sources only; no NonCommercial-licensed material (Chile project assigns commercial rights to a partner).
- **Inputs:** candidate actions mappable to AR6 WGIII options; a GPC inventory per city (by sub-sector and scope, not vehicle/fuel-disaggregated).

## Core idea: SPM.7 is an aggregation, run backward

SPM.7 / Table 12.3 is Chapter 12's *aggregation* of the sectoral chapters (6, 7, 9, 10, 11) into ~31 global options (the finer 43-option grain is in `releases/2023/data/spm7a_wgiii_options_2030_clean.csv`). Our task is the reverse — sectoral parameters *down* to one city — so we go to the same sectoral sources and do not reproduce the aggregation; the city's GPC baseline does the scale job. The option level survives only as (1) taxonomy for mapping actions, and (2) a sanity-check envelope. The calculation happens below the option, in the chapter reviews.

## The engine

```
reduction          = GPC_baseline_segment × abatement_fraction × uptake_fraction
abatement_fraction = 1 − (intensity_to × EF_to) / (intensity_from × EF_from)
```

The city adjustment enters through two local knobs: **grid emission factor** (`EF_to` for electrification) and **fuel blend** (`EF_from`, e.g. Brazil ethanol). Count the grid residual — electrification moves emissions GPC scope 1 → scope 2 (both in BASIC), never zero.

ASI fit (IPCC Avoid–Shift–Improve, Ch.5/10): this engine covers **Improve** (tech/fuel swap) and **Shift** (mode intensities) cleanly. **Avoid** (demand reduction, urban form) is a different lever — it reduces the *baseline activity*, not the intensity ratio — so it needs a parallel `baseline × activity_reduction × uptake` branch, with the activity term from external evidence, not EFs.

Buildings note: Chapter 9's own decomposition (Eq. 9.1) is `CO₂ = Pop × Sufficiency × Efficiency × Renewables`, with grid EF as the fourth term — the same engine, with abatement rates from Ch.9 rather than computed from EFs. See `ipcc-ar6-ch9-buildings`.

## What is IPCC's vs input data

| Term | Source | Provider |
|---|---|---|
| EFs (`EF_from`, `EF_to` components) | 2006 IPCC Guidelines Vol.2 + EFDB | IPCC |
| intensities / % reductions | sectoral chapters (6, 9, 10, 11) | IPCC |
| `uptake` default | backed out of the SPM.7 option range | IPCC (derived) |
| action→option taxonomy | Ch.12 / SPM.7 | IPCC |
| `GPC_baseline_segment` | city GPC inventory | local |
| grid EF, fuel blend | Ember / national fuel standard | local |
| VKT/fleet or end-use split to carve a sub-sector | national statistics (openly-usable) | local |

**IPCC tells you how much each unit drops; your data tells you how many units and how dirty this city's grid and fuel are.** IPCC potentials are *economic* (cost-screened) against a 2030 current-policy baseline; use them to sanity-check direction/magnitude, not as a direct equal of `abatement × uptake`.

## Which options are city-adjustable (categories)

Full 43-option map: see `releases/2023/data/spm7a_wgiii_options_2030_clean.csv` and the chapter reviews. Categories:

- **A — Clean** (grid EF / blend / climate / waste composition; computable now from EFs + city knobs, no chapter review): electric LDV/HDV, biofuels, onsite renewables, **waste & wastewater CH₄**.
- **B — Buildings regional-%** (Ch.9 regional % × city baseline × climate; `ipcc-ar6-ch9-buildings`): efficient buildings, lighting/appliances, sufficiency, retrofit of existing stock.
- **C — Partial** (needs city activity data IPCC doesn't surface): fuel-efficient vehicles (fleet turnover), mode-shift (mode share + per-mode intensity).
- **D — No city signal** (national/global context): all AFOLU, grid-scale energy supply (wind/solar/nuclear/CCS — but these *set* the grid EF used by A), shipping/aviation, F-gases, and the *process* part of industry (cement/chemicals).
- **Industry splits** (see `ipcc-ar6-ch11-industry`): ~29% is indirect electricity/heat → **grid-EF adjustable like buildings** (A-class); the process/feedstock part is true D; energy-efficiency is a national-rate. Industry is a weaker city lever overall (process is national/sectoral and GPC IPPU is BASIC+ only).

## Chapter review status / routing

- **Ch.9 Buildings — done** (`ipcc-ar6-ch9-buildings`). Regional %, Eq. 9.1, grid-exclusion nuance, LAC ~53% (2050, low estimate).
- **Ch.10 Transport — done** (`ipcc-ar6-ch10-transport`). ASIF mapping, identity vs estimated, Santiago/São Paulo example.
- **Energy supply (A2) — pending.** Grid-EF identity for electrification; the grid EF itself is a city input (Ember), so the chapter contributes little — sources: Ch.6 §6.4.7 (LCOE/displaced-EF), UNEP 2017. Thin review.
- **Waste/wastewater CH₄ (B-class) — pending.** Not a chapter rescale — use the country-resolved MACC datasets the SPM.7 row aggregates: US EPA (2019) Non-CO₂ tool, GAINS / Höglund-Isaksson et al. (2020), PBL / Harmsen et al. (2019). City parameter: organic-waste fraction / treatment type (first-order decay).
- **Industry (Ch.11) — reviewed** (`ipcc-ar6-ch11-industry`). Splits: indirect electricity/heat (~29%) is grid-EF adjustable; process/EE is national-rate. Weaker city lever (process is national + BASIC+ only).
- **AFOLU (Ch.7) — not needed for city adjustment** (category D; review only to confirm).

## GPC reconciliation

Actions map to GPC source codes (transport `II.1.x`, etc.; see `knowledge-base/topics/gpc-framework.md`). GPC is not vehicle/fuel-disaggregated, so carve `baseline_segment` with an external openly-usable split. Constraint: Σ(action baselines on a sub-sector) ≤ the sub-sector total; competing actions on the same segment (e.g. electrify vs mode-shift on `II.1.1`) are alternatives — take the envelope, don't sum (non-additivity, per SPM.7).

## Licensing

IPCC numeric data/facts usable commercially with attribution (SPM.7 data is CC BY 4.0); rebuild figures from data rather than embedding (IPCC copyright policy); 2006 Guidelines + EFDB free with attribution. Avoid NonCommercial sources (UNEP EGR, Project Drawdown, ClimateView TEF licence-unverified) and proprietary datasets *cited by* IPCC (ICCT, BNEF, IEA WEO) — use IPCC's assessed values instead. Not legal advice — review given the commercial assignment.

## Open questions (why this is still WORKING)

- **Differentiation ceiling:** potential alone gives ~2–3 tiers, city-actionable options pile into "medium". Folding in cost bins adds an axis but cost is $/tCO₂e, 2015–2020 vintage.
- **2030 vs 2050:** buildings regional % is 2050 (2030 interpolated); decide which horizon the ranking uses.
- **Lever magnitudes for buildings:** Eq. 9.1 localises the baseline/structure, but how far each lever goes still comes from Ch.9's literature synthesis.
- **Uptake:** single default vs per-action maturity — undecided.
- **Encoding:** continuous multipliers vs categorical tiers for the ordinal use case.
