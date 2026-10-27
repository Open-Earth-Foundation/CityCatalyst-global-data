# IPCC AR6 WGII — multidimensional feasibility of adaptation options (CCB FEASIB)

Dataset review entry for the data behind **AR6 WGII Cross-Chapter Box FEASIB** — the multidimensional feasibility assessment of adaptation options and climate responses, an update of the SR1.5 Chapter 4 feasibility framework. Each option is scored across the same **six feasibility dimensions** used for mitigation in SR1.5 (economic, technological, institutional, social/socio-cultural, environmental, geophysical), plus a **potential-feasibility** roll-up and a **mitigation-synergy** flag, assessed at global scale, near term, up to 1.5°C warming. This is the adaptation counterpart to `ipcc-sr15-mitigation-feasibility`: same dimension scaffold, options drawn from adaptation rather than mitigation. The release here is the **2022 WGII assessment** (figure published as SPM.4 / TS.6; carried into the 2023 Synthesis Report as SYR SPM.7a).

## Canonical downloads

- **Indicator-level source (the detailed tables):** AR6 WGII Chapter 18 Supplementary Material, Cross-Chapter Box FEASIB, Section SMCCB FEASIB.1 — Tables SMCCB FEASIB.1 through the per-transition set (`Table SMCCB FEASIB.1.1` onward). PDF: [IPCC_AR6_WGII_Chapter18_SM.pdf](https://www.ipcc.ch/report/ar6/wg2/downloads/report/IPCC_AR6_WGII_Chapter18_SM.pdf) (FEASIB section is pp. 18SM-11 to 18SM-43).
- **Figure-level scores (machine-readable):** the per-option High/Medium/Low dimension ratings behind Figure SPM.4(a) and Figure TS.6, archived by the WGII TSU at [doi:10.48490/tnk5-rv35](https://doi.org/10.48490/tnk5-rv35) via [IPCC DDC record 5916](https://ipcc-browser.ipcc-data.org/browser/dataset/5916/0).
- **Figure and full caption:** [AR6 WGII Figure SPM.4](https://www.ipcc.ch/report/ar6/wg2/figures/summary-for-policymakers/figure-spm-4/). The caption pins the data provenance: *{CCB FEASIB, Table SMCCB FEASIB.1.1, SR1.5 4.SM.4.3}*.
- **Synthesis-Report restatement (same data, near-term panel):** SYR SPM.7a / LR Fig 4.4a, [DDC record 8444](https://ipcc-browser.ipcc-data.org/browser/dataset/8444/0), also mirrored on [NASA SEDAC](https://sedac.ciesin.columbia.edu/ddc/ar6-syr-spm-7a-lr-fig4-4a/) with an Excel workbook download.

## Why we use it

- **The adaptation axis the mitigation priors do not cover.** `ipcc-sr15-mitigation-feasibility` scores mitigation options on the six dimensions; this dataset does the same for adaptation options, so the action catalogue's adaptation entries get an authoritative, literature-backed feasibility prior on the *same scaffold*. Pair the two when an action catalogue spans both mitigation and adaptation.
- **Stable global priors for adaptation actions** before local indicators are applied — usable as an ordinal signal (relative ordering of options), exactly as the SR1.5 priors are used for mitigation.
- **Explicit provenance.** Every cell traces to a published table and row in the Chapter 18 SM, with full citation lineage, and the figure-level roll-up traces to DDC record 5916.

## License

**CC BY 4.0** for the numeric figure data on the IPCC DDC (record 5916, doi:10.48490/tnk5-rv35) — usable commercially with attribution, redistribution fine with attribution. Cite both the dataset DOI and the report. The **Chapter 18 SM tables and text** (the indicator-level detail and citations) are governed by **IPCC copyright policy**, not CC BY — reproduce figures/text per [ipcc.ch/copyright](https://www.ipcc.ch/copyright/), and prefer rebuilding derived values from the assessed scores rather than redistributing the table images. Same split as the other AR6 IPCC entries in this catalog: DDC numeric data is open, SM prose/figures are not. *(License split: verified — DDC CC BY per record 5916 and repo precedent; SM under IPCC copyright per ipcc.ch/copyright.)*

## Spatial and temporal scope

- **Geography:** global assessment, not location-specific. Use as a **prior**, then adjust with local indicators where the methodology allows — identical posture to the SR1.5 mitigation priors. The authors note feasibility can differ by region; the published scores are the global synthesis.
- **Temporal reference:** near term, assessed **up to 1.5°C** global warming. The caption is explicit that literature above 1.5°C is limited, so feasibility at higher warming levels is **not robustly assessable** and is left unrated. Treat as a **2022-vintage** evidence base (WGII AR6); the 2023 SYR restatement carries the same underlying scores. Frozen — no update cadence; superseded only by AR7-cycle products.

## Interpretation warnings

- **"Insufficient evidence" is a dash, not a zero, and it is common.** Many option × dimension cells are unrated because the literature did not support a robust score. A dash means *not assessed*, not *low feasibility* — do not coerce dashes to a numeric low. This is the single most likely silent error downstream.
- **Evidence and agreement are separate axes from the score.** Each option carries an Evidence level (Robust / Medium / Limited) and an Agreement level (High / Medium / Low) that qualify how much weight the High/Medium/Low rating should bear. A "High" feasibility on Limited evidence / Low agreement is a weak signal; carry both qualifiers, do not drop them.
- **Scores are ordinal bands (High / Medium / Low), not cardinal values.** Do not average a High and a Low into a "Medium", and do not treat the three bands as evenly spaced. Use for relative ordering, standardise alongside other features before any weighted combination — same rule as the SR1.5 priors.
- **Potential feasibility is a roll-up, not a seventh independent dimension.** The per-option "potential feasibility" column summarises across the six dimensions; do not double-count it as an extra dimension when aggregating.
- **Options are not the action catalogue's options.** AR6 names adaptation responses (e.g. resilient power systems, integrated coastal zone management, forest-based adaptation, WASH, sustainable aquaculture) at a coarser grain than a city action catalogue. A mapping step (action → AR6 option) is required before these priors attach, and some catalogue actions will have no AR6 home — expect a `no_match` tail, as in the mitigation mapping.
- **Mitigation-synergy flag is directional, not quantitative.** The High/Medium/Low synergy-with-mitigation flag says an adaptation option also helps (or does not help) mitigation; it is not an abatement quantity and must not be read as one.

## Parsing notes

These are the things that break naive ingestion. The full assessment has been extracted — `releases/2022/extract_feasibility.ipynb` turns each note below into a cleaning step — so they double as the map of where extraction had to be careful.

- **The indicator ratings are color-encoded, exactly like SR1.5 4.SM.** Each indicator's High/Medium/Low rating is a colored bar in the cell, not text. A plain text extraction (WebFetch, naive `pdftotext`) recovers the structure — option names, the six dimensions and their indicators, Evidence/Agreement rows, the `NE`/`LE`/`NA` flags, citation lineage — but **not** the ratings. The ratings come from cell-fill color extraction with `pdfplumber`. Verified palette: bars are three blue families — dark `R<0.35` = **High**, mid `R≈0.5` = **Medium**, pale `R≈0.85` = **Low**; the cream `(1.0,0.954,0.852)` fill is header/label shading, never a rating.
- **`NA` is not `NaN`.** The `flag` column in the extracted CSV holds the literal string `NA` (not-applicable, 22 cells, almost all Geophysical). Pandas' default `read_csv` turns `"NA"` into `NaN` and silently merges these with true blanks — read with `keep_default_na=False` or `na_values=[]`. This is the single most likely silent ingestion error.
- **Table 3 has three option columns, not four.** Its caption lists four phrases (sustainable forest management/conservation, reforestation/afforestation, biodiversity management, agro-forestry) but the table renders three columns because the first two are merged into one option, **Forest-based adaptation** — matching how SPM.4 labels it. So there are **23 options total**, not 24. Don't derive the option count from caption phrases.
- **Tables straddle page breaks; option sets switch at caption positions, not page edges.** The energy table's Environmental/Geophysical rows sit at the top of the same page that starts table 2. A parser keyed on page boundaries mis-assigns these rows; key on the `Table SMCCB FEASIB.N` caption y-positions instead.
- **Indicator labels line-break mid-word.** Long labels hyphenate across lines (`Intergenera-` / `tional`, `Macroeconom-` / `ic`), so match on short prefixes, not full strings. Dimension labels sit at x≈48–60 and indicator labels at x≈75+, so the dimension/indicator columns separate cleanly at x≈68.
- **Citation columns dominate the table body.** Most of each row is the per-cell reference list (often 10+ studies), not data — key on indicator-name and dimension-header rows, never on line counts.
- **Tables 8–9 are a different structure.** After the seven feasibility tables, SMCCB FEASIB.2 gives adaptation↔mitigation synergy/trade-off tables (mitigation options as columns, synergy strength). They are not part of the per-cell feasibility extract and are excluded.

## Repository layout

The Chapter 18 SM PDF is **not redistributed** here (IPCC copyright); fetch it from the canonical link above into `releases/2022/sample/` (gitignored) to re-run the notebook.

| Path | Rows | Purpose |
|------|------|---------|
| `releases/2022/extract_feasibility.ipynb` | — | Self-contained extraction: reads the SM PDF, color-decodes the bars, validates, exports the two CSVs. Restart-and-run-all passes with the PDF present. |
| `releases/2022/data/ar6_wg2_feasibility_per_cell.csv` | 460 | One row per (option × dimension × indicator): 23 options × 20 indicators. `rating` ∈ {High, Medium, Low}; `flag` ∈ {NE, LE, NA}; exactly one of the two is set. |
| `releases/2022/data/ar6_wg2_feasibility_per_option.csv` | 23 | Per-option × dimension roll-up (dominant band) mirroring the SPM.4 / DDC-5916 figure grain. |

Extraction summary: 390 ratings (131 High, 191 Medium, 68 Low) + 70 insufficient-evidence flags (27 LE, 21 NE, 22 NA), zero blank. NA concentrates in Geophysical; NE/LE in Institutional and Socio-cultural.

## Current approved release

**2022** (dataset review folder; production approval is tracked in `catalog/index.yaml`). Extracted and validated; not yet promoted — see the release `review.md` for what the data can and cannot support.
