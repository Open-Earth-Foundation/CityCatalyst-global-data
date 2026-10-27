# Review — AR6 WGII adaptation feasibility, release 2022

## Scope and status

This release covers the AR6 WGII Cross-Chapter Box FEASIB multidimensional feasibility assessment of adaptation options — the adaptation counterpart to the SR1.5 mitigation feasibility priors, on the same six-dimension scaffold. **Research, not production-approved.** The full assessment is extracted and validated: `extract_feasibility.ipynb` reads the Chapter 18 SM PDF, color-decodes the rating bars, and writes `data/ar6_wg2_feasibility_per_cell.csv` (460 rows) and `data/ar6_wg2_feasibility_per_option.csv` (23 options). Restart-and-run-all passes against the source PDF, with spot-checks asserted against rendered pages.

What the extract contains: 23 adaptation options across five system transitions (energy; land and ecosystem; urban and infrastructure; overarching; cross-sectoral), each scored on all 20 indicators of the six feasibility dimensions. Of the 460 cells, 390 carry a High/Medium/Low rating (131 High, 191 Medium, 68 Low) and 70 carry an insufficient-evidence flag (27 LE, 21 NE, 22 NA); none are blank. The dimension-level roll-up reproduces the grain of Figure SPM.4 / DDC record 5916.

Everything here is **verified**: the ratings were read from the published SM tables by color and cross-checked visually on the rendered pages. The one deliberate interpretation is the dimension-level roll-up, which takes the dominant band across a dimension's indicators — a summary, not a published value; the published per-option potential-feasibility column (from SPM.4 / DDC 5916) is the authoritative roll-up if an exact match to the figure is needed.

## Visual summary

The notebook's chart shows cell states stacked by dimension. The shape: Economic, Technological and Socio-cultural are the most fully-rated dimensions and therefore the most discriminating across options; Geophysical is dominated by not-applicable cells (physical-feasibility and land-use indicators rarely apply to non-land options); Institutional and Socio-cultural carry most of the limited/no-evidence flags. Run `extract_feasibility.ipynb` for the rendered chart; the precise counts are in the tables of the README and above.

## What this data supports

These are global, near-term, ordinal feasibility ratings for adaptation options, and the load-bearing caveat is that insufficient-evidence cells are common and meaningful — a flag is not a low score.

The data supports statements like: *"At global scale and in the near term (up to 1.5°C), AR6 WGII rated [option] as High/Medium/Low feasibility on the [dimension] dimension."* It supports a relative ordering of adaptation options on a given dimension, used as one feature among several, exactly as the SR1.5 priors are used for mitigation. It supports attaching an authoritative feasibility prior to a city adaptation action once that action is mapped to one of the 23 AR6 options. It supports a per-indicator read (the 20-indicator grain) where a use case needs finer detail than the six-dimension summary — for example distinguishing an option's economic *employment* feasibility from its *microeconomic viability*.

## What this data does not support

The overclaim to watch for is treating a coarse, global, partly-unrated assessment as a precise local score.

It does not support a city-specific or sub-national feasibility number — the assessment is global; localisation is a separate modelling step this data does not perform. It does not support summing or averaging the bands into a single cardinal feasibility value; the three bands are ordinal and not evenly spaced, and the published potential-feasibility column is already the authors' roll-up. It does not support reading an `NA`, `NE` or `LE` flag as a low rating — `NA` means the indicator does not apply, `NE`/`LE` mean the evidence was absent or limited. It does not support feasibility claims above 1.5°C of warming; the authors state the literature is too limited and leave higher levels unrated. It does not support quantitative adaptation–mitigation synergy estimates: the synergy assessment (SM Tables 8–9) is directional strength, not a quantity, and is not part of this extract.

## Using it downstream

Use the bands as an ordinal signal and standardise alongside other features before any weighted combination — never feed raw High/Medium/Low as a 3/2/1 cardinal. Treat `NE`/`LE`/`NA` cells as missing-not-low and handle them explicitly (mask, or carry as a separate "not assessed" state) rather than imputing a value. Read the per-cell CSV with `keep_default_na=False` so the literal `NA` flag is not lost. Map the action catalogue to the 23 AR6 options before attaching priors, and keep an explicit `no_match` tier for catalogue actions with no AR6 home. When mitigation and adaptation actions are scored together, pair this release with `ipcc-sr15-mitigation-feasibility`: both sit on the identical six-dimension scaffold, so a combined feasibility feature is coherent. For anything needing only the dimension summary, prefer the per-option roll-up here or the published figure data (DDC 5916) over re-deriving from the indicator table.

## Notes on non-obvious fields

`rating` is the color-decoded band (High/Medium/Low) and is empty for unrated cells. `flag` carries the source markers `NE` (no evidence), `LE` (limited evidence), `NA` (not applicable) and is mutually exclusive with `rating` — a cell is rated or flagged, never both, and never blank. `transition` is the AR6 system-transition grouping the option belongs to, not a column in the source. `table` is the source table number (1–7) for traceability. In the roll-up file, a dimension cell is the **dominant** band across that dimension's indicators (mode), so it can hide within-dimension spread — go to the per-cell file when the indicator detail matters.

## Traceability

Indicator-level source: AR6 WGII Chapter 18 Supplementary Material, Cross-Chapter Box FEASIB, Tables SMCCB FEASIB.1–7 (pp. 18SM-11 to 18SM-31), IPCC copyright. Figure-level roll-up: WGII TSU archive doi:10.48490/tnk5-rv35, IPCC DDC record 5916, CC BY 4.0; restated in SYR SPM.7a (DDC record 8444, SEDAC doi:10.7927/hjha-bb25). Local input dependency: `sample/IPCC_AR6_WGII_Chapter18_SM.pdf` (gitignored; re-download URL in the review README). Extraction, palette calibration, and validation assertions: `extract_feasibility.ipynb`. Counterpart review: `reviews/ipcc/ipcc-sr15-mitigation-feasibility`.
