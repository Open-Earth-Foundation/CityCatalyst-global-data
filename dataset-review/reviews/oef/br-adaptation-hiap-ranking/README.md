# OEF — Brazil adaptation HIAP ranking (br-adaptation-hiap-ranking)

The action prioritisation (HIAP) for Brazilian cities ranks the 38 adaptation actions in the ICB × OEF action bank on three pillars: **impact**, **feasibility** and **alignment**. This folder brings the inputs for each pillar together in one place, keyed on the same 38 action IDs, ranks actions by impact for each city, and combines the three pillars into an overall ranking per city.

This is an OEF derived product. Each input stays authoritative in its source review and is not changed here.

## Inputs

The cleaned model inputs are in `releases/v1/data/input/`, one file per input, written by part 1 of `hiap_ranking.ipynb` (city risk by part 2). Join them on `action_id`, never on the action name.

| Pillar | File | Grain | What it holds | Source |
| --- | --- | --- | --- | --- |
| — | `actions.csv` | action (38 rows) | The updated action list: name, description, timeline | I Care Brasil workbook *Adaptation Action Impact Assessment, ICB × OEF, V15* (7 Oct 2026), tab *Final Action Bank* |
| Impact | `impact.csv` | action × sector × component (456 rows) | Eligibility (Direct / Indirect / Out of Scope), effectiveness, confidence, maladaptation, timeline, the 0–1 component score, and the AI rationale for each | Same workbook, tab *Action x sectors assessments* |
| Impact | `adaptabrasil_risk.csv` | city × sector × risk | AdaptaBrasil overall risk, hazard, exposure and vulnerability | CityCatalyst global API, fetched by part 2 |
| Feasibility | `actions_cost.csv` | action (38 rows) | Cost components (CTI, IR, E, T), cost index (IC) and cost band | *Action Cost Calculation* (`sample/Action_Cost_Calculation.xlsx`) |
| Feasibility | `legal_assessment_summary.csv` | action (38 rows) | Legal feasibility score (1–5) and grade | *Legal feasibility score profiles* (`sample/legal-feasibility-score-profiles_2.xlsx`, Oct 2026), tab *Summary* |
| Feasibility | `legal_assessment_complete.csv` | action × law (230 rows) | Every federal law behind the legal score: authority and competence grades, type, description, validation and link | Same workbook, one tab per action and *norm_database* |
| Alignment | `policy_alignment.csv` | action (38 rows) | Policy alignment grade and 0–1 score, document support, and the deciding policy passage | `reviews/br-federal-government/br-climate-policy-documents/releases/v2/data/results.csv` |

`data/mapping/` links the earlier model to this one: its actions, its test-city ranking and its risk structure (see *Comparison with the earlier model*). Results go to `data/output/`.

### Impact

Only **Direct** links get a component score (54 of 456). The score is `effectiveness^0.5 × confidence^0.25 × timeline^0.2 × maladaptation^0.05`. The notebook recalculates it and checks it against the workbook. Indirect and Out of Scope rows have no score.

The city step is part 2 of the notebook (see below).

`human_reviewed` marks the 44 rows where a reviewer confirmed or changed a value. All other values are AI output dated 6 Oct 2026.

### Feasibility

Feasibility has two parts: cost and legal feasibility.

**Cost.** Each action is scored on four components, CTI, IR, E and T, which give a cost index `IC = round((CTI + IR) ÷ 2 + E + T)` from 3 to 8: 3–4 low, 5–6 medium, 7–8 high. The cost workbook does not say what the four components stand for. The notebook recalculates the index and band, and checks the bands match the V15 action bank (they do for all 38).

Cost is the only finance field used to rank, as agreed with partners in September 2026. Other finance information stays in `reviews/oef/br-city-finance-feasibility` as context for cities and project preparation.

Cost does not come from `br-city-finance-feasibility` v2. That release uses the older V13 action bank, which has no `icare_0181` and a different cost band for 20 of the other 37 actions. It needs updating to V15.

**Legal feasibility.** A score from 1 to 5 for how much authority a municipality has to carry out the action, and its competence to make rules about it, under Brazilian federal law. Each action lists the federal laws that apply (4 to 8 each, 52 laws in all). Each law is graded for *authority* (total 1, partial 0.5) and *competence* (exclusive 1, supplementary 0.66, concurrent/private 0.33). Each grade is averaged over the action's laws and stretched to 1–5, and the score is the mean of the two. Scores run from 2.8 to 4.8: 15 actions are *Feasible*, 21 *Feasible with adjustments* and 2 *Feasible with heavy adjustments*. All laws are marked as checked by a person.

The notebook recalculates the score from the laws. It matches the workbook exactly, but the workbook formula differs from the method in two places, and the ranking uses the score as delivered until they are confirmed:

- It looks for partial authority under the Portuguese `parcial`, but the laws are tagged `partial`, so partial authority counts as 0, not 0.5. This affects 23 actions.
- It subtracts 0.33 from the competence total rather than the average, so an action whose laws are all concurrent/private scores about 2.2 instead of 1, and the result shifts with the number of laws.

