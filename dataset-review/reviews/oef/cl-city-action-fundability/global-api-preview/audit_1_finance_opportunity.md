# Audit — finance_opportunity (table 1 of 4)

Gate before the migration: every field the source supply reviews carry, mapped to a column, so nothing important from the dataset review is lost. Sources audited: `cl-mma/cl-mma-fondos` (richest — 24 cols), `cl-gore/cl-gore-fndr`, `cl-subdere/cl-subdere-fondos`, `cl-conaf/cl-conaf-fondos`, the harmonized `chile_finance_inventory.csv`, and the `finance_db/opportunities.csv` fixture.

## Field map

| Source field (review) | Column in `finance_opportunity` | Notes |
|---|---|---|
| `fund_name` / `program` | `opportunity_name` | one row per fund *line* |
| `fund_program` / `stream` | `program_family` | **added** — FPA runs parallel lines under one program |
| `funder_institution` | `funder_name` | |
| (funder level) | `funder_level` | national / regional / local |
| (denormalized) | `funder_channel` | competitive / public investment / intermediated |
| `provider` | `provider` | **added** — implementer ≠ funder (AgenciaSE for MinEnergía) |
| `instrument_type` | `instrument` | |
| `gpc_sectors` | `gpc_sectors` (JSONB) | mapped from funded works, not the name |
| `thematic_lines` | `thematic_lines` (JSONB) | **added** — the climate hook / traceability |
| `eligible_actor` | `eligible_actor` | |
| `eligible_actor_detail` | `eligible_actor_detail` | **added** — the decisive nuance (e.g. excludes municipalities) |
| `access_pathway` | `access_pathway` (raw) + `city_application` (derived) | **keep both** — raw text + normalized direct/facilitated/intermediated |
| (derived) | `funding_channel`, `access_tier` | access_tier flags the BIP-SNI gate (see §7.5 of design) |
| `open_date`, `close_date` | `open_date`, `close_date` | |
| `status` | `status` | close DATE is authoritative over section labels |
| `lifecycle` | `lifecycle` | **added** — post-award/convenio phase vs open |
| `status_as_of` | `status_as_of` | always record the as-of date |
| `recurrence` | `recurrence` | annual fund "closed now" ≠ dead |
| `next_call_estimate` | `next_call_estimate` | **added** — when an annual fund reopens |
| `amount_clp` | `amount_clp` | native CLP where stated |
| `amount_note` | `amount_note` | keeps units (CLP/UF/US$/%) |
| `amount_suspect`, `status_section_conflict` | `data_quality_flags` (JSONB) | **added** — extensible DQ flags (e.g. Rapa Nui amount defect) |
| `climate_relevance` | `climate_relevance` | |
| `specificity` | `specificity` | broad ≠ sector-specific |
| `source_url` | `source_url` | |
| `resolucion_url` | `resolucion_url` | **added** — Bases / Resolución Exenta provenance |
| `detail_level` | `detail_level` | **added** — detailed vs index extraction (coverage) |
| `notes` | `notes` | **added** — per-source caveats |
| (provenance) | `source_dataset`, `country_code`, `release_id`, `created_at`, `updated_at` | house convention |

## Decisions

- **Two DQ flags collapse into one `data_quality_flags` JSONB** rather than a boolean per flag — extensible as new sources add their own (e.g. `amount_suspect`, `status_section_conflict`, future `extraction_tier_merge`).
- **Keep `access_pathway` raw AND `city_application` derived** — the derivation is lossy (e.g. "direct application (via fondos.gob.cl)" → `direct`), so the original text is retained.
- **`next_call_estimate` is a String**, not a Date — the source value is often a window ("~Aug–Oct 2026"), not a calendar date.
- **Nothing dropped.** All 24 MMA columns and every other review's columns map to a column or a JSONB field.

## Result

35 data columns + 3 housekeeping (release_id, created_at, updated_at). Migration: `..._create_finance_opportunity.py` (down_revision `ba244429bef5`).
