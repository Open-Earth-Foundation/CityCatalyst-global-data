# UNEP-CCC — sectoral GHG mitigation potentials in 2030/2035 (EGR 2024 background report)

Dataset review entry for the measure-level data behind **"Bridging the gap: Sectoral greenhouse gas mitigation potentials in 2035"** (UNEP-CCC & Common Futures, 2024) — the background study for Chapter 6 of the UNEP Emissions Gap Report 2024. It assesses techno-economic mitigation potentials at costs up to **200 US$/tCO2e** for 2030 and 2035 (some sectors also 2040), against a current-policy baseline, across energy, AFOLU, buildings, transport, industry, waste, and F-gases.

**No machine-readable data annex is published** (verified 2026-06-05: the publication page offers only the PDF; the "supplementary material" referenced in the industry chapter is not published). The release here hand-transcribes the report's tables and machine-verifies every value against the PDF text — see `releases/2024/unep2035_extract_clean.ipynb`.

## Canonical downloads

- Report PDF (the only published artifact): [unepccc.org publication page](https://unepccc.org/publications/bridging-the-gap-sectoral-greenhouse-gas-mitigation-potentials-in-2035/) / [direct PDF](https://unepccc.org/wp-content/uploads/2024/10/sectoral-greenhouse-gas-emissions-reductions-potentials-in-2035.pdf)
- Parent report: [UNEP Emissions Gap Report 2024](https://www.unep.org/resources/emissions-gap-report-2024) (Chapter 6)
- Citation: UNEP-CCC and Common Futures, *Bridging the gap: Sectoral greenhouse gas mitigation potentials in 2035* (2024)

## Why we use it

- **The 2035 update of the SPM.7-style assessment** — same intellectual lineage (Blok et al. 2017 → IPCC AR6 SPM.7 → this), with a 2035 horizon and post-AR6 data (notably the solar/wind upgrade and the EV-into-baseline correction). Serves need `2026-06-action-reduction-potential` as a complement / cross-check to `ipcc-ar6-spm7-mitigation-potentials`.
- **Finer cost cut-off context but coarser cost structure** — single <$200/tCO2e cut-off (no cost buckets, unlike SPM.7).
- **About 50 measure-level rows across 7 sectors** with uncertainty ranges for most 2035 values; includes sectors SPM.7 handles thinly (waste split into solid/wastewater, buildings direct vs indirect).

## License — restrictive, read before any production use

**Not CC BY.** The copyright notice permits reproduction "in whole or in part and in any form for educational or non-profit services without special permission… provided acknowledgement of the source is made", but states **"No use of this publication may be made for resale or any other commercial purpose whatsoever without prior permission in writing from the UNEP Copenhagen Climate Centre."**

Consequences for us: fine for research, internal analysis, and non-profit deliverables with attribution; **production use inside a commercial offering requires written permission from UNEP-CCC** (contact: unep-ccc@un.org). Note the disclaimer also bars use "for publicity or advertising". The IPCC SPM.7 dataset (CC BY 4.0) does not have this constraint — prefer it where the two overlap and licensing matters.

## Spatial and temporal scope

- **Geography:** global potentials only — no regional/national breakdown (a few regional remarks in prose). Same "global prior, not local truth" caveat as SPM.7, plus the same displacement caveat for fast-decarbonizing grids like Chile's.
- **Time:** 2030 and 2035 snapshots vs a current-policy baseline (EGR 2024 Ch.4-compatible; IEA STEPS for energy CO2, EPA 2019 for non-CO2); industry, transport, buildings and waste also report 2040.
- **Cadence:** one-off study in the EGR cycle; a successor would likely accompany a future EGR. Supersedes UNEP (2017) Blok et al.; updates the AR6 SPM.7 2030 view to 2035.

## Interpretation warnings (headline)

- **Potentials are NOT additive** — overlaps are corrected only inside the published aggregates. Never sum measure rows; never sum sector rows without the Table 1 overlap corrections (−2.3 GtCO2e in 2030, −3.9 in 2035).
- **Two typos in the published PDF are kept as printed and flagged** in the clean CSVs: nuclear 2030 (5.9, likely 0.59; `suspect_value_2030`) and Table 1's agriculture 2035 range (`suspect_range_2035`). Filter on `flags`.
- **Buildings "indirect" potential is electricity-sector potential** — it is the bulk of the buildings number and is netted out in cross-sector totals.
- **GWP vintage mixes**: biogenic methane in waste uses GWP 27.2; baselines for non-CO2 are EPA 2019 interpolations. Mind GWP consistency when joining with other datasets.
- Full claim-by-claim guidance: `releases/2024/review.md`.

## Releases

- `releases/2024/` — transcription of the October 2024 report (sha256 `7f804f7d…`), clean CSVs + verification notebook. Research release; not production-approved (license constraint above). **Data is local-only**: because the license is not open, the PDF and CSVs live in the gitignored `sample/` folder — rebuild instructions in `releases/2024/review.md` ("Getting the data").
