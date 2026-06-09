# IPCC AR6 WGIII Chapter 9 — Buildings (regional potentials + decomposition)

Dataset review for **AR6 WGIII Chapter 9 (Buildings)** as the parameter source behind the city action-ranking methodology ([`methodology.md`](../ipcc-ar6-spm7-mitigation-potentials/methodology.md) in the SPM.7 review hub). Buildings is the highest-value chapter review: it holds the **regional mitigation percentages** that have no substitute in any downloadable dataset, plus the **decomposition equation** that makes a city-level estimate possible.

Companion to the SPM.7 option review (`ipcc-ar6-spm7-mitigation-potentials`), which aggregates this chapter's output up to the global "Efficient buildings / lighting / sufficiency / onsite renewables" options. This review goes the other way — to the regional % and the parametric structure underneath.

## Why we use it

- **Regional buildings potentials as % of baseline (Figure 9.16)** — the category-B inputs: per-region reduction potential, split by measure (sufficiency / efficiency / onsite renewables) and by emission source (direct / indirect). Includes **Latin America & Caribbean**, the project region.
- **The decomposition equation (Eq. 9.1)** — `CO₂ = Pop × Sufficiency × Efficiency × Renewables`, the localizable structure that lets a city estimate be built from its own floor area, energy intensity and grid EF rather than inheriting a continental average.
- **The synthesis method (§9.6.2)** — confirms IPCC's own procedure is *% of baseline × baseline emissions*, i.e. exactly the "regional % × city baseline" our method uses, one admin level finer.

## Canonical sources

- **Chapter 9 (Buildings):** https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-9/ — §9.1 (emission composition), §9.3.2 (Eq. 9.1 decomposition, LMDI), §9.5 (non-technological/sufficiency), §9.6.1 (Figure 9.15, 67-study synthesis; Table 9.4 sufficiency), **§9.6.2 (Figure 9.16, regional potentials; the method).** Read from the chapter PDF (uploaded), pages 9-20, 9-52 to 9-58.
- **Chapter 9 SM:** https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_Chapter09_SM.pdf — Tables 9.SM.2/9.SM.3 (efficiency/renewables technology menus with per-technology savings %), Table 9.SM.4 (non-technological measures, region × %).
- **Construction cross-reference:** Chapter 12 SM §12.SM.1.2 (confirms the 2030 SPM.7 buildings rows were built "in the same manner").
- **Emission factors / grid EF:** city-supplied (Ember etc.), not this chapter.

## License

Chapter 9 numeric facts usable in the commercial deliverable with attribution (facts not copyrightable; SPM.7-lineage data is CC BY 4.0). Figures: reproduce per [IPCC copyright policy](https://www.ipcc.ch/copyright/) — rebuild visuals from the values rather than embedding. **Note: Chapter 9 figures have NO downloadable data file** (unlike SPM.7); the regional % had to be read from the figure panels and chapter text.

## Spatial and temporal scope

- **Geography:** global with a 10-region breakdown (Figure 9.16) and a developed/developing aggregate (Figure 9.17). Resolution is regional, not city — downscaling to a city is our construction via Eq. 9.1 + the city's GPC baseline.
- **Time:** potentials are **2050** (Figure 9.16/9.17). The SPM.7/Table 12.3 buildings rows are 2030, *interpolated* toward these 2050 figures (Ch.12 SM). Any 2050 % used for a near-term ranking must carry that flag.
- **Baseline:** WEO 2019 Current Policies (IEA 2019c) — stated to differ slightly from other chapters.

## Interpretation warnings

- **Potential excludes grid decarbonisation.** §9.6.1: the potentials "exclude the impact of decarbonisation measures applied within the boundaries of the energy supply sector, i.e., the decarbonisation of grid electricity and district heat." So the buildings potential is reduced *energy use* valued at the *baseline* grid intensity — cleaning the grid is the energy sector's job (Ch.6), not a buildings action. Implication: the **indirect** share of buildings potential scales with the *city's* grid EF (kWh saved × grid EF), so clean-grid cities get less CO₂ per kWh saved.
- **Two different "indirect shares."** §9.1 reports 57% indirect of *total* building GHG (including 18% embodied, 2019). Figure 9.16 is *use-phase only* (direct + indirect, no embodied), where indirect is ~74% globally and ~67% for LAC. Use the use-phase split for the energy-measure adjustment; embodied (cement/steel) is a separate, non-grid lever.
- **2050, and LAC is a flagged low estimate.** §9.6.2: "only few potential studies... were available for... Latin America and Caribbean; therefore the potential estimates represent low estimates, and the real potentials are likely higher." Brazil is one of the few underlying LAC studies.
- **Regional % sub-splits are figure-read.** Regional *totals* and direct/indirect baselines are high-confidence; the per-measure (sufficiency/efficiency/renewable) splits per region are read off a dense figure — lower confidence (see CSV `confidence` column).

## Parsing notes

- Chapter 9 figures are image-only (no DDC data file); regional values were transcribed from the Figure 9.16 panels + §9.6.2 text. Global, developed and developing figures are text-verified; per-region figures are panel-read.
- Eq. 9.1 was applied in-chapter to **residential, use-phase** emissions only (non-residential lacked data); the structure generalizes but IPCC's own application was residential.

## Current release

**2023** (AR6 WGIII cycle). Regional potentials in `releases/2023/data/ch9_regional_buildings_potential_2050.csv`; method and assessment in `releases/2023/review.md`.
