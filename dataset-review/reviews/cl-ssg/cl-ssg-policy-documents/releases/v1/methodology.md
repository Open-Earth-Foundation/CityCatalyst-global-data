# Methodology · v1

A four-stage pipeline for extracting structured, auditable policy
evidence from collections of long-form PDF documents using LLMs. The
methodology is designed to separate model-independent contracts (data
shape, audit story, domain knowledge) from model-dependent operations
(token budgets, rate limits, output adherence) so that the
model-independent layer survives provider and model changes.

This document supersedes the earlier root-level `methodology.md`. The
earlier document described a single-stage extraction; v1 splits that
into two stages and adds explicit substrate filtering.

## The four stages

### Stage 1 · Substrate

PDFs are converted once to page-marked markdown plus a section map.

```
data/markdown/<source_document_id>/
  document.md                  page-marked markdown for the whole document
  section_map.json             per-page heading + skip flag
  document.json                page_count, sha256, language, source_url
```

Markdown preserves headings, tables, and lists in a form LLMs parse
reliably while stripping layout noise. The page-break marker
`<!-- page_break: N -->` is the audit thread that connects every later
atom back to its source page.

The section map is built by scanning headings on every page and
classifying each page into its current section. Pages whose section
matches a skip pattern (procurement, financial management annexes,
legal covenants, abbreviation lists, table of contents, gender annex,
etc.) are flagged for exclusion before any LLM call. On a 200-page
sector plan this typically removes 15–25% of pages without losing
substantive content.

The substrate is built once per document, deterministic, and never
re-derived during extraction. Atoms and synthesis read from it.

### Stage 2 · Atoms

For each document, iterate non-skipped sections. Within each section,
batch up to four consecutive pages into a single LLM call. Calls never
cross section boundaries. The model returns a JSON array of **atoms** —
small, single-fact units that carry verbatim evidence.

Why batched at 4 pages per call. Per-call output stays under any
model's output token budget. A typical 4-page batch yields 5–15 atoms
(~3,000–8,000 output tokens). Truncation, sub-batching, and per-document
operational tuning largely disappear as problems.

Atoms are family-agnostic. The same extraction prompt works for every
document family. Family-specific shaping happens in stage 3, not here.

Atoms are written to `data/atoms/<source_document_id>.jsonl` — one atom
per line. JSONL is preferred over a wrapping object because it lets you
append, stream, and grep without parsing the whole file.

### Stage 3 · Synthesis

For each document, select the most useful atoms by primitive_type with
hard caps (e.g. financing: 30, target: 20, action: 25), prioritized by:

1. document_status — final > draft > consultation
2. evidence_kind — quantitative > qualitative > categorical
3. presence of `raw_value_numeric` — atoms with parsed numbers first
4. explicitness — explicit > inferred

The selected atoms plus the document registry record are sent in a
single LLM call to a synthesis prompt that is **family-specific**. The
family rubric (under `v1/rubrics/`) tells the synthesis call how to
assemble the structured per-document policy summary.

Synthesis output is `data/summaries/<source_document_id>.json` — one
JSON object per document conforming to `policy_summary.schema.json`.
Every claim in the summary carries an `evidence_anchor` referencing
the atom_id and page that supports it.

This is where mitigation focus is applied. The synthesis stage filters
atoms by sector, measure_type, and family rubric to produce a
mitigation-focused summary. Atom extraction stays neutral so the same
atoms can later support adaptation or mixed-focus summaries without
re-extraction.

### Stage 4 · Alignment

Out of scope for v1 dataset construction. Documented here because it
shapes what the earlier stages need to produce.

For each city plus each candidate action, identify the applicable
policy summaries (from `data/summaries/`), compare the candidate
action against each summary's named_actions, headline_targets, and
priority_sectors, and produce an alignment score backed by evidence
anchors.

The alignment layer reads from `policy_summary.json` files, not from
atoms. Per-document deduplication and prioritization is already done
upstream in stage 3.

## What is stable, what evolves with model capability

The model-independent layer. Substrate (1), the atom and policy_summary
schemas, the family rubrics, the verbatim evidence discipline, and the
tracker. These encode the domain and the data contract, not the LLM's
quirks. They survive model upgrades intact.

The model-dependent layer. Per-call batching size (currently 4 pages),
output token budgets, structured-output formatting, retry-on-truncation,
provider abstraction. These exist because today's models have limits.
As context windows and output budgets grow, batches get larger,
truncation handling fades, structured output adherence improves.

