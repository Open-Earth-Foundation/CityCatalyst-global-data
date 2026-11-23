# Brazil adaptation module: technical handover

> The module gives each city its adaptation actions in a default order, to focus how the city reviews them. City choices filter the list and never change the order.

## Requirements from the confirmed adaptation methodology

1. **Ordered list.** For a city, provide the adaptation actions that act directly on a risk the city has, in a default order with a position number (29 actions in each test city). The order is there to focus how the city reviews the actions. It is not a ranking that justifies why one action comes first.
2. **Filters.** Every city choice (timeline, cost band, risk sector, co-benefit) is a filter. Filters narrow the list and do not enter the ordering logic.
3. **Re-sorting.** The city can sort on any single score: impact, legal feasibility, cost or policy alignment.
4. **Action detail.** Each action opens to the evidence behind its scores, plus context: co-benefits, legal norms, policy passages, finance programmes and past projects. Policy documents and past projects show the top 5 and the total, with a full list on request.
5. **Supporting actions.** Each action lists its supporting actions, marked as a pre-action (comes first) or a co-action (goes with it). The 9 supporting actions (planning, monitoring and enabling) are not ordered and only appear on the actions they are linked to.
6. **City finance context.** The CAPAG credit screen and MUNIC preparation capacity are shown once per city. They are not scored.
7. **Plan generation.** The city can generate an implementation plan for an action it picks.

**Question for the team:** the order is not presented as a recommendation, so do we still need explanation text per action, or a ranking report? The evidence in the action detail may be enough.

## Compared with hiap-meed

`hiap-meed` prioritises mitigation actions for Chile, but it is the closest existing service to this module.

| | `hiap-meed` | Brazil adaptation module |
|---|---|---|
| Actions | Action pathways from the Global API | 38-action Brazil adaptation bank |
| What impact is based on | Emissions reduction as a share of the city's total | AdaptaBrasil risk (`/api/v1/cities/{locode}/climate-risk/adapta`) |
| How actions are ordered | Hard filter, then weighted impact, alignment and feasibility | Weighted impact, feasibility and alignment, with fixed weights |
| City choices | Preferences, exclusions and weight overrides sent in the request change the score | Filters in the frontend. They don't change the order |
| When the order is produced | On each request | Ahead of time, for every city. Shown by default |
| Output | Ranked actions with evidence summaries, optional explanations | Ordered actions with their position and all scores |
| Detail and context | Reference-data endpoints | Action detail, plus full lists of policy documents and past projects |
| AI step | Explanations and 8-chapter output-plan report | Plan generation (explanations and report: see the question above) |

## What sets the order

**overall = 0.55 × impact + 0.225 × feasibility + 0.225 × alignment**

| Part | How it is scored | Changes by city? |
|---|---|---|
| Impact | The action's best AdaptaBrasil risk cell for the city, divided by the city's top action (top action = 1) | Yes |
| Feasibility | Half legal (1 to 5 score rescaled to 0 to 1), half cost (low 0.6, medium 0.5, high 0.4) | No |
| Alignment | Policy alignment score | No |

All scores are 0 to 1. Equal overall scores share a position. Only actions with a Direct link to a risk the city has get a position. An action with a Direct link to no risk scored for the city is listed after them with no position (none of the test cities has one).

Impact is the only part that differs between cities, and it depends only on the city's AdaptaBrasil risk. `build_sample_data.ipynb` has the calculation and checks it against I Care's results for the five test cities.

## What this means for the build

The testing sessions confirmed how the actions are ordered and which inputs the order needs. None of those inputs come from the city, so:

- **The order can be there by default.** There is no step where the city enters information and requests an ordering. The order can be computed ahead of time from the stored action scores and the city's AdaptaBrasil risk, for every municipality, and recomputed when an action score or the AdaptaBrasil data changes. `city-action-order.csv` shows the shape.
- **Filtering and re-sorting can happen in the frontend**, on fewer than 40 rows already in the response.
- **Plan generation is the step that runs when the city asks for it.** The current plan creator already takes an action ID and city data.

## Data

One CSV per table, keyed on `action_id` or `locode`. The notebooks read the input tables from `sample/`, and the mock responses show every field with real values.

| Kind | Tables |
|---|---|
| Fixed per action (the scores) | impact links, legal feasibility, cost, policy alignment |
| Fixed per action (context) | action text, legal norms, policy evidence, co-benefits, pre- and co-actions, finance programmes, past projects |
| Per city (inputs) | AdaptaBrasil risk, finance profile |
| Per city (derived) | `city-action-order.csv` |

## API

Four endpoints. Every response field is defined in `mock-api/api-fields.csv` with a role: **order** (position and the scores behind it), **attribute** (a property of the action, such as timeline, cost band, grades, sectors and co-benefits), **identity**, or **context**.

| Endpoint | Returns |
|---|---|
| `GET /api/v1/cities/{locode}/adaptation-actions` | The ordered actions for the city: position, all scores, the risk cell where impact is highest, the action's attributes and detail counts, plus the city's finance context |
| `GET /api/v1/adaptation-actions/{action_id}` | Everything behind one action, the same for every city: its supporting actions marked `pre_action` or `co_action`, and the top 5 policy documents and past projects with their totals |
| `GET /api/v1/adaptation-actions/{action_id}/policy-documents?page=&page_size=` | All policy documents for the action, one row per document with its best passage, strongest first |
| `GET /api/v1/adaptation-actions/{action_id}/past-projects?page=&page_size=` | All past projects for the action, high matches first, then the most recent |

Everything city-specific is in the city list; the action detail and the two full lists are the same for every city. The full lists use the same order as the detail, so the detail's top 5 is always their first 5. Examples for Caxias do Sul (`BR CXL`) and for drainage (`c40_0048`) are in `mock-api/`, built by `build_mock_api.ipynb`.

## Notes on inputs

The structure is confirmed. The values in the sample are the latest we have and will change, so read the order as an example, not a result.

- **Impact** uses I Care's assessment V15. A revised version is coming.
- **Policy alignment** is a draft for all 38 actions and is under C40 review.
- **Two action IDs are provisional** (`new0001`, `new0002`) and may change.
- **Finance programmes** linked to actions are candidates, and past projects have not been reviewed.
- **Risks outside AdaptaBrasil** (sea-level rise, extreme heat) are not shown separately in this version.
- **One supporting action** (`icare_0164`, hydrological monitoring) is linked only to another supporting action (`icare_0171`), so it is not shown on any ordered action.
