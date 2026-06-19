# Review — cl-ssg-actions, release v1

## Scope and status

Research, not production-approved, and not yet in the catalog. The release holds the consolidated SSG / OpenEarth action menu as one tidy table (`data/cl_ssg_actions_consolidated.csv`, 196 actions) produced by `extract_clean.ipynb`, plus a mapping into `modelled.action_pathway` produced by `ssg_action_pathway_mapping.ipynb`: `data/cl_ssg_actions_pathway.csv` (the 94 SSG actions in `action_pathway` column shape) and `data/cl_ssg_action_equivalence.csv` (synonym and candidate-duplicate links to loaded actions). A sector→GPC (`subsector_number`/`gpc_reference_number`) crosswalk is deferred.

## Visual summary

The menu is dominated by **stationary energy** (64 of 196), with a long tail across AFOLU, IPPU and transportation (32–36 each) and smaller sets for waste, water and scope-3. By origin it is roughly even: 102 `OE`, 94 `SSG`. The Avoid-Reduce-Replace tags (SSG only) lean to Reduce and Replace, with Avoid a distant third. The most important chart is **attribute coverage**: cost, timeline, KPIs and Spanish text populated only for `OE`, priority only for `SSG` — the asymmetry that governs every cross-source use. Run the notebook for the rendered charts.

## What this data supports

Claims are mostly about *coverage of the action space* and *coarse, source-scoped attributes*; the load-bearing caveat is that an attribute claim is valid only within the source that populated it.

Across both sources it supports coverage claims keyed on name and sector: "the menu offers 196 candidate mitigation actions spanning all GPC mitigation sectors, concentrated in stationary energy (64)". Within `OE` it supports coarse-band attribute claims: "34 of the 102 OpenEarth actions are tagged high investment cost; 53 sit in a 5-to-10-year window", plus the bilingual claim that Spanish names exist for all 102. Within `SSG` it supports priority-framing claims: "43 of the 94 SSG actions are Reduce-type and 37 are Replace-type". And it supports a modest overlap claim: 34 `OE` actions are flagged as also present in the SSG menu.

## What this data does not support

The overclaim to watch for is reading a blank cell as a fact about the action rather than about which source collected the attribute, and treating this menu as quantitative or Chile-specific.

It does not support a cost claim for any `SSG` action or an Avoid-Reduce-Replace claim for any `OE` action — those attributes exist only on the other half, so a filter on either silently drops 94 or 102 rows. It supports no tCO2e, reduction-potential, or $/tCO2e statement (there is no impact field, only a low/med/high band for half the rows). It supports no spatial or temporal claim (no geography or date column; timeline is a duration band). And despite the name it does not support "these are Chile-specific actions" — the wording is generic and transfers to any city.

## Mapping to action_pathway and de-duplication

This release maps the **94 SSG actions** into the `modelled.action_pathway` column shape; the `OE` half (c40/icare/ipcc) is already loaded there by the `action_pathways_to_modelled` pipeline, so it is not re-loaded. The mapping supports the claim "the 94 SSG actions are 94 new master records in `action_pathway` under `publisher_id='ssg'`". It supports "filtering `action_pathway` by `publisher_id` returns a unique per-source list, and the cross-source master list is the loaded OE rows plus these 94" — because the source is already cross-source de-duplicated (the 34 `Match` rows name SSG twins that were folded into the OE rows and excluded, none present among the 94).

It does **not** support "every SSG action is confirmed distinct from every loaded action": a name-similarity re-scan drafted one medium and about thirteen low-confidence look-alikes (e.g. SSG "Retrofit non-residential buildings" against loaded "Retrofit residential buildings"), recorded as `candidate_duplicate` rows for adjudication, not applied. It does not support intra-SSG dedup by name either — the closest SSG pairs are distinct by design (domestic-water vs space heating; corporate vs personal vs commercial vehicles), so any further collapse needs curated judgement. And the mapping is **lossy in known ways**: `priority_or_paradigm` has no target column; `intervention_type`/`investment_cost`/`implementation_timeline`/`*_summary_i18n` are null for SSG; `subsector_number`/`gpc_reference_number` await a sector→GPC crosswalk; `generation_method='expert_reviewed'` and `action_role='pathway'` are drafted defaults pending sign-off.

## Using it downstream

Treat the rows as candidate-distinct actions keyed on `consolidated_id` (or `src_action_id` in the mapped table), never on names (trailing spaces, typos). Before using any attribute, check it exists for your source: cost, timeline, KPIs, dependencies and Spanish text are `OE`-only; priority is `SSG`-only; sector, subsector and English name are the only cross-source fields. Split multi-valued fields first (`priority_or_paradigm` on comma, `matched_action_names_from_other_database` on " | "). Pair with **`cl-ssg-finance`** for fundability (join conceptually on the action). For abatement potential, this is the demand-side list only; the potential must come from an external source.

## Notes on non-obvious fields

`is_matched` (added in cleaning) is true only for the 34 `OE` rows linked into the SSG menu; false means "not matched", not "verified unique". `match_status` and `matched_action_names_from_other_database` sit only on `OE` rows and point *into* SSG action names. `priority_or_paradigm` ("1. Avoid" … "5. Offset", plus "Not recommended") is an ordinal label, not a quantity. `implementation_timeline` is a duration band, not a date. `primary_purpose` and `action_type` were dropped from the tidy output (empty and constant in source).

## Traceability

Produced from a single internal export with no DOI; `OE` row lineage is in `source_original_id` (IPCC, C40, I-Care). The merge's build record is not in the file (open provenance gap, noted in the README). All structural claims here are asserted in the notebook and pass on restart-and-run-all.

### References

- Cleaning notebook → `extract_clean.ipynb`
- Mapping notebook → `ssg_action_pathway_mapping.ipynb`
- Tidy output → `data/cl_ssg_actions_consolidated.csv`
- action_pathway-shaped SSG rows → `data/cl_ssg_actions_pathway.csv`
- Equivalence crosswalk → `data/cl_ssg_action_equivalence.csv`
- Target model / pipeline → `cc-mage/pipelines/action_pathways_to_modelled`
- Dataset-level provenance, licence, parsing → `../../README.md`
- Funding companion → `reviews/cl-ssg/cl-ssg-finance`
- Reduction-potential need → `dataset-discovery/needs/2026-06-action-reduction-potential`
