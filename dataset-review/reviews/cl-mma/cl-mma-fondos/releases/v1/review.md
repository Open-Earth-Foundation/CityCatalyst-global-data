# Review — cl-mma-fondos, release v1

## Scope and status

Research release (not yet production-approved; approval tracked in `catalog/index.yaml`). Produced by `cl_mma_fondos_extract_clean.ipynb` from the MMA funds portal `fondos.mma.gob.cl`, captured 2026-06-08. Output: `data/cl_mma_fondos_v1.csv` — 55 MMA fund lines (45 FPA, 9 FPR, 1 Recambio de Calefactores programme), in two tiers: 7 *detailed* (current-cycle fichas, full Antecedentes parsed) and 48 *index* (name / URL / open-date / status enumerated from the FPA + FPR hubs, 2020–2026). `data/hub_index.json` is the index-tier input. Dataset-level facts (license, provenance, parsing quirks) live in the README one level up; this file is about what the *data* supports.

## What this data supports

- "As of 2026-06-08, MMA's environmental funds (FPA, FPR) have no open call; the most recent cycle closed in October 2025." — true; the portal is a current-cycle board and all 55 captured lines are `status=closed`. Always cite the `status_as_of` date.
- "The FPR and the three core FPA lines (Proyectos Sustentables Ciudadanos, Establecimientos Educacionales, Pueblos Indígenas) reopen on a roughly annual cycle, typically opening Aug–Oct for the following execution year." — supported by the archive: these four streams appear in 5–7 of the 7 cycles 2020–2026 (`recurrence=annual`, `next_call_estimate ≈ ago–oct 2026`). State it as an expectation, not a guarantee (see anti-claims).
- "A Chilean municipality can apply directly to the FPR (up to CLP 14M); FPA lines are for non-profit private organisations, indigenous communities, or research bodies, not municipalities." — supported per-row by `eligible_actor` / `eligible_actor_detail` from each ficha.
- "MMA environmental funding spans waste/circular-economy, energy efficiency & renewables, biodiversity, and climate-change lines." — supported via `gpc_sectors` / `thematic_lines` for detailed rows; for index rows the sector tag is inferred from the title only (coarser).
- "Each detailed fund links to its governing Resolución Exenta." — true; `resolucion_url` holds the official administrative act for the 7 detailed rows.

## What this data does not support

- "This fund is recurring, so it will open again next year." — NO. `recurrence=annual` is a pattern observed over 2020–2026, not a commitment; Chilean concursable funds depend on the annual Ley de Presupuestos and can be cut, delayed, rescoped, or renamed. Treat `next_call_estimate` as planning guidance.
- "These special calls (Alto del Carmen, TSEJ zones, Rapa Nui extraordinario, fauna/Pudú, wildfire) are part of the regular offer." — NO. They are `recurrence=one-off` / `sporadic`: tied to a specific comuna, a sacrifice-zone remediation programme, or a one-time allocation. Do not assume they return.
- "FPA grants are about CLP 6M." — only for the citizen/education/indigenous lines. Amounts are per-line and range to CLP 60–70M for the Alto del Carmen calls. Never generalise an amount across "FPA".
- "The Rapa Nui 2026 grant is CLP 100,000,000." — NO. The source ficha prints `$ 10.000.0000` (an extra zero); `amount_suspect=True` flags it. Intended value is ~CLP 10M; confirm from the Bases PDF before quoting.
- "Index-tier rows carry verified eligibility/amount/sector." — NO. Index rows have only name, URL, open-date, status, and a title-inferred sector; eligibility and amount are blank until the ficha is fetched (`detail_level=index`).
- "A closed status means the fund is discontinued." — NO. For `recurrence=annual` rows, closed means between cycles; read `recurrence` + `next_call_estimate` alongside `status`.

## Using it downstream

- For the fundability work, combine `status` with `recurrence`: an action is well-positioned if it matches a fund that is open now **or** `recurrence=annual` (reliably reopening). A match to a `one-off`/`sporadic` closed call is weak evidence of future fundability.
- Filter the city-facing reference by `eligible_actor` (municipalities can act on FPR directly; FPA lines they facilitate for local orgs).
- This release replaces the *environment* slice of the static `cl-ssg/cl-ssg-finance` inventory (sibling catalog entry); pair the two only with the SSG set marked superseded for these funds.
- Treat `index` rows as leads, not finished records — enrich by fetching the ficha before presenting amount/eligibility.

## Notes on non-obvious fields

- `recurrence` — derived from how many of the 7 cycles (2020–2026) the line's *stream* appears in, not from any per-fund declaration. `annual` ≥5/7; `sporadic` intermittent; `one-off` single appearance; `ongoing (rolling…)` for Recambio (per-comuna, not an annual concurso).
- `next_call_estimate` — populated only for `annual` streams; an inference, not a published date.
- `status_section_conflict=True` — the portal's index still grouped the line as "open" after its close date; status was set from the close date, which is authoritative.
- `amount_suspect=True` — malformed amount string in the source (currently only Rapa Nui 2026).
- `detail_level` — `detailed` (ficha parsed) vs `index` (hub listing only); many fields are intentionally blank for `index`.

## Traceability

Source: `https://fondos.mma.gob.cl/` (FPA hub `/fpa/`, FPR hub `/fpr/`, per-fund fichas), captured 2026-06-08; governing acts are the linked Resoluciones Exentas. Inputs: `data/hub_index.json` (committed). Recurrence basis: cycle-count pivot over the 2020–2026 archive (reproduced in the notebook's recurrence cell). All field values verified against the live portal on the capture date; refresh by re-running the notebook's load path.
