# Action Fundability Review

Goal: score each action by how fundable it is, not by picking one funding opportunity.

## What to check

1. **Sector fit**: action sector/subsector matches opportunity scope.
2. **Actor fit**: implementing actor is eligible.
3. **Geography fit**: opportunity covers city/regional/national context.
4. **Instrument fit**: instrument matches action type (infrastructure, planning, regulatory, program, financial).
5. **Timing fit**: opportunity is open/recurring and usable now.
6. **Constraint fit**: barriers are manageable (co-financing, capacity, complexity).

## Simple score (0-12)

Score each check from 0 to 2, then sum:

- **10-12**: High fundability
- **7-9**: Medium fundability
- **0-6**: Low fundability

## Keep it clean

- Sector fit is required. If sector fit is 0, do not match.
- Use broad funds carefully; they can inflate scores.
- Do not rely on keywords alone.

## How the calculation works

1. Start with all funding opportunities.
2. Keep only opportunities with sector relevance to the action (direct first; broad cross-sector is downweighted).
3. For each remaining opportunity, score actor fit, geography fit, instrument fit, timing fit, and constraint fit.
4. Build an action-level fundability score from:
   - quality of top direct matches,
   - weighted depth of specific matches,
   - share of strong matches,
   - small cross-sector bonus,
   - penalty if top matches are too generic/repetitive.
5. Output:
   - `fundability_score_100` (0-100),
   - `fundability_band_relative` (percentile rank),
   - `fundability_band_absolute` (fixed thresholds).
