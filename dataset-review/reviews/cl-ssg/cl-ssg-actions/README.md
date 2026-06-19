# Chile SSG consolidated climate actions (cl-ssg-actions)

A de-duplicated menu of **196 candidate mitigation actions** assembled for the Chile SSG / MEED programme by merging two libraries: an OpenEarth set (`OE`, 102 rows, drawn from the IPCC, I-Care and C40 taxonomies) and a Sustainability Solutions Group set (`SSG`, 94 rows). The action *content* is generic and globally worded; the "Chile" in the name is the curation context, not the wording, which names no Chilean place, programme, or policy. This is the "what could a city do" layer — not an inventory, reduction-potential estimate, or finance source (those are the sibling reviews `cl-ssg-emissions`, the `2026-06-action-reduction-potential` need, and `cl-ssg-finance`). It pairs naturally with `cl-ssg-finance`, which scores how fundable each action is.

## Canonical sources

Internal curated working data, not a published dataset with a DOI. Assembled inside the SSG / OpenEarth workstream and supplied as a single spreadsheet, `consolidated_climate_actions_database.xlsx` (one sheet), dropped into `sample/` by Amanda, 2026-06. The two libraries are themselves derived: `OE` rows carry upstream ids (`source_original_id`) tracing to the IPCC (36), I-Care (49) and C40 (17); `SSG` rows carry none. The merge's own build record (who matched what, when, with what tool) is **unanswered** in the file.

## Access

Manual hand-off, no API or feed. The file is small (196 rows, ~0.3 MB as CSV), so the cleaned derivative is committed to `data/` and the raw export sits in `sample/`. To refresh: drop a newer export into `sample/`, re-run `releases/v1/extract_clean.ipynb` (restart-and-run-all), commit the regenerated `data/`.

## License

**Decided here, not verified** — no licence statement travels with the file. The merged table is internal working product of the SSG / OpenEarth programme, usable within it; treating it as openly redistributable is not supported by anything in the file. Upstream content keeps its own terms (IPCC reusable with attribution; C40 and I-Care have their own conditions), so redistribution outside the programme should clear those rather than rely on this entry. There is no personal data, so data-protection rules do not bite.

## Spatial and temporal scope

There is **no spatial or temporal dimension at all** — no country, region, comuna, coordinate, year, or date. Every action is a timeless, place-less measure, and `implementation_timeline` is a duration band ("<5 years"), not a calendar date. A keyword scan for Chilean terms matched at most one row. So Chile relevance is purely contextual: this is the set a Chile-facing programme curated, but the actions transfer to any city. Frozen-vs-updated status is **unanswered** (no version marker), so v1 is treated as a frozen snapshot of the 2026-06 export.

## Interpretation warnings

The thing that silently bites every downstream use is that **this is two datasets stacked in one shape, and almost every attribute column belongs to only one source.** The merge aligned row identity and classification, but not the descriptive attributes, so a blank cell usually means "not collected for that source", not "this action lacks that property". This table is the load-bearing fact of the review:

| Attribute | `OE` (102) | `SSG` (94) |
|---|---|---|
| Spanish name / description | present | absent |
| `implementation_timeline`, `investment_cost`, `kpis`, `dependencies` | present | absent |
| `priority_or_paradigm` (Avoid/Reduce/Replace) | absent | present (90) |
| `source_original_id` (upstream trace) | present | absent |
| `match_status` cross-link | present on 34 | links point *into* SSG |

The consequence: filtering the whole table on `investment_cost` silently drops every `SSG` action; ranking on `priority_or_paradigm` silently drops every `OE` action. Cross-source work is honest only on the fields populated for both — name and sector.

Three smaller traps. `primary_purpose` is **entirely empty** (a dead column). `action_type` is **uniformly "mitigation"** (no adaptation, no information). And the 196 rows are **already cross-source de-duplicated**, not a raw union: the 34 `Match` rows name SSG actions that were folded into the `OE` row and *excluded* from the file (none of the 34 matched names appears among the 94 SSG rows), so the `OE` row is the surviving master for those concepts. Treat the 196 as a de-duplicated master list with the dedup done on the OE side; a fuzzy re-scan finds only a few weak residual look-alikes (see the mapping notebook). Note also that `priority_or_paradigm` is multi-valued ("2. Reduce,3. Replace (or switch)") and its leading "1."–"5." is an ordinal label, not a quantity.

