# Brazil action-to-adaptation-risk mapping

This pipeline produces one warehouse-ready file:

[`data/output/action_risk_mapping.csv`](data/output/action_risk_mapping.csv)

Its grain is one action × sector × component × eligible indicator. An ineligible or unresolved mapping is retained as one row with blank indicator fields so that negative decisions are not lost. The file contains the categorical inputs required by the later prioritisation calculation, but it does not calculate a city result.

## Processing order

```text
PDF documents → page-marked text → action matching → evidence extraction → quote grounding → warehouse CSV
```

We extract every retrieved document before matching because document extraction is reusable. We do **not** extract all action-specific evidence first. Evidence is searched only after matching identifies the eligible action, sector, component and indicator combinations. A proposed assessment may screen retrieved, non-rejected candidate sources; a released assessment requires the source, screening decision and evidence to be human-accepted.

| Script | Purpose |
| --- | --- |
| `01_prepare_inputs.py` | Prepare reference data and maintain the complete action × sector × component proposal queue. Existing decisions are preserved. |
| `02_extract_documents.py` | Convert retrieved PDFs to page-marked text. Existing hash-matching text is skipped. |
| `03_match_actions.py` | Validate the active action-to-indicator proposals and create the evidence screening scope. |
| `04_extract_evidence.py` | Validate the active page-located evidence proposals for eligible mappings only. |
| `05_verify_evidence_grounding.py` | Compare every quote with its cited extracted PDF page. Strong matches pass, layout-sensitive matches require human review, and insufficient matches stop the run. |
| `06_build_warehouse_output.py` | Require grounded evidence, apply the deterministic rules, write the proposed warehouse rows and create the joined review CSV. |

Run everything:

```bash
python3 pipeline/run_all.py
```

Run these commands from `releases/v1/`. The pipeline resolves all data and schema paths relative to this release directory, so it does not read or write implementation files at the dataset root.

The active inputs can also be named explicitly:

```bash
python3 pipeline/run_all.py \
  --mapping-input data/input/mapping_proposals.csv \
  --evidence-input data/input/evidence_proposals.csv \
  --match-run-id all_sector_mapping
```

Run one stage:

```bash
python3 pipeline/02_extract_documents.py
python3 pipeline/02_extract_documents.py --document doc_3251148a9115 --force
python3 pipeline/03_match_actions.py --input path/to/mapping_proposals.csv
python3 pipeline/04_extract_evidence.py --input path/to/evidence_proposals.csv
python3 pipeline/05_verify_evidence_grounding.py
python3 pipeline/06_build_warehouse_output.py
```

The matching and evidence judgements are AI-assisted or analyst-authored. Their canonical proposal CSVs are retained in `data/input/`; the numbered scripts handle queue maintenance, validation, normalization and deterministic derivation. The queue can be completed one sector at a time, while every rerun rebuilds one combined output.

Stage 5 verifies that each quote is present on its cited page before Stage 6 calculates an assessment. When evidence is still proposed, `assessment_basis` is `proposed_evidence`. After the evidence and screening decisions are accepted, rerunning Stage 6 derives the release result from accepted evidence only.

## Files that matter

- `data/input/mapping_proposals.csv` is the complete editable matching queue.
- `data/input/evidence_proposals.csv` contains one page-located quote per evidence record.
- `data/reference/` contains stable reference inputs.
- `data/documents/raw/` contains the PDFs.
- `data/documents/text/` contains page-marked extracted text.
- `data/output/action_risk_mapping.csv` is the file intended for warehouse ingestion.
- `data/output/assessment_evidence_review.csv` is the generated file to share for review. Each row shows a component assessment together with one linked evidence quote; mappings with no evidence still receive one row. A compact coverage field makes any mapped indicators without linked evidence explicit.
- The other CSVs in `data/output/` preserve mapping, screening and evidence lineage.
- `outputs/icare-review-2026-08-30/icare_adaptation_assessment_review.xlsx` is the reviewer-friendly workbook generated from the joined review data. It retains source action IDs, omits generated processing IDs and places layout-sensitive grounding matches first in Evidence Review.

The current combined result contains all six sectors: 636 component mappings, 1,236 warehouse rows and 733 joined review rows. All mappings have an eligibility decision: 219 are eligible and linked to one or more terminal indicators, while 417 are not eligible. The eligible mappings have complete proposed screening across their sector source set. Of these, 176 have page-located evidence and 43 are explicitly `none_demonstrated`; none remain `review_required` or `not_assessed`. The proposed effectiveness distribution is 43 `none_demonstrated`, 77 `low`, 83 `medium` and 16 `high`. The evidence file contains 273 proposed records. Human acceptance is still required before release.

Stage 5 grounds all 273 evidence records against their cited pages: 94 are normalized exact matches, 162 meet the ordered-match threshold and 17 are layout-sensitive matches requiring visual confirmation. No insufficient match reaches Stage 6.

Effectiveness is derived from evidence direction and whether evidence covers the whole or only part of the action. Numeric findings may be retained in the optional `quantified_value` evidence field, but quantification is not required and does not change the effectiveness class.

Reviewer decisions are applied back to the canonical mapping and evidence records by their IDs, then stage 5 is rerun. The joined review CSV is regenerated rather than treated as a second source of truth.

The assessment concepts and rules are documented in [`../../methodology.md`](../../methodology.md). The detailed source-workbook review is in [`review.md`](review.md).
