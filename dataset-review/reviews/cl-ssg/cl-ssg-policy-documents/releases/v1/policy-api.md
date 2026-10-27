# City action policy scores API (v1)

Global API endpoint that returns **how strongly Chilean policy documents support each climate action for a given city**, plus ranked evidence citations. Primary consumer: **hiap-meed** (action prioritization alignment block).

Dataset: **cl-ssg-policy-documents** v1 (curated by [Sustainability Solutions Group](https://ssg.coop/)). Scoring rubric version: **v0.2.0**.

---

## What this API answers

For a city (UN/LOCODE) and each climate action:

1. **How much policy support exists?** → `policy_support_score` (0–1) and `policy_support_category` (`strong` / `medium` / `weak` / `none`).
2. **Why?** → `policy_evidence`: top passages from plans, PARCC, PACCC, NDC, etc., with document context.
3. **How local is the evidence?** → `meta.spatial_document_coverage` states whether scores are based on national-only, regional, or municipal documents for that city.

Scores are computed at request time from stored policy findings for the selected dataset release—not pre-materialized per city.

---

## Endpoint

```
GET /api/v1/cities/{locode}/action-policy-scores
```

### Query parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `locode` | path | required | City UN/LOCODE (e.g. `CL ANF`, `CL ZAL`) |
| `release_id` | UUID | latest v1 | Dataset release to score against |
| `top_evidence_limit` | int | `5` | Max evidence items per action (0–20) |
| `src_action_id` | string | — | Return a single action only (e.g. `c40_0010`) |

### HTTP status

| Status | Meaning |
|--------|---------|
| `200` | Success |
| `404` | Unknown city/release, or no scored actions for this city |
| `422` | Invalid parameters |

### Example

```http
GET /api/v1/cities/CL%20ZAL/action-policy-scores?top_evidence_limit=3
```

---

## Response structure

All JSON keys are **snake_case**.

```json
{
  "meta": { },
  "scores": [ ]
}
```

| Top-level key | Meaning |
|---------------|---------|
| `meta` | Provenance, request context, spatial coverage caveat, counts |
| `scores` | One object per climate action that has policy support for this city |

---

## `meta` fields

| Field | Meaning |
|-------|---------|
| `generated_at_utc` | When this response was built (ISO 8601, UTC) |
| `backend_consumer` | Intended downstream (`hiap-meed`) |
| `upstream_provider` | Serving system (`global-api`) |
| `scoring_rubric_version` | Rubric used for scores (`v0.2.0`) |
| `total_records` | Number of actions in `scores` |
| `total_evidence_items` | Total items across all `policy_evidence` arrays |

### `meta.api_context`

Echoes the request:

| Field | Meaning |
|-------|---------|
| `endpoint` | `GET /api/v1/cities/{locode}/action-policy-scores` |
| `locode` | Requested city |
| `city_name` | Comuna / city name |
| `release_id` | Release UUID used |
| `top_evidence_limit` | Evidence cap per action |
| `src_action_id` | Action filter, if any |

### `meta.spatial_document_coverage`

**Important for interpretation.** Describes the **most local level of policy documents** available for this city in the current release.

| Field | Meaning |
|-------|---------|
| `location_scopes_included` | Which levels appear in the corpus: `national`, `regional`, `municipal` |
| `finest_location_scope` | Deepest level present: `municipal` > `regional` > `national` |
| `caveat` | Plain-language guidance on how to read the scores |

| `finest_location_scope` | How to interpret scores |
|-------------------------|-------------------------|
| `national` | Based on national instruments only (e.g. NDC, national frameworks)—not regional PARCC or municipal PACCC for this city |
| `regional` | Includes regional plans; no municipal PACCC for this comuna in the release |
| `municipal` | Includes city-level plans (e.g. PACCC) where mapped—most locally specific |

---

## `scores[]` — per action

| Field | Type | Meaning |
|-------|------|---------|
| `src_action_id` | string | Climate action ID (e.g. C40, IPCC, ICARE codes) |
| `policy_support_score` | number | Overall support strength, **0–1** (see scoring summary below) |
| `policy_support_category` | string | Readable band: `strong` \| `medium` \| `weak` \| `none` |
| `best_relevance` | string | Strongest document-level relevance for this action: `high` \| `medium` \| `low` \| `none` |
| `n_findings` | integer | Count of distinct findings that contributed (after deduplication) |
| `n_docs` | integer | Number of distinct source documents |
| `sum_strength` | number | Sum of weighted finding strengths (before saturation curve) |
| `policy_evidence` | array | Top-ranked supporting passages (see next section) |

### Score bands (`policy_support_category`)

| `policy_support_score` | Category |
|------------------------|----------|
| ≥ 0.66 | `strong` |
| ≥ 0.33 | `medium` |
| > 0 | `weak` |
| 0 | `none` |

### Scoring summary (v0.2.0)

Scores combine many document findings for the city and action:

1. **Territorial filter** — National documents always apply; regional documents match the city’s region; municipal documents match the city’s comuna/locode.
2. **Per-finding weight** — Each passage is weighted by document proximity (national vs PARCC vs PACCC), extractor confidence (`signal_strength`), relation type (`signal_relation`, e.g. commit vs reference), and `explicitness`.
3. **Saturation** — Many weak findings do not stack linearly; strength saturates with constant K = 4.0.
4. **Relevance cap** — The best document relevance grade (`best_relevance`) caps the final score so tangential docs cannot produce a `strong` rating alone.

Full rubric detail: `releases/v1/design/scoring_rubric.md`.

---

## `policy_evidence[]` — per action

Ranked list of the strongest supporting passages (up to `top_evidence_limit`). `evidence_rank` 1 is strongest.

| Field | Meaning |
|-------|---------|
| `evidence_rank` | Rank within this action (1 = strongest) |
| `signal_type` | Kind of policy signal (e.g. `action`, `target`, `funding`, `governance`) |
| `signal_relation` | How the text relates to the action (e.g. `commits`, `targets`, `monitors`, `references`, `restates`) |
| `signal_strength` | Extractor confidence: `high` \| `medium` \| `low` |
| `document_name` | Source document title |
| `document_type` | Document class (e.g. `parcc`, `paccc`, `framework`, `sector_plan`)—affects how “local” the finding is weighted |
| `doc_relevance` | How relevant the **whole document** is to this action: `high` \| `medium` \| `low` |
| `explicitness` | `explicit` (directly about the action) or `inferred` (requires interpretation) |
| `page` | Page in the source PDF |
| `evidence_strength` | Combined rubric weight for this passage |
| `evidence_text` | Verbatim excerpt |

Internal database IDs are not exposed in the API.

### Controlled vocabulary (common values)

**`signal_relation`** (policy commitment strength):

| Value | Typical meaning |
|-------|-----------------|
| `commits`, `targets`, `target`, `funds` | Strongest—explicit commitment, target, or funding |
| `monitors`, `monitor`, `governs` | Implementation / governance |
| `prioritizes`, `identifies` | Thematic priority or risk identification |
| `references`, `contextualizes`, `restates` | Weaker—cross-reference or repetition of higher-level policy |

**`document_type`** (examples):

| Value | Typical source |
|-------|----------------|
| `paccc` | Municipal climate plan |
| `parcc` | Regional climate plan |
| `environmental_program` | Communal environmental programme |
| `framework`, `sector_plan` | National strategy / sector plan |
| `territorial_plan` | Territorial planning instrument |

---

## Using this API in hiap-meed

### What the prioritizer uses today

The **alignment** block reads `policy_support_score` per action (0–1) and optionally signal summaries for explainability. Configure via `HIAP_MEED_POLICY_SIGNALS_DATA_SOURCE` (`mock` or `api`; API client is not wired yet).

Minimum mapping from this API:

| API field | hiap-meed `PolicySignalByAction` |
|-----------|----------------------------------|
| `src_action_id` | `action_id` |
| `policy_support_score` | `policy_support_score` |

`policy_evidence` can feed explainability (document name, relation, excerpt) without changing the alignment formula.

Always surface `meta.spatial_document_coverage.caveat` in UI or reports when scores might be national- or regional-only.

---

## Differences vs hiap-meed policy-signals mock

The existing **hiap-meed mock** (`actions_policy_signals_api_mock.json`) targets an older contract. Do not assume parity.

| Topic | Mock | This API |
|-------|------|----------|
| Route | `GET /v1/cities/{locode}/policy-signals` | `GET /api/v1/cities/{locode}/action-policy-scores` |
| Root array | `policy_signals` | `scores` |
| Action id field | `action_id` | `src_action_id` |
| Evidence | Grouped `policy_signals` with `evidence_ids` counts | `policy_evidence` with full `evidence_text`, ranked |
| Score extras | Score only | + `policy_support_category`, `best_relevance`, `n_findings`, … |
| Spatial caveat | None | `meta.spatial_document_coverage` |
| `location_scope` | `National`, `Regional`, `Communal` | `national`, `regional`, `municipal` |
| `signal_relation` | `supports`, `provides`, `assigns`, … | `commits`, `targets`, `monitors`, … |
| Score formula | Simple weighted sum ÷ 3 | Rubric v0.2.0 (saturation + relevance cap) |

**Scores are not numerically comparable** between mock and live API for the same city/action until the mock is regenerated from this endpoint.

---

## Example response (abbreviated)

```json
{
  "meta": {
    "generated_at_utc": "2026-05-19T14:00:00+00:00",
    "scoring_rubric_version": "v0.2.0",
    "total_records": 42,
    "total_evidence_items": 126,
    "api_context": {
      "locode": "CL ZAL",
      "city_name": "Valdivia",
      "top_evidence_limit": 3
    },
    "spatial_document_coverage": {
      "location_scopes_included": ["national", "regional", "municipal"],
      "finest_location_scope": "municipal",
      "caveat": "Policy support scores use documents at national, regional, municipal level..."
    }
  },
  "scores": [
    {
      "src_action_id": "c40_0010",
      "policy_support_score": 0.42,
      "policy_support_category": "medium",
      "best_relevance": "high",
      "n_findings": 8,
      "n_docs": 3,
      "sum_strength": 1.24,
      "policy_evidence": [
        {
          "evidence_rank": 1,
          "signal_type": "action",
          "signal_relation": "commits",
          "signal_strength": "high",
          "document_name": "Plan de Acción Regional de Cambio Climático",
          "document_type": "parcc",
          "doc_relevance": "high",
          "page": 42,
          "evidence_strength": 0.49,
          "evidence_text": "..."
        }
      ]
    }
  ]
}
```
