# IPCC AR6 — mitigation options, costs and potentials 2030 (Figure SPM.7)

Dataset review entry for the data behind **AR6 Figure SPM.7**: estimated emissions reduction potential and cost of about 31 mitigation options in 2030, assessed by WGIII with a common methodology across all sectors (about 175 underlying sources). Two published versions exist: the WGIII original (2022) and the SYR restructured merge (2023). The release here uses the **SYR version**, whose `Final` sheet matches the published SYR figure; the WGIII original is preserved inside the same file as the `WGIII data` sheet.

## Canonical downloads

- SYR version (this release): [doi:10.48490/3c86-xp02](https://doi.org/10.48490/3c86-xp02) via [IPCC DDC record 6119](https://ipcc-browser.ipcc-data.org/browser/dataset?id=6119)
- WGIII original: [doi:10.48490/ayfg-tv12](https://doi.org/10.48490/ayfg-tv12)
- Figure and full caption: [AR6 WGIII Figure SPM.7](https://www.ipcc.ch/report/ar6/wg3/figures/summary-for-policymakers/figure-spm-7/)

## Why we use it

- **The potential axis for action prioritization** — per-option reduction potential (GtCO2e/yr in 2030) split into cost buckets (<0 to 200 US$/tCO2e) with uncertainty bounds, from a single internally consistent methodology. Supports ordinal ranking of mitigation actions (need `2026-06-action-reduction-potential`).
- **Pairs with `ipcc-sr15-mitigation-feasibility`** — SPM.7 explicitly excludes feasibility-beyond-cost; the SR1.5 dataset provides exactly that axis. Together they give potential × feasibility priors for action scoring.
- **Near-native TEF mapping** — ClimateView's Transition Element Framework compendium is built on the WGIII SPM.7 structure, and the file's `New categories` sheet crosswalks SYR ↔ WGIII categories. Curated mapping: `releases/2023/data/spm7a_option_to_tef.csv` (house schema; 19/31 options map to ≥1 TE, adjudicated 2026-06-05). The 12 unmapped options are essentially the non-city-actionable set (nuclear, CCS/CCU, fugitive CH4, F-gases, material efficiency, food-loss prevention, land/agriculture) — TEF's gaps act as a city-relevance filter, but only 19 options' potential evidence flows through to TEs.

## License

**CC BY 4.0**, stated on the DDC record. Cite both the dataset DOI and the report (SYR SPM, IPCC 2023). Redistribution fine with attribution.

## Spatial and temporal scope

- **Geography:** global potentials extrapolated from sectoral studies — use as a prior for ordinal ranking, not as local truth. Potentials depend on what an option displaces: for fast-decarbonizing grids (e.g. Chile), electricity-displacing options carry different local potential than the global figure implies.
- **Time:** 2030 snapshot against a current-policy (about 2019) baseline. The caption warns relative importance shifts beyond 2030. Dataset is frozen (v0.0.1, 2023) — no update cadence to track; superseded only by AR7-cycle products or the UNEP-CCC 2035 potentials update.

## Interpretation warnings

- **Potentials are NOT additive** — assessed independently per option; do not sum into a "total potential".
- **Uncertainty is typically 25–50%** of total potential; adjacent-ranked options are effectively ties. Bounds are missing for about a third of options.
- **Cost buckets are stale-ish** — study costs mostly 2015–2020, no inflation correction; conservative for solar/wind/EVs. Use as coarse tiers, not boundaries. The 100–200$ bucket may be underestimated; grid integration costs and externalities excluded.
- **Four options (electric vehicles, dietary shift, food-loss reduction, CCU) have all potential in "no costs allocable"** — they vanish from cost-bucket-based rankings unless handled explicitly (e.g. a separate "cost unquantified" tier).
- **Uncertainty intervals overlap heavily** — even top-5 options overlap 7–18 others (see fit analysis in `releases/2023/spm7a_extract_clean.ipynb`). The data supports coarse tiers (top/middle/tail), not a strict 1–31 ordering; present downstream rankings as tiers.

## Parsing notes

- Use the `Final` sheet for the published (SYR-collapsed) figure; **stop parsing at the `MERGING:` marker row** — rows below are working notes (geothermal/hydro split) that double-count.
- **The `WGIII data` sheet holds a finer grain than the figure** — 43 options vs the `Final` sheet's 31, with the LDV/HDV, public-transport/bikes, and shipping/aviation splits un-collapsed. Extracted to `data/spm7a_wgiii_options_2030_clean.csv`. (General lesson: an IPCC figure's xlsx can contain a less-merged source sheet behind the published figure — check for it before treating the figure grain as the finest available.)
- Sheets are padded to 1000 phantom rows; option names carry trailing spaces and one truncated label ("Carbon capture with ").
- Sector headers (ENERGY, LAND/WATER/FOOD, ...) are inline rows, not a column.
- `smooth` flag marks options whose cost-bucket breakdown is uncertain (gradual color in the figure) — bucket values for these are evenly spread estimates, not measurements.
- Source-side rounding residues: cost buckets sum to ≤0.02 GtCO2e off the stated total for "Geothermal and hydropower" and "Forest and fire management" (found during extraction; asserted as known exceptions in `releases/2023/spm7a_extract_clean.ipynb`).

## Current approved release

**2023** (dataset review folder; production approval is tracked in `catalog/index.yaml`).
