# Documentation & Metadata

## Philosophy

Documentation that lives disconnected from the data and code it describes tends to drift and become unreliable. The standard we aim for is documentation that is **close to what it describes**, **structured where it needs to be queried**, and **narrative where it needs to be understood**.

This means we maintain two distinct layers:

- **Structured metadata** — the canonical catalog of every dataset we work with, from initial discovery through to production. Versioned, machine-readable, lives in `dataset-review/catalog/` in this repo. For production datasets, it also feeds the database and API.
- **Rich documentation** — the methodology reasoning, domain research, mapping decisions, and context behind the data. Human-readable, narrative, lives in Notion. This is the source of truth for understanding *why* things are the way they are.

The two layers should always be linked. The structured metadata points to the rich documentation. Anyone querying the API or looking at the database can trace back to the full context.

---

## The Dataset Catalog (YAML)

Every dataset we work with — from initial discovery through to production — has an entry in the dataset catalog. This is a single YAML file at `dataset-review/catalog/index.yaml` in this repo and is the master record of all datasets across all stages of maturity.

The catalog serves two purposes. For all datasets, it provides a shared, searchable reference of what data exists and what state it is in. For production datasets specifically, it feeds the `publisher_datasource` and `dataset_release` tables in the database, which are exposed via the API to downstream applications.

### Dataset lifecycle in the catalog

An entry is created when a dataset is first identified as worth reviewing — not when a pipeline is built. The entry evolves as the dataset progresses:

| State | What it means | `production_approved_release` |
|---|---|---|
| **Research** | Identified, may have initial notes | `null` |
| **Reviewed** | Full review completed, scored | `null` |
| **Production** | Pipeline built, serving live data | Set to active version |

### Structure

Each entry is a flat dataset record with a nested publisher and releases list. License is tracked **at both the dataset and release level** — the dataset-level license reflects the current known terms, while per-release entries confirm the license at the time of retrieval (licenses can change between releases). Data quality and production approval are tracked at the release level only. Production-specific fields are added to the dataset entry when any release is approved for production.

**Research state (minimal entry):**
```yaml
- id: cl-ine-censo
  name: Chile Population and Housing Census
  dataset_url: https://www.ine.gob.cl/estadisticas/sociales/censos-de-poblacion-y-vivienda/
  publisher:
    id: cl-ine
    name: Instituto Nacional de Estadísticas (Chile)
    url: https://www.ine.gob.cl/
  description: >
    Official Chile Population and Housing Census providing demographic,
    housing, employment, and infrastructure indicators at national to
    sub-city level.
  coverage:
    geography: country
    countries: [CL]
    spatial_levels: [country, region, comuna]
  themes:
    - socioeconomics
    - housing
  update_frequency: irregular_census
  priority: medium
  releases:
    - version: "2024"
      version_number: 1
      source_url: https://www.ine.gob.cl/estadisticas/sociales/censos-de-poblacion-y-vivienda/
      released_at: null
      retrieval_method: manual_download
      api_endpoint: null
      path: reviews/cl_ine_censo/2024
      production_approved: false
      license:
        id: CC-BY-4.0
        name: Creative Commons Attribution 4.0 International
        url: https://creativecommons.org/licenses/by/4.0/
        commercial_use: true
        note: null
```

