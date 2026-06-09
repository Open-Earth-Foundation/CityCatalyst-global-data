# Project Drawdown — Drawdown Explorer solutions table

Dataset review entry for the **Drawdown Explorer** "Table of Solutions" export: about 156 climate solutions classified into recommendation tiers, with per-solution effectiveness, achievable adoption ranges, GHG impact ranges (Gt CO2-eq/yr), point costs (US$/tCO2e), and qualitative co-benefit tags.

This is the **2025 Explorer relaunch**, which replaced the older "Table of Solutions" (about 90 solutions, GtCO2e summed 2020–2050 under two named scenarios) that discovery records describe. The old and new products are not comparable; the old bulk data lives in the archived [ProjectDrawdown/solutions](https://github.com/ProjectDrawdown/solutions) GitHub repo and is not reviewed here.

## Canonical access

- Explorer UI: <https://drawdown.org/explorer>
- CSV export: <https://drawdown.org/explorer-solutions-table-export.csv> (linked as "Download CSV" on the Explorer page; undated, un-versioned — the export mutates in place as Drawdown fills in "Coming Soon" rows)

## License — restrictive, gates everything

**Not open data.** Site footer: "Copyright © 2014–2026 Project Drawdown. All rights reserved." The [Terms of Use](https://drawdown.org/terms-of-use) (last updated 2025-06-04, verified 2026-06-05):

- license Content for the user's "own internal, personal use" only;
- expressly prohibit "use, reproduction, modification, distribution or storage of any Content for any purpose other than using the Services ... without prior written permission";
- prohibit copying or storing "any significant portion of the Content".

Third-party descriptions claiming Creative Commons licensing refer to the pre-2025 site. **Consequences:** no production ingestion, no user-facing redistribution of values, and the full export is **not stored in this repo** — `releases/2025/data/` keeps only our derived mapping and the aggregate comparison; 10-row samples plus the re-download procedure live in `releases/2025/sample/`. Anything beyond internal evaluation needs written permission from <info@drawdown.org>. (For contrast: UNEP-CCC allows non-commercial reproduction with attribution; IPCC SPM.7 is CC BY.)

## Why we reviewed it

Candidate for need `2026-06-action-reduction-potential` (ordinal ranking of mitigation actions, TEF-mapped). Screened 2026-06-04 as `investigate` with two unknowns — bulk export and license — both resolved 2026-06-05 in this review. See `releases/2025/review.md` for the comparison against `ipcc-ar6-spm7-mitigation-potentials` and the resulting decision.

## Interpretation warnings (dataset level)

- **"GHG Impact" is not a 2030 potential.** It is effectiveness × the *achievable adoption range* — a full-deployment envelope with no target year and no cost cap. Do not treat it as comparable to SPM.7 or UNEP-CCC 2030/2035 potentials (the release review quantifies how different the rankings are).
- **Only "Highly Recommended" solutions are quantified** (55 of 156 rows at capture). "Worthwhile" / "Keep Watching" / "Not Recommended" rows carry tier labels only, and about 43 Highly Recommended rows are still "Coming Soon" — including many city-relevant ones (distributed solar PV, building envelopes, district heating, electric trucks & buses, nuclear).
- **Costs are single points**, no cost buckets, several blank (solar, both wind rows, green hydrogen) — weaker than SPM.7 for cost-aware ranking.
- **No uncertainty semantics**: the impact range reflects the adoption scenario span, not parameter uncertainty.
- The export is **un-versioned and mutates in place**; re-downloads will not reproduce this release. Quantified-row count is the cheap drift indicator.

## Current approved release

None — **research-only**; not production-approved (license). Reviewed release: `releases/2025`.