Correcting both would change 33 of the 38 scores, mostly by 0.1 to 0.4 (rank correlation with the delivered scores 0.92).

### Alignment

The grades are provisional. They are drafts from policy alignment v2, and no rows have been reviewed yet: 26 Strong, 10 Medium, 2 Weak. Policy alignment v2 also has not been committed yet.

## City impact ranking

Part 2 of the notebook follows steps 5–10 of the workbook's *Formulas* tab. For each city it multiplies an action's sector score by the city's overall AdaptaBrasil risk, weighted towards whichever of vulnerability and exposure the action targets. It keeps each action's best risk and ranks the actions within the city.

City risk comes from the CityCatalyst global API rather than the workbook: `/api/v1/cities/search` finds the city's locode, and `/api/v1/cities/{locode}/climate-risk/adapta` returns its AdaptaBrasil risk by sector and risk. This means any Brazilian municipality can be ranked, not only the workbook's five test cities. Add cities to `CITIES` at the top of the notebook.

The five test cities are the check: their ranks must match the workbook's *Municipal Impact Rank* exactly (190 city × action results). Spot checks of Caxias do Sul and Itaubal show the API serves the same values as the workbook.

The API response is saved to `data/input/adaptabrasil_risk.csv` (one row per city, sector and risk), and the ranking to `data/output/city_ranking.csv`. The current file holds the five test cities taken from the V15 workbook's *City risk indices* tab (the same values the API serves; no time frame is recorded). Delete it to fetch from the API again.

## Overall ranking

Part 3 of the notebook writes `br_adaptation_hiap_ranking.xlsx`. For each city and action:

**overall score = impact × 55% + feasibility × 22.5% + alignment × 22.5%**

**feasibility = cost × 50% + legal × 50%**

All pillars are on a 0–1 scale. Impact is the city's normalised impact score (the top action in the city scores 1). Cost comes from cost band, on the methodology scale: low 0.6, medium 0.5, high 0.4 (medium is neutral, the same value used when cost is missing; the scale is for review in pilot testing). Legal is the legal feasibility score rescaled from 1–5 to 0–1. Alignment is the policy alignment score. Only impact varies by city.

Actions with no impact score get no rank, as in the I Care workbook. Ties share a rank (1, 1, 2).

