---
name: pull-request-standards
description: Create pull requests with repository-derived context, concise title/body standards. Use when creating, automating, or polishing a PR for global-data.
---

# Pull Request Standards — global-data

Use this whenever you draft, automate, or polish a PR for `CityCatalyst-global-data`.

## Derive context

- Owner / repo: `git remote get-url origin` → `Open-Earth-Foundation/CityCatalyst-global-data`.
- Head: `git rev-parse --abbrev-ref HEAD`.
- Base: **`develop`** (this repo's default).

## Title

- ≤72 chars, imperative.
- Conventional-Commit-flavoured: `feat(pipeline): add ghgi_eurostat_v2026`.
- Ticket prefix when applicable.

## Body (short, practical)

```markdown
## Summary
1–3 sentences: what changed and why.

## Changes
- bullet
- bullet

## Catalog updates (if applicable)
- which `catalog/index.yaml` entry was changed
- which `dataset-review/.../review.yaml` was added or updated

## Pipeline runs (if applicable)
- pipeline name + dev run timestamp + row counts
```

## Push policy

Assume the branch is already pushed when the user asks to create a PR. Do **not** run `git push` unless explicitly asked.

## Who merges

- **Pipelines / catalog / code** — any tech-team member after standard review (≥1 approval, CI green).
- **Agentic + standards foundation** (`AGENTS.md`, `.cursor/rules/`, `.cursor/skills/`, `engineering-standards/`, `docs/agent-runbook.md`) — CTO sign-off required; then anyone merges.
- **Agents** never merge their own PRs and do not open PRs unless explicitly told to in the active task. If asked to open the PR, use `gh pr create --base develop`.
