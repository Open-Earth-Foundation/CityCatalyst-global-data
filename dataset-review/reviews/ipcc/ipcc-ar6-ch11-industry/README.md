# IPCC AR6 WGIII Chapter 11 — Industry (potentials + decomposition)

Dataset review for **AR6 WGIII Chapter 11 (Industry)** as a parameter source for the city action-ranking methodology ([`methodology.md`](../ipcc-ar6-spm7-mitigation-potentials/methodology.md) in the SPM.7 review hub). Triggered to test our working assumption that industry is category D ("no city signal, flat national rate"). **That assumption was partly wrong** — see review.md.

## Why we use it

- **To classify industry correctly** for the city ranking — which industry emissions respond to a city parameter (grid EF) and which don't.
- **Equation 11.1** — industry's Kaya decomposition, with an explicit territorial/sub-global term, i.e. structurally localizable like buildings' Eq. 9.1.
- **Table 11.1** — the direct / indirect-electricity / indirect-heat / process split that determines the grid-adjustable share.

## Canonical sources

- **Chapter 11 (Industry):** https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-11/ — Eq. 11.1 + Table 1 (decomposition drivers), Table 11.1 (emissions structure), §11.4.1–11.4.2 (potentials), Figure 11.13 (option groups). Read from the chapter HTML; figure caption from the figure page.
- **Construction cross-reference:** Chapter 12 SM §12.SM.1.2 — industry potentials are "global emissions reduction potentials per technology class per sector" from ~75 studies (Figure 11.13). No regional breakdown.
- **Emission factors / grid EF:** city-supplied (Ember), not this chapter.

## License

Industry numeric facts usable commercially with attribution (SPM.7-lineage data CC BY 4.0); figures per IPCC copyright policy (rebuild from values). Underlying datasets cited by Ch.11 (IEA, World Steel, industry bodies) are proprietary — use IPCC's assessed values, not those sources, for the clean-room build.

## Spatial and temporal scope

- **Geography:** global, by technology class — **no regional or city breakdown** in the potentials. Eq. 11.1 is localizable in principle (territorial term Dm=1), but the chapter's *potentials* are global.
- **Time:** mitigation contributions to 2050/2070; energy-efficiency contribution assessed at **10–40% by 2050**.

## Interpretation warnings

- **Industry is NOT uniformly "no city signal."** ~29% of industry emissions are indirect (electricity 21% + heat 8%, Table 11.1) and therefore **grid-EF dependent**, plus electrification of direct combustion (the FSW+El option) is grid-dependent — the same pattern as buildings. The genuinely city-insensitive part is process emissions (cement/chemicals/F-gas, ~16%+) and the global per-tech efficiency rates.
- **Industry is a weaker *city* lever than buildings/transport.** Process emissions (steel, cement, chemicals) are national/sectoral, rarely a municipal authority; and in GPC they are IPPU (sector IV) = **BASIC+ only**, often outside a city's headline inventory. Industrial electricity is scope 2 (in BASIC), but decarbonising it overlaps grid action (national). So the city-actionable, city-adjustable industry slice is narrow: industrial electricity + energy-efficiency programmes + electrification incentives.
- **Potentials are global per technology class** — applying them to a city is a flat national rate with no city differentiation, except for the grid-EF-dependent slice.
- **Figure 11.13 / Table 11.1 are figure/table-locked** — no DDC data file; values transcribed from the chapter.

## Parsing notes

- Eq. 11.1's `Dm` term ("share of allocated emissions, valid only for sub-global levels; Dm=1 for territorial") is the consumption-vs-production switch — set Dm=1 for a city territorial inventory.
- Table 11.1 shares sum to ~80% across the four named rows; the ~20% remainder is F-gases / waste / other non-CO₂.

## Current release

**2023** (AR6 WGIII cycle). Assessment in `releases/2023/review.md`.