The workbook calculates everything in formulas. Change the weights, the cost/legal split, the cost-band scores or the impact rule on its *Settings* tab, and every score and rank updates. Tabs: *Overall ranking* (each action's rank in each city, best and mean rank), *City scores* (the calculation), then the detail behind each pillar: *Impact*, *Impact assessment*, *Feasibility*, *Legal basis* (the laws behind each legal score), *Alignment*.

Check run on the file: at the default weights every rank matches the notebook's own calculation.

With the methodology cost scale (0.6 / 0.5 / 0.4), cost only nudges the ranking: at the default weights one cost band is worth about 0.02 of impact. Legal feasibility (2.8 to 4.8, rescaled to 0.45 to 0.95) now separates actions more than cost does. Splitting feasibility 50/50 between cost and legal, rather than using cost alone, moves the median action 1 place, and each city keeps 9 or 10 of its top 10; actions with high legal scores, such as shelters (`c40_0049`), rise most.

## Comparison with the earlier model

The earlier HIAP model ranked 44 older adaptation actions for all 5,569 municipalities and exported each city's top 20 (`sample/hiap_actions_extract_2026-10-12.csv`, gitignored). Part 4 of the notebook compares it with the new ranking.

Action IDs alone can't link the two lists: original actions were merged, split, or kept their ID but changed scope. `data/mapping/previous_to_updated_actions.csv` takes the 53 original adaptation actions (ID, name and description, from the original action bank export `sample/original_actions.json`) and maps each to the updated list as *same* (17), *revised* (19), *replaced* (16), *split* (2 extra rows) or *no successor* (1, the firefighting brigade), with a confidence and a note. Two updated actions, `new0001` and `new0002`, are *new*. **It is a draft for review**; the least certain row is `icare_0188` (pollution-related health surveillance) → `ipcc_0094`, with `icare_0185` as the alternative.

Each city's old top 20 is translated through the crosswalk and compared with the new top 20, both overall and impact-only. The notebook reports how much of the top 10 and top 20 is shared, which actions entered or left (and why), and how far shared actions moved. Output: `data/output/comparison_earlier_model.csv`.

Five cities are a thin basis. Add more to `CITIES` and rerun the notebook to widen the comparison.

`data/mapping/previous_ranking_test_cities.csv` holds the earlier model's top 20 for the five test cities, one row per original action, with the updated action it maps to and `remapped_rank`: the earlier ranking expressed in updated actions (several originals merging into one take the best rank).

### Risk structure

The earlier model used the CCRA risk assessment (`/api/v0/ccra/risk_assessment/city/{locode}/{scenario}` on the CityCatalyst global API), which scores 15 *impact area × hazard* pairs (for example *public health × floods*). The new model uses AdaptaBrasil's 12 *sector × risk* cells (for example *Geohydrological disasters × Floods, flash floods and waterlogging*).

- `data/mapping/previous_risk_ccra_test_cities.csv`: the CCRA results for the five test cities, fetched 14 Oct 2026 (357 rows). *Current* (2024) has risk, hazard, exposure and vulnerability scores. *Optimistic* and *pessimistic* (2030 and 2050) only have hazard scores; their risk, exposure and vulnerability are 0. The API spells the scenario `pesimistic`; the file uses `pessimistic`. Adaptive capacity and sensitivity are empty everywhere and are left out.
- `data/mapping/previous_to_updated_risks.csv`: maps each CCRA pair to the AdaptaBrasil risk it corresponds to, as *close*, *partial* or *no match*, with a confidence and a note. Floods, landslides, diseases and water stress match closely (CCRA's single disease risk splits into four AdaptaBrasil diseases). Heat-health, heat on infrastructure and sea-level rise have no AdaptaBrasil counterpart, so the new model cannot see them. **It is a draft for review.**

For the five test cities, the two models share 2–4 of their top 10 actions and 9–12 of their top 20. Most of the difference comes from two places: planning, monitoring and regulatory actions that the old model ranked highly now have no impact score and drop out, and actions the old export never ranked (the two new actions, and originals such as shelters and coastal protection) enter. Impact-only overlap is just as low, so the change comes from the impact method, not the pillar weights.

### Actions cities picked

`data/mapping/previous_city_selections.csv` holds the adaptation actions cities picked in the earlier model (3 per city, 35 cities, 105 rows), from a CityCatalyst export of 15 Oct 2026: the original action ID and English name, its earlier rank, and whether it was picked from the earlier ranking (`ranked`) or from outside its top 20 (`unranked`). Ranked picks match the earlier export's ranks. Four picked IDs (`icare_0149`, `icare_0151`, `icare_0155`, `icare_0161`) are not in the original action bank and have no name; they need checking. Of the five test cities only Caxias do Sul and Sobral appear.

## Open points

- Nine actions have no Direct link, so they get no impact score and cannot be ranked. All are monitoring, planning or regulatory actions.
- Impact scores are close together: 32 of 54 fall between 0.59 and 0.66. How the pillars are weighted will matter a lot.
- Should timeline count under impact, as it does in the workbook, or under feasibility?
- The legal feasibility formula needs confirming with its author (see Feasibility above). The 50/50 split between cost and legal is a proposal.

## Structure

```
br-adaptation-hiap-ranking/
├── README.md
└── releases/v1/
    ├── hiap_ranking.ipynb      the whole model: 1 inputs, 2 city impact, 3 overall ranking and workbook, 4 earlier model
    ├── br_adaptation_hiap_ranking.xlsx   overall ranking with weights you can change
    ├── data/
    │   ├── input/            cleaned model inputs (see Inputs)
    │   │   ├── actions.csv
    │   │   ├── impact.csv
    │   │   ├── adaptabrasil_risk.csv           from the API (part 2); test cities currently from the V15 workbook
    │   │   ├── actions_cost.csv
    │   │   ├── legal_assessment_summary.csv
    │   │   ├── legal_assessment_complete.csv
    │   │   └── policy_alignment.csv
    │   ├── mapping/            the earlier model, linked to this one
    │   │   ├── previous_to_updated_actions.csv   original adaptation actions → updated actions (draft for review)
    │   │   ├── previous_ranking_test_cities.csv  earlier top 20 per test city, remapped to updated actions
    │   │   ├── previous_risk_ccra_test_cities.csv  earlier risk structure (CCRA API) for the test cities
    │   │   ├── previous_to_updated_risks.csv     CCRA impact × hazard → AdaptaBrasil sector × risk (draft for review)
    │   │   └── previous_city_selections.csv      adaptation actions cities picked in the earlier model
    │   └── output/
    │       ├── city_ranking.csv                part 2
    │       ├── overall_ranking.csv             part 3, default weights
    │       └── comparison_earlier_model.csv    part 4
    └── sample/           source workbooks (V15, cost, legal), the original action bank and the earlier model export (gitignored)
```

Run `hiap_ranking.ipynb` from `releases/v1/`. It needs `pandas` and `openpyxl`, the files in `sample/`, the policy alignment v2 results, and internet access to the CityCatalyst global API for cities not yet in `data/input/adaptabrasil_risk.csv`. Default weights, splits and cities are set at the top.

## Licence

This product inherits the most restrictive licence of its inputs and grants no new rights. The impact workbook is an I Care Brasil working file for the project and must not be redistributed. Alignment draws on Brazilian federal policy documents; see that review for their reuse terms.

## Status

Research. The inputs are not production-approved, the alignment grades are unreviewed drafts, and the weights, cost/legal split and cost-band scores are proposals. The legal feasibility formula is unconfirmed.
