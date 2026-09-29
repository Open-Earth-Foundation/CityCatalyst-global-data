# Review — COFIEX meeting results, release 2025–2026

## Scope and status

This research release contains 138 decisions from five COFIEX meetings, one cleaned table, a restartable build notebook and a draft adaptation mapping. Reviewed English translations cover all 114 distinct Portuguese project descriptions and all 138 rows; the Portuguese source descriptions remain paired in `project_description_pt`. It is not production-approved because rights and mapping adjudication remain open. The cleaned table and crosswalk are not committed while row-level redistribution is under review. They are written to this release's `sample/` folder; run `build_release.py` to regenerate them from the source extract held in the same folder.

## What this data supports

“COFIEX approved or did not approve the named operation at the recorded meeting, with the published proponent, lender and amount” is supported. The release preserves 80 approvals and 58 non-approvals, which makes it useful for observing the preparation gate rather than only successful operations.

## What this data does not support

An approval is not an external loan contract, disbursement or completed project. A rejection at one meeting is not permanent ineligibility; projects can return under changed names or amounts. Amounts in different currencies cannot be combined without an explicit dated conversion.

## Using it downstream

Keep approved and non-approved decisions separate. Candidate cross-meeting matches should be based on proponent, project title and lender and must retain every source observation. Link approved operations to SADIPEM and lender portfolios to find later stages; absence of a match is not evidence that financing stopped.

`translation_status=complete_human_reviewed_translation` means the English project description was selected from the release's reviewed exact-match dictionary. It does not apply to `notes_pt`, publisher titles or recipient legal names, which remain source Portuguese or proper names.

## Benchmark values a city can use

Municipal and state operation sizes can provide order-of-magnitude external-borrowing precedents within the same currency and borrower class. They are requested or approved financing amounts at the preparation gate, not final project costs or disbursed totals.

## Traceability

The draft mapping uses explicit drainage, slope, restoration, water and climate-resilience terms. High-confidence links are direct; medium links remain pending. All 138 source records appear in the mapping, including explicit `none` rows.
