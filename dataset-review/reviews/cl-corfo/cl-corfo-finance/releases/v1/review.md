# Review — cl-corfo-finance, release v1

## Scope and status

Research release (not production-approved). CORFO's climate-relevant financing instruments for need `2026-06-cl-finance-opportunities`: Crédito Verde, Programa Expande, CORFO guarantees, the green-hydrogen facility, and Innova R&D. Added to fill the debt/blended **instrument** gap and the **private-firm** actor that the SSG-vs-inventory comparison surfaced. Hand-curated from CORFO pages, captured 2026-06-08 (see "Extraction & refresh" in the README). Output: `data/cl_corfo_programs_v1.csv` (5 rows). Dataset-level facts in the README one level up.

## What this data supports

- "Chilean firms can finance ERNC, energy-efficiency, circular-economy and green-hydrogen projects through CORFO's Crédito Verde (up to US$30M, 20-year term), delivered via banks/leasing." — supported (`instrument_type=loan`, intermediated).
- "CORFO's 2026 Expande call prioritises decarbonisation, green hydrogen, clean energy and CO2 capture for growth-stage firms." — supported (`recurrence=annual`, explicit).
- "CORFO instruments add loans, guarantees and blended finance to a previously grant-only inventory." — supported; 3 of 5 rows are non-grant.

## What this data does not support

- "A municipality can apply to CORFO for these." — NO. Every instrument targets **private firms**; the city role is to refer local businesses / municipal enterprises. Coverage for a *city* does not change.
- "These are grants." — NO. Crédito Verde is a loan (repayable), guarantees are contingent, the H2 facility is blended/concessional debt. Read `instrument_type`; "fundability" via debt depends on firm bankability, not grant eligibility.
- "CORFO funds the firm directly." — NO for Crédito Verde / guarantees: CORFO funds/【backs the financial institution, which lends to the firm (intermediated).
- "The green-hydrogen facility is open with fixed terms." — NO; it is emerging/phased (`detail_level=index`) — confirm current terms.
- "CORFO content is open data." — it is **CC BY-NC-ND 3.0** (NonCommercial, NoDerivatives); attribute, keep non-commercial, don't republish derivative text (see README).

## Using it downstream

- In the coverage indicator, CORFO adds **sector-specific industry/energy supply**, but with `eligible_actor=private firm` it is not city-accessible, so it surfaces as a Moderate (broad-only) for a *city* action — correctly demonstrating that industry's coverage gap is an **actor** gap (cities don't implement industrial decarbonisation; firms do), not a supply gap. This is the cleanest argument for adding action-actor inference before reading coverage at the action level.
- Treat as the **firm-facing / debt** layer of the inventory; pair with the grant layer (MMA/SUBDERE/MINVU/energy) — they serve different actors and instruments.
- `detail_level=index` rows (green hydrogen, Innova) are leads — confirm live terms.

## Notes on non-obvious fields

- `instrument_type` carries the debt/guarantee/blended distinction — the reason CORFO was added; do not treat as grants.
- `access_pathway=intermediated` for Crédito Verde and guarantees — there is a bank/leasing step between CORFO and the firm.
- `specificity=broad` for guarantees and Innova (enable firm credit/innovation generally); sector-specific for Crédito Verde, Expande, H2.
- `eligible_actor` is firm for all rows — the key contrast with the municipal grant sources.

## Traceability

Sources (captured 2026-06-08): corfo.cl/cpp Crédito Verde page, programasyconvocatorias listing (JS-rendered), green-hydrogen fund press; Crédito Verde figures from 2024 press (US$83M placed). Licence CC BY-NC-ND 3.0 (site footer). Extraction prompt + refresh steps are in the README ("Extraction & refresh"); the committed `data/` CSV is the snapshot (the same prompt also runs in the OEF harness). To deepen: enumerate the JS-rendered calls list with a JS-capable fetch; pull per-instrument bases for exact eligibility/amounts.
