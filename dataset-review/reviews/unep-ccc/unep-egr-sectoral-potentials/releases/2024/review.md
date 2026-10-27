# Review — UNEP-CCC sectoral mitigation potentials 2030/2035, release 2024

What this release's data can and cannot support. Dataset-level facts (license, provenance) live in the review README one level up.

## Scope and status

All data files live in `sample/`, which is **gitignored**: the source license is not an open license (no redistribution for commercial purposes; see README), so neither the PDF nor the transcribed tables are committed. See "Getting the data" below to rebuild the folder locally.

- `sample/unep2035_potentials_clean.csv` — 88 rows: measure-level mitigation potentials (GtCO2e/yr vs current-policy baseline, <$200/tCO2e) for 2030 and 2035 (2040 where published) across energy, AFOLU, buildings, transport, industry, waste, F-gases; with uncertainty ranges, source tables, source references, and data-quality `flags`.
- `sample/unep2035_sector_summary.csv` — 13 rows: Table 1 cross-assessment summary (UNEP 2017 / IPCC AR6 / EGR 2024 columns), overlap corrections, corrected totals, and the 1.5°C emissions gap rows.
- `sample/spm7_unep_comparison.csv` — 29-pair crosswalk to the SPM.7 options, basis for the comparison and decision below.
- Produced by `unep2035_extract_clean.ipynb` (self-contained: transcription in §0, machine-verified — all 568 scalars string-matched back to their PDF page; aggregation sanity checks pass).
- Status: research release; **not production-approved** — license requires written permission for commercial use (see README).

## Getting the data

1. Download the report PDF (free, no registration) from the UNEP-CCC publication page: <https://unepccc.org/publications/bridging-the-gap-sectoral-greenhouse-gas-mitigation-potentials-in-2035/> (direct file: `…/wp-content/uploads/2024/10/sectoral-greenhouse-gas-emissions-reductions-potentials-in-2035.pdf`)
2. Save it as `sample/sectoral-greenhouse-gas-emissions-reductions-potentials-in-2035.pdf`. The notebook asserts sha256 `7f804f7db2e50c28ee7d01ab3f4c471741dffe795222ebfa9f1c73efeb079fc1` (October 2024 version) — if UNEP-CCC replaces the file, re-verify the transcription before accepting a new hash.
3. Run `unep2035_extract_clean.ipynb` top to bottom — it regenerates all three CSVs into `sample/`, re-verifies all 568 values against the PDF, and rebuilds the SPM.7 crosswalk (§7; needs the committed SPM.7 clean CSV and `scipy`).

## Comparison with SPM.7 and decision

Compared against `ipcc-ar6-spm7-mitigation-potentials` over a 29-pair crosswalk (`sample/spm7_unep_comparison.csv`):

