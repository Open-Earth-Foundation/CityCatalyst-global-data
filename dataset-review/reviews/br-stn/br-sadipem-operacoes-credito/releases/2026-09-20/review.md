# Review — SADIPEM credit-operation requests, release 2026-09-20

## Scope and status

This research release contains all 28,402 PVLs in the 20 September 2026 public batch, a cleaned table with English field names and complete paired translations for finite controlled values, and a draft mapping from published loan purpose to the adaptation action bank. Portuguese values remain in `*_pt`. Uncatalogued purpose-derived descriptions remain explicitly pending. It is not production-approved.

## What this data supports

“A named public entity filed a credit-operation request with the recorded lender, currency, amount, purpose, status and status date” is supported. When the status is `Deferido`, the record supports that the Treasury or delegated bank cleared the operation at that review stage. The PVL number is unique in this snapshot and is the source identifier.

## What this data does not support

SADIPEM does not establish that a cleared loan was signed, disbursed or completed. It publishes no project object, so a purpose such as sanitation cannot be narrowed to drainage, water supply or sewage. Purpose-level adaptation links are therefore medium-confidence context only and project amounts must not be attributed to mapped actions.

## Using it downstream

Use the English `status` for display and preserve `status_pt` as the authoritative published label. The same pairing applies to applicant type, operation type, creditor type, currency and analysing body. Use the seven-digit IBGE code for municipalities and do not substitute CityCatalyst `city_id`; downstream city joins must ultimately resolve to `locode` or `actor_id`. Keep external and domestic operations separate and avoid double-counting operations later found in COFIEX or lender portfolios.

## Benchmark values a city can use

SADIPEM is useful for borrower, lender and amount precedents at the published purpose level. It is not a project-cost database. Medians should be calculated within purpose, currency, borrower type and status because the complete table mixes unrelated credit purposes and stages.

## Traceability

The source is ODbL and public reuse must retain attribution and satisfy the share-alike/access obligations for a publicly used derivative database. The build validates all 28,402 rows and unique PVLs and exact dictionary coverage for 3 applicant types, 6 operation types, 7 creditor types, 5 currencies, 28 statuses and 2 analysing-body values. Controlled translations are complete on all rows. Purpose-derived English text is complete on 12,770 rows and explicitly pending on 15,632. The adaptation mapping remains byte-for-byte unchanged at SHA-256 `4093b3b85cfeb2309e7d91b14faf88a4abdc5a4161c20d2afbfc9b410cd2deb2`.
