# MMA Fondo de Protección Ambiental — awards (cl-mma-fpa-awards)

Project-level **award records** (proyectos adjudicados) of MMA's **Fondo de Protección Ambiental (FPA)** — Chile's first national competitive fund (since 1998), financing citizen, school, and indigenous-community environmental projects. This is the "who got funded" companion to the supply review `cl-mma/cl-mma-fondos` (join by program, not a key), and the repo's second awards dataset after `cl-conaf/cl-conaf-bn-awards` — the first with **cross-sector** precedent at **comuna** resolution.

> **Status: built (FPA 2021–2025), not promoted.** `releases/v1/` holds **655 projects**, 16 regions, 202 comunas (100% keyed to CUT), two schema eras normalised to one table; per-year counts for 2021/2022/2025 reconcile to official headlines. Includes the **clasificación → action crosswalk** (`data/cl_mma_fpa_awards_to_actions.csv`). Remaining: 2016–2020 (only in the JS search tool).

## Sources

All MMA (public), captured 2026-06-17. Programme context: [FPA portal](https://fondos.mma.gob.cl/fpa/) · [ChileAtiende ficha 76453](https://www.chileatiende.gob.cl/fichas/76453-fondo-de-proteccion-ambiental-fpa) · [2026 headline](https://mma.gob.cl/fondo-de-proteccion-ambiental-financiara-144-proyectos-de-organizaciones-ciudadanas-durante-2026/) (4,194 projects since 1998, >CLP 24 bn; max ~CLP 6 M/project).

Two entry points for the awards themselves:

- **Public project search** — http://www.fpa.mma.gob.cl/busqueda/busquedaPublica.php — the canonical multi-year DB, covers **all years incl. 2016–2020**, but **JavaScript-rendered** (needs Chrome tooling; not file-fetchable). Note `http://`.
- **"Fondos Adjudicados" hub** — https://fondos.mma.gob.cl/category/fondos-adjudicados/ — paginated; each concurso's page links its *Publicación de Resultados* + *Resolución* PDFs.

Per-year results booklets (the parsed source for v1; booklet format starts 2021):

| Year | Concurso | PDF |
| --- | --- | --- |
| 2025 | XXVIII | `…/2025/01/Publicacion_de_Resultados_FPA_2025.pdf` |
| 2024 | XXVII (Proyectos Sustentables) | `…/2024/01/Publicacion-Resultados-Concursos-FPA-2024-Proyectos-Sustentables.pdf` |
| 2023 | XXVI | `…/2023/01/Resultados-Concursos-FPA-2023-publicacion.pdf` |
| 2022 | XXV | `…/2022/01/Publicacion-Resultados-FPA-2022.pdf` |
| 2021 | XXIV | `…/2021/04/Resultados-FPA-2021.pdf` |
| 2016–20 | — | no booklet; use the search tool / per-concurso resolutions |

PDFs live under `https://fondos.mma.gob.cl/wp-content/uploads/`; the normalised pipe-tables parsed from them are in `releases/v1/sources/`.

**Two schema eras** (both normalised by `build_fpa_awards.py`): *producto* (2021–22) — columns `Folio·Org·RUT·Proyecto·Producto·Comuna·Monto·Nota`, variable amounts ($4–8 M), 6 concursos; *línea-temática* (2023–25) — `Folio·Proyecto·RUT·Org·Línea·Comuna·Monto·Nota`, flat $6 M, 3–5 líneas. 2023 merges water+energy into one line (sub-sector keyword-inferred, `sector_inferred=True`). An `era`/`clasificacion` column preserves the original label.

## License

Public-interest government information (MMA, public funds) — project name, organisation, comuna, theme, amount, year are public. Awardees are **organisations** (juntas de vecinos, NGOs, schools, indigenous communities), but records may name a natural person, so **RUT/person-level PII is dropped at build** (`build_fpa_awards.py`); only de-identified fields are committed. No explicit open licence (e.g. CC BY) is published — attribute to MMA, confirm before large-scale redistribution.

## Scope & interpretation warnings

National, all 16 regions, resolvable to **comuna** (the project's location, not a municipal applicant). v1 covers 2021–2025; the programme runs since 1998 (older years pending).

- **City-as-enabler, not applicant.** Eligible actors are citizen orgs, schools, indigenous communities — municipalities don't apply directly. FPA is enabler/intermediated precedent, not municipal-eligible supply.
- **Awarded ≠ disbursed.** Rows are selected projects (`award_stage=adjudicado_inicial`); execution/payment are later. Re-adjudicaciones not captured.
- **Amounts are CLP** (not UTM, unlike CONAF), per-concurso ceilings; older nominal amounts aren't inflation-adjusted.
- **Cross-sector / education tilt.** The big "Cambio Climático y Descontaminación" line is largely environmental education — `specificity` flags broad projects so they don't over-credit a GPC sector.
- **2023 water/energy split** is keyword-inferred for 22 rows; **2023/2024 counts** lack an official headline to check against.

## Mapping to actions

Because each row carries the funded thematic line (`clasificacion`), FPA awards *can* be mapped to the city action list (unlike INDAP/CONAF awards, where the intervention type is absent). The crosswalk `data/cl_mma_fpa_awards_to_actions.csv` (analysis notebook §6) maps at the **clasificación grain**, keyed on the raw string so a join tags every award; case/accent variants folded. **442 of 655 awards (67%) map at high/medium confidence**, reaching 8 actions (waste, community solar, solar-thermal, wetlands, green space, compost, building retrofit, biodiversity). The unmapped 33% is two known archetype gaps — the broad environmental-education line and "Ecotecnias hídricas" (water-efficiency). Link, don't attribute; rows await human adjudication.

## Release contents (v1, not promoted)

`releases/v1/`: `build_fpa_awards.py` (reproducible, repo-relative paths) · `analysis_fpa_awards.ipynb` (profile → validate → aggregate → visualise → map; restart-and-run-all passes, charts inline) · `data/cl_mma_fpa_awards_projects.csv` (655 de-identified projects) · `data/cl_mma_fpa_awards_to_actions.csv` (crosswalk) · `sources/` (normalised tables) · `review.md`. Validated: per-year reconciliation (2021/2022/2025), folios unique, CUT 655/655, 16 regions, no PII. Next: backfill 2016–2020, capture re-adjudicaciones, adjudicate the mapping.

## Related

`cl-mma/cl-mma-fondos` (supply side) · `cl-conaf/cl-conaf-bn-awards` (sibling awards) · `cl-mdsfam/cl-bip-projects` (public-investment pipeline — no record overlap; relate only at comuna/region × sector) · `oef/cl-city-action-fundability` (consumes this as award precedent via the crosswalk).
