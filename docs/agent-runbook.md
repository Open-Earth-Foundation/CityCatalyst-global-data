# Agent Runbook — global-data

The curated list of tasks an autonomous agent (Cursor agent, agentic-coder, Cloud Agents) is allowed to pick up without further approval.

> **Rules of the road**
> - Pick the **top unchecked item** in the bucket that fits.
> - Branch off `develop`. One ticket = one PR.
> - Use the matching skill (linked).
> - **Do not open the PR yourself unless explicitly told to.** Push the branch and stop.
> - Cross items out as you ship.

---

## Quick (≤ 30 min, ≤ 5 files)

- [ ] **Update `README.md`** to reference `knowledge-base/` instead of `domain-knowledge/`. Skill: `docs-after-change`.
- [ ] **Fix typo** in `knowledge-base/catalog/index.yaml`: `items/climate-projec.md` → `items/climate-project.md`.
- [ ] **Audit knowledge-base topics** — sweep `knowledge-base/topics/` for stale or thin pages, expand or cross-link as needed. Skill: `repo-doc-audit`.
- [ ] **Audit `cc-mage/requirements.txt`** — list deps actually imported by blocks (boto3, requests, sqlalchemy) that aren't pinned. Add them with current versions.
- [ ] **Fill `metadata.yaml.description`** for any pipeline where it is `null`. Skill: `mage-pipelines.mdc`.
- [ ] **Add CI step** to fail on `metadata.yaml.description: null` (lint over `cc-mage/pipelines/**`).

## Medium (≤ 2h, ≤ 20 files)

- [ ] **Promote real Layer 2 tests** in 5 oldest pipelines. Replace `assert output is not None` with schema + uniqueness + plausibility checks. Rule: `mage-blocks-python.mdc`.
- [ ] **Audit SQL exporters for UPSERT** — find any `data_exporter` with `export_write_policy: append` writing to `modelled.*` that is **not** an `INSERT … ON CONFLICT … DO UPDATE`. Skill: `sql-block-idempotency`.
- [ ] **Add `created_at` / `updated_at` / `release_id`** to any `modelled.*` table missing them. See `engineering-standards/data-model-design.md` "backlog".
- [ ] **Catalog hygiene** — for every dataset with `production_approved: true` whose `pipeline_name` or `data_quality` is null, fix or downgrade. Skill: `definition-of-done-check`.
- [ ] **Fill `knowledge-base/collections/collection.yaml`** — current placeholders have no IDs. Wire to existing topics + datasets.

## Large (half-day+)

- [ ] **GitHub Actions: per-pipeline test job** — currently only `mage-ai-develop.yml` (Docker build). Add a CI job that runs Mage `@test` decorators against a sample for changed pipelines. Skill: `script-quality-gate`.
- [ ] **`dq_*` pipelines** — one per `modelled.*` table doing post-write Layer 3 plausibility checks (negative values, gas codes in allowed set, year ranges). Skill: `scaffold-mage-pipeline`.
- [ ] **Promote v2026 ClimateTRACE pipelines** — when CT publishes the new release, scaffold the `_v2026` fork and run the `definition-of-done-check`.

## Continuous

- [ ] **Run `repo-doc-audit`** monthly.
- [ ] **Verify `production_approved` rows** weekly (script can be a `dq_catalog_health` pipeline).

---

## Adding tickets

1. Write a 1-line description **+ matching skill**.
2. Bucket Quick / Medium / Large by capability budget per agent run.
3. Mention an existing branch if one exists.
