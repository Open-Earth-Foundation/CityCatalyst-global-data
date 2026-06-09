# Review — AR6 WGIII Chapter 11 (Industry), 2023

Tests our working assumption (industry = category D, flat national rate, no city signal) against the chapter. Context: [`methodology.md`](../../../ipcc-ar6-spm7-mitigation-potentials/methodology.md). Tags: **[V]** verified from the cited page, **[F]** figure/table-read, **[I]** inferred.

## Verified facts

- **Emissions structure (Table 11.1, 2019, ~20 GtCO₂e)** **[V]**: direct combustion **35%** (iron/steel 12%, cement-related in minerals, chemicals…); **indirect electricity 21%**; indirect heat **8%**; process CO₂ **16%** (non-metallic minerals/cement 10%, chemicals 3.6%); remainder ~20% F-gas/waste/other non-CO₂.
- **Decomposition (Equation 11.1)** **[V]**: `GHG = POP × GDP/POP × MStock/GDP × (MPR+MSE)/MStock × Dm × E/(MPR+MSE) × (GHGed+GHGeind)/E × GHGoth/(MPR+MSE)`. The term `(GHGed+GHGeind)/E` is direct+**indirect** combustion emissions per energy → addressed by electrification / fuel switching / energy decarbonisation; `GHGoth/(MPR+MSE)` is process/F-gas/waste per material → feedstock decarbonisation / CCUS. `Dm` is an explicit territorial-vs-consumption term, **"valid only for sub-global levels" (Dm=1 territorial)**.
- **Option groups (Figure 11.13)** **[F]**: CIEL (carbon intensity of electricity, indirect), EE (energy efficiency), ME (material efficiency), Circularity, FeedCI (feedstock carbon intensity), FSW+El (fuel switch + electrification with low-carbon electricity). Grouped technology packages, direct/indirect split.
- **Energy efficiency contribution 10–40% by 2050** **[V]**; other drivers grow for deep decarbonisation.
- **Global per technology class, ~75 studies, no regional breakdown** **[V]** (Ch.12 SM).

## How it aligns with our assumptions — and where it doesn't

**Wrong, and worth correcting:** we treated industry as uniformly category D (flat national rate, no city signal). In fact **~29% of industry emissions are indirect (electricity 21% + heat 8%)** and therefore scale with the city's **grid EF**, and the electrification option (FSW+El) is grid-dependent — exactly the buildings pattern. So industry **splits**, like buildings did:

- **Grid-EF adjustable (city signal):** industrial electricity + heat (indirect), and electrification of direct combustion. Same identity logic as buildings/transport — kWh valued at the city grid EF. ~A-class.
- **National-rate, no city signal (true D):** process emissions (cement/chemicals/F-gas), material efficiency, circularity, and the global per-tech energy-efficiency rate.

**Aligned:** the *deep process* part genuinely has no city signal (global per-tech), so our flat-rate treatment is right *for that slice*. And our illustrative EE rate (0.15) sits at the **low end of the chapter's 10–40%** range — acceptable as illustrative, but cite the range.

**New (improves the method):** Eq. 11.1 is a localizable decomposition with an explicit territorial term — so a bottom-up city industry estimate is structurally possible, same status as buildings' Eq. 9.1 (structure localizable; lever magnitudes still from the global synthesis).

## Fit into the overall goal (city ranking)

Industry is a **weaker city lever than buildings or transport**, for two structural reasons, not data reasons:

1. **Authority:** process decarbonisation (steel, cement, chemicals, feedstock) is national/sectoral — rarely a municipal action. The city-actionable industry levers are narrow: industrial electricity (grid), energy-efficiency programmes, electrification incentives.
2. **Inventory scope:** industrial process emissions are GPC IPPU (sector IV) = **BASIC+ only**, often outside a city's headline (BASIC) inventory. Industrial *energy* (I.3 combustion) and *electricity* (scope 2) are in BASIC.

So for the ranking: keep industry **split** — the electricity/electrification slice as a *city-adjusted* (grid-EF) row, and the EE/process slice as a flagged *national-rate* tier (and note the process part may be out of the city's BASIC scope entirely). This replaces the earlier "all industry = one flat national-rate block."

## What this supports

- Splitting industry into a grid-adjustable electricity slice (~29% indirect) and a national-rate process/EE slice.
- A directional industry contribution using EE 10–40% and the global option mix — flagged as undifferentiated except for the grid term.
- The structural claim that industry, like buildings, is grid-EF-sensitive on its electricity share.

## What this does not support

- City-differentiated *process* potentials (cement/chemicals) — global per-tech, no city signal, and usually outside municipal authority/BASIC scope.
- Precise per-option industry magnitudes for a city without reading Figure 11.13's values (figure-locked) — current notebook rates are illustrative.

## Data dependencies (open)

- **[F→V] Figure 11.13 option magnitudes** — transcribe from the figure (or the chapter PDF) to replace the illustrative notebook rates.
- **City industrial-electricity baseline** — split the GPC `I.3` + scope-2 industrial electricity from process (IPPU) to apply the grid-EF term to the right share.
- **Scope decision** — whether the city ranking includes IPPU (BASIC+) at all.

## Traceability

- Source: AR6 WGIII [Chapter 11](https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-11/) Eq. 11.1, Table 11.1, §11.4, Figure 11.13; construction cross-ref Ch.12 SM §12.SM.1.2.
- Created 2026-06-08. Revises the category-D treatment of industry in `methodology.md` and the national-rate industry rows in `action_ranking_calc.ipynb`.