## Parsing notes

The main hazard is **embedded newlines inside cells**: `kpis`, `dependencies` and many descriptions contain literal line breaks, so the raw CSV is ~1,178 physical lines for 196 records. Read it with a quoted-field parser (`pandas.read_csv`), never line-by-line. Beyond that: one sheet with a clean header row; `consolidated_id` (`CONS_0001` …) is unique and the safe key; `sector_names`/`subsector_names` are single-valued GPC-style slugs and the only classification populated for both sources; `matched_action_names_from_other_database` is multi-valued on " | " (not comma); and some names carry trailing spaces and source-side typos, so strip whitespace and join on `consolidated_id`, never on names.

## How this was produced

`releases/v1/extract_clean.ipynb` (load → clean → validate → export → visualise) reads with a quoted-field parser, trims whitespace, normalises the two multi-valued fields, drops the dead `primary_purpose` and constant `action_type`, and asserts the structural facts (196 unique ids, the 102/94 split, 34 matches, the per-source attribute pattern) before exporting. Single committed output: `data/cl_ssg_actions_consolidated.csv`. Charts render inline in the notebook; precise aggregates are tabled in `review.md`.

## Alignment to `modelled.action_pathway`

The `OE` half (sourced from c40/icare/ipcc) is **already in `modelled.action_pathway`** via the `action_pathways_to_modelled` Mage pipeline, so this review adds only the **94 SSG actions** to that model. The mapping notebook `releases/v1/ssg_action_pathway_mapping.ipynb` produces two crosswalks in `data/`: `cl_ssg_actions_pathway.csv` (the 94 SSG rows in `action_pathway` column shape — `publisher_id='ssg'`, `name_i18n`/`description_i18n` as `{"en","es","pt"}` JSON with EN-only content, `action_type='mitigation'`) and `cl_ssg_action_equivalence.csv` (which SSG concepts relate to loaded actions). Because the file is already de-duplicated, the 94 are 94 **new master records**: a `publisher_id` filter returns a unique per-source list, and the cross-source master list is the loaded OE rows plus these 94. Mapping gaps to know: `priority_or_paradigm` has no target column; `intervention_type`, `investment_cost`, `implementation_timeline` and the `*_summary_i18n` fields are null for SSG (not collected); `subsector_number`/`gpc_reference_number` need a sector→GPC crosswalk (deferred); and `generation_method='expert_reviewed'` plus `action_role='pathway'` are drafted defaults pending confirmation.

## Relationship to other datasets

- **`cl-ssg/cl-ssg-finance`**: the funding side; this menu is the demand side its fundability scoring consumes. Pair conceptually on the action (no shared key).
- **`cl-ssg/cl-ssg-emissions`** and the **`2026-06-action-reduction-potential`** need: the missing quantitative layers. This menu carries **no tCO2e, no reduction potential, no cost figure** (only low/med/high), so abatement ranking needs an external source.
- **Upstream taxonomies** (IPCC, C40, I-Care; the SSG transition-element menu): this is a merge of those, so it overlaps them by construction.

## Current approved release

Not promoted (research). First release **v1**: `extract_clean.ipynb`, `ssg_action_pathway_mapping.ipynb`, the cleaned `data/cl_ssg_actions_consolidated.csv` (196 rows), the mapping crosswalks `data/cl_ssg_actions_pathway.csv` (94 SSG rows) and `data/cl_ssg_action_equivalence.csv`, and `review.md`. Not yet entered in `catalog/index.yaml` (promotion is a separate, user-approved step). Evidence tags: structure, coverage, the source asymmetry, the dead/constant columns, the already-deduplicated nature, and the embedded-newline quirk are **verified** (asserted in the notebooks); the generic-not-Chile reading is **verified** (keyword scan plus name inspection); the candidate-duplicate links and the drafted `generation_method`/`action_role` defaults are **inferred / pending adjudication**; licence and merge provenance are **decided / unanswered**.
