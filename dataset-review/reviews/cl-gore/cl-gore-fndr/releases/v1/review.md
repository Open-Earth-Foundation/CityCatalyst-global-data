# Review — cl-gore-fndr, release v1

## Scope and status

Research release (not production-approved). The **regional tier** for need `2026-06-cl-finance-opportunities`: FNDR instruments delivered by the 16 Gobiernos Regionales — FNDR investment (Glosa 03 / SNI), FRIL, the 8% activity subvención (Medio Ambiente line), and FRPD. Hand-curated at instrument level from SUBDERE + representative GORE pages, captured 2026-06-08 (see "Extraction & refresh" in the README). Output: `data/cl_gore_fndr_programs_v1.csv` (4 rows). Dataset-level facts in the README one level up.

## What this data supports

- "A Chilean municipality can fund minor local infrastructure through its Gobierno Regional's FRIL (projects up to ~CLP 180M)." — supported; `eligible_actor=municipality`, `specificity=broad`.
- "Regional governments fund infrastructure broadly through the FNDR (the main regional investment channel), via the national investment system (SNI/RS)." — supported; `access_pathway` notes the SNI route.
- "Each region runs an annual 8% subvención with an environmental-protection/education line that NGOs can apply to (up to ~CLP 30M, 6-month activities)." — supported; `recurrence=annual`, `climate_relevance=explicit`, actor = NGOs.

## What this data does not support

- "These are climate funds." — mostly NO. FNDR/FRIL/FRPD are general regional/municipal investment (`climate-adjacent`); only the 8% Medio Ambiente line is explicit, and it funds activities, not capital works.
- "A single amount/date applies." — NO. Delivery is per-region (16 GOREs); the figures are illustrative — confirm with the specific Gobierno Regional.
- "A municipality can apply to the 8% Medio Ambiente line." — NO. That line's applicants are NGOs/non-profits, not municipalities.
- "FNDR investment is a quick application." — NO. It requires SNI evaluation and an RS recommendation; real lead time.
- "FRIL/FNDR are strong action-specific fundability signals." — NO. They are `specificity=broad` and capped at Moderate in scoring; they raise baseline fundability but do not indicate a tailored fit.

## Using it downstream

- In the fundability score these behave like the SUBDERE broad funds: they add Moderate matches across almost any municipal action (lifting baseline coverage, esp. for sectors with no dedicated national fund), but cannot produce Strong matches (capped at Moderate). So adding GORE/FNDR widens coverage but does **not** lift transport/industry actions to High — that still needs a sector-specific (e.g. transport) fund.
- The 8% Medio Ambiente line is the only sector-specific row, but its NGO actor means it is a Moderate (not Strong) match for a city action.
- Pairs with `cl-subdere` (national municipal infra) — together they are the broad-fund backbone; keep both flagged `broad` so scoring down-weights them jointly.

## Notes on non-obvious fields

- `specificity=broad` on 3 of 4 rows — the scoring control; these match across sectors and are capped at Moderate.
- `recurrence` reflects the budget cycle (FNDR/FRIL annual/ongoing) or the 8% annual call; not a cycle-count derivation.
- `detail_level=index` (FRPD) — region-dependent specifics pending.
- One row = 16 regional variants; treat amounts as illustrative.

## Traceability

Sources (captured 2026-06-08): SUBDERE FNDR Glosa 03; GORE pages (gobiernosantiago.cl/fndr, goremaule.cl FNDR 8% 2026, gorearica FRPD 2026 ficha). Extraction prompt + refresh steps are in the README ("Extraction & refresh"); the committed `data/` CSV is the snapshot (the same prompt also runs in the OEF harness). To deepen: harvest the 16 GORE sites for per-region amounts/dates; the 8% is the most standardised across regions.
