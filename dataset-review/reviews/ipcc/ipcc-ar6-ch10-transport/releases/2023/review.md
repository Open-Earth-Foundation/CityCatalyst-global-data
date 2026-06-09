# Review — AR6 WGIII Chapter 10 (Transport), abatement parameters, 2023

What Chapter 10 can and cannot provide as inputs to the ASIF ranking engine (`reduction = GPC_segment × abatement_fraction × uptake`). Method context: [`methodology.md`](../../../ipcc-ar6-spm7-mitigation-potentials/methodology.md) in the SPM.7 review hub. Evidence tags: **[V]** verified from the cited IPCC source, **[I]** inferred/illustrative, **[U]** unanswered/dependency.

## Verified parameters

Sector structure (the denominators a city ranking sits inside):

- Road transport 6.1 GtCO2e = **69%** of transport; shipping 0.8 (9%), aviation 0.6 (7%), rail + other 1.4. **[V]** §10.1.2 / Fig 10.1.
- Within passenger transport: cars + 2/3-wheelers + minibuses ≈ **75%** of passenger CO2; collective transport (bus + rail) ≈ **7%** of emissions while carrying ~**20%** of pkm. **[V]** §10.1.2.
- Transport indirect (grid) emissions ≈ **2%** today, rising with electrification, "especially where carbon-intense electricity grids operate." **[V]** §10.1.2 — direct confirmation that `EF_to` (grid) is the governing city parameter.
- LATAM transport GHG growth **2.4%/yr** (1990–2019). **[V]** §10.1.2.

Abatement anchors (IPCC-assessed, cite the chapter — not the underlying datasets):

- New LDVs: **~50%** per-km CO2 reduction achievable by 2030 vs 2005 (fuel economy); EV sales share ~30–35% by 2030. **[V]** Ch.12 SM p.12SM-6 (ICCT 2019; cross-checked Ch.10).
- LDV EV potential **0.5–0.7 GtCO2e "depending on the carbon intensity of the electricity"**. **[V]** Table 12.3 — the source states the grid dependence outright.
- Carpooling: **~11%** vkm and **~12%** emissions reduction. **[V]** §10.2.3 (ITF 2020).
- Shipping: **39%** (30–56%) reduction vs BAU, ~one-third attributed to biofuels. **[V]** §10.6.4 (Bouman et al. 2017).
- Biofuels: ~**10%** of transport fuel by 2030 feasible; conversion efficiency/GHG ranges in Table 10.5. **[V]** Ch.12 SM (IRENA 2016), Table 10.5.
- SPM.7 sanity-check envelope (GtCO2e 2030): LDV fuel efficiency 0.6, LDV EV 0.5–0.7, public transport 0.5, bikes 0.2, HDV efficiency 0.4, shipping 0.5, aviation 0.12–0.32, biofuels 0.6–0.8. **[V]** Table 12.3.

Emission factors (the `EF` terms): 2006 Guidelines Vol.2 Ch.3 + EFDB; ethanol CO2 is a memo item (biogenic), so blended petrol carries a lower fossil EF. **[V]**

## Mapping each transport option to the ASIF engine

| Action (option) | `abatement_fraction` form | City knobs | GPC segment | Downscalable |
|---|---|---|---|---|
| **Electrify LDVs** | identity: `1 − (i_EV·EF_grid)/(i_ICE·EF_fuel)` | grid EF; blend | `II.1.1`→`II.1.2` | **Yes** [V] |
| **LDV fuel efficiency** | assessed %: up to ~50% new-vehicle, fleet-weighted by turnover | (blend) | `II.1.1` | Partial — fleet-age split external [U] |
| **Shift to public transport / bikes** | modal intensity ratio (transit ≈ 2.7× lower/pkm) on shifted pkm | — | `II.1.1`→`II.2`/none | Partial — needs mode-share + shift fraction [U] |
| **Raise biofuel blend** | fuel-switch: fossil fraction displaced (biogenic memo) | blend | `II.1.1` | **Yes** (national blend) [V] |
| **HDV efficiency / shipping / aviation** | assessed % | — | `II.1.x`/inter-city | National context, not a city action [V] |

