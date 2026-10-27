# Unified legal classification — methodology (v2)

## Purpose

A single legal-feasibility classification across the full OEF action catalogue for Chile, bringing the legal layer of the earlier sector assessments forward into the v2 framing. It keeps **only the legal dimension** — governance capacity and financing are deliberately left out (they need real data, not expert scoring, and are tracked as separate future layers). The output is a gate/classification — *is there a legal basis for this action, and at what level of government* — not a complete feasibility ranking.

Data file: `legal-classification-v2.csv` (100 actions).

## Why bring v1 into v2 (not the reverse)

v2 changes the definition and approach (from "can the municipality act" to "is there a legal basis at the competent level"). Rather than rewrite the published v1 release, v1's legal results are carried forward into this v2 artifact and re-expressed in the harmonized model. v1 releases stay untouched.

## The harmonized legal model

Every action gets two legal sub-judgments on the enabled/conditional/blocked scale, plus a verdict by the original v1 rule. The two axes are defined to mean the same thing — and carry the same polarity (high = legally clear to proceed) — on both the municipally-led and nationally-led sectors:

- **authority** — is a body legally empowered to act for this action? (standing / competence)
- **permission** — does an in-force norm actually permit the action, free of prohibition? (clearance / *procedencia*)
- **legal_verdict** — `enabled` if both are enabled; `blocked` if either is blocked; else `conditional`.
- **legal_verdict_score** — a flat ordinal code: enabled = 1, conditional = 0.5, blocked = 0. This matches how the verdict is actually formed (non-compensatory rule logic — any axis blocked ⇒ blocked, both enabled ⇒ enabled), and avoids the false precision of a weighted average over inputs that are themselves only 1/0.5/0. Treat it as ordinal (for ranking tiers and filtering), **not cardinal** — do not average it across actions as if 0.5 meant "half feasible." Fine within-tier prioritisation is expected to come from the finance/governance layers, not the legal gate.

This replaces the original v1 axis names (ownership / restrictions), which did not survive the move to IPPU/AFOLU: "ownership" was municipality-specific, and "restrictions" (a prohibition signal) was being filled from C1, which actually measures instrument *existence* (an enablement signal) — wrong concept, even though it happened to yield the right verdict. The relabel was verified verdict-neutral: re-deriving all 52 IPPU/AFOLU rows under the faithful split changes **zero** verdicts.

The key reframe: authority is read as competence **at the responsible level of government**, not specifically the municipality. A `responsible_level` column (municipal / shared / national) preserves the distinction so the energy/waste/transport rows (municipally-led) and the IPPU/AFOLU rows (mostly national) are never silently treated as the same question. An `input_evidence` column records, per row, what evidence backs each axis.

## Sources and crosswalk

**Municipally-led sectors (stationary_energy 31, waste 10, transport 7 = 48 actions)** come straight from v1 `legal-analysis-v1.csv` (expert legal review of ownership + restrictions). `responsible_level` is derived from ownership: enabled→municipal, conditional→shared, blocked→national.

**IPPU (28) + AFOLU (24) = 52 actions** are derived from the v2 workbook's legal components only (C1, C2), dropping C3 budget and C4 climate alignment:

| Harmonized field | v2 source | Mapping |
|---|---|---|
| authority | C1 instrument-exists + C2 mandate | enabled if explicit instrument (C1∈{35,25}) **and** direct mandate (C2=20); blocked if no instrument (C1=0) **or** no mandate (C2=0); else conditional |
| permission | C1 *procedencia* tier | 35 (plenamente procedente) → enabled · 25/18/10 (partial / natural-vehicle caveats) → conditional · 0 (no instrument) → blocked |
| responsible_level | Contexto "Rol Municipal" | Ninguno → national · any active role → shared |
| legal_basis / justification | Análisis Cualitativo (Base legal, Conclusión) | carried where present |

For the municipally-led v1 rows the mapping is a straight carry-over: ownership → authority, restrictions → permission.

v2 codes (IPPU-NN/AFOLU-NN) carry no canonical OEF ID; all 52 were joined to the catalogue `action_id` by exact Spanish-description match (all unique, no duplicates, none unmatched).

## What this construction demonstrates

Across the 52 IPPU/AFOLU actions, the legal-only verdict diverges from v2's overall band for exactly **one** action — IPPU-20 (legally `enabled`: explicit instrument + direct mandate, but v2 rates it "Con condiciones" purely because budget and climate alignment are weak). That single divergence is the point: stripping finance and policy-alignment out leaves a legal signal that mostly tracks the instrument/mandate structure and isolates cases where non-legal factors, not the law, are the constraint.

## Handling of blocked actions (city_disposition)

"Blocked" is not permanent impossibility — both source methodologies define it as *not actionable under current conditions*. So blocked actions are not deleted; they are tagged for how a city-facing tool should treat them, via `city_disposition` (+ `block_reason`):

- **hard_filter (17 actions)** — `blocked` and competence sits exclusively with a national regulator or a regulated private utility (CNE, SEC, SISS, MTT, transmission/distribution/sanitary concessionaires). The city has no legal lever, so these are hidden from the city's selectable action list to avoid false signaling. They remain in the dataset as national context. `block_reason = handled_elsewhere`.
- **show_with_challenge (12 actions)** — kept visible to the city, flagged with the specific blocker:
  - 4 where the city has a facultative/partial role (`block_reason = city_facultative_role`): segregated collection, consumer sufficiency, municipal PSA, agroecological procurement.
  - 8 national policy gaps where no operative instrument exists anywhere yet (`block_reason = no_instrument_gap`): CCU, CCS, EPR-strengthening, material substitution, lightweight materials, feedstock decarbonization, net-zero supply chains, product-as-service. Surfaced so cities see the national dependency / advocacy opportunity rather than a silent gap.

All `enabled` and `conditional` actions are `city_disposition = show`. Net: 83 of 100 actions shown to the city, 17 hard-filtered.

## Caveats

- **Definitional shift is real.** For the municipally-led sectors "legal basis" means the municipality can act; for IPPU/AFOLU it means a national instrument + mandate exists. Same gate, different reach. Always read alongside `responsible_level`; do not pool the `legal_verdict_score` into a single cross-sector ranking without that column in view.
- **15 AFOLU verdicts are provisional.** `qualitative_backing = pending` marks the AFOLU actions whose v2 scores have no qualitative narrative yet; their authority/permission values come from the quantitative components alone.
- **Residual axis asymmetry.** On the municipal half, `permission` is a prohibition-check with the instrument assumed (the municipality's own powers); on the national half it also confirms an instrument exists. Same axis meaning and polarity, slightly different evidentiary bar — recorded per row in `input_evidence`.
- **Coverage: 100 of 101.** One transport action (`ipcc_0105`, active mobility via road-space reallocation) has no legal assessment in either source and is not in the file.
- **Legal ≠ will-happen.** This is a permission/basis layer. Governance capacity and financing refine *within* these tiers later; they do not fold into this score.
