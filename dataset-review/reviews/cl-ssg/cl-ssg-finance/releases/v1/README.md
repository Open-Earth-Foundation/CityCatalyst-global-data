# Chile finance opportunities - SSG curated inventory (v1)

Curated inventory of climate-relevant financing opportunities for Chile, prepared for MEED / SSG finance screening and action matching workflows.

The authoritative row-level file for this release is:

- `data/funding_database_v1_sin_duplicados.csv`

## Why we use it

- Provides a machine-readable list of financing opportunities with actor, instrument, territorial scope, sector coverage, and source link.
- Supports early screening of "what funding instruments might fit this action/city context" before detailed eligibility review.
- Preserves analyst notes and provenance fields used during SSG curation.

## Current release

- **v1 (2026-03-19 curation date in source file)**.
- File name indicates de-duplication effort: `funding_database_v1_sin_duplicados.csv`.

## File profile (v1)

- Rows: **405**
- Columns: **19**
- Main identifier fields: `n°_id`, `opportunity_id`
- Main content fields: `opportunity_name`, `source_actor_name`, `instrument_type`, `geographic_scope`, `eligible_actor_types`, `gpc_sector`, `sector_scope`, `status`, `application_window`, `source_url`
- Curation/provenance fields: `provider_actor_id`, `notes_internal`, `last_updated`, `Doc_Source`, `Grupo_Duplicado`, `Desición `

## Data dictionary

- `id`: Numeric row index in this release.
- `opportunity_id`: Opportunity code (e.g., `CHL_ED_008`).
- `opportunity_name`: Name/title of the financing opportunity.
- `source_actor_name`: Institution offering the instrument/program.
- `source_actor_type`: Actor type classification (e.g., `national_government`, `private_sector`, `multilateral_agency`).
- `instrument_type`: Financing instrument class (e.g., `grant`, `loan`, `technical_assistance`, `blended`).
- `geographic_scope`: Territorial applicability (national/regional/comunal/global combinations).
- `eligible_actor_types`: Eligible applicant actor types (single or comma-separated).
- `gpc_sector`: Sector mapping used for climate/action relevance screening.
- `sector_scope`: Normalized sector scope (e.g., `cross_sector`, `energy`, `waste`, `transport`).
- `status`: Availability/status tag (dominantly `recurring` in this release).
- `application_window`: Timing information (e.g., rolling/opening period).
- `source_url`: Source webpage or official program link.
- `provider_actor_id`: Provider identifier where available; often `No especificado`.
- `notes_internal`: Internal analyst notes (context, barriers, mappings, caveats).
- `last_updated`: Last update date for the row/opportunity when available.
- `Doc_Source`: Internal source document(s) used in curation.
- `Grupo_Duplicado`: Duplicate-group marker used during de-duplication review.
- `Desición `: Duplicate-resolution decision (`Son lo mismo`, `No es lo mismo`, or blank). Note the trailing space in the header.

## Known strengths

- Broad coverage across actor types and instrument types.
- Includes both operational fields (status/window/link) and analyst context (`notes_internal`).
- Keeps provenance (`Doc_Source`) and duplicate-resolution metadata for auditability.

## Known limitations / handling notes

- Header quality issues are present and should be normalized in ETL (`n°_id`, `Desición ` with trailing space).
- Some values are intentionally non-specific (`No especificado`) and should not be treated as missing by default business logic.
- `Grupo_Duplicado` and `Desición ` are curation fields, not end-user product fields.
- `notes_internal` may contain mixed-language free text and pipe-separated notes; parse as unstructured text.
- `source_url` validity was not re-checked as part of this README update.