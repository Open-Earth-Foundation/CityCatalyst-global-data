# SUBDERE / SINIM — municipal fiscal & institutional capacity indicators

Comuna-level **fiscal-autonomy** and **institutional-capacity** indicators from SINIM (run by SUBDERE). A targeted pull of 11 indicators for **all 345 comunas**, **2024–2025**, populating the city/"who" layer of the climate-action fundability work — the dimension the MEED *Nota Diversidad Municipal* defines but leaves empty.

**At a glance**

- **Status:** research / exploratory — not in a pipeline, not catalog-registered.
- **Coverage:** 345 comunas · 16 regions · 2024 & 2025 · keyed on CUT code.
- **License:** in use now under attribution + a no-raw-values design; **commercial clearance requested from SUBDERE in parallel** (see License).
- **Headline:** the typical comuna has low fiscal autonomy (median FCM dependency ~71%) — most cannot self-finance capital-intensive actions.

## Canonical downloads

**Source:** SINIM (SUBDERE). Two routes:

- **Official portal** `datos.sinim.gov.cl` — [Datos Municipales](https://datos.sinim.gov.cl/datos_municipales.php) selector (variables × comunas × years) → SpreadsheetML `.xls`; dictionary exports the same way. **Canonical; latest years (2024–2025).**
- **Community mirror** `bastianolea/sinim_datos_comunales` — series 2019–2023 as parquet/Excel/RDS; `obtener.R` for scripted pulls. Bulk/history only; **its own licence is restrictive.**

**Re-download (this release):** raw lives in `releases/v1/sample/` (gitignored). At the portal, select the 11 codes below, all comunas, 2024–2025, "Sin Corrección Monetaria", export.

**Variables pulled** (SINIM code → cleaned column → unit):

| Code | SINIM name | Cleaned column | Unit | Dimension |
| ----- | ----- | ----- | ----- | ----- |
| IADM75 | Dependencia del FCM sobre Ingresos Propios | `fcm_dependency_pct` | % (0–100) | Fiscal autonomy |
| IADM74 | Ingresos Propios Permanentes per Cápita (IPPP) | `ipp_percapita_mclp` | M$ | Fiscal autonomy |
| IADM10 | Disponibilidad Presupuestaria por Habitante | `presup_percapita_mclp` | M$/inhab | Fiscal headroom |
| FETRO | FET Royalty a la Minería | `fet_royalty_mineria_mclp` | M$ | Fiscal need flag |
| IADM25 | Nivel de Profesionalización del Personal | `professionalization_pct` | % (0–100) | Technical capacity |
| IRH17 | N° Funcionarios (Planta y Contrata) | `staff_total` | count | Technical capacity |
| IRH07 | N° Planta — Escalafón Profesional | `staff_planta_profesional` | count | Technical capacity |
| IRH14 | N° Contrata — Escalafón Profesional | `staff_contrata_profesional` | count | Technical capacity |
| IRH06 | N° Planta — Escalafón Directivo | `staff_planta_directivo` | count | Management capacity |
| IRH13 | N° Contrata — Escalafón Directivo | `staff_contrata_directivo` | count | Management capacity |
| ISOC001 | Índice de Pobreza CASEN | `poverty_casen_pct` | % | Socioeconomic context |

**Cleaned outputs (`releases/v1/data/`):**

- `sinim_municipal_capacity_2024-2025.csv` — 345 × 29 (11 vars × 2 years + 2 derived staff totals).
- `municipal_who_features_2025.csv` — 2025 fields + INE population + coarse tiers, ready to match to actions.

## Why we use it

- **Differentiates comunas** — turns the flat per-sector finance-coverage label into a city-specific readiness signal.
- **Fills the `[DATA PENDING]` cells** of the *Nota Diversidad Municipal* (`reviews/cl-ssg/cl-ssg-legal-signals`): fiscal autonomy + technical capacity.
- **Feeds MEED+ HIAP Feasibility** — "can this city realistically pay for / deliver this action?"
- **Joins** `cl-ssg-projects` on CUT; modulates `cl-city-action-fundability`. **Pairs with** `cl-ine-censo` (population — joined) and `cl-casen` (poverty).

## License

> **Decision (Jun 2026): in use now, under attribution + a no-raw-values design, while a written commercial-use clearance request to SUBDERE runs in parallel.**

- **Portal terms** (`datos.sinim.gov.cl`) authorize use **"sin fines comerciales"** with mandatory attribution. *[verified]*
- **Conflicting signals on the same source** point the other way: a **CC BY 2.0 Chile** footer badge and Chile's national open-data default (**CC0 1.0 / CC BY 4.0**, Ley 20.285) — both allow commercial use.
- **Net:** non-commercial / internal research is clearly fine; **commercial use is unresolved** until SUBDERE says which terms govern.

**How we proceed meanwhile** *(practical risk reduction, not legal advice)*:

- Use SINIM only as an **input to the derived classification** — **never surface or export raw SINIM values** in a product (derived/analytical use, not redistribution = the lower-risk end).
- Always attribute: *"Fuente: Sistema Nacional de Información Municipal (SINIM), SUBDERE, Ministerio del Interior."*
- The clearance request to SINIM's Unidad de Información Municipal is what removes the residual risk.

**Sources:** [SINIM terms](https://datos.sinim.gov.cl/informacion_municipal.php) · [Gobierno Digital standard](https://wikiguias.digital.gob.cl/Est%C3%A1ndares/Datos-Abiertos) · Ley 20.285.

## Spatial and temporal scope

- **Geography:** 345 comunas, 16 regions; keyed on 5-digit CUT (`comuna_cut`, leading zeros kept).
- **Nature:** local truth — records reported by each municipality, compiled by SUBDERE's UIM.
- **Time:** 2024 & 2025 (`_2025` primary). Updated annually. **Units:** nominal CLP.

## Interpretation warnings

The traps worth knowing before using a field:

- **`fcm_dependency_pct`** — FCM over *own income* (incl. FCM), 0–100. **Not** "% of total revenue"; don't compare thresholds across the two definitions.
- **Money is nominal** — 2024→2025 deltas include inflation. Single-year levels/ratios are fine; deflate before reading trend.
- **`professionalization_pct`** — generic professional-title share. **Not** climate/planning capacity, nor proof of a SECPLA/environmental unit. Coarse signal.
- **Staff counts** — exclude *honorarios* / *código del trabajo*; small/rural comunas staff that way, so counts **understate** workforce and the ~16 nulls are non-reporting, **not** zero.
- **`poverty_casen_pct`** — latest CASEN **carried forward**, not annual; small-comuna estimates uncertain.
- **`fet_royalty_mineria_mclp`** — new fund (Law 21.591, from 2025) targeting FCM dependency >50% *or* bottom-80th-pct own income → a State "fiscally weak" flag, but a *received transfer* (opposite direction to own income). **2025 only.**
- **Population** isn't in the SINIM pull — it comes from `cl-ine-censo` (joined in `municipal_who_features_2025.csv`).

## Parsing notes

- **`.xls` is SpreadsheetML XML**, not binary Excel/HTML — `read_excel`/`read_html` return nothing. Parse `<Row>`/`<Cell>`/`<Data>` and **honor `ss:Index`** (skips blank cells; ignoring it shifts later values).
- **Two-row header** (variable label, then year); data starts at row 3.
- **`comuna_cut`** = 5-digit zero-padded CUT — keep as string.
- **Sentinels:** this extract had blanks only, but SINIM emits `s/i` / `n/d` — mapped to empty. Fill ~340–345/345 (fiscal/poverty/FETRO), 327–329/345 (staff).
- Formal extraction notebook (Phase B) **not yet written**; cleaning lives in `sinim_capacity_exploration.ipynb`.

## Current approved release

**v1** — research/exploratory; not in `catalog/index.yaml` yet. **Promotion prerequisites:** (1) commercial-licence clearance from SUBDERE (requested), (2) action-side tags (formulation demand, self-financeability).
