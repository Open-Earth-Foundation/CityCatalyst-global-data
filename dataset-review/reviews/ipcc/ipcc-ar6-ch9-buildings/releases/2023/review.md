# Review — AR6 WGIII Chapter 9 (Buildings), 2023

What Chapter 9 provides for the city buildings adjustment, and how it relates to our method. Context: [`methodology.md`](../../../ipcc-ar6-spm7-mitigation-potentials/methodology.md) in the SPM.7 review hub. Tags: **[V]** verified from the cited page, **[F]** figure-read (lower confidence), **[I]** inferred.

## The method — and it is our method

§9.6.2 (p. 9-57) states IPCC's own procedure verbatim **[V]**:

> "First, national potential estimates reported as a share of baseline emissions in 2050 were aggregated into regional potential estimates. Second, the latter were multiplied with regional baseline emissions to calculate the regional potential in absolute numbers... The sector mitigation potential reported in Chapter 12 for the year 2030 was estimated in the same manner."

So IPCC's method *is* **% of baseline × baseline emissions**. Our category-B approach (regional % × city baseline) is exactly this procedure run one admin level finer. The overlap rule is also confirmed **[V]**: measures are assembled "according to the SER framework (Box 9.1) and correcting the amount of the potential at each step for the interaction of measures," efficiency before renewables per SR1.5 (lower demand → more low-carbon supply choice). Our overlap caveat was faithful.

## The decomposition — the localizable structure

§9.3.2, **Equation 9.1** **[V]**:

```
CO₂ = Pop × (m²/Pop) × (EJ/m²) × (MtCO₂/EJ) = Pop × Sufficiency × Efficiency × Renewables
```

Four multiplicative drivers, mapping to SER + population, with the **grid emission factor as the fourth term** (`MtCO₂/EJ`). This is the parametric structure for a city estimate: populate each term with city data (population, floor area per capita, energy intensity, grid EF); a lever reduces one term. Paired with LMDI (Eq. 9.2) for exact overlap attribution. Caveat **[V]**: applied in-chapter to residential, use-phase emissions only.

Table 9.4 gives the sufficiency lever parametrically **[V]** — floor-area-per-capita reductions (e.g. to 15–29 m²/cap) yielding 32–45% global building-energy cuts — tying Eq. 9.1's sufficiency term to actual magnitudes.

## Critical nuance — grid decarbonisation is excluded

§9.6.1 (p. 9-54) **[V]**: the potentials "exclude the impact of decarbonisation measures applied within the boundaries of the energy supply sector, i.e., the decarbonisation of grid electricity and district heat." The buildings potential is reduced *energy use* at the *baseline* grid intensity. So:

- The **indirect** share of buildings potential = kWh saved × grid EF → scales with the **city's** grid EF.
- A clean-grid city (e.g. in Brazil) gets *less* CO₂ benefit per kWh saved from efficiency/sufficiency than a dirty-grid city.
- Grid cleaning itself is an energy-sector action (Ch.6), not a buildings action — do not double-count it here.

This corrects the earlier framing: buildings is grid-EF-sensitive, but through baseline-intensity electricity savings, not through grid decarbonisation.

## Regional potentials (Figure 9.16, 2050, % of baseline)

Full table in `data/ch9_regional_buildings_potential_2050.csv`. Headlines:

- **Global 61%** (8.2 GtCO₂): sufficiency 10% + efficiency 42% + onsite renewable 9%. **[V]** p9-57.
- **Developing 59%** (5.4 GtCO₂); **developed 65%** (2.7 GtCO₂). **[V]** p9-58.
- **Latin America & Caribbean ≈ 53%** of a ~463 MtCO₂ 2050 baseline (~309 indirect / ~154 direct → **~67% indirect**). **[F]** Figure 9.16 panel; flagged a **low estimate** (few studies; Brazil = de Melo & de Martino Jannuzzi 2015). **[V]**
- Other regions [F]: N. America 70%, Eastern Asia 73%, Middle East 68%, Europe+Eurasia 66%, Southern Asia 57%, Africa 53%, Asia-Pacific Developed 46%, SE Asia+Pacific 43%.

## What this supports

- *"Buildings potential in city X (LAC) is ~53% of baseline by 2050, mostly from efficiency, ~⅔ grid-dependent"* — via Figure 9.16 + the city's GPC buildings baseline, flagged 2050/low-estimate.
- *"This city's buildings ranking is grid-sensitive on its electricity share"* — via the §9.6.1 exclusion + Eq. 9.1's `MtCO₂/EJ` term.
- A bottom-up city estimate via Eq. 9.1 (Pop × floor/cap × energy/floor × grid EF), with lever magnitudes from Figure 9.16 / Table 9.4 / SM component rates.

## What this does not support

- A 2030 city tCO₂e — the regional % is 2050; 2030 is interpolated, and outputs stay ordinal.
- Treating grid cleaning as a buildings action (it's energy-sector; double-counts).
- High-confidence per-measure regional sub-splits — those are figure-read; only totals and direct/indirect baselines are solid.
- Embodied emissions (18% of total building GHG, §9.1) — outside Eq. 9.1 and Figure 9.16 (use-phase only); a separate materials lever.

## Data dependencies (open)

- **[F→V] Precise regional sub-splits** (sufficiency/efficiency/renewable per region) — re-read Figure 9.16 panels carefully or obtain Table SM9.6 if it tabulates them.
- **City baseline by end-use** — split the GPC buildings inventory into space heating/cooling, water heating, appliances/lighting to apply Eq. 9.1 and the climate (degree-day) factor to the right share.
- **2030 vs 2050** — decide whether to use the 2050 regional % directly (flagged) or re-derive a 2030 share consistent with Ch.12's interpolation.

## Traceability

- Source: AR6 WGIII [Chapter 9](https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-9/) §9.1, §9.3.2, §9.6.1–9.6.2, Figs 9.15/9.16, Table 9.4 (chapter PDF, pages read 9-20, 9-52 to 9-58); [Ch.9 SM](https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_Chapter09_SM.pdf).
- Method cross-check: Ch.12 SM §12.SM.1.2.
- Created 2026-06-08, superseding the earlier A1 buildings sketch (now consolidated into the SPM.7 review's `methodology.md`).
- Baseline: WEO 2019 Current Policies. Project region values (illustrative grid EFs): Chile ~253, Brazil ~130 gCO2e/kWh.
