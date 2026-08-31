# Active assessment inputs

These two CSVs are the editable inputs for the action-to-risk assessment. Generated
files in `data/output/` must not be edited as a substitute for changing these inputs.

## `mapping_proposals.csv`

One row represents one action × sector × component decision. Stage 1 maintains the
complete six-sector work queue and preserves existing decisions. A new combination is
initialized as `review_required`, with no indicators and `screening_status=not_started`.

Work one sector at a time:

1. Compare the action's primary mechanism with that sector-component's terminal indicators.
2. Set `proposed_eligibility` to `eligible`, `not_eligible` or `review_required`.
3. For an eligible row, list the applicable indicator IDs and explain the direct pathway.
4. For an ineligible row, leave indicator IDs blank and set screening to `not_required`.
5. Do not mark proposed screening complete until every retrieved, non-rejected candidate
   source for the sector has been checked. At that point, list the complete source set in
   `screened_source_ids`. Release still requires human acceptance of the sources and checks.

## `evidence_proposals.csv`

One row represents one page-located quote for one eligible action × sector × component
mapping. Multiple evidence rows may support or qualify the same component assessment.
Rows must record the physical PDF page, addressed indicators, direction, action scope,
maladaptation signal and extraction run ID. `quantified_value` is optional and does not
change the effectiveness class.

Stage 5 compares every quote with the extracted text for its cited physical PDF page.
Exact and strong ordered matches pass automatically. Matches affected by table or column
layout are marked for human review; insufficient page matches stop the pipeline.

## Rerun

Run the complete build:

```bash
python3 pipeline/run_all.py
```

Or make the active inputs explicit:

```bash
python3 pipeline/run_all.py \
  --mapping-input data/input/mapping_proposals.csv \
  --evidence-input data/input/evidence_proposals.csv \
  --match-run-id all_sector_mapping
```

The run always rebuilds one combined output. The current queue is fully assessed, with no
`review_required` rows. If future actions or sectors are added, new unresolved combinations
remain visible as `review_required` / `not_assessed`; they are not silently omitted or treated
as evidence gaps.
