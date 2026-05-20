# City action mitigation feasibility scores API (2018)

Global API endpoint that returns **how feasible each climate action is for a given city**, blending IPCC SR1.5 global priors with city-level socioeconomic and land-cover indicators. Primary consumer: **hiap-meed** (socioeconomic half of the feasibility block).

Dataset: **ipcc-sr15-mitigation-feasibility** release **2018** (IPCC SR1.5 Ch.4 SM Tables 4.SM.7–15). Methodology: `../../review.md`. Full example payload: `example_response.json`.

---

## What this API answers

For a city (UN/LOCODE) and each mapped climate action:

1. **How feasible is it overall?** → `action_score` (0–1) and `rank_within_city`.
2. **Which IPCC option does the action map to?** → causal-chain fields (`global_mitigation_option`, `action_mapping_strength`, `option_family`).
3. **Why?** → `breakdown`: six feasibility dimensions, each with global IPCC verdicts and city bridge evidence.
4. **How local is the adjustment?** → `city_indicators[]` under each global indicator shows which city attributes moved the score (quintile bucket, direction, contribution).

Scores are computed at request time from `modelled.action_mitigation_feasibility_chain` (deterministic scoring chain) and `modelled.city_attribute` (city quintiles)—not pre-materialized per city.

---

## Endpoint

```
GET /api/v1/cities/{locode}/action-mitigation-feasibility-scores
```

### Query parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `locode` | path | required | City UN/LOCODE (e.g. `CL ZAL`, `CL CNE`) |
| `release_id` | UUID | latest 2018 | `modelled.dataset_release.release_id` for this dataset |
| `country_code` | string | `CL` | ISO-3166 alpha-2; city attributes are loaded for this country |
| `src_action_id` | string | — | Return a single action only (e.g. `c40_0034`, `icare_0045`) |

### HTTP status

| Status | Meaning |
|--------|---------|
| `200` | Success |
| `404` | Unknown release, or no scored actions for this city/release/filter |
| `422` | Invalid parameters |

### Example

