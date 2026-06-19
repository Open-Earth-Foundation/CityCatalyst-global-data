# cl-mma-fpa-awards — v1 release review (5-year backfill, 2021–2025)

Status: **research / exploratory.** Five concurso years (FPA 2021–2025) extracted, de-identified, sector-mapped, and keyed to comuna CUT. Not promoted.

## What this release contains

`data/cl_mma_fpa_awards_projects.csv` — **655 awarded projects, FPA 2021–2025**, one row per project.

Coverage: **16/16 regions**, **202 distinct comunas** (100% keyed to CUT), total **CLP 3,536,000,000**. The 2021/2022/2025 counts match the MMA-announced totals exactly (independent completeness check); 2023/2024 had no single headline figure to check against and should be confirmed.

GPC-sector spread: waste 174 · cross 174 · afolu 162 · stationary_energy 100 · water 45.

## Two schema eras (both normalised to one table)

- **Línea-temática era (2023–2025)** — columns Folio·Proyecto·RUT·Org·**Línea Temática**·Comuna·Monto·Nota; flat **$6,000,000**. 2024–2025 use 5 líneas; **2023 merges** water+energy into one "Eficiencia Hídrica y Energética" line — sub-sector is **inferred by keyword** (`sector_inferred=True`, 22 rows: 16 energy / 6 water).
- **Producto era (2021–2022)** — columns Folio·**Org**·RUT·Proyecto·**Producto**·Comuna·Monto·Nota; **variable amounts** ($4M/$6M/$7M/$8M); **six** concursos (adds Fundaciones y Corporaciones, Áreas Verdes Comunitarias, Conservación de Humedales Urbanos). A `producto → GPC sector` map handles these (Punto Verde→waste; Invernadero y Compostaje→waste; Fotovoltaico/Solar Térmico→stationary_energy; Áreas Verdes Comunitarias→afolu; Humedales Urbanos→afolu; Cambio Climático y Descontaminación→cross).

An `era` and a `clasificacion` (original línea/producto string) column are carried so nothing is lost; `sector_inferred` flags the lower-confidence 2023 rows.

## Columns

`fund, funder_institution, concurso_year, concurso_n, concurso_code, concurso, era, folio, nombre_proyecto, organizacion, organizacion_tipo, clasificacion, gpc_sector, sector_inferred, specificity, comuna, comuna_cut, region, monto_clp, nota, eligible_actor, access_pathway, award_stage, status_as_of`.

## Sources & method

Consolidated annual results booklets (MMA, captured 2026-06-17), parsed to one-row-per-project pipe tables in `sources/`:
- 2025 `…/2025/01/Publicacion_de_Resultados_FPA_2025.pdf`
- 2024 `…/2024/01/Publicacion-Resultados-Concursos-FPA-2024-Proyectos-Sustentables.pdf`
- 2023 `…/2023/01/Resultados-Concursos-FPA-2023-publicacion.pdf`
- 2022 `…/2022/01/Publicacion-Resultados-FPA-2022.pdf`
- 2021 `…/2021/04/Resultados-FPA-2021.pdf`

`build_fpa_awards.py` parses both era layouts, drops RUT, maps class→sector (with 2023 keyword inference), derives comuna_cut+region from the repo's `cl-mdsfam/cl-casen/.../provincia_comuna.csv` (346-comuna register), validates, and emits the CSV. Reproduce: `python3 build_fpa_awards.py` (runs in-repo; prints the validation block). Full source index in the dataset `README.md`.

## Validation (all passing)

Folios unique within every year; amounts per era as expected (2021 {4,6,7,8}M · 2022 {4,6,8}M · 2023–25 {6}M); **CUT coverage 655/655**; 16 regions; no RUT/personal-ID in output; 2021/2022/2025 totals reconcile to official headline counts.

## Known limitations

- **Initial adjudication only** (`award_stage=adjudicado_inicial`); re-adjudicaciones not captured.
- **Awarded ≠ disbursed.**
- **2023 water/energy split is inferred** for 22 rows (keyword heuristic) because the source merged the line; treat those sub-sectors as lower-confidence (`sector_inferred=True`).
- **Producto→sector** involves judgment for "Invernadero y Compostaje" (mapped to waste; composting-led, though it also has an agriculture/AFOLU aspect).
- **2023/2024 counts** not cross-checked against an official headline.

## Analysis notebook

`analysis_fpa_awards.ipynb` (executed, charts rendered inline — not exported as image files) profiles, validates, and visualises the table — block-structured load → profile → validate → aggregate → visualise → findings. Reproduce: re-run top-to-bottom (reads `data/`). Headline analytical findings:

- **Taxonomy shift is the key caveat.** Across the Producto→Línea change (2022→2023), `cross` ("Cambio Climático y Descontaminación") falls from ~42% of producto-era awards to ~15%, while **water appears only from 2023** (the new "Ecotecnias hídricas" line) and AFOLU rises to ~34%. This is a *labelling* change, not a change in what communities built — use line-era years for clean sector precedent and treat `cross` as mixed (see notebook §4.2).
- **Geography:** La Araucanía leads (124 awards, ~19%, indigenous-community energy/water); top comunas Arica, Padre Las Casas, Teodoro Schmidt, Iquique, Temuco; thinnest in Magallanes/Antofagasta. 202/345 comunas have ≥1 award.
- **Awardees:** indigenous communities/associations (171), school parents' centres (140), juntas de vecinos (86) — **no municipality is ever the awardee** (confirms city-as-enabler).
- **Selectivity & size:** scores 2.15–3.10 (mean 2.75, selected set); flat CLP 6 M in the línea era, CLP 4–8 M by line in the producto era. Only 5 organisations won in ≥3 distinct years (broad rotation, little capture).

## Mapping to actions

Unlike the INDAP and CONAF awards (which carry only beneficiary + amount), FPA award rows carry the funded **thematic line** (`clasificacion`), so the intervention type is on the record and the awards *can* be mapped to the city action list. The crosswalk `data/cl_mma_fpa_awards_to_actions.csv` (built in the analysis notebook, §6) maps at the **clasificación grain** — one row per distinct line, keyed on the raw `clasificacion` string so a naive join tags every award; case/accent variants are folded. Link, don't attribute: an award's amount weights its line's action, never split.

Coverage is strong: **442 of 655 awards (67%) map at high/medium confidence**, reaching 8 distinct actions across waste (`c40_0037`), community solar (`icare_0012`), solar-thermal (`icare_0016`), wetlands (`ipcc_0060`), green space (`c40_0042`), organic waste/compost (`icare_0064`), building retrofit (`c40_0016`) and biodiversity/restoration (`ipcc_0053`). This is the first awards source to give broad cross-sector revealed precedent, directly attacking the fundability coverage hole (most actions previously had AFOLU-only precedent).

The unmapped **33% (213 awards)** is two buckets, both the same archetype gaps seen elsewhere: the broad **"Cambio Climático y Descontaminación Ambiental"** line (largely environmental education — `specificity = broad`, no action archetype) and **"Ecotecnias hídricas"** (the domestic/agricultural water-efficiency gap also seen for MOP and INDAP-Riego). A third archetype gap to log upstream with whoever owns the action list: **environmental education / awareness**. All mapping rows are agent drafts and **await human adjudication**.

## Next steps

- **2016–2020** to extend toward the full ~4,050-since-1998 history — only in the JS search tool (`fpa.mma.gob.cl/busqueda`) → needs the Chrome tooling or per-concurso resolution PDFs.
- Capture re-adjudicaciones; promote the build to a block-structured notebook to match `cl-conaf-bn-awards` before promotion.
