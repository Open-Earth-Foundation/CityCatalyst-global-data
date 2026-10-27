
# CityCatalyst Global Data
Production data pipelines and ETL for the CityCatalyst platform. Ingests emissions and activity data from global and national sources, transforms and models it, and loads it into the GlobalAPI database for use in city-level greenhouse gas inventories.

## Repository layout

```
cc-mage/                  Mage.ai pipeline project
  pipelines/              One folder per pipeline (ghgi_, ccra_, cap_, dq_ prefixes)
  data_loaders/           Shared loader blocks
  transformers/           Shared transformer blocks
  data_exporters/         Shared exporter blocks
  utils/                  Shared Python utilities
  local_scripts/          Ad-hoc and exploratory scripts (not part of any pipeline)
  io_config.yaml          Mage runtime storage/connection config

mage_data/                Mage local metadata/state (runtime-generated)

dataset-review/           Dataset discovery and tracking
  catalog/index.yaml      Unified dataset catalog — one entry per dataset from first
                          discovery through production
  reviews/                Source-level dataset review notes
  collections/            Groupings of datasets by theme or source

engineering-standards/    Team design principles and conventions
  project-structure-and-architecture.md
  naming-conventions.md
  data-quality-and-validation.md
  documentation-and-metadata.md

domain-knowledge/         Shared domain definitions and reference materials
  catalog/                Domain dataset catalog and metadata
  collections/            Curated thematic groupings
  topics/                 Topic references and glossary pages

ARCHITECTURE.md           Technical reference — data stages, DB schema, pipeline block flow
AGENTS.md                 Agent guardrails and repository-specific constraints
docker-compose.yml        Local orchestration for Mage + dependencies
dev.env                   Example local environment configuration
```

For the full technical architecture (S3 stages, database schema, Mage block structure) see [`ARCHITECTURE.md`](./ARCHITECTURE.md).

For team conventions and design principles see [`engineering-standards/`](./engineering-standards/).

---

## Local Development: Set up steps

#### Database

You have to create a Postgres database user:

```bash
createuser ccglobal
```

```bash
createdb ccglobal -O ccglobal
```

#### Configuration

Copy `dev.env` to `.env` and edit it to match your configuration.

```bash
cp dev.env .env
```

#### Start Mage-ai

```bash
docker compose up
```

Navigate to http://localhost:6789