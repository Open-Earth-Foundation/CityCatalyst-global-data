# Review — cl-minenergia-fondos, release v1

## Scope and status

Research release (not production-approved). The **municipally-relevant subset** of Ministry of Energy / AgenciaSE funding for the energy slice of need `2026-06-cl-finance-opportunities`, scoped down by request to programmes a municipality can apply to, run, or facilitate. Snapshot produced via the OEF extraction harness from official programme pages captured 2026-06-08. Output: `data/cl_minenergia_programs_v1.csv` — 6 programmes (Comuna Energética, Asistencia Técnica para Municipios, Parque Solar Comunitario, Casa Solar, FAE, Mejor Escuela). Hand-curated (no single portal); dataset-level facts (sources, license, parsing) are in the README one level up.

## What this data supports

- "Chile's Ministry of Energy offers municipally-relevant energy programmes across efficiency and small-scale renewables." — supported; all 6 rows are `climate_relevance=explicit`, `gpc_sectors` include `stationary_energy`.
- "A municipality can engage the Ministry's energy support directly through Comuna Energética and Asistencia Técnica para Municipios." — supported; `eligible_actor=municipality` for both (Comuna Energética: 141 comunas adhered, per the programme page).
- "A municipality can enable residential rooftop solar for its residents by enrolling its comuna in Casa Solar (≈50% co-financing + aggregate-purchase discount)." — supported; `eligible_actor=household`, `access_pathway=facilitated-by-city`.
- "The FAE funds small-scale renewable energy access (PV up to 10 kWp; solar thermal up to 1,500 L) for community-role organisations in rural/isolated/vulnerable areas." — supported from the ChileAtiende ficha.

## What this data does not support

- "These energy funds open on an annual cycle." — NO. They are standing/rolling programmes or sporadic, not annual concursos; `recurrence` is ongoing / sporadic, never "annual". Read `status_as_of` and re-check the live AgenciaSE bulletin.
- "A municipality can apply to the FAE." — NO. FAE eligibility is community-role organisations (indigenous communities, juntas de vecinos, NGOs, bomberos), explicitly not municipalities; and it is currently dormant (last call closed 2024-07-20).
- "Comuna Energética / Asistencia Técnica are grants." — NO. They are mainly technical assistance / certification (with co-financing windows attached); `instrument_type` reflects this.
- "Program X awards CLP N." — mostly unsupported: amounts are per-call (in each call's bases), not stated at programme level; `amount_clp` is null for most rows with the reason in `amount_note`. Only Casa Solar (≈50% co-financing) and FAE (capacity limits) have figures, and those are rates/limits, not a grant ceiling.
- "AgenciaSE content is open data." — NO. AgenciaSE is a private-law foundation with an all-rights-reserved notice; treat as public-interest facts with attribution, confirm before bulk redistribution (see README license).

## Using it downstream

- For fundability scoring, treat these as `stationary_energy` matches. None are currently a clean "open annual grant"; the strongest live options are Casa Solar (rolling, facilitative) and Comuna Energética (municipal, ongoing). FAE is dormant — weak evidence of future availability.
- Pair with `cl-mma` (environment/waste/biodiversity) — minimal overlap; together they cover the environment + energy mitigation funding for a city. SUBDERE (municipal infrastructure) and MINVU (urban/green) remain to be reviewed for the broader picture.
- Treat `detail_level=index` rows (Asistencia Técnica, Parque Solar, Mejor Escuela) as leads — confirm current call mechanics on the AgenciaSE bulletin before presenting to a city.

## Notes on non-obvious fields

- `provider` vs `funder_institution` — money is public (Min. Energía); delivery/website is usually AgenciaSE (private-law foundation). Both recorded because it matters for citation and licence.
- `recurrence` here means programme cadence (ongoing / sporadic), not the cycle-count derivation used in `cl-mma` (these aren't annual concursos, so no cycle archive to count).
- `amount_clp` null is expected — see `amount_note`; programme pages rarely state a single figure.
- `detail_level` — `detailed` (fields read off the programme page) vs `index` (programme identified; specifics pending the live call/bases).

## Traceability

Sources (captured 2026-06-08): comunaenergetica.cl, casasolar.cl, ChileAtiende FAE ficha 36666, mejorescuela.cl, energia.gob.cl (Parque Solar reporting, financing finder), agenciase.org convocatorias. Extraction prompt + refresh steps are in the README ("Extraction & refresh"); the committed `data/` CSV is the snapshot (the same prompt also runs in the OEF harness). Refresh by re-reading each `source_url` and the latest AgenciaSE bulletin.
