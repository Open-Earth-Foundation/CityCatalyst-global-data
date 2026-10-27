# Review — FNMC projects, release 2025-11

## Scope and status

This research release contains 82 non-reimbursable FNMC project records, one cleaned table, a restartable extraction notebook, and a draft adaptation-action crosswalk. English field names and controlled-value translations are present. All 81 distinct Portuguese project titles are retained in `project_name_pt`, and all 82 records have a reviewed English title in `project_name` with `translation_status=reviewed_english_translation`. The release is not production-approved.

## What this data supports

“FNMC recorded 82 non-reimbursable projects from 2011 through November 2025 with R$152,850,266.43 in committed FNMC value” is supported and reconciles to the publisher table. The data also supports project-level statements about the executing institution, source theme, agreement term, counterpart funding, transferred value and amount not transferred.

## What this data does not support

The headline R$152.8 million should not be called disbursed finance because the source’s row-level transferred total is a different field. An agreement start date is not an award-decision date, and the dataset is not an application universe, so it cannot support success rates. The adaptation crosswalk is a draft: high links rely on explicit project terms, medium links require human adjudication, and `none` does not mean the project has no climate value.

## Using it downstream

Use `transfer_instrument_id` together with `record_id`; two publisher instrument labels repeat. Preserve committed, counterpart, total, transferred and not-transferred values as separate measures. The reviewed English title is suitable for discovery and display, but legal names, programme names and uncertain source spellings remain traceable through `project_name_pt`; the source's literal `Itax? Mirim` spelling is intentionally preserved there.

## Benchmark values a city can use

The 82 projects range from R$120,263 to R$12.04 million in committed FNMC value, with a median of about R$0.80 million. These are comparator priors for the non-reimbursable arm, not grant ceilings or expected awards. The project table should be filtered by source activity area and recipient type before using a precedent for a municipal action.

## Traceability

The canonical MMA CSV is CC BY with an unspecified version. The build asserts 82 records, unique release keys and an exact R$152,850,266.43 committed-value reconciliation. Source text and controlled-value translations are kept side by side, and the action mapping links without allocating project amounts across actions.
