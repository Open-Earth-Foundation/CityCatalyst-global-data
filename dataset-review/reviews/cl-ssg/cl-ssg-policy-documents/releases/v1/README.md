# cl-ssg-policy-documents · v1

Clean-slate redesign of the Chilean climate and territorial policy
extraction pipeline, informed by what the previous iteration taught and
by the FinBRAZEEC reference pipeline.

This folder is the canonical home for the v1 architecture. Inputs and
outputs used by the substrate stage live under `v1/`: source PDFs in
`policy-pdf/`, mapping in `data/source_pdf_map.csv`, registry inputs in
`data/registry/`, and generated substrate in `data/markdown/`.

## Architecture in one paragraph

PDFs are converted to page-marked markdown with a section heading map
that flags noise sections (procurement, annexes, abbreviations) for
skipping. Non-skipped pages are batched within a single section and
sent to a small-model atom extractor, which returns per-page atoms —
small, single-fact units that carry verbatim evidence and (where
present) parsed numeric values. Atoms are stored as JSONL per document.
A second, larger-model synthesis pass per document selects the highest-
priority atoms by primitive type and produces a structured per-document
policy summary. Downstream alignment scoring compares city candidate
actions against applicable summaries, not against raw atoms.

## Policy–action alignment (deterministic)

After `profile_facets.py` / `profile_channel.py` have produced
`data/derived/actions_profiled.csv` and `data/derived/signals_profiled.csv`,
run the matcher (no LLM):

```bash
cd dataset-review/reviews/cl-ssg/cl-ssg-policy-documents/releases/v1
python3 scripts/v1_match_signals_to_actions.py match
python3 scripts/v1_match_signals_to_actions.py status
python3 scripts/v1_match_signals_to_actions.py verify
```

Outputs live under `data/policy_action_alignment/` (`_index.csv` plus
`<source_document_id>/<action_id>.json` score cards). Use `--force` on
`match` to delete that directory before a full rebuild. The matcher uses
a channel / intervention–outcome bridge gate (outcome-only rows are
dropped), default `--min-score` **0.45**, a `max + bonus` aggregate for
`policy_score`, and a coarse `match_quality` field on each JSON card
(`strong` / `moderate` / `weak`).

## Per-city action ranking (deterministic)

After matcher outputs exist, aggregate locality-weighted rankings per
Chilean comuna (`local_codes.csv` + `source_documents.json`; no LLM):

```bash
cd dataset-review/reviews/cl-ssg/cl-ssg-policy-documents/releases/v1
python3 scripts/v1_aggregate_per_city.py aggregate
python3 scripts/v1_aggregate_per_city.py status
python3 scripts/v1_aggregate_per_city.py inspect 08101
```

Writes `data/city_action_alignment/_index.csv`, per-comuna folders with
`_city_summary.json` and `<action_id>.json` cards. Use `--force` on
`aggregate` to wipe the output tree first; `--only-city` / `--only-region`
for partial runs.

## What lives where

```
v1/
  README.md                       this file
  methodology.md                  the four-stage architecture, refined
  scripts/
    v1_build_substrate.py         stage 1 CLI (convert/inspect/verify/map)
    v1_match_signals_to_actions.py  deterministic signal×action matcher
    v1_aggregate_per_city.py         per-comuna rankings from alignment cards
  policy-pdf/                     source PDFs used by source_pdf_map.csv
  data/
    source_pdf_map.csv            maintained PDF mapping (v1-relative paths)
    registry/
      source_documents.json       source metadata registry
      local_codes.csv             territorial code mapping input
      data_requirements_general_policies.csv  policy requirement input
    markdown/
      <source_document_id>/       generated substrate artifacts
    derived/                      profiled actions/signals CSVs
    policy_action_alignment/      matcher score cards + index
    city_action_alignment/        per-comuna summaries and action rankings
  schemas/
    atoms.schema.json             stage 2 output: per-document atom JSONL contract
    policy_summary.schema.json    stage 3 output: per-document summary JSON contract
    extraction_rules.md           normative rules for atom extraction
  rubrics/
    parcc.md                      synthesis rubric for regional climate plans
    sector_plan.md                synthesis rubric for national mitigation plans
    framework.md                  synthesis rubric for NDC, ECLP, LMCC
    territorial_plan_thin.md      synthesis rubric for territorial planning instruments
    environmental_program.md      synthesis rubric for PRAS programs
```

The rubrics are different from the previous family templates. The
templates told the LLM how to do per-slice extraction, which is no
longer the contract. The rubrics tell the synthesis stage how to
assemble a per-document summary from atoms, family by family.

## What carries forward from the previous iteration

- The methodology (refined, not replaced)
- The verbatim evidence discipline
- Page-grounded references with `page_start` and `page_end` integers
- The substrate concept: pre-converted, page-marked text per document
- The tracker pattern: workflow state separate from extracted content
- Domain knowledge encoded in the family rubrics
- The provider abstraction in the harness
- The PDF source corpus in `policy-pdf/`
- The document registry in `data/registry/source_documents.json`

## What changes

- Two extraction stages instead of one. Atoms are family-agnostic,
  small, cheap. Synthesis is family-specific, larger, single-call per
  document. Output truncation as an operational problem largely
  disappears because per-call output is bounded.
- Section-filter via heading map. Procurement, legal, annex, and
  table-of-contents pages are skipped before any LLM call.
- Section-aware page batching. Up to four consecutive pages from the
  same section are batched into one call. Calls do not cross sections.
- Atoms carry parsed numeric fields (`raw_value_numeric`, `raw_unit`)
  alongside text fields. Comparing targets across documents stops
  being a string-parsing problem.
- An `evidence_kind` field on every atom (quantitative, qualitative,
  categorical) lets synthesis prioritize numeric evidence cleanly.
- Mitigation focus is a synthesis-stage concern, not a per-call filter.
  Atom extraction stays neutral; synthesis selects mitigation-relevant
  atoms by sector, measure_type, and the document's family rubric.

## What is intentionally archived

- The single-stage extractor harness with sub-batching, page-fraction
  hints, focus filter, and per-slice retry. Useful machinery for the
  problem it was solving; not the problem v1 is solving.
- The slice-based decomposition. Slices are replaced by section-batched
  page groups, which match how the source documents are actually
  structured.
- Pre-verbatim sample JSONs and legacy scaffolds.

The previous iteration's harness, schemas, and outputs remain on disk
under `data/legacy/` and the older top-level directories. They can be
referenced for diff, comparison, or recovery, but they are not part of
the v1 contract.