**Production state (full entry, additional dataset-level fields required):**
```yaml
- id: epa-ghgrp-manufacturing
  name: Manufacturing Industries and Construction Direct Emitters (GHGRP)
  dataset_url: https://www.epa.gov/ghgreporting/
  publisher:
    id: epa
    name: Environmental Protection Agency
    url: https://www.epa.gov/
  description: >
    Detailed GHG emissions from large-scale industrial facilities across
    the US, reported annually under the EPA Greenhouse Gas Reporting Program.
  coverage:
    geography: country
    countries: [US]
    spatial_levels: [point_source]
  themes:
    - stationary_energy
    - industrial_processes
  gpc_reference_numbers:
    - III.1.1
    - III.1.2
  update_frequency: annual
  priority: 1
  # --- Required once any release is production_approved: true ---
  dataset_slug: epa-ghgrp-manufacturing
  dataset_name:
    en: Manufacturing Industries and Construction Direct Emitters (GHGRP)
    es: ...
    pt: ...
    fr: ...
    de: ...
  releases:
    - version: "2023"
      version_number: 3
      source_url: https://www.epa.gov/ghgreporting/data-sets
      released_at: "2023-01-01"
      retrieved_at: "2024-01-15"
      retrieval_method: api
      methodology_url: https://www.epa.gov/ghgreporting/ghgrp-technical-guidance
      internal_review_url: https://www.notion.so/openearth/...
      api_endpoint: https://data.epa.gov/efservice/
      path: reviews/epa_ghgrp_manufacturing/2023
      is_latest: true
      production_approved: true
      pipeline_name: epa_ghgrp_manufacturing_raw
      pipeline_version: null
      license:
        id: us-government-works
        name: US Government Works
        url: https://www.usa.gov/government-works
        commercial_use: true
      data_quality:
        documentation: 3
        methodology: 2
        coverage: 2
        granularity: 3
        freshness: 2
        accessibility: 3
    - version: "2022"
      version_number: 2
      source_url: https://www.epa.gov/ghgreporting/data-sets
      released_at: "2022-01-01"
      retrieved_at: "2023-02-10"
      retrieval_method: api
      methodology_url: https://www.epa.gov/ghgreporting/ghgrp-technical-guidance
      internal_review_url: https://www.notion.so/openearth/...
      api_endpoint: https://data.epa.gov/efservice/
      path: reviews/epa_ghgrp_manufacturing/2022
      is_latest: false
      production_approved: true
      pipeline_name: epa_ghgrp_manufacturing_raw
      pipeline_version: null
      license:
        id: us-government-works
        name: US Government Works
        url: https://www.usa.gov/government-works
        commercial_use: true
      data_quality:
        documentation: 3
        methodology: 2
        coverage: 2
        granularity: 2
        freshness: 2
        accessibility: 3
    - version: "2021"
      version_number: 1
      source_url: https://www.epa.gov/ghgreporting/data-sets
      released_at: "2021-01-01"
      retrieved_at: "2022-03-05"
      path: reviews/epa_ghgrp_manufacturing/2021
      is_latest: false
      production_approved: false
      license:
        id: us-government-works
        name: US Government Works
        url: https://www.usa.gov/government-works
        commercial_use: true
```

### Required fields

**All entries (research state and above):**

| Field | Notes |
|---|---|
| `id` | snake_case, unique across the catalog |
| `name` | Human-readable dataset name |
| `dataset_url` | URL of the dataset landing page |
| `publisher.id`, `publisher.name`, `publisher.url` | Publisher details |
| `description` | Plain-language description of the dataset |
| `coverage` | Geography, countries, and spatial levels — updated per release if it changes |
| `themes` | One or more theme tags |
| `update_frequency` | How often the source updates |
| `priority` | Team priority: `high`, `medium`, or `low` |
| `releases` | At least one release entry |

**All release entries:**

| Field | Notes |
|---|---|
| `version` | Human-readable version label (e.g. `"2023"`, `"v2"`) |
| `version_number` | Sequential integer starting at 1, increments with each new release |
| `source_url` | URL of this specific release |
| `retrieval_method` | How the data is obtained: `api`, `manual_download`, `sftp`, `email`, etc. |
| `api_endpoint` | API endpoint if `retrieval_method` is `api`, otherwise `null` |
| `path` | Path to review documents in `dataset-review/` in this repo |
| `production_approved` | `true` or `false` |
| `license` | License for this specific release, including `commercial_use` flag — confirmed per release |

**Release fields required when `production_approved: true`:**

| Field | Notes |
|---|---|
| `retrieved_at` | Date we retrieved this release |
| `released_at` | Date the source published this release |
| `is_latest` | Exactly one release per dataset must be `true` |
| `pipeline_name` | The Mage pipeline name used to process this release |
| `pipeline_version` | Pipeline version suffix if versioned (e.g. `"2"`), otherwise `null` |
| `data_quality` | All six generic quality categories scored 1–3 |
| `gpc_reference_numbers` | GPC sectors covered by this release (can change between releases) |
| `methodology_url` | URL to the source publisher's own methodology documentation — can differ per release if the source updates its methodology |
| `internal_review_url` | URL to OEF's internal Notion review page for this release — the narrative analysis, mapping decisions, and data quality assessment |

