# Review — cl-subdere-sinim, release v1

## Scope and status

Historical research review — **rejected for production use**, not in a pipeline.

- **Licence:** the SINIM portal permits non-commercial use with attribution; this does not meet the commercial production requirement.
- **Production decision:** do not ingest, publish or use this release in the production product unless SUBDERE grants explicit written commercial-use permission.
- **Retention:** the raw samples, two derived CSVs and exploratory notebook were removed on 31 August 2026. Only this review and the dataset-level README remain.
- **Replacement:** fundability v3 uses `cl-subdere-sim-bep` for autonomy and `cl-municipal-capacity-tier` for capacity; it contains no SINIM-derived fields.

Dataset-level facts (provenance, licence, parsing) live in the README and are not repeated here. The claims below are retained as historical review evidence only; they do not authorize downstream or commercial use.

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

Do **not** use this release downstream in the production product. The following design notes are historical and have been superseded by the commercially reusable v3 replacements.

- **Partition into coarse tiers, not scores** — a **2×2** of financial autonomy (High/Low) × delivery capacity (High/Low): *self-starter / capable-but-cash-tight / funded-but-thin / needs-full-support*. Prefer the 2×2 over the SUBDERE population bracket (the bracket reintroduces the per-capita/size artifacts). **Superseded for the fundability model (Aug 2026):** its v3 capacity axis knowingly adopts the population bracket, trading this review's preference for freedom from the self-reporting and *honorarios* defects documented above, and accepting more collinearity between the two axes. The preference stated here still stands for any other use of these indicators; see `reviews/oef/cl-city-action-fundability/releases/v3/review.md` for the trade as adjudicated.
- **Map each action attribute to its axis:** `investment_cost` (capital intensity) → financial autonomy; formulation demand (needs-BIP / specialist team) → delivery capacity. Where the action stresses an axis the comuna is Low on, output a **finance route label**, not a number.
- **Action-side tags still needed** — formulation demand and self-financeability are not in the action set; derive from `reviews/cl-ssg/cl-ssg-legal-signals` (which already scores per-action technical capacity and financing accessibility), not by hand.
- **Pair with:** `cl-ine-censo` (population + socioeconomic attributes), `cl-casen` (authoritative poverty), `cl-city-action-fundability` (instrument/actor/access the route resolves against), `cl-ssg-projects` (CUT join — weak, size-confounded revealed-capacity signal, suggestive only).
- **Historical MEED+ HIAP design:** the data was considered for Feasibility only, never Impact or Alignment; it is not used by the current v3 city profile.
- **Commercial-use rule (not legal advice):** do not use SINIM raw values or classifications derived from this release in the commercial production product without explicit written SUBDERE clearance.

## Notes on non-obvious fields

- `fcm_dependency_pct` — FCM ÷ own income (incl. FCM); high = dependent = low autonomy. Not "% of total budget".
- `fet_royalty_mineria_mclp` — a *received* transfer; non-zero = State-flagged fiscally weak; opposite direction to own-income; 2025 only.
- `fiscal_autonomy_tier` / `capacity_tier` (formerly in the removed `municipal_who_features_2025.csv`) — illustrative terciles, not adjudicated cutoffs; partitioning method was never promoted.
- Staff `*_total` and profesional/directivo counts exclude honorarios; nulls (~16) = non-reporting, not zero-staff.

## Traceability

- **Removed inputs:** SINIM portal export `datos_municipales_20260616…_Sin-Corrección-Monetaria.xls`, dictionary exports and derived CSVs are not retained.
- **Removed derivation:** `sinim_capacity_exploration.ipynb` was removed because it contained outputs derived from the restricted source.
- **Indicator methodology:** SINIM variable dictionary (README variable table).
- **Replacement verification:** Mage run 170 produced 341 OEF v3 rows and zero retired SINIM-source rows in the configured database.
