# Project Structure & Architecture

## What is a Project

A project is initiated when we are working on a **new concept that does not exist in our current data model** — something that requires domain research, new modelling decisions, and validation before it can be built into production infrastructure. It is not a label for every piece of work. Routine additions or extensions to existing workflows — a new data source feeding an established pipeline, a new sector following an existing pattern — do not need to be treated as new projects.

The distinction matters because projects carry a different kind of investment: they require time to understand, design, and prototype before any production code is written. Treating them differently from regular pipeline work protects that space.

---

## Project Lifecycle

Every project moves through three phases. These are not rigid gates — the expectation is that work moves forward continuously, with team members using their judgement about when enough has been established to progress. The phases are a shared language for where a project is and what kind of work is happening, not a checklist to satisfy before proceeding.

### Phase 1 — Research & Conceptual Design

The goal of this phase is to understand the domain well enough to know what we are building and why. Work here is exploratory: reading frameworks and standards, understanding how concepts relate, and sketching how the data would fit together at a conceptual level.

**Outputs:**
- A summary of relevant domain knowledge, standards, or frameworks (e.g. GPC alignment, scientific methodologies)
- A conceptual data model showing how entities and concepts relate
- A reasonable sense of where the data comes from — not a fully sourced dataset, but enough confidence that the concepts are achievable

A project is ready to move into Phase 2 when the team has shared understanding of the concept and a credible path to getting the data.

### Phase 2 — Physical Design & Prototyping

This phase translates the conceptual model into concrete structures. The work here is about proving the design before committing to production build. Data sources are reviewed in more detail, a physical data model is defined, sample or synthetic data is created, and mock API contracts are sketched out to validate the overall design.

The project repo lives in this phase — everything from Phase 1 through to working sample data and contracts is housed here. No production pipelines are built yet.

**Outputs:**
- Physical data model
- Sample data representing the expected shape and content of real data (stored in `sample-data/`)
- Mock API contracts
- A clear picture of how the data will flow through our 4-stage architecture

A project is ready to move into Phase 3 when the physical model has been reviewed, the API contracts are defined, and the sample data is a good enough representation of what we want to achieve.

### Phase 3 — Production Implementation

The project graduates into the main repo. Mage pipelines are built, real data begins flowing, and the work goes through the standard dev → test → prod cycle. From this point, the pipeline is maintained as part of our core infrastructure.

The project repo is no longer where active development happens, but it remains as a reference — the research, conceptual model, and sample data document the origin and reasoning behind the implementation.

---

## Repository Structure

For a map of what lives where in this repo, see the [README](../README.md#repository-layout). This section covers the *rules* behind that layout — what belongs where and why.

### Project Repos

Each new project gets its own repository. The project repo is the home for all work up to and including sample data — it is a space for research, design, and prototyping, not for production code.

### Main Repo (this repo)

Production pipeline code lives here. When a project graduates to Phase 3, the Mage pipelines and any database-level objects are built in `cc-mage/`, following the standard 4-stage architecture. The dataset catalog entry in `dataset-review/catalog/index.yaml` is updated to mark the dataset as `production_approved: true`.

The main repo is not the place for research or prototyping. Exploratory scripts that are not part of any pipeline belong in `cc-mage/local_scripts/` and should be clearly named to distinguish them from production code.

### Knowledge Hub

When a project completes Phase 1 or graduates to Phase 3, the domain knowledge and conceptual model should be contributed to the company knowledge hub. This ensures the reasoning behind our data work is centrally accessible and reusable across the team, not buried in a project repo. The knowledge hub is where we maintain the *why and what* — conceptual models, methodology documentation, domain research. The *how* stays in the main repo alongside the implementation.

---

## Mapping to the 4-Stage Architecture

All production data work follows our standard 4-stage flow. New projects should be designed with this in mind from Phase 2 onwards — the physical data model and sample data should reflect where data will land at each stage.

| Stage | Location | Purpose |
|---|---|---|
| `files` | S3 | Raw source data, no transformation. Centralised storage for all source files. |
| `raw_data` | S3 (Parquet) + PostgreSQL schema | Cleaned and structured data. Parsed, typed, and staged for modelling but not yet mapped to the target schema. |
| `modelled` | PostgreSQL schema + S3 | Data modelled to GPC standards, aggregated to city level, and conforming to the target data model. Primary input to the GlobalAPI. |
| `reporting` | PostgreSQL + S3 | Reporting-optimised tables for Metabase dashboards. Lean and query-performant — not a full copy of modelled data. |

For the full technical detail of the architecture — including the database schema and standard Mage block flow — see [`ARCHITECTURE.md`](../ARCHITECTURE.md).

When designing a new project, be explicit about which stages it touches and where its outputs will land. Not every project needs to go end-to-end — but the entry and exit points should be defined before moving into production build.

---

## Guiding Principles for This Section

- **Projects are for new concepts.** If the pattern already exists, use it — don't create a new project unnecessarily.
- **The project repo is a thinking space.** Keep production code in the main repo.
- **Sample data should be representative, not exhaustive.** It exists to validate the design, not replace real data.
- **The README is a contract.** It should always reflect the current state and point to where the work lives.
- **Move at the speed of understanding.** Phases exist to describe where you are, not to slow you down.
