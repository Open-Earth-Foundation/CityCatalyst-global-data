# Extraction notebook — skeleton and rules

One notebook per release, at the release root (e.g.
`releases/2023/spm7a_extract_clean.ipynb`). Worked example:
`reviews/ipcc/ipcc-ar6-spm7-mitigation-potentials/releases/2023/`.

## Why blocks stay simple

Pipelines are Mage, and Mage is block-based (loader → transformers →
exporter). A notebook whose blocks are self-contained ports to a pipeline
nearly mechanically. Simplicity here is pipeline-readiness, not just style.

## Skeleton (fixed order)

1. **Header** (markdown) — what this is, source DOI, link to review README
   and need id. Three lines, not an essay.
2. **Load raw** — read the file, zero transformations.
3. **Clean** — one concern per block, each block implementing exactly one
   README parsing note (cite it in a comment). If a needed step has no
   parsing note, add the note to the README first.
4. **Validate** — assertions, not eyeballing: expected record counts,
   spot-checks against published values, no leaked working rows, internal
   sums within tolerance. Known source-side defects are asserted as named
   exceptions, never silently absorbed. If assertions fail, do not export.
5. **Export** — one tidy table to `data/` (committed; see file placement
   convention in SKILL.md).
6. **Fit analysis** — only the questions the originating need raises
   (typically 2-4 cells). Open-ended exploration belongs elsewhere.
   When a product question arrives later ("can we support five bands?"),
   answer it with a new evidence cell here and write the resulting claim
   into review.md — the canonical example is the banding analysis in the
   SPM.7 notebook (§5.4: longest uncertainty-separated chain caps the
   number of distinct levels the data certifies).
7. **Findings** (markdown) — what extraction confirmed, what surprised,
   what flowed back into the README.

## Block rules

- One transformation per block, named result, no clever chaining.
- Each block runnable given only the blocks above it.
- Restart-and-run-all must pass before the notebook is committed.
- Every code block ends with a small visible output (print or head) so a
  reader can follow state without running it.

## Findings flow back

Anything the notebook teaches about the data (defects, distribution
surprises, fit caveats like "supports tiers, not strict ranks") is written
into the README's interpretation warnings or parsing notes with a pointer
to the notebook. The README is what downstream users read; the notebook is
its evidence.
