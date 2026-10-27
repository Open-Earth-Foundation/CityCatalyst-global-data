# Review — cl-mtt-fondos, release v1

## Scope and status

Research release (not production-approved). The transport-sector slice of need `2026-06-cl-finance-opportunities` (gap 1 in the need's `gaps.md`): MTT/DTPR funding to renew and decarbonise public and shared transport. Snapshot hand-curated from official programme pages captured 2026-06-16. Output: `data/cl_mtt_programs_v1.csv` — 3 programmes (national public-transport subsidy / fleet renewal, Renueva tu Micro, Renueva tu Colectivo). Dataset-level facts (sources, license, parsing) are in the README one level up.

## What this data supports

- "Chile funds the renewal and electrification of regional public transport." — supported; the reformed subsidy law (Aug 2024) earmarks >=50% of regional Fondos de Apoyo Regional to operation + fleet renewal and incentivises zero-emission buses, charging infrastructure and public bicycles; 1,028 e-buses awarded for 2026-27.
- "A taxi-colectivo operator can get an EV-weighted renewal subsidy." — supported; Renueva tu Colectivo gives a higher (~CLP 6.8M) special subsidy for electric replacement, reajustado cada marzo.
- "Transport finance exists at the national/regional public level for a city's transport actions." — supported as a `transportation` GPC match for scoring.

## What this data does not support

- "A municipality can apply for these transport funds." — NO. The eligible actor is a transport operator, or the GORE administers the funds; `access_pathway = intermediated` for all three rows. The city's role is enabling/convening, not applicant.
- "These programmes state a fixed grant amount." — mostly NO. The national subsidy's amount is set per-region in each GORE's bases (`detail_level = index`, `amount_clp` null); only Renueva tu Colectivo carries a programme-level figure, and it is approximate and region-dependent.
- "All three are zero-emission programmes." — NO. The subsidy-law zero-emission line and the colectivo EV subsidy are `explicit`; Renueva tu Micro is `climate-adjacent` (cleaner-vehicle renewal, not exclusively zero-emission).
- "This is the complete transport-finance picture." — NO. MinEnergía electromobility incentives, municipal cycling infrastructure, and any GORE-specific transport lines are not captured here; this is the MTT operator-subsidy core only.

## Using it downstream

- For fundability scoring, treat as `transportation` matches but apply the actor/access down-weight: none is a direct municipal grant, so under the need's score logic they can be Moderate at best for a municipality-implemented action — they score better against actions implemented by operators.
- Pair with `cl-minenergia` for the electromobility/charging context; cite MTT for operator subsidies to avoid double-counting.
- Treat `index` rows (national subsidy, Renueva tu Micro) as leads — confirm the current per-region call and amount on `dtpr.gob.cl`/SEREMI before presenting to a city.

## Notes on non-obvious fields

- `provider` vs `funder_institution` — money/policy is MTT; per-region delivery is via GORE/SEREMI. Both recorded because access mechanics and citation differ by region.
- `amount_clp` null is expected for the index rows — see `amount_note`; per-call amounts live in GORE bases.
- `recurrence` — Renueva tu Colectivo is annual (March reajuste); the national subsidy is ongoing per-region; Renueva tu Micro periodic.

## Traceability

Sources (captured 2026-06-16): gob.cl subsidy-law note, dtpr.gob.cl, ChileAtiende fichas 25058 (Renueva tu Micro) and 43671 (Renueva tu Colectivo), mtt.gob.cl gestión 2022-2026, energia.gob.cl electromobility platform. Extraction prompt + refresh steps in the README. Evidence tags recorded in the README's "Current approved release".
