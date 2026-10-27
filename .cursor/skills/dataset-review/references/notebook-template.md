# Extraction notebook — skeleton and rules

One notebook per release, at the release root (e.g.
`releases/2023/spm7a_extract_clean.ipynb`). Worked examples:
`reviews/ipcc/ipcc-ar6-spm7-mitigation-potentials/releases/2023/` for the
fit-analysis pattern, and `reviews/cl-conaf/cl-conaf-bn-awards/releases/v1/`
for the PII-drop and aggregates-as-charts patterns.

Engineering conventions (block flow, idempotency, parameters, validation
layers, naming) are not restated here — they live in
`knowledge-base/topics/engineering-standards/` and this template defers to
them. This file covers only the review-notebook shape on top of those.

## Why blocks stay simple

Pipelines are Mage, and Mage is block-based (loader → transformers →
exporter). A notebook whose blocks are self-contained ports to a pipeline
nearly mechanically. Simplicity here is pipeline-readiness, not just style.

## Skeleton (fixed order)

1. **Header** (markdown) — what this is, source DOI, link to review README
   and need id. Three lines, not an essay.
2. **Load raw** — read the file, zero transformations. The one exception
   is personal data: if the source carries PII, drop the identifying
   columns here, at load, before anything else, keeping only
   non-identifying derivatives (e.g. `presenter_type`, never name or
   email). The raw file itself is never committed; it lives in `sample/`.
3. **Clean** — one concern per block, each block implementing exactly one
   README parsing note (cite it in a comment). If a needed step has no
   parsing note, add the note to the README first.
4. **Validate** — assertions, not eyeballing: expected record counts,
   spot-checks against published values, no leaked working rows, no PII
   columns in the output, internal sums within tolerance, and units
   confirmed where the source omits them (cross-check an internal total
   against a published figure). Known source-side defects are asserted as
   named exceptions, never silently absorbed. If assertions fail, do not
   export.
5. **Export** — one tidy, pipeline-ready table to `data/` (committed).
   Exactly one committed data file per dataset; aggregates are not written
   as extra CSVs or image files (see Outputs and placement).
6. **Visualise & fit** — render the aggregates the review will cite
   (by-year, by-region, composition, unit rates, execution lag, and so on)
   as charts **inline in the notebook**. Do not save them as image files —
   **never call `fig.savefig(...)`, never write `.png`/image files, and never
   create a `figures/` folder.** The rendered notebook is where the charts
   live, and review.md carries the precise figures as tables and points to
   the notebook for the visuals. Make the charts clean and readable (a title, labelled axes,
   sorted bars, sensible colours, no chartjunk) — they are read by people,
   not just generated. This step also holds the need-driven fit cells: only
   the questions the originating need raises (typically 2-4 cells), not
   open-ended exploration. When a product question arrives later ("can we
   support five bands?"), answer it with a new evidence cell here and write
   the resulting claim into review.md. The canonical fit example is the
   banding analysis in the SPM.7 notebook (§5.4: the longest
   uncertainty-separated chain caps the number of distinct levels the data
   certifies).
7. **Findings** (markdown) — what extraction confirmed, what surprised,
   what flowed back into the README.

## Block rules

- One transformation per block, named result, no clever chaining.
- Each block runnable given only the blocks above it.
- Restart-and-run-all must pass before the notebook is committed.
- End each block with one small visible output so a reader can follow state
  without running it. For anything tabular, let Jupyter render the frame
  (end the cell with the DataFrame, or `display(df)` / `df.head()`) rather
  than `print()` — a rendered frame is readable; a printed one is not.
  Reserve `print` for short scalars or status lines. One small output per
  block, not a wall of prints.

## Outputs and placement

One dataset, one committed data file. The release holds two output
locations, plus charts that live only in the rendered notebook:

- `data/` (committed): exactly one pipeline-ready table — the
  de-identified, typed, tidy CSV a Mage loader would consume. Not a dumping
  ground for every aggregate.
- `sample/` (gitignored): the raw source export and any large or
  PII-bearing working files. Re-download instructions go in the README so
  the notebook re-runs from a clean clone.
- Charts: rendered inline in the notebook, **not saved as image files and
  not committed as a `figures/` folder**. The rendered notebook is the
  single source for the visuals; review.md gives the precise aggregates as
  tables and points to the notebook for the charts.

## Findings flow back

Anything the notebook teaches about the data (defects, distribution
surprises, fit caveats like "supports tiers, not strict ranks") is written
into the README's interpretation warnings or parsing notes with a pointer
to the notebook. The README is what downstream users read; the notebook is
its evidence.