```http
GET /api/v1/cities/CL%20ZAL/action-mitigation-feasibility-scores?country_code=CL&src_action_id=icare_0045
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
| `meta` | Provenance, request context, counts |
| `scores` | One object per climate action with an A/C-scorable chain for this release |

---

## `meta` fields

| Field | Meaning |
|-------|---------|
| `generated_at_utc` | When this response was built (ISO 8601, UTC) |
| `endpoint` | `GET /api/v1/cities/{locode}/action-mitigation-feasibility-scores` |
| `locode` | Requested city |
| `country_code` | Country used for city-attribute lookup |
| `release_id` | Release UUID used |
| `src_action_id` | Action filter, if any (`null` when returning all actions) |
| `total_records` | Number of actions in `scores` |

---

## `scores[]` — per action

| Field | Type | Meaning |
|-------|------|---------|
| `locode` | string | City UN/LOCODE |
| `src_action_id` | string | Climate action ID (C40, IPCC, ICARE codes) |
| `global_mitigation_option` | string | IPCC SR1.5 mitigation option name (e.g. `Solar PV`, `Reduced food wastage`) |
| `action_mapping_strength` | string | How confidently the catalogue action maps to that option |
| `option_family` | string | Sector scope used for city-bridge matching (e.g. `nbs`, `waste`, `energy_supply`) |
| `action_score` | number | Overall feasibility, **0–1** (mean of dimension scores) |
| `n_feasibility_dimensions` | integer | Count of dimensions with at least one A/C-scored indicator |
| `dimension_scores` | object | Six dimension scores (see below) |
| `breakdown` | object | Full audit trail keyed by dimension |
| `rank_within_city` | integer | Rank by `action_score` descending (1 = highest feasibility) |

### Causal chain fields

These three fields trace **catalogue action → IPCC mitigation option** and govern which city bridges can apply.

| Field | Common values | Meaning |
|-------|---------------|---------|
| `global_mitigation_option` | `Solar PV`, `Soil carbon sequestration & biochar`, `Reduced food wastage`, … | Verbatim SR1.5 option name from `actions_to_sr15_mapping.csv` |
| `action_mapping_strength` | `direct` \| `partial` \| `weak` \| `cross_cutting` | Mapping confidence; weaker mappings inherit the option prior with less editorial certainty |
| `option_family` | `energy_supply`, `transport`, `buildings`, `industrial`, `nbs`, `waste`, `sustainable_intensification`, … | Sector scope; city bridges in `sr15_indicator_to_city_indicator.csv` must match this scope (or `all`) |

**Example:** `c40_0034` → `Reduced food wastage` / `weak` / `waste`. Geophysical indicators like `limited_land_use` have LULC bridges only under `nbs`, so `city_indicators` is empty for waste actions even when MapBiomas data exists for the city.

### `dimension_scores`

Six IPCC feasibility dimensions. Keys use full names; values are **0–1**.

| Key | IPCC dimension |
|-----|----------------|
| `economic` | Economic |
| `technological` | Technological |
| `institutional` | Institutional |
| `socio_cultural` | Socio-cultural |
| `environmental` | Environmental |
| `geophysical` | Geophysical |

A dimension is omitted from `dimension_scores` only when no A/C indicators exist for that action (unusual for mapped actions).

---

## `breakdown` — dimension drill-down

Object keyed by dimension name (same keys as `dimension_scores`). Each dimension contains:

| Field | Meaning |
|-------|---------|
| `dimension_score` | Average of indicator scores in this dimension (0–1) |
| `n_global_indicators` | Count of A/C-scored global indicators in this dimension |
| `global_indicators` | Array of indicator-level evidence (see next section) |

---

## `global_indicators[]` — per dimension

One row per IPCC global indicator with an **A** (barrier) or **C** (supportive) verdict. B / NE / LE / NA cells are excluded from scoring and do not appear here.

| Field | Meaning |
|-------|---------|
| `global_indicator` | SR1.5 indicator slug (e.g. `cost-effectiveness`, `limited_land_use`) |
| `global_verdict` | Human-readable IPCC direction: `supportive` (C) or `barrier` (A) |
| `global_contribution` | Numeric prior signal: `+1` (supportive) or `-1` (barrier) |
| `n_city_indicators` | Count of active city bridges that adjusted this indicator |
| `avg_city_contribution` | Mean signed bridge contribution (−1…+1), or `null` when `n_city_indicators = 0` |
| `indicator_score` | Blended 0–1 score after merging global prior and city bridges |
| `city_indicators` | Active city bridge rows (see below); empty when no scope-matching bridge or missing city data |

### When `city_indicators` is empty

This is **expected**, not missing data, when:

- No city bridge is defined for this `(global_indicator, option_family)` pair (e.g. LULC on `waste` actions).
- The bridge exists but the city lacks a quintile bucket in `city_attribute` for that indicator.
- IPCC coded the cell B / NE / LE (those cells never appear in this API).

---

## `city_indicators[]` — per global indicator

Each active bridge that matched the city's data for this indicator.

| Field | Meaning |
|-------|---------|
| `city_indicator` | City attribute key (e.g. `poverty_rate`, `primary_forest_share`) |
| `category` | Quintile bucket: `very low` \| `low` \| `medium` \| `high` \| `very high` |
| `direction` | Bridge sign: `positive` (higher bucket → more feasible) or `negative` (higher bucket → less feasible) |
| `capacity` | Numeric bucket weight: 0.00 / 0.25 / 0.50 / 0.75 / 1.00 |
| `contribution` | Signed adjustment: `direction_sign × (2 × capacity − 1)`, rounded to 3 dp |

### City data sources (Chile v1)

| Indicator family | Example keys | Datasource |
|------------------|--------------|------------|
| Socioeconomic | `poverty_rate`, `median_household_income`, `public_transport_share` | cl-casen 2022 |
| Demographic / employment | `home_ownership`, `literacy_rate`, `employment_agriculture_utilities` | cl-ine-censo 2024 |
| Land cover | `primary_forest_share`, `urban_built_share`, `pasture_share`, … | cl-mapbiomas LULC |

Bridge definitions and literature lineage: `../sr15_indicator_to_city_indicator.csv`.

---

## Scoring summary

Three-layer rollup (matches `../../sample/query.sql` and `modelled.city_action_mitigation_feasibility_scores`):

1. **City capacity** — Map quintile `category` → `capacity` (0…1).
2. **Indicator score** — For each A/C global indicator:
   - `sr15_signal` = +1 if `supportive` (C), −1 if `barrier` (A).
   - `bridge_contribution` = sign × (2 × capacity − 1) for each active city bridge.
   - If bridges exist: `indicator_score = ((sr15_signal + avg(bridge_contribution)) / 2 + 1) / 2`.
   - If no bridges: `indicator_score = (sr15_signal + 1) / 2` (global prior only).
3. **Dimension score** — Mean of indicator scores in the dimension.
4. **Action score** — Mean of dimension scores → exposed as `action_score`.

### A/C rule (city adjustment gate)

City data adjusts the score **only** where IPCC found a directional effect (A or C). B (neutral), NE (no evidence), LE (limited evidence), and NA (not applicable) cells contribute neither to scoring nor to city adjustment. This is methodologically conservative: every city bridge traces to an IPCC-published directional finding.

Full methodology: `../../review.md` § "Scoring an action for a city".

---

## Interpretation caveats

| Topic | Guidance |
|-------|----------|
| **Ordinal use** | Relative ordering of actions within a city is more reliable than absolute `action_score` values. Standardise alongside other ranking features before weighted combination. |
| **Environmental / geophysical** | These dimensions often reflect the SR1.5 global prior with little city discrimination unless LULC bridges apply (`nbs`, `energy_supply`, etc.). |
| **Mapping strength** | `weak` or `cross_cutting` mappings inherit option priors with less catalogue specificity; treat as lower-confidence causal links. |
| **Coverage** | ~86–99 actions per city depending on release; ~16 catalogue actions have no SR1.5 option match and are omitted entirely. |
| **Country scope** | v1 city attributes are loaded for Chile (`country_code=CL`). Other countries require matching `city_attribute` pipelines. |

---

## Using this API in hiap-meed

### What the prioritizer uses today

The **feasibility** block currently computes:

```
feasibility_score = 0.5 × legal + 0.5 × socio
```

The **socio** half loops over `actions[].socioeconomicIndicators[]` from the actions catalogue, mapping city buckets to weighted scores inline (`app/modules/prioritizer/blocks/feasibility.py`).

### Minimum mapping from this API

| API field | hiap-meed use |
|-----------|---------------|
| `src_action_id` | `action_id` lookup key |
| `action_score` | Replace inline socio computation (0–1) |
| `dimension_scores` | Explainability / dimension-level UI |
| `breakdown.global_indicators[].city_indicators` | Replace `socioeconomic_indicator_rows` evidence |
| `global_mitigation_option` | Replace `sr15_option` in summary mock |
| `action_mapping_strength` | Replace `match_strength` in summary mock |

Legal half and the 50/50 split can stay as-is unless product reweights. See § "Changes from mock `socioeconomicIndicators`" below for migration rationale.

---

## Changes from mock `socioeconomicIndicators`

The hiap-meed actions catalogue mock (`CityCatalyst/hiap-meed/data/mock/actions_api_mock.json`) embeds feasibility hints per action as `socioeconomicIndicators[]` — expert-authored rows with `indicator_key`, `direction`, `weight`, and free-text `rationale`. A typical waste action might list income, poverty, unemployment, transport employment, and electricity access with weights summing ~1.0; the prioritizer scores these inline against city quintiles in `feasibility.py`.

This API replaces that pattern. The mock was useful for prototyping UI and ranking flow, but it had three problems we could not defend in a review:

1. **No external provenance.** Weights and rationales were editorial. There was no link to a published feasibility framework, so two reviewers could disagree on whether `electricity_access_rate` should weigh 0.20 vs 0.15 for the same action with no way to adjudicate.
2. **Per-action indicator shopping.** Each action could declare a different indicator set. That made scores incomparable across actions (different denominators and signals) and encouraged post-hoc justification rather than a shared scoring model.
3. **Single-layer city adjustment.** The mock blended city quintiles directly into one socio score. It ignored the global literature on whether an indicator actually matters for that mitigation option — e.g. assigning transport employment to a waste action without an IPCC directional finding.

The IPCC SR1.5 pipeline fixes this with a **two-layer, auditable chain**:

| Layer | Source | Role |
|-------|--------|------|
| Global prior | SR1.5 Ch.4 SM Tables 4.SM.7–15 (A/B/C verdicts, cited) | "How feasible is this option globally?" |
| City adjustment | Literature-cited bridges in `../sr15_indicator_to_city_indicator.csv` | "How does this city's profile modify the prior?" — **only** where IPCC coded A or C |

Indicators are not hand-picked per action. They flow from **action → IPCC option → option family → scope-matched bridge**. A waste action mapped to `Reduced food wastage` inherits economic bridges scoped to `all` (e.g. `cost-effectiveness` × income/poverty) but not geophysical LULC bridges scoped to `nbs`. That is why the live response for `c40_0034` shows fewer city indicators than the mock list suggested — not missing data, but stricter bridge eligibility.

**What you lose:** per-action free-text `rationale` in the API payload; bespoke indicator sets tuned to action wording.

**What you gain:** traceability to IPCC cells and peer-reviewed bridge citations; consistent cross-action scoring; six-dimension breakdown; causal chain metadata (`global_mitigation_option`, `action_mapping_strength`, `option_family`).

For methodology detail see `../../review.md` (especially § "Scoring an action for a city", "A/C rule", and "Quality threshold: strong bridges only"). For hiap-meed wiring, replace the socio loop with an `action_score` lookup by `(locode, src_action_id)` and use `breakdown` for explainability.

| Topic | Catalogue mock | This API |
|-------|----------------|----------|
| Provenance | Expert editorial weights | IPCC SR1.5 A/C priors + literature-cited bridges |
| Per-action rows | `indicator_key`, `direction`, `weight`, `rationale` | Computed `city_indicators[]` from quintiles |
| Score formula | Weighted bucket average ÷ 3 | Two-layer SR1.5 prior + city blend (see § "Scoring summary") |
| Dimensions | Single socio score | Six IPCC feasibility dimensions |

**Scores are not numerically comparable** between the catalogue socio loop and this endpoint for the same city/action until hiap-meed is rewired.

---

## Differences vs prior API mocks

Do not assume parity with older contracts.

### vs `action_indicator_feasibility_summary.json`

| Topic | Summary mock | This API |
|-------|--------------|----------|
| Route | `GET /v1/cities/{locode}/action-indicator-feasibility` | `GET /api/v1/cities/{locode}/action-mitigation-feasibility-scores` |
| Root array | `actions` | `scores` |
| Action id | `action_id` | `src_action_id` |
| IPCC option | `sr15_option` | `global_mitigation_option` |
| Mapping | `match_strength` | `action_mapping_strength` |
| Option scope | not exposed | `option_family` |
| Extra mock fields | `option_evidence`, `option_agreement`, `action_name` | not exposed (catalogue-side metadata) |
| Detail | summary only | full `breakdown` inline |
| Ranking | not included | `rank_within_city` |

### vs `action_indicator_feasibility_detail.json`

The live API **merges summary + detail**: every action includes the full `breakdown` tree. The detail mock's `dimensions[] → cells[]` structure maps to `breakdown.{dimension}.global_indicators[]`.

| Detail mock field | Live API field |
|-------------------|----------------|
| `cells[].global_indicator` | `global_indicators[].global_indicator` |
| `cells[].global_relation` | `global_indicators[].global_verdict` |
| `cells[].city_indicator` | `city_indicators[].city_indicator` |
| quintile label | `city_indicators[].category` |
| signed score chain | `global_contribution`, `contribution`, `indicator_score` |

---

## Example response (abbreviated)

From `example_response.json` — Valdivia (`CL ZAL`), action `icare_0045` (NBS / soil carbon):

```json
{
  "meta": {
    "generated_at_utc": "2026-05-20T10:26:39.139737+00:00",
    "endpoint": "GET /api/v1/cities/{locode}/action-mitigation-feasibility-scores",
    "locode": "CL ZAL",
    "country_code": "CL",
    "release_id": "05da7e3a-9db5-4db7-0e1b-e419c0ac7d5e",
    "src_action_id": null,
    "total_records": 99
  },
  "scores": [
    {
      "locode": "CL ZAL",
      "src_action_id": "icare_0045",
      "global_mitigation_option": "Soil carbon sequestration & biochar",
      "action_mapping_strength": "direct",
      "option_family": "nbs",
      "action_score": 0.908,
      "n_feasibility_dimensions": 5,
      "dimension_scores": {
        "economic": 0.917,
        "technological": 1,
        "socio_cultural": 0.875,
        "environmental": 1,
        "geophysical": 0.75
      },
      "breakdown": {
        "geophysical": {
          "dimension_score": 0.75,
          "n_global_indicators": 1,
          "global_indicators": [
            {
              "global_indicator": "limited_land_use",
              "global_verdict": "supportive",
              "global_contribution": 1,
              "n_city_indicators": 1,
              "avg_city_contribution": 0,
              "indicator_score": 0.75,
              "city_indicators": [
                {
                  "city_indicator": "primary_forest_share",
                  "category": "medium",
                  "direction": "positive",
                  "capacity": 0.5,
                  "contribution": 0
                }
              ]
            }
          ]
        }
      },
      "rank_within_city": 41
    }
  ]
}
```

Contrast with `c40_0034` (`waste` / `weak`): same city shows empty `city_indicators` on geophysical LULC indicators because no waste-scoped bridge exists—see § "When `city_indicators` is empty".

---

## Related artifacts

| File | Purpose |
|------|---------|
| `example_response.json` | Full live export for `CL ZAL` (99 actions) |
| `../../review.md` | Dataset methodology and bridge inventory |
| `../scoring_chain.csv` | Deterministic chain loaded to `modelled.action_mitigation_feasibility_chain` |
| `CityCatalyst/global-api/routes/city_action_mitigation_feasibility_scores.py` | Route implementation |
| `CityCatalyst/global-api/migrations/sql/city_action_mitigation_feasibility_scores.sql` | Scoring SQL function |