- **Ordinally the same dataset family**: Spearman rank correlation 0.81 (2030 vs 2030) and 0.88 (IPCC 2030 vs UNEP 2035). Solar and wind are the unambiguous top tier in both.
- **One structural difference**: UNEP demotes the land options out of the top band — reduced ecosystem conversion 4.0 → 1.8 (outside SPM.7's own uncertainty range), ag carbon sequestration 3.4 → 2.2, A/R 2.8 → 2.6. Mostly baseline vintage (post-2019 policy moved avoided deforestation into the baseline) plus narrower scope (non-forest ecosystems excluded).
- **2030 demand-side values shrink** ≥50% vs SPM.7 (biofuels, diets, EVs, fossil CCS) for the same baseline-vintage reason; diets and EVs converge again by 2035. No band changes under the 3-band scheme.

**Decision (Amanda, 2026-06-05): SPM.7 remains the ranking source.** Same ordinal story, CC BY license, cost buckets, and the adjudicated TEF/action mappings. This release is retained as cross-check evidence only, supplying two caveats to carry into SPM.7 use: (1) treat the land options' high band as baseline-sensitive — under current baselines they sit closer to the medium band, which mainly affects the land-rich action-list mapping's high tier; (2) treat SPM.7's 2030 demand-side potentials (EVs, biofuels, diets) as upper bounds. No measure→TEF mapping will be built for this dataset.

## How to read the schema

- `row_type`: `baseline` rows are sector reference emissions, not potentials; `aggregate` rows are the only summable level; `measure` rows overlap each other.
- `component` (buildings only): `direct` (fuel use in buildings), `indirect` (electricity — counted in the energy sector in cross-sector totals), `total`. Use `component == 'total'` unless you specifically need the split, and never add buildings `indirect` to electricity rows.
- `flags`: filter out `suspect_*` cells before any quantitative use; `range_only` (F-gases) means no central estimate exists.
- Missing uncertainty bounds mean "not stated", not zero — most 2030 measure rows in the energy table have no published range.

## What this data supports

- *"Globally, [measure] sits in a higher 2035 mitigation-potential tier than [measure]."* — valid when uncertainty ranges don't overlap; check the bounds. The clear 2035 top tier: solar (7.9), wind (7.7), then forest measures (A/R 3.6, reduced deforestation 2.6, IFM 2.2).
- *"The 2035 potential of [measure] is [X] GtCO2e at <$200/tCO2e."* — with the cost cut-off stated; this dataset has no cost buckets, so no cheaper-than-$X claims below the 200 cut-off (the few in-text cost remarks — e.g. >50% of forestry under $50 — are noted in `notes`).
- *"Between 2030 and 2035 the potential of [measure] grows/shrinks by [X]."* — the dataset's main addition over SPM.7; e.g. solar 4.2→7.9, industry electrification 1.6→2.1, EVs stay small (0.3→0.6) because EV growth moved into the baseline.
- *"Total 2035 potential (41, range 36–46 GtCO2e) exceeds the 1.5°C emissions gap (32, range 20–37)."* — the report's headline claim, reproducible from the summary CSV.
- Cross-assessment drift claims (UNEP 2017 vs AR6 vs this) via the summary CSV — e.g. agriculture's assessed potential fell from 6.7 to 1.4–2.0 largely on cost-evidence and baseline grounds.

## What this data does not support

- *"City [A] should prioritize [measure]."* — global priors; no regional or national resolution at all (weaker than SPM.7, which at least has sectoral-study provenance by region in the report text).
- *"Total opportunity = sum of rows."* — measures overlap; sectors overlap (buildings/industry × electricity). Only published aggregates and the overlap-corrected total are summable.
- **Any use of nuclear 2030 or Table 1's agriculture 2035 range** — typo cells, flagged (`suspect_value_2030`, `suspect_range_2035`).
- Cost-effectiveness rankings — single $200 cut-off, no cost dimension. Pair with SPM.7's cost buckets if cost ordering matters.
- Fine-grained rankings: with full-range uncertainties (AFOLU is a *full* range, not a central estimate), adjacent measures are ties. Tiering discipline as in the SPM.7 review: ~3 bands maximum.
- 2040 comparisons across all sectors — 2040 is published only for electricity (aggregate), transport, industry, buildings, waste, CH4 from fossil fuels; AFOLU and solar/wind per-measure 2040 are absent.
- Feasibility claims — like SPM.7, feasibility-beyond-cost is out of scope (pair with `ipcc-sr15-mitigation-feasibility`).

## Using it downstream

- No TEF/action mapping exists or is planned for this dataset (see decision above). If that ever changes, go through the `sample/spm7_unep_comparison.csv` crosswalk and reuse the adjudicated `spm7a_option_to_tef.csv` rather than re-adjudicating ~50 rows.
- When this dataset and SPM.7 disagree on 2030 (e.g. EVs 0.3 vs 0.8), the cause is usually **baseline vintage** (2023 baselines absorb recent deployment), not methodology conflict. Prefer this dataset's 2035 numbers and SPM.7's cost structure; state baselines when quoting both.
- Waste CH4 uses GWP 27.2 (biogenic); check GWP basis before joining to GHGI-derived tables.
- License gate: anything user-facing or commercial built on these numbers needs UNEP-CCC written permission first. For ordinal action-ranking evidence in research, attribution suffices.

## Notes on non-obvious fields

- `source_refs` is the literature column as printed — it tells you which upstream study a measure's number actually comes from (often IEA NZE, EPA 2019, Austin 2020, IPCC AR6 Ch.7/11); useful when chasing a number upstream beats trusting the transcription.
- Industry has two aggregates: use the **corrected** one (autonomous implementation removed) for cross-sector work — Table 1 does.
- Geothermal table values are rounded versions of more precise in-text numbers (0.45/0.63); the text numbers are in `notes`.
- Shipping's single measure row equals its aggregate by construction.

## Traceability

- Source PDF: `sample/sectoral-greenhouse-gas-emissions-reductions-potentials-in-2035.pdf` (local-only, gitignored), sha256 `7f804f7db2e50c28ee7d01ab3f4c471741dffe795222ebfa9f1c73efeb079fc1`, retrieved 2026-06-05 from unepccc.org (manual download — sandbox network restrictions; recorded in session notes).
- Transcription + verification: `unep2035_extract_clean.ipynb` (transcription inlined in §0), Claude-assisted, 2026-06-05.
- Review: Amanda, 2026-06-05.
