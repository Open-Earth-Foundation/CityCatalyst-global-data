---
name: docs-after-change
description: Mandatory after any code/config change. Keeps READMEs, ARCHITECTURE, and dataset reviews in sync.
---

# docs-after-change — global-data

Run this **after every change** and **before** handing back to the user.

## Touched a pipeline?

- Update `dataset-review/reviews/<publisher>/<dataset>/README.md` if the pipeline shape or scope changed.
- Update the per-release `review.yaml` if you added a new release or changed `production_ready`.
- Update `catalog/index.yaml` for the affected dataset (release `is_latest`, `production_approved`, `pipeline_name`, `data_quality`).
- If the DAG diagram in `ARCHITECTURE.md` shows this pipeline, update it.

## Touched the data model?

- Update `engineering-standards/data-model-design.md` "backlog" if the change closed a gap.
- Update `ARCHITECTURE.md` table-summary if a `modelled.*` table changed.

## Touched standards?

- Cross-link any new standards file from `AGENTS.md` and `README.md`.

## Touched the README itself?

- Make sure references match the current tree (e.g. `knowledge-base/`, not the old `domain-knowledge/`).
- Verify command examples still work (`docker compose up`, `mage start cc-mage`).

## Reporting

Final reply to the user must include:

- which docs you reviewed
- which docs you changed and why (1–3 bullets)
- any docs you intentionally did **not** change (and why)
