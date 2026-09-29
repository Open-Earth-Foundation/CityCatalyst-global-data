# Review — BNDES non-automatic financing operations, release 2026-09-01

## Scope and status

This research release contains 23,815 subcredit rows rolling up to 8,388 contract numbers, a cleaned bilingual table, a source-value translation table, extraction and mapping notebooks, and a complete draft crosswalk from 6,594 distinct Portuguese project descriptions to the adaptation action bank. The cleaned table uses English column names and pairs translated controlled values and project descriptions with their Portuguese `*_pt` source text. Medium-confidence mappings remain pending adjudication. Nothing is production-approved.

## Visual summary

The source is much broader than climate finance. Only 450 of 8,388 contracts receive any draft adaptation link, and only 104 contracts have a high-confidence link. The strongest clusters are water and sanitation, nature restoration, rural and traditional communities, and urban drainage. Generic sanitation descriptions dominate the medium-confidence queue and should not be treated as direct climate adaptation without adjudication.

## What this data supports

“BNDES recorded the published subcredit under the named contract, client, project description, financing instrument, contracted amount, disbursed amount and contract status” is supported. Contracted subcredit values can be rolled up by contract number because the publisher defines subcredits as financial components of a contract.

“The BNDES portfolio contains contracts with explicit adaptation-relevant project descriptions” is supported for the high-confidence direct and component mappings. The strongest evidence comes from descriptions explicitly naming drainage, resilience, restoration, risk or related interventions.

## What this data does not support

The 23,815 rows are not 23,815 projects or contracts. A contract can have many subcredits, clients, dates, descriptions and places. Byte-identical rows cannot be safely dropped because the source publishes no subcredit identifier.

The dataset does not support an adaptation-finance total from all keyword-linked records. Mappings link descriptions to actions but never allocate contract amounts, and generic water or sanitation investment is only a weak related signal unless the description names climate risk or resilience.

## Using it downstream

Preserve the subcredit table as the auditable financial layer and use contract number only as a rollup, with child parties, descriptions and locations retained. Keep `identical_group_id` and `is_identical_extra` so totals can be reported with duplicate sensitivity. Publicly used derivative databases must satisfy ODbL attribution and share-alike/access requirements.

## Benchmark values a city can use

Contract-level comparisons should be made only after summing subcredits by contract number and filtering to similar client nature, instrument, project type, year and location. The release can provide contracted and disbursed precedents, but it should not present a single “typical BNDES climate project” across the full portfolio.

## Notes on non-obvious fields

`raw_row_id` identifies the published row, not a publisher-issued subcredit. `is_identical_extra` marks rows beyond the first byte-equivalent observation but does not declare them erroneous. English translations are paired with `*_pt`; the Portuguese value remains authoritative if a translation is disputed.

## Traceability

The complete source CSV matches the publisher’s size and MD5. The extraction notebook asserts the 23,815 rows, 8,388 contracts, geography validation and duplicate groups. The mapping notebook validates that every distinct description appears exactly once or more in the many-to-many crosswalk, every action identifier resolves to the held action bank, and every `none` result is retained.

