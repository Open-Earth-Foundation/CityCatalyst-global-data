# Brazil adaptation module: v2

> The data, ordering and mock API behind the Brazil adaptation module, built from the consolidated action bank (12 Nov 2026). It replaces the v1 ranking with a default order per city that the city filters.

`technical-handover-explained.md` sets out the requirements for the team building the module.

## Files

| File | What it is |
|---|---|
| `technical-handover-explained.md` | Technical handover: requirements, ordering, API, comparison with hiap-meed |
| `build_sample_data.ipynb` | Refreshes the input tables from the consolidated workbook, lists every change, and builds `city-action-order.csv` |
| `city-action-order.csv` | The default order of actions for the five test cities |
| `mock-api/` | Example API responses (city list for Caxias do Sul; action detail and its two full lists for `c40_0048`), `build_mock_api.ipynb` that builds them, and `api-fields.csv`, which defines every response field |

The mock responses show every field with real values. Both notebooks read the workbook and input tables from `sample/`.

## How the nearest existing tables map

| File | Existing table in `modelled` | Main difference |
|---|---|---|
| `adaptation-action.csv` | `action_pathway` | `action_name_en/pt` and `description_en/pt` become the `_i18n` JSON columns |
| `actions-impact.csv` | `action_pathway_mitigation_impact` | Adaptation impact is a link to a sector and component with four graded factors, not a metric value |
| `actions-legal-feasibility.csv`, `actions-legal-norms.csv` | `action_legal_assessement` | Brazil scores authority and competence per norm; Chile stores verdict, ownership and restrictions |
| `actions-policy-alignment.csv`, `actions-policy-evidence.csv` | `action_policy_signals` | The grade and score are worked out before loading, so they need an action-level row |
| `actions-projects.csv` | `finance_project` + `finance_project_action` | Kept as one file because almost every project links to a single action |
| `finance-programs.csv`, `actions-finance-programs.csv` | `finance_opportunity` + `finance_opportunity_action` | Programmes are described by source, channel, instrument and recipient |
| `actions-relations.csv` | none | New |
| `city-action-order.csv` | none | New: city × action with a Direct link, 145 rows |

The existing tables use `src_action_id`. These files use `action_id`.

## Notes on single files

- **Impact.** Only Direct links have a `component_score` (54 of 456). Nine actions have no Direct link and so no impact score; they are the supporting actions. The city impact score is recalculated with the methodology formula and matches I Care's results in the workbook for all five cities.
- **Cost.** The index is the sum of five graded components divided by 3: technical or institutional complexity (1 to 3), resource intensity (1 to 3), spatial scale (1 local, 2 whole municipality), maintenance (0 occasional, 1 constant) and implementation time. The source workbook calls them CTI, IR, E, M and T.
- **Co-benefits.** `score` is final (C40 where given, else I Care). `reviewer_notes` says which, and what C40 changed.
- **Relations.** A row means `related_action_id` is a pre-action (comes first) or co-action (goes with it) of `action_id`. Some pairs are listed as both. This is how supporting actions reach the city: on the actions they are linked to.
- **Programmes linked to actions.** An action is linked to a programme when a plan row graded Strong or Medium for that action names the programme, mostly in the plan's funding-source column. 30 actions get at least one programme.
- **City finance profile.** `credit_screen` is the code from the CAPAG review. The preparation capacity score follows section 5.2.3.1: ten MUNIC checks, 11 points at most, with a national median of 5. A check the city did not answer counts as 0.
- **City risk.** Energy availability has an overall index only, so hazard, exposure and vulnerability are blank for it, and it is left out of impact.
- **City action order.** Only the 29 actions with a Direct link are in it; the 9 supporting actions are not ordered. An action with a Direct link to no risk scored for the city has no `position` or `overall_score` (none in the test cities). Equal scores share a position. All scores are 0 to 1.
