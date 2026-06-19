# Review — cl-subdere-sinim, release v1

## Scope and status

Research / exploratory — not production-approved, not in a pipeline.

- **Licence:** non-commercial use with attribution is clear; **commercial use unresolved — clearance requested from SUBDERE, proceeding in parallel** under attribution + a no-raw-values design (see README).
- **What this release is:** the SINIM 2024–2025 pull turned into the city/"who" layer of the fundability work.
- **Artifacts:**
  - `data/sinim_municipal_capacity_2024-2025.csv` — 11 indicators × 345 comunas, cleaned.
  - `data/municipal_who_features_2025.csv` — fiscal/capacity fields joined to INE-census population + coarse tiers.
  - `sinim_capacity_exploration.ipynb` — distributions, FETRO validation, correlations, projects join.

Dataset-level facts (provenance, licence, parsing) live in the README and are not repeated here. This document is the contract for what the **capacity layer can and cannot say once matched to actions**; the partitioning method itself is design intent, not yet built.

## What this data supports

Claims you could lift into a report — each with the condition that keeps it honest:

| Claim | Condition that keeps it honest |
| ----- | ----- |
| "The typical Chilean comuna has low fiscal autonomy — median FCM dependency ~71% (2025); ~3 in 4 exceed 50%." | Dependency is over *own income* (incl. FCM), not total revenue. |
| "Comuna X has higher/lower **financial autonomy** than Y." | Report as High/Low **tiers**, not a precise rank; never on per-capita income alone. |
| "Comuna X has higher/lower **delivery capacity** than Y." | Coarse tier from `staff_total` + `professionalization_pct`; a generic proxy, not climate capacity; excludes honorarios. |
| "Financial autonomy and delivery capacity are **distinct axes**." | Supported (2025 corr ≈ 0.22) — treat as two partitions, not one composite. |
| "How easy an action is depends on **action demand × comuna capacity**." | It's a **route/effort categorisation** (self-deliverable → own-budget → competitive fund → external co-finance/TA/pooling), not a funding probability. |
| "Comuna X is among those the State itself flags as fiscally weak." | Via the FET flag (`fet_royalty_mineria_mclp_2025` > 0; ~87% of comunas); 2025 column only. |

## What this data does not support

Overclaims, written out before they happen:

| Overclaim (do NOT say) | Why not |
| ----- | ----- |
| "This action has an N% chance of being funded in comuna X." | Capacity/autonomy ≠ funding *outcome*; no award/disbursement history here. |
| "Comuna X is the 4th most fundable/capable." | Data supports 3–4 tiers, not fine ordinal ranking. |
| "Comuna X is fiscally strong — high own-income per capita." | Per-capita misleads for tiny comunas (rural/mining show *highest* IPP-per-cápita yet are most dependent, smallest-staffed). Use dependency + absolute budget/staff. |
| "This action scores lower in a low-capacity comuna." | Low capacity makes it *harder/needs an external route*, not less valuable — informs Feasibility only, never Impact/Alignment. |
| "A low-autonomy comuna is less fundable for everything." | For grants (FET, FNDR) low autonomy can *raise* eligibility; the real barrier is formulation capacity, not poverty. |
| "Few staff ⇒ cannot deliver." | Counts exclude honorarios; small comunas staff that way — counts understate, nulls ≠ zero. |
| "2024 vs 2025 real-terms change / current poverty." | Money is nominal (undeflated); poverty is carried-forward CASEN, not annual. |

## Using it downstream

- **Partition into coarse tiers, not scores** — a **2×2** of financial autonomy (High/Low) × delivery capacity (High/Low): *self-starter / capable-but-cash-tight / funded-but-thin / needs-full-support*. Prefer the 2×2 over the SUBDERE population bracket (the bracket reintroduces the per-capita/size artifacts).
- **Map each action attribute to its axis:** `investment_cost` (capital intensity) → financial autonomy; formulation demand (needs-BIP / specialist team) → delivery capacity. Where the action stresses an axis the comuna is Low on, output a **finance route label**, not a number.
- **Action-side tags still needed** — formulation demand and self-financeability are not in the action set; derive from `reviews/cl-ssg/cl-ssg-legal-signals` (which already scores per-action technical capacity and financing accessibility), not by hand.
- **Pair with:** `cl-ine-censo` (population + socioeconomic attributes), `cl-casen` (authoritative poverty), `cl-city-action-fundability` (instrument/actor/access the route resolves against), `cl-ssg-projects` (CUT join — weak, size-confounded revealed-capacity signal, suggestive only).
- **Feed to MEED+ HIAP Feasibility** with the reason attached ("harder here: ~85% FCM-funded, ~35 staff") — never Impact or Alignment.
- **Commercial-use design rule (not legal advice):** use SINIM only as an **input to the derived classification**; do **not** surface or export raw SINIM values in any product. This keeps use at the derived/analytical end (lower risk) rather than redistribution (higher risk) — narrowing, not removing, the commercial-licence question (see README → License).

## Notes on non-obvious fields

- `fcm_dependency_pct` — FCM ÷ own income (incl. FCM); high = dependent = low autonomy. Not "% of total budget".
- `fet_royalty_mineria_mclp` — a *received* transfer; non-zero = State-flagged fiscally weak; opposite direction to own-income; 2025 only.
- `fiscal_autonomy_tier` / `capacity_tier` (in `municipal_who_features_2025.csv`) — illustrative terciles, not adjudicated cutoffs; partitioning method still open.
- Staff `*_total` and profesional/directivo counts exclude honorarios; nulls (~16) = non-reporting, not zero-staff.

## Traceability

- **Inputs:** SINIM portal export `datos_municipales_20260616…_Sin-Corrección-Monetaria.xls` + dictionary exports (`sample/`, gitignored; re-download in README); INE population `reviews/cl-ine/cl-ine-censo/releases/2024/data/raw_data_cl_ine_censo.csv`; join check vs `reviews/cl-ssg/cl-ssg-projects/.../projects_profiled.csv`.
- **Derivation + validation:** `sinim_capacity_exploration.ipynb` (restart-and-run-all passes).
- **Indicator methodology:** SINIM variable dictionary (README variable table).
- **Partitioning/interaction model:** this document (design intent; not yet implemented).
