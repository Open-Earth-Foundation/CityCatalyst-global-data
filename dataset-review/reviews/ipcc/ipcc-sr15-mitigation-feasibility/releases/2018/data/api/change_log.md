# Change log — SR1.5 feasibility vs prior socioeconomic mock

How this release replaces the previous `action_socioeconomic` placeholder mock, and how the API mocks in this folder differ from HIAP-MEED `socioeconomicIndicators` in `CityCatalyst/hiap-meed/data/mock/actions_api_mock.json`.

---

## Dataset & scoring (replaces `action_socioeconomic` mock CSV)

The system previously used a **510-row mock CSV** with `(action_id, indicator_key, direction, weight)` — placeholder values and no published methodology. The current pipeline replaces it.

| Change | Reason |
|--------|--------|
| **Mock placeholder weights → IPCC-anchored A/C verdicts.** Every score traces to a specific SR1.5 Ch.4 SM cell (Tables 4.SM.7–15) with original IPCC citations. | Full provenance to a peer-reviewed source; the mock had none. |
| **Free-form (action, indicator) weights → A/C rule for city adjustment.** City signal only where IPCC found a directional effect (A = barrier, C = supportive). B / NE / LE use the SR1.5 prior only. | Avoids inventing direction where the IPCC literature did not. |
| **Editorial weights → strong-only bridges with literature lineage.** SR1.5 ↔ city bridges must cite canonical empirical work; weak bridges were dropped. | Each sign claim is defensible to a reviewer (see `sr15_indicator_to_city_indicator.csv`). |
| **Single coarse score → two-layer scoring (SR1.5 prior + city adjustment).** Per-cell → dimension → action. | Auditable chain; one feasibility feature with traceable provenance. |
| **AVG formula aligned to SR1.5 Table 4.SM.5.** Divide by `#effective_indicators` (including NE/LE), not A+B+C only. | Matches IPCC; missing evidence drags scores down as intended. |
| **Standalone mock → input to multi-feature ranking.** Feasibility sits beside legal, policy alignment, and emissions potential. | Other channels cover what socioeconomic feasibility does not. |

**Artifacts:** `feasibility_full_view.csv`, `simple_scorer.ipynb`, files under `data/` and `sample/`.

---

## API mocks vs HIAP `socioeconomicIndicators`

### Original (`actions_api_mock.json`)

Embedded **per action** in the catalogue. Expert-authored rows:

| Field | Role |
|-------|------|
| `indicator_key` | City attribute (e.g. `poverty_rate`) |
| `direction` | `supportive` or `constraining` for that action |
| `weight` | Blend weight within the action (~0.15–0.25) |
| `rationale` | Free-text justification |

No SR1.5 option, no global dimensions, no computed scores

### `action_indicator_feasibility_summary.json`

**City-scoped** (`locode`: `CL CNE`), **86 scorable actions**.

| vs HIAP mock | |
|--------------|--|
| One object per action, not per indicator | |
| `action_score` + six `dimension_scores` from scorer | |
| `sr15_option`, `match_strength`, `option_evidence`, `option_agreement` | |
| No `weight` or `rationale` text | |

**Endpoint (mock):** `GET /v1/cities/{locode}/action-indicator-feasibility` — for prioritizer / ranking.

### `action_indicator_feasibility_detail.json`

**Single-action** drill-down (example: `c40_0010` @ `CL CNE`).

| vs HIAP mock | |
|--------------|--|
| `dimensions[]` → `cells[]` (global indicator × city bridge) | |
| `global_indicator`, `global_relation`, numeric score chain | |
| `city_indicator`, quintile, signed/adjusted scores | |
| No manual weights; bridges in `sr15_indicator_to_city_indicator.csv` | |

**Endpoint (mock):** `GET /v1/cities/{locode}/actions/{action_id}/indicator-feasibility` — for audit / UI detail.

---

## At a glance

| | Prior `action_socioeconomic` CSV | HIAP `socioeconomicIndicators` | Summary JSON | Detail JSON |
|--|----------------------------------|-------------------------------|--------------|-------------|
| Provenance | Placeholder | Expert editorial | IPCC SR1.5 + scorer | Same |
| Scope | All actions × indicators | Per action in catalogue | Per city, 86 actions | Per city + one action |
| Output | direction + weight | direction + weight + rationale | `action_score`, dimension scores | Per-cell audit trail |

**Regenerate API mocks:** export cells in `../simple_scorer.ipynb` (from `feasibility_full_view.csv`).

---

## HIAP-MEED ranking model (implications)

**Today:** `hiap-meed` does **not** call these mocks. Feasibility is computed in `app/modules/prioritizer/blocks/feasibility.py`:

- `feasibility_score = 0.5 × legal + 0.5 × socio`
- **Legal:** soft requirements (`recommended` / `optional`) vs city legal catalogue.
- **Socio:** for each `action.socioeconomic_indicators[]` row from the actions API, map the city’s `attribute_category` bucket to −2…+2, flip sign if `constraining`, apply `weight`, average, then normalize to [0, 1].
- **Final rank** (orchestrator): `impact × w_i + alignment × w_a + feasibility × w_f` (defaults ~0.55 / 0.22 / 0.23).

**If wired to `action_indicator_feasibility_summary.json`:**

| Area | Effect |
|------|--------|
| Socio half | Replace the per-indicator loop with a **lookup** of precomputed `action_score` (0–1) by `(locode, action_id)`. Legal half and the 50/50 split can stay as-is unless product reweights. |
| Actions API | `socioeconomicIndicators[]` becomes **optional / legacy** for feasibility; catalogue can slim down once the city feasibility endpoint is live. |
| City API | Inline socio scoring still needs nine **canonical** buckets in `feasibility.py`; SR1.5 bridges also use `literacy_rate`, `disability_prevalence`, `indigenous_identification_rate`, `mean_years_schooling`, `fixed_internet_household_share`, `employment_agriculture_utilities` — only relevant if scoring stays in-process instead of via summary API. |
| Coverage | Summary has **86** actions; **16** catalogue actions have no SR1.5 option match and are omitted. Prioritizer needs a policy: exclude, `socio = 0`, or fallback to old rules. |
| Rank order | **Will change** vs current mocks: methodology is IPCC prior + A/C city adjustment, not editorial per-action weights. |
| Explainability | Evidence should expose `dimension_scores`, `sr15_option`, and detail `cells[]` — not `socioeconomic_indicator_rows` / `weight` / `rationale`. Update `explanations.py` and tests (e.g. `test_feasibility_block_with_mock_api_data`). |

**No change** to impact or alignment blocks, request shape (`POST /v1/prioritize`), or top-level weight keys — only how the socio component of feasibility is sourced.
