# Review — cl-conaf-fondos, release v1

## Scope and status

Research release (not production-approved). The forestry / nature-based (AFOLU) slice of need `2026-06-cl-finance-opportunities` (gap 2 in the need's `gaps.md`): CONAF's Ley de Bosque Nativo funding. Snapshot hand-curated from official CONAF pages captured 2026-06-16. Output: `data/cl_conaf_programs_v1.csv` — 2 lines (the bonificación concurso + the adjacent research fund). Dataset-level facts (sources, license, parsing) are in the README one level up.

## What this data supports

- "Chile funds native-forest conservation, recovery and sustainable management, with an open 2026 cycle." — supported; the Fondo de Conservación (Ley 20.283) 2026 concurso is open, total ~CLP 6.98 bn, applications close noon 1 Jul 2026, results late Aug 2026.
- "The fund covers fire- and soil-relevant works." — supported; financiable activities include cortafuegos (firebreaks), obras de conservación de suelos, raleos, podas, establecimiento de regeneración, PFNM and asesoría profesional.
- "There is a dedicated small-landowner line." — supported; two lines (pequeños propietarios, accompanied by CONAF through the process; and otros interesados).
- "This is an `afolu` GPC match for scoring nature-based / forestry actions." — supported.

## What this data does not support

- "A municipality can apply to this fund as a city." — only as a landowner of eligible native forest; the eligible actor is the forest property owner. For most cities the role is facilitating local owners, not receiving the grant. `access_pathway` reflects this.
- "The award is ~CLP 6.98 bn." — NO. That is the total fund across all awards; the per-applicant benefit is a per-hectare bonificación (literal C cap ~10 UTM/ha). Read `amount_note`, not the fund total.
- "The status is recurring/stable." — NO. It is a dated annual cycle; the 2026 window closes 1 Jul 2026 and the row goes stale within weeks. Re-verify before surfacing.
- "The research fund is a city finance opportunity." — NO. The Fondo de Investigación del Bosque Nativo is research-only (universities), recorded as adjacent context.

## Using it downstream

- For fundability scoring, treat the bonificación as an `afolu` match. It can be Strong only for an action implemented by an eligible forest landowner (incl. a municipality on municipal land) while the cycle is open; otherwise Moderate/Weak on actor/timing grounds.
- The hard per-ha cap and the bases literales mean adequacy (amount vs project cost) must be checked against the bases PDF before any city relies on it.
- Pair with MINVU urban parks / future urban-arborización lines for the full nature-based picture; CONAF is the rural/native-forest core.

## Notes on non-obvious fields

- `amount_clp` null is expected — the benefit is per-hectare (UTM/ha), not a single project figure; structure is in `amount_note`.
- `status = open` is genuinely point-in-time and short-lived here — `status_as_of = 2026-06-16`, closes 1 Jul 2026.
- `recurrence = annual` with an April launch / July close rhythm; refresh around the annual launch.

## Traceability

Sources (captured 2026-06-16): conaf.cl programme page + 2026 launch announcements, concursolbn.conaf.cl application portal/bases, Fondo de Investigación del Bosque Nativo XVII concurso 2026 (UdeC VRID listing). Per-ha caps from press coverage of the bases — confirm against the official bases PDF at the portal. Extraction prompt + refresh steps in the README.