The six `data_quality` categories are: `documentation`, `methodology`, `coverage`, `granularity`, `freshness`, `accessibility`. These apply across all data types. For emissions datasets, a more detailed scoring using the [Data Scoring Framework](https://www.notion.so/openearth/Data-Scoring-Framework-233eb557728b806cb162cfd9fc66925a) should be included in the review documents at `path`.

**Additional dataset-level fields required when any release has `production_approved: true`:**

| Field | Notes |
|---|---|
| `dataset_slug` | kebab-case, used in API URLs |
| `dataset_name` | Multilingual object with at minimum `en` |

### Rules

- **Create entries early.** A dataset gets a catalog entry when it is first identified, not when a pipeline is built. The entry matures as the dataset progresses.
- **One release entry per ingestion.** When a new version of a dataset is retrieved, a new release is appended with the next `version_number`. Previous releases stay with `is_latest: false`. Release entries are never deleted.
- **`production_approved` is set at the release level.** Each release independently tracks whether it is approved for production. The production seeder processes releases where `production_approved: true` and `is_latest: true`. Only one release per dataset should have `is_latest: true`.
- **`methodology_url` is the source's methodology, not ours.** It should point to the publisher's own technical documentation — the evidence that we have read and understood how they produce their data. It can differ between releases if the source updates its methodology.
- **`internal_review_url` is required before any release can be `production_approved: true`.** OEF's internal Notion review must exist and be linked before a release ships. This is where mapping decisions, quality assessment, and GPC alignment reasoning are documented.
- **License is tracked per release.** Licenses can and do change between releases. Always confirm the license for each release being ingested and do not assume it matches the previous release.
- **Long descriptions belong in review documents and Notion.** The `path` field in each release points to review documents in `dataset-review/` in this repo. The YAML holds structured facts; detailed narrative lives in review docs and Notion.
- **`data_quality` is required for production releases.** Generic quality scores must be completed for every release marked `production_approved: true`. Scores from prior releases should not be carried forward without re-evaluation.

### Migration from the old format

The existing `datasource_seeder.yaml` remains in use until datasets are migrated. New datasets always use the new catalog format. Existing datasets migrate opportunistically — when a new release is retrieved or a pipeline is updated. The old format is not extended for new work.

---

## Methodology Documentation (Notion)

Every production dataset requires a methodology page in Notion. This is created during Phase 1 or Phase 2 of a project and maintained as the dataset evolves.

A methodology page should cover:

- **Source overview** — what the dataset is, who publishes it, and what it measures
- **Scientific methodology** — the approach used by the source to calculate or collect the data, including tier level and emission factor sources where relevant
- **Assumptions and limitations** — what the data does and does not capture, known gaps or biases
- **GPC alignment** — how the data maps to GPC reference numbers and what adjustments were made
- **Transformation decisions** — key mapping or processing decisions made during pipeline development and the reasoning behind them
- **Data scoring** — the completed scoring from the Data Scoring Framework, with brief justifications

Methodology pages follow a consistent structure so they are comparable across datasets. A template is available in Notion.

---

## Domain Research (Knowledge Hub)

Research produced during Phase 1 of a project — domain notes, framework reviews, conceptual models — starts in Notion but should be graduated to the knowledge hub as it is finalised. The knowledge hub is the central reference for domain knowledge that may be reused across projects.

The distinction:

- **Notion** — active research, working documents, draft methodology reviews
- **Knowledge hub** — finalised domain knowledge, conceptual models, reference methodology summaries

Not everything needs to graduate. The test is: would this be useful context for someone starting a new project in this domain in the future?

---

## Code Documentation

### README files

Every project repo requires a README that covers:

- What the project is and why it was started
- Current phase and status
- Where the production implementation lives (once graduated)
- Links to methodology documentation and knowledge hub entries
- Any non-obvious setup or context needed to work with the sample data

Every Mage pipeline in the main repo requires a brief header comment stating what it does, what datasets it processes, and which stage of the architecture it operates in.

### Inline documentation

- Complex logic should have an inline comment explaining the *why*, not just the *what*
- Mapping decisions (e.g. sector assignments, emission factor selections) must be commented at the point where they happen
- Functions that implement scientific methodology should have a docstring linking to or summarising the methodology

### What not to document

Avoid documenting the obvious. A comment that says `# multiply by 1000 to convert kg to tonnes` adds noise without value. The standard is: comment when the reasoning is non-obvious, not when the code speaks for itself.

---

## When Documentation Is Written

Documentation is not a finishing step — it is part of the work.

| Documentation type | When it is written |
|---|---|
| Catalog entry (research state) | When a dataset is first identified as worth reviewing |
| Methodology page (Notion) | During Phase 1, before pipeline build begins |
| Review documents (`path`) | During Phase 2, as part of dataset review |
| Catalog entry (production fields) | When dataset is approved for production, before pipeline ships |
| Release entry | When a new release is retrieved, before the pipeline runs |
| README (project repo) | At the start of the project, updated as phases progress |
| Code comments and docstrings | As the code is written |
| Knowledge hub entry | When Phase 1 research is finalised |

If documentation does not exist before a pipeline ships to production, the pipeline is not complete. Documentation is part of the definition of done.
