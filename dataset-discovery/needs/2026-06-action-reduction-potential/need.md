---
id: 2026-06-action-reduction-potential
title: Emissions reduction potential per mitigation action (TEF-mapped)
status: open            # open | resolved | gap_confirmed | superseded
opened: 2026-06-04
requested_by: amanda
serves: action-prioritization

outcome:
  candidates:           # promote/investigate ids from candidates.yaml
    - ipcc-ar6-spm7-mitigation-potentials
    - climateview-tef-validated-data
    - project-drawdown-solutions
    - unep-egr-sectoral-potentials
  resolution_notes: null
---

## Context

Supports ranking candidate mitigation actions in CityCatalyst-style action
prioritization for the Chile/Brazil project. Ranking is ordinal — "which
actions are likely biggest" — not quantitative target-setting. Actions map
to ClimateView TEF transition elements.

The TEF taxonomy is already cataloged (`climateview-transition-elements`) but
its license is unverified; candidates that bundle potentials with the taxonomy
may inherit that issue.

Key search insight: TEF's Mitigation Compendium is explicitly structured from
IPCC AR6 WGIII Figure SPM.7, so the SPM.7 dataset maps onto TEF near-natively.

## Open questions

- Is cost-effectiveness part of "best action", or is raw potential enough?
  (Determines whether $/tCO2e moves to must-have in search.yaml.)
- ~~Project Drawdown bulk data export and license not yet verified (site fetch
  timed out during discovery).~~ Resolved 2026-06-05: export exists (direct
  CSV from the Explorer), but license is all-rights-reserved (ToU 2025-06-04;
  written permission needed for any storage/redistribution) and the dataset
  has changed — the 2025 Explorer relaunch replaced the 2020–2050 scenario
  table with a no-target-year, no-cost-cap "achievable adoption" envelope.
  Reviewed in `reviews/project-drawdown/project-drawdown-solutions`: rank
  agreement with SPM.7 is chance-level (Spearman 0.31–0.42), so unlike UNEP
  it is not even usable as a cross-check. Decision (confirmed after
  discussion — see the review's "Takeaways" section for the 2030-horizon
  and cost-column reasoning): not a ranking source; retained as research
  reference for option discovery, the Not Recommended screen, and
  speed-of-action (co-benefits come from other catalog datasets). Verdict
  moved investigate → deprioritize.
- ~~UNEP EGR ch.6 data annex availability not yet verified.~~ Resolved
  2026-06-05: no annex exists; tables transcribed, reviewed, and compared
  against SPM.7 in `reviews/unep-ccc/unep-egr-sectoral-potentials`.
  Decision: ordinally near-identical to SPM.7 (Spearman 0.81–0.88), so
  SPM.7 stays the ranking source (also CC BY vs UNEP's non-commercial
  license); UNEP retained as cross-check evidence only, no TEF mapping.
  Two caveats carried into SPM.7 use: land options' high band is
  baseline-sensitive, and 2030 demand-side values are upper bounds.
