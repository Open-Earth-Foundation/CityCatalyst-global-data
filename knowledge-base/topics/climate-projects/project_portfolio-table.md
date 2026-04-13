# `modelled.project_portfolio` — Table Context

This document explains how to read and interpret rows from `modelled.project_portfolio`.
It is intended as context for AI-assisted data querying and interpretation.

Related: [`project_summary-table.md`](./project_summary-table.md) — the AI-enriched profile table linked to each portfolio row.

---

## Purpose

`project_portfolio` is the **master catalog** of climate-related projects ingested into
the platform. Each row is one project from one funder source. It stores the metadata
that came directly from the source API or data feed — project identity, geography,
sector, financing scale, and timeline.

This table is populated from raw source data without AI enrichment. Values are as
reported by the funder's data system. It is the entry point for project discovery
and the join anchor for `project_summary`.

---

## Schema

| Column | Type | Description |
|---|---|---|
| `project_id` | uuid (PK) | Internal identifier, deterministically derived as `MD5('world_bank-{source_project_id}')` |
| `source_name` | varchar | Funder system identifier (e.g. `world_bank`, `idb`, `gcf`) |
| `source_project_id` | varchar | Project ID in the funder's own system (e.g. `P006634`) |
| `source_project_url` | text | Link to the project page on the funder's website |
| `project_name` | text | Project title as reported by the funder |
| `project_description` | text | Short description from the source, if available |
| `project_status` | varchar | Status as reported by source (see values below) |
| `project_type` | varchar | Lending instrument type from source (e.g. Investment Project Financing) |
| `country_code` | varchar | ISO 3166-1 alpha-2 country code |
| `country_name` | varchar | Country name as reported by source |
| `world_region_name` | varchar | Funder's regional grouping (e.g. `Latin America and Caribbean`) |
| `approval_at` | datetime | Board approval date |
| `closing_at` | datetime | Project closing / end date |
| `total_commitment_amount` | decimal | Total commitment in source currency (see `currency_code`) |
| `total_project_cost_amount` | decimal | Total project cost including co-financing, if reported |
| `currency_code` | varchar | Currency of commitment amounts (may be null if USD is assumed) |
| `sector_name` | text | Primary sector classification from source |
| `theme_name` | text | Primary theme from source (e.g. `Climate change`) |
| `instrument_type` | varchar | Lending instrument label from source |
| `borrower_name` | text | Borrowing entity (government, ministry, agency) |
| `implementing_agency_name` | text | Agency responsible for implementation |
| `release_id` | uuid | FK to `modelled.dataset_release` |
| `created_at` | datetime | Row creation timestamp |
| `updated_at` | datetime | Last update timestamp |

---

## How to read a row

**Example:**
```
source_name:               world_bank
source_project_id:         P006634
project_name:              Brazil Urban Transport Corridors
country_code:              BR
sector_name:               Transportation
approval_at:               2018-06-15
total_commitment_amount:   250000000
currency_code:             null  (assumed USD for World Bank)
project_status:            Active
```

**Plain-language interpretation:**
> This is a World Bank project (ID P006634) in Brazil, approved in June 2018, for urban
> transport infrastructure with a USD 250M commitment. Status is active as of the last
> data retrieval.

---

## `project_status` values

Status values are sourced directly from the funder's system and vary by source. For
World Bank projects:

| Value | Meaning |
|---|---|
| `Active` | Project currently under implementation |
| `Closed` | Project has reached its closing date |
| `Pipeline` | Approved but not yet effective |
| `Dropped` | Cancelled before implementation |

---

## Relationship to `project_summary`

`project_portfolio` and `project_summary` are joined on `project_id`. Not every
portfolio row has a corresponding summary — a summary is only created when the pipeline
has successfully processed project documents through the AI synthesis step.

```sql
SELECT pp.project_name, pp.country_name, pp.total_commitment_amount,
       ps.project_summary_text, ps.sector_name, ps.total_budget_amount_usd
FROM modelled.project_portfolio pp
LEFT JOIN modelled.project_summary ps ON ps.project_id = pp.project_id
WHERE pp.source_name = 'world_bank'
  AND pp.country_code = 'BR';
```

Use `project_portfolio` when you want to:
- Count projects, filter by country/sector/status, or check what's in the catalog
- Access source-reported financial figures without AI processing
- Find the source URL or original project ID for verification

Use `project_summary` when you want:
- Enriched detail extracted from project documents (financing structure, actions, risks)
- AI-structured fields for comparison across projects (replicability, co-benefits, etc.)
- Evidence-backed values with traceability to source documents

---

## Current data sources

| `source_name` | Publisher | Coverage |
|---|---|---|
| `world_bank` | The World Bank | Global climate-filtered portfolio via Projects API |

Additional sources (IDB, GCF, AfDB) are planned but not yet ingested.

---

## Known limitations

- `currency_code` is often null for World Bank rows; amounts are understood to be USD
- `project_description` is typically null — descriptions are in `project_summary.project_summary_text`
- `sector_name` and `theme_name` reflect the funder's own classification, which may not
  align with the platform's sector taxonomy
- `world_region_name` is the funder's regional grouping, not a sub-national location;
  it should not be used for city or region-level filtering
- Multi-country projects may have only the primary country in `country_code`