The identity actions (electrify, blend) are computed directly from EFs + intensities — no external evidence. The mode-shift action needs the per-mode intensity (figure dependency below) plus a city mode-share; fuel-efficiency needs a fleet-turnover assumption.

## Worked example — electrify LDVs, Santiago vs São Paulo

Tags as above; intensities **[I]** illustrative pending fleet data, grid EFs and blend are real inputs.

| Term | Santiago (CL) | São Paulo (BR) |
|---|---|---|
| ICE LDV tailpipe `i_ICE·EF_fuel` (scope 1) | 165 gCO2/km [I] | ~130 gCO2/km (E30: ethanol ~22% energy share, biogenic memo) [I] |
| EV residual `i_EV·EF_grid` = 0.18 kWh/km × grid | 0.18×**253** = 45.5 [grid V] | 0.18×**130** = 23.4 [grid V] |
| `abatement_fraction` = 1 − residual/baseline | 1 − 45.5/165 = **0.72** | 1 − 23.4/130 = **0.82** |
| Net BASIC reduction (scope1 − scope2 residual) | 165 − 45.5 = **119.5 gCO2/km** | 130 − 23.4 = **106.6 gCO2/km** |

Two honest results:

- **São Paulo has the higher *fractional* abatement (82% vs 72%)** — the clean hydro grid dominates, even though Brazil's ethanol blend has already partly decarbonized the petrol baseline.
- **Santiago has the higher *absolute* per-km reduction (119.5 vs 106.6)** — its baseline petrol is higher (no blend), so each electrified km removes more.

This is the ranking subtlety from the methodology made concrete: **rank by absolute per-unit reduction within a service unit** (Santiago's EV action looks stronger per km), but **by percentage when comparing across unit types** (São Paulo's electrification is the more complete decarbonization). The grid residual (45.5 / 23.4 gCO2/km) is never zero and lands in `II.1.2` (scope 2, in BASIC) — count it.

## What this data supports

- *"Electrifying LDVs reduces more per km in city A than city B"* — valid via the identity, using the city's grid EF and fuel blend; both are verified inputs.
- *"This city's transport ranking is grid-sensitive"* — valid; §10.1.2 establishes the dependence and the engine quantifies it.
- *"Mode-shift beats electrification here"* (or vice-versa) — conditional: valid only once a per-mode intensity (figure data) and a city mode-share/shift fraction are supplied; until then mode-shift is ranked on the 2.7× system proxy with that caveat stated.

## What this data does not support

- A city tCO2e *target* — outputs are ordinal; SPM.7's ±50% transport uncertainty and non-additivity carry through.
- Summing EV + fuel-efficiency + mode-shift on the same `II.1.1` baseline — they compete; take the envelope.
- City-level shipping/aviation ranking — out of scope (national/international).
- Precise modal-shift magnitudes without the figure data (see dependency).

## Data dependencies (open)

- **[U] Per-mode energy intensities (MJ/pkm).** In Chapter 10 figure data, not text. Needed for an exact mode-shift `abatement_fraction`; interim proxy = 2.7× from §10.1.2. Acquire the Fig 10.x figure-data file (IPCC DDC) in a future release.
- **[U] VKT/fleet split** to carve `II.1.1` into LDV/HDV and petrol/diesel — external, openly-usable national transport statistics (not IEA, per clean-room).
- **[U] EV on-road energy intensity** (kWh/km) point value — illustrative 0.18 used; confirm against an open source (e.g. national type-approval data) rather than the IEA/ICCT figures.

## Traceability

- Source: AR6 WGIII [Chapter 10](https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-10/); construction in [Ch.12 SM](https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_Chapter12_SM.pdf) §12.SM.1.2.
- EFs: 2006 IPCC Guidelines Vol. 2 Ch. 3 + EFDB.
- Consolidated 2026-06-05; cross-cutting method now in the SPM.7 review's `methodology.md`.
- City inputs (illustrative): Chile grid ~253 gCO2e/kWh, Brazil ~130; Brazil petrol E27→E30, Chile ~no blend.
