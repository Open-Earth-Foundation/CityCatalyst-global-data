# Review — Project Drawdown Explorer solutions table, release 2025

What this release's data can and cannot support. Dataset-level facts (license, provenance, access) live in the review README one level up.

## Scope and status

- **Full data not stored** — license (see README and `sample/README.md` for re-download instructions). The review was performed on the full 2026-06-05 capture: 156 solution-action rows, 17 columns; cleaned/typed to `status` (`quantified` 55 / `tier_only` 45 / `coming_soon` 56) with data-quality `flags`. All 55 quantified rows are "Highly Recommended"; no other tier has numbers.
- `sample/` — 10-row illustrative samples of the raw export and the cleaned version, plus re-download notes.
- `data/drawdown_spm7_crosswalk.csv` — 54 quantified solutions mapped to SPM.7 options (Clean Cooking has no SPM.7 counterpart). Value columns stripped; the mapping is our adjudication work. Re-running the script on a fresh download regenerates the valued version locally.
- `data/drawdown_spm7_option_comparison.csv` — 21 matched SPM.7 options with Drawdown impact sums vs SPM.7 totals; basis for the decision below.
- Produced by `drawdown_extract_clean.py` (validation: 52/55 rows' effectiveness × achievable adoption reproduces the stated GHG impact within 2×; the 3 misses are flagged below).
- Status: research release; **not production-approved** — license prohibits redistribution and storage without written permission (see README).

## Comparison with SPM.7 and decision

Mapped to `ipcc-ar6-spm7-mitigation-potentials` over 21 matched options (one-to-many: e.g. 16 Protect rows → "Reduce conversion of natural ecosystems"; sums of Drawdown ranges per option, with the usual non-additivity caveat — adequate for an ordinal check):

- **Weak rank agreement**: Spearman 0.31 (Drawdown mid vs SPM.7 total), 0.35 (high end), 0.42 on the 10 one-to-one pairs — none significant. Three-band (top/mid/tail) agreement is 33%, i.e. chance level. Compare UNEP-CCC vs SPM.7: 0.81–0.88.
- **Agreement exists only at the very top**: solar and wind are the top tier in both, ecosystem-conversion protection is high in both.
- **The divergence is methodological, not error.** Drawdown's "GHG Impact" is a no-target-year, no-cost-cap full-deployment envelope against current adoption; SPM.7 is a 2030 potential within ≤US$200/tCO2e. So slow-to-saturate options score relatively higher in Drawdown (refrigerant phase-out 2.5–2.7 vs SPM.7 F-gas 1.24; recycling ~2.3 vs 0.48; landfill CH4 + composting ~2.8 vs 0.81), and options whose 2030 potential rests on near-term land-use change score relatively lower (ag carbon sequestration 1.45 vs 3.44; restoration/afforestation 0.9 vs 2.84).

**Decision (Amanda, 2026-06-05): not a ranking source and not a cross-check.** SPM.7 remains the ranking source for `2026-06-action-reduction-potential`. Unlike UNEP-CCC (same quantity, near-identical ordering, kept as corroborating evidence), Drawdown measures a different quantity with chance-level ordinal agreement, so it cannot corroborate or challenge an SPM.7-based ranking. Retained as a research reference (see below). License alone would also have blocked production use. Confirmed after challenge and discussion same day; key takeaways recorded next.

## Takeaways from review discussion (2026-06-05)

Three challenges were raised against the decision and resolved:

- **"Is the 2030 deadline necessary?"** No — and it isn't the load-bearing choice. Any "best actions" ranking implies *some* horizon, and dated sources agree with each other (SPM.7 2030 vs UNEP-CCC 2035: Spearman 0.81–0.88), so the ordering is robust to the 2030-vs-2035 choice. If the horizon should move, swap to UNEP's 2035 numbers — the ranking barely changes. Drawdown is the outlier not because its deadline differs but because its envelope is **undated and cannot be re-dated**: the export contains no adoption trajectories, so "full achievable" converts to no particular year. An undated ceiling systematically favors slow-to-saturate options (recycling, transit) over near-term ones (fuel switching, fossil CH4) — that is the entire rank divergence.
- **"Drawdown has cost data too."** It does (51/55 quantified rows), but ordering by it misleads three ways: values mix regimes — demand-side rows are dominated by lifetime fuel/vehicle savings (public transit −3,300, carpooling −3,119 US$/tCO2e), so they rank as the "cheapest climate levers" on transport economics, not abatement cost; near-zero impact denominators explode the ratio (shared e-bikes +22,860, glass recycling +9,000 — solutions with ~0.00 Gt impact, not expensive ones); and the four largest potentials (solar, both wind rows, green hydrogen) are unpriced, so they vanish from any cost ordering. Coarse cost tiers over the priced subset would be defensible; a MACC-style ordering is not. SPM.7's capped buckets avoid all three failure modes.
- **"The end user is a city official seeking best actions — which use cases does each source serve?"** Dated potentials (SPM.7/UNEP) serve the ranking: what goes in the action plan this cycle, what to do first (cost tiers), what stands up in a public document (IPCC, CC BY, uncertainty bounds). Drawdown serves adjacent questions: full-menu option discovery (156 solutions incl. emerging), an expert anti-recommendation screen (its Not Recommended tier: waste-to-energy, corn ethanol, blue hydrogen, DAC...), and communication framing (speed-of-action, solution pages). Neither is city-resolved; both are global priors that the TEF mapping + feasibility scoring localize. Drawdown's co-benefit tags were initially noted as a unique axis, but co-benefits are covered by other datasets in the catalog, so they are **not** a retention rationale.

## How to read the schema

- `status`: only `quantified` rows have numbers. `tier_only` rows (all Worthwhile / Keep Watching / Not Recommended) carry classification, sector, cluster, mode only. `coming_soon` rows have no data at all yet.
- The (action, solution) pair is the key — "Forests: Boreal" appears under both Protect and Restore as genuinely different solutions.
- `ghg_impact_low/high_gt` is the impact at the low/high end of the *achievable adoption* range — a scenario span, not an uncertainty interval. `mid` is the simple midpoint, computed here, not published.
- `flags`: `cost_missing` (solar, both wind rows, green hydrogen — exactly the rows a cost-aware ranking most needs); `degenerate_range` (Clean Cooking: identical low/high, scenario span not modeled); `negligible_impact` (shared e-bikes, glass recycling: 0.00–0.00 after rounding).
- Internal-consistency misses from the build script: the two `negligible_impact` rows (division by ~0) and **Silvopasture**, where effectiveness × achievable adoption implies ~1.4 Gt at the low end vs the stated 0.40 — likely a stock/flow subtlety in their model; treat Silvopasture's numbers with caution.
- Costs are negative for ~half of quantified rows (savings); they are lifetime point estimates, methodology not exposed per row.

## What this data supports

- *"Drawdown classifies [solution] as Highly Recommended / Worthwhile / Keep Watching / Not Recommended."* — the tier system covers all 156 rows and is the only axis that does.
- *"At full achievable adoption, [solution] could avoid/remove X–Y GtCO2e/yr."* — with the no-year, no-cost-cap framing stated explicitly.
- Qualitative enrichment of an action list: `speed_of_action` (Emergency Brake / Gradual / Delayed), climate-pollutant coverage (CH4/BC flags for SLCP-focused screens), and adaptation / environment / well-being co-benefit tags — though co-benefits are sourced from other catalog datasets, so the distinctive axes here are the tier classification (esp. Not Recommended as an anti-recommendation screen) and speed-of-action.
- Solution-scoping prose via the per-solution Explorer pages (linked from the UI; not captured in this release).

## What this data does not support

- **Ordinal ranking of mitigation actions by potential** — the need this candidate was screened for. Chance-level agreement with SPM.7 plus the no-target-year framing make it unusable for "which actions are likely biggest by 2030"-type questions.
- Anything **city-resolved** — global figures, no regional breakdown.
- Anything **summable** — solutions overlap (e.g. heat pumps vs windows vs insulation all reduce the same heating demand); no published guidance on overlaps.
- **Cost-effectiveness ranking** — single points, missing for the biggest options, no buckets.
- Coverage-complete sector screens — ~43 Highly Recommended rows are still "Coming Soon", concentrated in electricity supply, buildings retrofits, and freight; a sector ranking built today would silently omit them.
- Any production or user-facing use — license (README).

## Using it downstream

- If a future need wants the tier / speed axes (co-benefits come from other catalog datasets): get written permission first (info@drawdown.org), then re-capture the export — this release will be stale by then (un-versioned, mutates in place).
- The crosswalk in `data/drawdown_spm7_crosswalk.csv` was adjudicated per-solution and can be reused; via SPM.7 it composes with the existing `spm7a_option_to_tef.csv` to reach TEF if ever needed.
- Re-review trigger: Drawdown quantifying the "Coming Soon" rows (watch quantified-row count vs 55) or publishing a license/permission pathway.

## Traceability

- Raw export: captured 2026-06-05 from <https://drawdown.org/explorer-solutions-table-export.csv> via the session's fetch tool and transcribed to file (sandbox network restrictions prevented a byte-level download; original BOM dropped); sha256 of the reviewed capture `b860d22287af9623070c7fee3431f48c533d2ea01fc312fcee983edb05834457`, 156 rows. Verified against an independent same-day capture of the rendered Explorer page (10 distinctive value strings spot-checked, all present; row count and tier counts consistent). **Full file removed from the repo same day for license reasons** — 10-row sample in `sample/`, re-download procedure in `sample/README.md`.
- Cleaning + crosswalk + comparison: `drawdown_extract_clean.py`, Claude-assisted, 2026-06-05. Spearman figures printed by the script.
- Terms of Use verified 2026-06-05 (last updated 2025-06-04).
- Review: Amanda, 2026-06-05.
