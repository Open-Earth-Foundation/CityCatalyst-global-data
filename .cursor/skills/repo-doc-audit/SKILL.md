---
name: repo-doc-audit
description: One-off full repo documentation audit. Use only when explicitly requested. Disabled by default to avoid expensive runs.
disable-model-invocation: true
---

# repo-doc-audit — global-data

Run on demand for a full repo audit. Expected output: a short report + suggested fixes.

## Scope

- `README.md` accuracy (commands, paths, env vars, references — current tree uses `knowledge-base/` not `domain-knowledge/`).
- `AGENTS.md` and `ARCHITECTURE.md` against the actual tree.
- All `engineering-standards/*.md` for internal consistency (terminology, paths, identity keys).
- Per-publisher `dataset-review/reviews/<…>/README.md` against the latest `review.yaml`.
- `catalog/index.yaml` completeness — every `production_approved: true` row has `pipeline_name` + `data_quality`.
- Pipeline `metadata.yaml` `description` is non-null and matches the README.
- `requirements.txt` covers what the blocks actually import (boto3, sqlalchemy, requests, etc.).

## Method

1. Read the current tree (`find . -type f`) and compare against doc claims.
2. For each mismatch, score impact 1–10. Report ≥ 5 only.
3. Provide minimal-edit suggestions.
4. Apply edits only if the user explicitly says so.

## Non-goals

- Style enforcement.
- Rewriting unfamiliar standards prose.