Two things will not get easier and you should always plan for them.
Page-grounded evidence remains essential because audit does not go
away. Family-specific synthesis remains essential because no model can
infer what makes a useful per-document summary in your domain without
you encoding the rubric.

## Failure modes worth designing for upfront

Paraphrase drift. The model lightly rewords source text into
`evidence_text`. Mitigation: schema requires verbatim, validator
confirms substring match against page text from the substrate, the
extraction prompt explicitly frames evidence_text as a copy operation
rather than a writing task.

Output truncation. The model hits its output token cap mid-array.
Mitigation: per-call output is bounded by 4-page batching and small
atom shape. If it ever does happen, escalate output budget and retry,
not split the slice.

Cross-document restatement. Operational documents restate national
framework targets verbatim, which can be miscounted as local
commitments. Mitigation: atom carries `_doc_type`, synthesis stage
deduplicates restatements via doc-type priority and an
`echoes_atom_id` link if the synthesis prompt detects restatement.

Section-skip false positives. The heading map skips a page that
actually contained a useful target buried under a procurement-shaped
heading. Mitigation: section_map.json is reviewable and editable, the
skip patterns are conservative (only obvious noise), and a manual
override file can force-include specific pages.

Schema drift. JSON Schema and markdown documentation diverge.
Mitigation: lock the JSON Schema as the source of truth, and write
the markdown rules in `extraction_rules.md` alongside, version-stamped.

Sparse documents. A document yields few atoms either because it is
genuinely sparse or because it uploaded as a scanned PDF with bad text
extraction. Mitigation: substrate stage marks low-text pages,
synthesis records `coverage_notes` flagging documents with
suspiciously low atom counts.

## Lean playbook

If you are starting a new extraction project from scratch, do this in
order. The same six steps that produced this methodology will work
for any structured-extraction problem with PDFs as input.

First, pick five pilot documents that you believe represent the typical
shape of the corpus.

Second, write the atom schema and the policy_summary schema as JSON
Schemas. Decide what is verbatim, what is normalized, what is numeric.

Third, build the substrate stage on the pilot. Spot-check the section
maps; refine the skip patterns until 90% of skipped pages are
genuinely noise.

Fourth, write one family rubric against one pilot document. Hand-build
the policy_summary for that document by reading the atoms it produces
and writing the synthesis output yourself. This is how you discover
what the rubric needs to say.

Fifth, build the atom extractor and the synthesis pass. Run on the
five pilots. Compare automated synthesis against your hand-built one;
iterate the rubric, not the extractor, when the failure is
domain-shaped.

Sixth, scale. Add the rest of the family rubrics. Run the full corpus.
Add a tracker once you have more than ten documents.

The atom extractor is mostly model-agnostic. The synthesis pass is
where domain knowledge concentrates. Plan to spend more time iterating
the rubrics than tuning the extractor.

## Notes specific to this project

| Stage | Concrete artefact (intended) |
| --- | --- |
| Substrate | `scripts/v1_prechunk_pdfs.py`, `data/markdown/<id>/` |
| Atom schema | `v1/schemas/atoms.schema.json` |
| Policy summary schema | `v1/schemas/policy_summary.schema.json` |
| Extraction rules | `v1/schemas/extraction_rules.md` |
| Family rubrics | `v1/rubrics/{parcc, sector_plan, framework, territorial_plan_thin, environmental_program}.md` |
| Atom extractor | `scripts/v1_extract_atoms.py` |
| Synthesizer | `scripts/v1_synthesize.py` |
| Tracker | `data/registry/extraction_tracker.json` (extended schema) |

Specific learnings carried forward from v0 that informed v1:

- Spanish-language source means evidence_text must preserve accents,
  smart quotes, and ligatures verbatim. Validator normalization (NFC,
  ligature fold, smart-quote fold) handles comparison without losing
  fidelity in storage.
- Chilean PARCCs are adaptation-dominant and frequently restate
  national NDC and ECLP commitments. Family rubrics handle this
  explicitly: PARCC summaries credit local commitments distinctly
  from restatements.
- The previous focus filter at extraction time has been replaced by
  focus selection at synthesis time. This avoids re-extracting when
  the focus changes and preserves adaptation evidence in the atoms
  layer for future use.
- The previous five-slice template per family has been replaced by a
  single section-aware atom extractor plus a family rubric for
  synthesis. The rubrics retain the domain knowledge from the old
  templates without binding it to per-slice extraction.
