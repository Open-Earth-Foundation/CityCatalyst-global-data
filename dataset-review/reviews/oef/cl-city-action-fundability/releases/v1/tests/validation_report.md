# Validation report — `modelled.finance_opportunity`

**PASS** — 24/24 checks passed, 0 hard failure(s). 99 rows.

## Checks

- ✅ **pk opportunity_id unique & not-null** — 0 duplicate keys, 0 null keys
- ✅ **opportunity_id not null** — 0 nulls
- ✅ **source_opportunity_id not null** — 0 nulls
- ✅ **opportunity_name not null** — 0 nulls
- ✅ **source_dataset not null** — 0 nulls
- ✅ **release_id not null** — 0 nulls
- ✅ **funder_name not null** — 0 nulls
- ✅ **source_url not null** — 0 nulls
- ✅ **unique (release_id, country_code, source_opportunity_id)** — 0 duplicate groups
- ✅ **fk release_id -> modelled.dataset_release.release_id** — 0 orphan rows
- ✅ **funding_channel in allowed set** — 0 rows with unexpected value(s): []
- ✅ **access_tier in allowed set** — 0 rows with unexpected value(s): []
- ✅ **instrument in allowed set** — 0 rows with unexpected value(s): []
- ✅ **recurrence in allowed set** — 0 rows with unexpected value(s): []
- ✅ **status in allowed set** — 0 rows with unexpected value(s): []
- ✅ **climate_relevance in allowed set** — 0 rows with unexpected value(s): []
- ✅ **amount_currency in allowed set** — 0 rows with unexpected value(s): []
- ✅ **amount in range [100000, 100000000000]** — 0 out-of-range rows
- ✅ **row rule: close_date >= open_date** — 0 violating rows
- ✅ **row rule: close_date <= DATE '2031-12-31'** — 0 violating rows
- ✅ **row_count** — 99 (expected 99)
- ✅ **distinct source_dataset** — 10 (expected 10)
- ✅ **group_counts funding_channel** — got {'intermediated': 3, 'public investment': 7, 'competitive fund': 89} (expected {'competitive fund': 89, 'public investment': 7, 'intermediated': 3})
- ✅ **close_date non-null >= 6** — 7 non-null

## What we can say about this data

**By source:** cl-mma/cl-mma-fondos 55, cl-indap/cl-indap-fondos 9, cl-mop/cl-mop-fondos 7, cl-minenergia/cl-minenergia-fondos 6, cl-corfo/cl-corfo-finance 5, cl-minvu/cl-minvu-fondos 4, cl-gore/cl-gore-fndr 4, cl-subdere/cl-subdere-fondos 4, cl-mtt/cl-mtt-fondos 3, cl-conaf/cl-conaf-fondos 2

**Columns with nulls:**

- `funder_level`: 99/99 null (100%)
- `amount_currency`: 99/99 null (100%)
- `legal_basis_url`: 92/99 null (93%)
- `close_date`: 92/99 null (93%)
- `amount`: 91/99 null (92%)
- `provider`: 72/99 null (73%)
- `notes`: 55/99 null (56%)
- `amount_note`: 55/99 null (56%)
- `open_date`: 45/99 null (45%)
- `thematic_lines`: 44/99 null (44%)
- `eligible_actor_detail`: 43/99 null (43%)

**`funding_channel` values:** competitive fund (89), public investment (7), intermediated (3)
**`access_tier` values:** competitive (89), gated (7), intermediated (3)
**`instrument` values:** grant (83), subsidy (4), blended (4), technical_assistance (4), loan (2), guarantee (1), co_financing (1)
**`status` values:** closed (57), ongoing (18), periodic (17), open (5), emerging (1), in_rollout (1)
**`recurrence` values:** annual (39), ongoing (25), sporadic (19), one_off (11), time_boxed (3), periodic (2)
**`specificity` values:** sector-specific (79), broad (20)
**`climate_relevance` values:** explicit (77), climate_adjacent (17), indirect (5)

**`amount`:** min 6000000.0, max 100000000.0, avg 33600000.0, non-null 8
**`open_date`:** 2019-08-16 → 2025-10-02 (54 non-null)
**`close_date`:** 2025-09-17 → 2025-10-30 (7 non-null)
