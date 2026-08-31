# SUBDERE / SINIM — municipal fiscal & institutional capacity indicators

Historical review of comuna-level **fiscal-autonomy** and **institutional-capacity** indicators from SINIM (run by SUBDERE). The reviewed 2024–2025 extract is **not a production dataset** and is not retained because the governing portal terms do not permit commercial use.

**At a glance**

- **Status:** rejected for production use — catalogued for traceability with `production_approved: false`; no pipeline consumes it.
- **Coverage:** 345 comunas · 16 regions · 2024 & 2025 · keyed on CUT code.
- **License:** non-commercial use with attribution; not acceptable for the commercial production product without explicit written clearance from SUBDERE.
- **Retention:** raw samples, derived CSVs and the exploratory notebook were removed on 31 August 2026. This folder retains review and provenance notes only.
- **Headline:** the typical comuna has low fiscal autonomy (median FCM dependency ~71%) — most cannot self-finance capital-intensive actions.

## Canonical downloads

**Source:** SINIM (SUBDERE). Two routes:

- **Official portal** `datos.sinim.gov.cl` — [Datos Municipales](https://datos.sinim.gov.cl/datos_municipales.php) selector (variables × comunas × years) → SpreadsheetML `.xls`; dictionary exports the same way. **Canonical; latest years (2024–2025).**
- **Community mirror** `bastianolea/sinim_datos_comunales` — series 2019–2023 as parquet/Excel/RDS; `obtener.R` for scripted pulls. Bulk/history only; **its own licence is restrictive.**

No source extract is retained in this review. The portal route and variable list below remain for provenance only. Do not download or reintroduce the data into a production pipeline unless SUBDERE grants explicit commercial-use permission.

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

**Removed artifacts (not retained):**

- `sinim_municipal_capacity_2024-2025.csv` — 345 × 29 (11 vars × 2 years + 2 derived staff totals).
- `municipal_who_features_2025.csv` — 2025 fields + INE population + coarse tiers, ready to match to actions.

## Historical purpose and replacement

This review originally tested SINIM as the city/"who" layer for climate-action fundability. It is no longer used downstream:

- **Capacity replacement:** `reviews/oef/cl-municipal-capacity-tier`, derived from commercially reusable INE census population.
- **Autonomy replacement:** `reviews/cl-subdere/cl-subdere-sim-bep`, using the reviewed SIM/BEP source.
- **Consolidated product:** `reviews/oef/cl-city-action-fundability/releases/v3` contains no SINIM-derived fields.
- **Database:** Mage run 170 loaded the OEF v3 profile and verified zero `cl-subdere/cl-subdere-sinim` rows remained in `modelled.city_finance_profile`.

## License

> **Production decision (Aug 2026): do not use or distribute this dataset in the commercial production product.**

- **Portal terms** (`datos.sinim.gov.cl`) authorize use **"sin fines comerciales"** with mandatory attribution. *[verified]*
- **Conflicting signals on the same source** point the other way: a **CC BY 2.0 Chile** footer badge and Chile's national open-data default (**CC0 1.0 / CC BY 4.0**, Ley 20.285) — both allow commercial use.
- **Net:** the explicit non-commercial portal term governs this review. Conflicting footer/default signals are not sufficient clearance for commercial production.

**Required handling** *(not legal advice)*:

- Do not ingest SINIM into a production pipeline or commercial product.
- Do not retain or redistribute the reviewed raw or derived extracts in this repository.
- Always attribute: *"Fuente: Sistema Nacional de Información Municipal (SINIM), SUBDERE, Ministerio del Interior."*
- Reconsider the dataset only if SUBDERE supplies explicit written commercial-use permission.

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
- The exploratory notebook and all input/output files were removed with the restricted data. These parsing notes are retained only as review evidence.

## Production status

There is **no production-approved release**. Catalog release `v1` remains `production_approved: false`, has no pipeline, and retains no data artifacts. A future release would require explicit commercial-use clearance and a fresh review; the existing v1 files must not be restored or relabelled as production data.
