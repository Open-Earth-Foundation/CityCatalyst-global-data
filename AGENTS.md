# CityCatalyst Global Data — Agent Brief

**Read this first.** Every AI agent (Cursor, Cursor Cloud Agent, agentic-coder, Codex, Claude Code) and every new human contributor opens this file before touching the repo.

This is a 1-page contract. Full conventions live in `.cursor/rules/`, named workflows in `.cursor/skills/`, and team standards in `engineering-standards/`.

---

## What this repo is

Production ETL feeding the **CityCatalyst Global API**. Pipelines run in **Mage.ai** (`cc-mage/`), orchestrated locally via Docker on port 6789. Data flows in 4 stages: `files` → `raw_data` → `modelled` → `reporting`. See `ARCHITECTURE.md` for the deep-dive.

## Identity mappings you must get right

These are the most common source of mistakes in SQL and Python. **Internalise them.**

| Identifier | What it is | Where it appears |
|------------|------------|-----------------|
| `actor_id` | UN/LOCODE city code (e.g. `BR SAO`) | `modelled.emissions`, `modelled.emissions_factor` |
| `locode` | Same as `actor_id` — the city's primary key | `modelled.city_polygon` |
| `city_id` | GeoHash of the city centroid — **NOT** a primary key. **Never** join on this | `modelled.city_polygon`, some staging tables |
| `datasource_name` | Short string key linking emissions back to a publisher. **Exact-match FK** | All `modelled.*` tables — must match `publisher_datasource.datasource_name` exactly |
| `gpc_reference_number` | GPC sector ref (e.g. `II.1.1`) | `modelled.emissions`, `modelled.ghgi_methodology` |
| `gpcmethod_id` | UUID linking emission record to a methodology | FK between `emissions`, `activity_subcategory`, `ghgi_methodology` |

Always use `actor_id` / `locode` for city identity — never `city_id`. When referencing datasets, `datasource_name` must be an exact string match (use `=`, not `LIKE`).

The full machine-readable rule lives at `.cursor/rules/identity-keys.mdc`.

## Critical constraints

- **Do not rename `cc-mage/`** — Mage's project config is hardcoded.
- **Do not delete release folders** under `dataset-review/reviews/<…>/releases/<v>/`. Old releases are part of the historical record. When updating, add a new `<v+1>` and flip `is_latest`.
- **Staging tables are temporary** — `raw_data.*_staging` is intermediate. Don't read from another pipeline.
- **Don't use `city_id` as a join key** — use `actor_id` / `locode`.

## Things that look similar but are different

**`emissions_factor` vs `formula_input`:**
- `emissions_factor` — standard EF used in `emissions = activity × EF`.
- `formula_input` — parameters for more complex calculations (waste composition, biological treatment …).

**Some publishers have two pipeline patterns:**
- **File-based** — reads from S3, standard `extract → stage → modelled` flow. Authoritative for production.
- **API-based** — pulls directly from publisher API for a specific city. Ad-hoc only, not production ingestion.

When in doubt about which pattern a pipeline uses, **read the block code** — `metadata.yaml.description` may be outdated.

---

## What you must NOT do

- **Do not open a PR unless explicitly told to** in the active task. Push the branch and stop; a human reviews and opens it.
- **Do not merge your own PR if you are an agent.** Humans review and merge.
- **Do not commit secrets.** AWS keys, DB passwords, `*.env`, `credentials*.json` → hard stop.
- **Do not flip `production_approved: true`** without running the `definition-of-done-check` skill first.
- **Do not introduce new deps** in `cc-mage/requirements.txt` without justification.
- **Do not modify `AGENTS.md`, `.cursor/rules/`, `.cursor/skills/`, `engineering-standards/`, or `docs/agent-runbook.md` without CTO review.** These are the agentic + standards foundation; the CTO is the curator. (Product / pipeline code merges are unaffected — any tech-team member can merge as today.)

## What you must always do

- Branch off `develop`. Conventional Commits with ticket where applicable.
- Run `docs-after-change` after any edit.
- Use the matching skill: `add-publisher` / `add-dataset-release` / `scaffold-mage-pipeline` / `sql-block-idempotency` / `definition-of-done-check`.
- Make `modelled.*` writes idempotent (`INSERT … ON CONFLICT … DO UPDATE`).

---

## Where to find what

### Rules

| Topic | Open |
|-------|------|
| General code taste | `.cursor/rules/general.mdc` |
| Repo + data architecture | `.cursor/rules/project-architecture.mdc` |
| Identity keys (locode, actor_id, datasource_name) | `.cursor/rules/identity-keys.mdc` |
| Branches, commits, PRs | `.cursor/rules/git-conventions.mdc` |
| Security baseline (secrets, AWS, DB) | `.cursor/rules/security-baseline.mdc` |
| OS / shell defaults | `.cursor/rules/os-shell.mdc` |
| Python style for blocks | `.cursor/rules/python-style.mdc` |
| Mage pipelines | `.cursor/rules/mage-pipelines.mdc` |
| Mage Python blocks | `.cursor/rules/mage-blocks-python.mdc` |
| Mage SQL blocks (UPSERT) | `.cursor/rules/mage-blocks-sql.mdc` |
| Dataset review + catalog | `.cursor/rules/dataset-review-catalog.mdc` |

### Skills

| Want to | Use |
|---------|-----|
| Scaffold a new Mage pipeline | `scaffold-mage-pipeline` |
| Add a new publisher / dataset | `add-publisher` |
| Add a new release of a dataset | `add-dataset-release` |
| Audit a SQL block for idempotency | `sql-block-idempotency` |
| Run the production-readiness checklist | `definition-of-done-check` |
| Generate S3 upload commands | `s3-upload-raw-data` |
| Write a commit message | `commit-message-standards` |
| Open / draft a PR | `pull-request-standards` |
| Review a PR | `pr-review-gate` |
| Update docs after a change | `docs-after-change` |
| Simplify code touched in this PR | `simplify-after-change` |
| Author / update an LLM prompt | `prompt-schema-authoring` |
| Quality-gate a runnable script | `script-quality-gate` |
| Run a full repo doc audit | `repo-doc-audit` (manual trigger only) |

### Standards (authoritative)

These are the team's canonical engineering standards. Rules and skills above are derived from them — when they disagree, **`engineering-standards/` wins** and we open a PR to fix the lesser doc.

- `engineering-standards/data-quality-and-validation.md`
- `engineering-standards/pipeline-design-patterns.md`
- `engineering-standards/documentation-and-metadata.md`
- `engineering-standards/naming-conventions.md`
- `engineering-standards/project-structure-and-architecture.md`
- `engineering-standards/data-model-design.md`
- `engineering-standards/definition-of-done.md`

### Domain knowledge

Topical notes for the data domain live in `knowledge-base/topics/`. Some are still stubs (`glossary.md`, `gpc-framework.md` — open PRs welcome).

---

## Curated backlog for autonomous agents

`docs/agent-runbook.md` is the authoritative list of tickets safe for an agentic run.

---

## Quickstart (humans)

```bash
# Postgres user/db
createuser -s ccglobal && createdb -O ccglobal ccglobal

# Local Mage stack
cp dev.env .env       # ask the CTO if you need real secrets in io_config.yaml
docker compose up     # http://localhost:6789
```

---

## Questions / corrections

If anything in this file or `.cursor/` is wrong, missing, or stale — **fix it in the same PR** that surfaced the gap. The agent contract only works if it's trustworthy.
