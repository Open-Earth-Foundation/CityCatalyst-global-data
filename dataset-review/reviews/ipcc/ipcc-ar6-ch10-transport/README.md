# IPCC AR6 WGIII Chapter 10 — Transport (abatement parameters)

Dataset review entry for **AR6 WGIII Chapter 10 (Transport)** as a *parameter source* for the city action-ranking methodology ([`methodology.md`](../ipcc-ar6-spm7-mitigation-potentials/methodology.md) in the SPM.7 review hub). It holds the transport-sector abatement parameters that feed the ASIF engine, plus the adjustment mechanics and worked example.

What this review is **not**: a re-extraction of SPM.7's transport potentials. Those are the Chapter-12 *aggregation* and are reviewed in `ipcc-ar6-spm7-mitigation-potentials`. This review goes one level below the option, to the parameters Chapter 10 (and the 2006 Guidelines EFs) provide for computing `abatement_fraction` per action.

## Why we use it

- **The `abatement_fraction` parameters for transport** — mode energy intensities, EV-vs-ICE efficiency, fuel-efficiency improvement rates, modal-shift intensity ratios. These are the engineering ratios the ranking engine downscales to a city, against the city's GPC transport baseline.
- **Confirms the city-parameter dependence** — Chapter 10 states transport grid (indirect) emissions are ~2% today but rise with electrification "especially where carbon-intense electricity grids operate" (§10.1.2), i.e. the grid emission factor is load-bearing exactly as the methodology assumes.

## Canonical sources

- **Chapter 10 (Transport):** https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-10/ — §10.1.2 (sector composition, drivers), §10.2 (systemic change, mode choice), §10.3 (alternative fuels, Tables 10.4/10.5), §10.4 (vehicle technologies, lifecycle), §10.6 (shipping/aviation), §10.7 (assessment).
- **Construction of the SPM.7 transport rows:** Chapter 12 SM §12.SM.1.2, p. 12SM-5–6 ([PDF](https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_Chapter12_SM.pdf)) — names the underlying sources (ICCT 2019; ITDP & UC-Davis 2015; Bouman et al. 2017; IRENA 2016).
- **Emission factors (`EF_from`, `EF_to` components):** 2006 IPCC Guidelines Vol. 2 Energy, Ch. 3 Mobile Combustion (road = §3.2) + the Emission Factor Database (EFDB). The biogenic-carbon rule (ethanol CO2 reported as a memo item) lives here — it is *why* Brazil's E27→E30 blend lowers the petrol baseline.

## License

- Chapter 10 **numeric facts/data**: facts are not copyrightable; AR6 figure data on the IPCC DDC is CC BY 4.0. Usable in the commercial deliverable with attribution.
- Chapter 10 **figures/text**: reproduce per [IPCC copyright policy](https://www.ipcc.ch/copyright/) (limited reproduction, attribution, no alteration) — rebuild visuals from data rather than embedding.
- 2006 Guidelines + EFDB: free to use with attribution.
- **Clean-room caveat:** Chapter 10's quantitative anchors are often drawn from ICCT, ITF, IEA and BNEF datasets. Use the **IPCC-assessed values in the chapter**, not those underlying proprietary datasets (IEA/ICCT/BNEF terms are restrictive). This keeps the build commercial-safe.

## Spatial and temporal scope

- **Geography:** global assessment with regional growth detail (LATAM transport GHG growth 2.4%/yr, 1990–2019; §10.1.2). Parameters (intensity ratios, EFs) are context-portable; the *scale* comes from the city's GPC inventory, not this chapter.
- **Time:** AR6 cycle (lit. to ~2021); SPM.7 transport potentials target 2030 vs a current-policy baseline. Frozen; superseded only by AR7.

## Interpretation warnings

- **Per-mode energy intensities live in figures.** Chapter 10's precise MJ/pkm by mode are in figure data (Fig 10.x), not the chapter text. For an exact modal-shift `abatement_fraction`, extract the figure data; an interim system-level proxy is verifiable from §10.1.2 (collective transport = 7% of passenger CO2 on ~20% of pkm → roughly 2.7× lower carbon per pkm than private modes). Flagged as a data dependency in `review.md`.
- **GPC is not vehicle/fuel-disaggregated.** Carving the on-road baseline (`II.1.1`) into LDV vs HDV, or petrol vs diesel, needs an external openly-usable VKT/fleet split — not from this chapter.
- **Inter-city modes are not city actions.** Shipping, aviation and most HDV potential are national/international; for the *city* ranking they are national context, not rankable city actions.
- **Don't sum competing actions.** EV, fuel-efficiency and mode-shift all draw on the same on-road baseline — rank as alternatives, take the envelope (non-additivity, as in SPM.7).

## Parsing notes

- The chapter HTML renders narrative prose; tables (10.4 ICE engine tech; 10.5 biofuel efficiency/GHG ranges) and figures need the PDF or DDC figure-data files for clean numeric extraction.
- Underlying-source values (ICCT 50% per-km cut; carpooling 11%/12%) are quoted by IPCC with citations — record them as IPCC-assessed, cite the chapter, do not pull from the proprietary source directly.

## Current release

**2023** (AR6 WGIII cycle). Parameters and mechanics in `releases/2023/`.
