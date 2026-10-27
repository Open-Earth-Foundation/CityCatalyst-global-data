# Mapping method — dataset units → target taxonomy

(Method reference for the skill. The release-facing document that captures
what the mapped data can support is `review.md` — see
`references/review-template.md`.)

Output: a crosswalk csv in the release `data/`, produced by a dedicated
notebook at the release root. Worked example:
`reviews/ipcc/ipcc-ar6-spm7-mitigation-potentials/releases/2023/spm7a_tef_mapping.ipynb`
→ `data/spm7a_option_to_tef.csv`.

A release can carry **multiple mappings to different targets** (e.g. SPM.7
maps to both TEF elements and the city action list). Each is its own
notebook + csv; the principles below are invariant across targets.

## House schema

When the target is TEF, match the existing `action_to_tef_*.csv` files
exactly:

```
src_action_id, publisher_id, action_name, action_type, action_role,
stable_id, short_label, sector_path, mapping_confidence, rationale
```

For other targets, adapt analogously (source id/name columns, target
id/name/classifier columns, then `mapping_confidence, rationale` — see
`spm7a_option_to_action.csv` for a worked non-TEF example). The invariants
are the row semantics, not the column names.

- Many-to-many: one row per (source unit, target element) pair.
- `mapping_confidence`: high | medium | none. `none` rows are kept with
  empty target fields and a rationale — they are the record that mapping
  was considered and found impossible, and they stop re-investigation.
- `rationale`: one line, written for the next person who questions the row.

## Principles

1. **Link, don't attribute.** Quantities (potentials, emissions, costs)
   stay at the source unit's granularity. Never split a value across
   mapped targets — fan-out would double-count and invent precision.
   Targets inherit pointers and tiers, not numbers.
2. **Check for existing bridges first.** The repo often already has partial
   crosswalks (e.g. TEF elements carry `ipcc_ref` compendium codes; source
   files sometimes embed their own category crosswalk sheets). Use them
   before inventing matches.
3. **Curated table over fuzzy matching.** The mapping lives in the notebook
   as an explicit, readable list (option → target codes, confidence,
   rationale). Pattern rules are allowed for genuine families of
   near-identical targets (e.g. "Retrofitting ..." across building types)
   but every pattern expansion is printed for audit.
4. **Draft-then-adjudicate.** The agent drafts all rows with confidence
   tags; the human reviews mediums/lows and the none-list. At scale (>~20
   judgment rows), present **judgment clusters** — the recurring patterns
   behind groups of rows — rather than row-by-row lists; the human decides
   each pattern once. Record the adjudication date and person in the
   notebook findings.
5. **Instruments are medium by convention.** Policy levers *toward* an
   option (certification, procurement rules, EPR, pricing, urban form) are
   not the option itself — tag them medium with a rationale saying so, or
   exclude them; decide once per mapping and state the choice.
5. **Validate before export:** every source unit appears (mapped or none),
   every target code resolves to an active catalog entry, no duplicate
   pairs. Print coverage stats (units mapped, distinct targets referenced).
6. **Mind licensing of the target catalog.** If the taxonomy export is
   gitignored/local-only (e.g. TEF, license pending), the mapping csv may
   reference stable ids, but the notebook must note the dependency and
   point to re-export instructions.

## What coverage means

Low mapped-coverage is a finding, not a failure — analyze *which* units
don't map and why. (SPM.7 → TEF: the unmapped set was almost exactly the
non-city-actionable options, so the taxonomy's gaps acted as a relevance
filter. That insight went into the README.)

**Coverage is a property of the target taxonomy, not the dataset.** The
same 31 SPM.7 options mapped 19/31 to TEF but 25/31 to the action list,
and the top potential band reached 4 TEs vs 16 actions — because the
targets differ in what they contain. Never conclude "this dataset covers
little" from one mapping; compare targets.

Report coverage **in both directions**: source units mapped/unmapped AND
target entries reached/unreached. The unreached-target list is its own
finding (e.g. grid/T&D actions get no evidence because the source has no
transmission option) and belongs in review.md so nobody misreads absence
of evidence as evidence of weakness.
