# cl-ssg-projects v1 — Review Notes

The project files follow a consistent FICHA-IDI template structure and are suitable for reliable PDF-to-JSON extraction.

## Most Useful Fields for Matching Projects to Mitigation Actions

For matching against mitigation actions in `cl-ssg-legal-signals/releases/v1/data/actions.json`, the strongest project fields are:

- `etapas[].clasificacion.sector`
- `etapas[].clasificacion.subsector`
- `etapas[].iniciativa.nombre`
- `etapas[].iniciativa.descriptor`
- `etapas[].narrative.justificacion`
- `etapas[].narrative.descripcion_etapa`
- `etapas[].conclusiones_analisis`

Supporting (but secondary) signals:

- `etapas[].solicitud_financiamiento.rows[].asignacion_presupuestaria`
- `etapas[].clasificacion.etapa_actual`
- `etapas[].ubicacion.*`

## Suggested Matching Approach

1. Match first at `gpc_sector` level to define candidate action groups.
2. Refine with `gpc_subsector -> gpc_sector(id)` consistency checks.
3. For projects mapping to more than one valid sector/subsector family, label as `cross-sector`.
4. Apply semantic/text similarity only within the surviving taxonomy-filtered candidates.
5. Use budget allocation/type fields as a tie-breaker (infrastructure vs planning/program patterns).

## Suggested Scoring (Taxonomy First)

- `gpc_subsector` match: 0.45
- `gpc_sector(id)` consistency: 0.25
- Description similarity: 0.30

Suggested confidence labels:

- `high`: exact/near-exact subsector + strong description similarity.
- `medium`: sector-consistent + moderate description similarity.
- `low`: sector-only or weak text signal.
- `cross-sector`: valid multi-sector mapping (store all candidate sectors/subsectors).

---

# FICHA IDI field reference — for project replicators

A guide to the fields in `ficha_idi.schema.v1.0.0.json`, organised around the
questions someone replicating a Chilean climate-action project would actually
ask. Each field is given with its **JSON path**, the **Spanish label** as it
appears in the PDF, an **English translation**, what the field tells you, and
notes on typical content or quirks.

A FICHA IDI ("Iniciativa De Inversión") is the standard one-pager Chile's
*Sistema Nacional de Inversiones* (SNI / BIP — Banco Integrado de Proyectos)
emits for every public-investment project. So while the corpus is broader than
"climate" projects, the same schema describes road repairs, stormwater works,
solar lighting, urban parks, ecosystem restoration, etc. For climate-action
case studies, treat this guide as the field-by-field translation key.

---

## At a glance — the 11 questions a replicator asks

| Question                      | Where to look                                          |
| ----------------------------- | ------------------------------------------------------ |
| 1. What is this project?      | `iniciativa`, `clasificacion.etapa_actual`             |
| 2. What sector / domain?      | `clasificacion.sector` / `subsector`                   |
| 3. Where is it?               | `ubicacion`                                            |
| 4. Why is it being done?      | `narrative.justificacion`                              |
| 5. What does it actually do?  | `narrative.descripcion_etapa`, `resumen_resultados.indicadores.componentes` |
| 6. Who benefits?              | `resumen_resultados.beneficiarios_directos`            |
| 7. How much does it cost?     | `solicitud_financiamiento`                             |
| 8. How long does it take?     | `resumen_resultados.duracion_meses`, `programacion_inversion.aportes_directos[].inicio` / `termino` |
| 9. Who runs it / partners?    | `instituciones_participantes`, `funcionario_responsable` |
| 10. What does success mean?   | `resumen_resultados.indicadores`                       |
| 11. Was it approved? executed?| `iniciativa.rate`, `resultado_analisis`, `historial_presupuesto`, `observaciones_admisibilidad` |

Below, each question is broken out with the underlying fields. The full schema
lives at [`releases/v1/schemas/ficha_idi.schema.v1.0.0.json`](schemas/ficha_idi.schema.v1.0.0.json).

---

## 1. What is this project?

| JSON path                                   | Spanish (PDF)                              | English                                | Notes                                                                                                                                                  |
| ------------------------------------------- | ------------------------------------------ | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `etapas[i].iniciativa.codigo_bip`           | Código BIP                                 | BIP project ID                         | Format `<numeric>-<suffix>`, e.g. `40060934-0`. The numeric part is the canonical project ID; reuse across years means same project, different cycles. |
| `etapas[i].iniciativa.nombre`               | Nombre IDI                                 | Project name                           | Spanish, often UPPERCASE. e.g. `"TRANSFERENCIA PRODUCCIÓN DE BIOINSUMO PARA RECUPERAR SUELOS DEGRADADOS DEL JARDÍN"`.                                |
| `etapas[i].iniciativa.tipologia`            | Tipología                                  | Project type                           | One of `PROYECTO` (works/infrastructure), `PROGRAMA` (transfer/programme of activities), `ESTUDIO BÁSICO` (study/research).                          |
| `etapas[i].iniciativa.descriptor`           | Descriptor                                 | Sub-programme code                     | A short tag indicating the funding line, e.g. `"PRU"` (Programa Recuperación Urbana), `"SUBTÍTULO 33"` (transfer-of-capital budget line). May be null. |
| `etapas[i].clasificacion.etapa_actual`      | Etapa actual                               | Current project stage                  | Lifecycle stage: `PERFIL` (concept), `PREFACTIBILIDAD` (pre-feasibility), `FACTIBILIDAD` (feasibility), `DISEÑO` (design), `EJECUCION` (execution).  |
| `etapas[i].header.proceso_presupuestario`   | Proceso Presupuestario                     | Budget process year                    | The fiscal year the FICHA was filed for, e.g. 2024.                                                                                                  |
| `etapas[i].header.postula_a`                | Postula a                                  | Applies for stage                      | Which lifecycle stage the request is for (often the same as etapa_actual, sometimes the next).                                                       |
| `etapas[i].clasificacion.situacion_solicitud` | Situación de la solicitud               | Request situation                      | `NUEVA` = new request, `ARRASTRE` = continuation of a multi-year project.                                                                            |
| `document.fecha_creacion_solicitud`         | Fecha Creación Solicitud                   | Request creation date                  | When the request was first filed (ISO date).                                                                                                          |
| `document.fecha_ultima_modificacion`        | Fecha Última Modificación                  | Last modification date                 | When the FICHA was last edited.                                                                                                                      |

---

## 2. What sector / domain?

| JSON path                                       | Spanish (PDF)                  | English                          | Notes                                                                                                                                                                                |
| ----------------------------------------------- | ------------------------------ | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `etapas[i].clasificacion.sector`                | Sector                         | Sector                           | High-level classification. Observed values include `RECURSOS HÍDRICOS` (Water Resources), `RECURSOS NATURALES Y MEDIO AMBIENTE` (Natural Resources & Environment), `ENERGÍA` (Energy), `TRANSPORTE` (Transport), `VIVIENDA Y DESARROLLO URBANO` (Housing & Urban Development), `MULTISECTORIAL`, `MINERÍA` (Mining). |
| `etapas[i].clasificacion.subsector`             | (right side of "Sector / Subsector") | Sub-sector                | E.g. `AGUAS LLUVIAS` (Stormwater), `MEDIO AMBIENTE` (Environment), `ALUMBRADO PÚBLICO` (Public Lighting), `TRANSPORTE FERROVIARIO` (Rail Transport), `DESARROLLO URBANO` (Urban Development).                                            |
| `etapas[i].clasificacion.sector_subsector_raw`  | Sector / Subsector (verbatim)  | Raw sector string               | The original `"X / Y"` string, kept for transparency.                                                                                                                                 |
| `etapas[i].clasificacion.componente_analisis`   | Componente de Análisis         | Analysis scope                  | `NACIONAL` (national-level review), `REGIONAL`, `INTERREGIONAL`, `MULTIREGIONAL`. Tells you who reviewed/approves the project.                                                       |
| `etapas[i].clasificacion.seia`                  | SEIA                           | Environmental impact status     | Whether the project triggered Chile's SEIA (Sistema de Evaluación Ambiental). Values: `NO CORRESPONDE` (not applicable), `DECLARACION` (Environmental Impact Declaration filed), `ESTUDIO` / `EIA` (Environmental Impact Study filed), `NO INGRESA` (didn't enter SEIA). |
| `etapas[i].clasificacion.area_desarrollo_indigena` | Área de Desarrollo Indígena | Indigenous development area     | Boolean. `true` means the project sits inside an officially designated Indigenous Development Area (relevant for consultation requirements).                                       |

---

## 3. Where is it?

| JSON path                                | Spanish (PDF)                      | English                          | Notes                                                                                                                                                          |
| ---------------------------------------- | ---------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `etapas[i].ubicacion.tipo`               | (parsed from "Loc. Geográfica")    | Location level                   | Granularity: `REGION`, `PROVINCIA`, `COMUNA` (municipality), `INTERREGIONAL`, `MULTIREGIONAL`, `MULTICOMUNAL`, `NACIONAL`. Tells you the geographic resolution. |
| `etapas[i].ubicacion.nombre`             | (parsed from "Loc. Geográfica")    | Location name                    | E.g. `"VALPARAISO"`, `"ANTOFAGASTA"`, `"VIÑA DEL MAR"`. Use with `tipo` to disambiguate (`REGION DE VALPARAISO` vs `COMUNA DE VALPARAISO`).                  |
| `etapas[i].ubicacion.raw`                | Loc. Geográfica                    | Verbatim location field          | Original string, in case you need to re-parse.                                                                                                                  |
| `etapas[i].ubicacion.distrito`           | Distrito                           | Electoral district number        | Mostly administrative; useful to cross-reference with electoral district maps if needed.                                                                       |
| `etapas[i].ubicacion.circunscripcion`    | Circunscripción                    | Senate constituency              | Senate-level electoral grouping. Same caveat as distrito.                                                                                                      |
| `etapas[i].vinculacion.proyecto_relacionado` | Proyecto Relacionado            | Linked project                   | Object with `codigo` and `tipo_relacion` (`COMPLEMENTARIO` = complementary, `SUSTITUTO` = replaces). Tells you if this project is part of a larger initiative. |

---

## 4. Why is it being done?

| JSON path                                    | Spanish (PDF)                          | English                              | Notes                                                                                                                                                                                                                                                  |
| -------------------------------------------- | -------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `etapas[i].narrative.justificacion`          | Justificación del Proyecto / Programa  | Justification / problem statement    | Long Spanish prose, typically 1-3 paragraphs, describing the problem the project addresses. **This is the single most useful field for understanding the climate driver** — fire damage, water scarcity, flood vulnerability, energy poverty, etc. |

For a worked example see the bottom of this document.

---

## 5. What does it actually do?

| JSON path                                                     | Spanish (PDF)                                 | English                              | Notes                                                                                                                                                                                                  |
| ------------------------------------------------------------- | --------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `etapas[i].narrative.descripcion_etapa`                       | Descripción de la Etapa Programada (PROYECTO) / Descripción de las Actividades a Realizar en la Etapa (PROGRAMA) | Activities description       | Long Spanish prose explaining the activities, methodology, materials, and approach. **This is your main source for "how to replicate"**.                                                              |
| `etapas[i].resumen_resultados.indicadores.proposito`          | Propósito                                     | Project purpose                       | One sentence (or a short list) describing the strategic objective. Often expressed as the change to be produced.                                                                                       |
| `etapas[i].resumen_resultados.indicadores.componentes`        | Componentes                                   | Components / work packages            | Numbered list of the discrete things the project produces (e.g. `["Diseñar y construir sistemas...", "Producir microorganismos...", "Evaluar el efecto..."]`). **The replication blueprint**.        |
| `etapas[i].resumen_resultados.indicadores.indicadores_componentes` | Indicadores de Componentes              | Component indicators                  | How each component will be measured. Often a paragraph rather than a tidy list.                                                                                                                        |

> Note: `componentes` and the indicadores fields are **only populated for ~9% of records**, mostly those at PROGRAMA / EJECUCION stage. Records at PERFIL stage usually have these sections present but empty.

---

## 6. Who benefits?

| JSON path                                                               | Spanish (PDF)                       | English                       | Notes                                                                                                                                                                       |
| ----------------------------------------------------------------------- | ----------------------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `etapas[i].resumen_resultados.beneficiarios_directos.hombres`           | Beneficiarios Directos > Hombres    | Direct beneficiaries — male   | Integer count. Source units vary — sometimes individuals, sometimes households, sometimes companies.                                                                        |
| `etapas[i].resumen_resultados.beneficiarios_directos.mujeres`           | Beneficiarios Directos > Mujeres    | Direct beneficiaries — female | Same as above.                                                                                                                                                              |
| `etapas[i].resumen_resultados.beneficiarios_directos.total`             | Beneficiarios Directos > Total      | Direct beneficiaries — total  | The total. Note: often equal to `hombres + mujeres` but sometimes printed even when the M/F split is not given.                                                            |

> Caveat: the unit (people / households / companies / hectares) is **not** in
> a structured field — you have to read `descripcion_etapa` to interpret. For
> the bioinsumo example, `total = 200_000` refers to liters of bioinsumo, not
> people; for the ERNC programme `total = 160` refers to companies.

---

## 7. How much does it cost?

| JSON path                                                                   | Spanish (PDF)                                  | English                          | Notes                                                                                                                                                                                                                |
| --------------------------------------------------------------------------- | ---------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `etapas[i].solicitud_financiamiento.totales.costo_total`                    | Solicitud de Financiamiento — Total > Costo Total | Total cost (M$)                  | **This is the project budget, in thousands of CLP**. To convert: `costo_total × 1000` = CLP; divide by `tipo_cambio_clp_per_usd` for USD. E.g. `costo_total: 90000` = 90,000,000 CLP ≈ 105,847 USD at 850 CLP/USD. |
| `etapas[i].solicitud_financiamiento.tipo_cambio_clp_per_usd`                | Tipo de Cambio (footer)                        | CLP/USD exchange rate            | The official rate the FICHA was priced at, for the budget year.                                                                                                                                                     |
| `etapas[i].solicitud_financiamiento.moneda_presupuesto.year`                | Moneda Presupuesto YYYY                         | Reference budget year            | The year the costs are denominated in. Use this if you want to deflate to a different base year.                                                                                                                    |
| `etapas[i].solicitud_financiamiento.moneda_presupuesto.factor`              | Factor                                          | Inflation factor                 | Multiply by this to convert nominal CLP to a unified base year (CDIPRES uses this for cross-year comparison).                                                                                                       |
| `etapas[i].solicitud_financiamiento.rows[].fuente`                          | Fuente                                          | Funding source                   | Who pays. Common values: `F.N.D.R.` (Fondo Nacional de Desarrollo Regional — regional development fund), `SECTORIAL` (line-ministry budget), `MUNICIPAL` (municipal budget), `EMPRESA` (state-owned enterprise), `PRIVADO`. |
| `etapas[i].solicitud_financiamiento.rows[].asignacion_presupuestaria`       | Asignación Presupuestaria (Item)                | Budget line / category           | What the money goes to: `OBRAS CIVILES` (civil works), `CONSULTORÍAS` (consulting), `CONTRATACIÓN DEL PROGRAMA` (programme implementation), `GASTOS ADMINISTRATIVOS` (admin), `EQUIPAMIENTO` (equipment), etc.    |
| `etapas[i].solicitud_financiamiento.rows[].costo_total`                     | Costo Total (per row)                           | Cost from this source            | Per fuente × asignación. Sum equals `totales.costo_total`.                                                                                                                                                          |
| `etapas[i].solicitud_financiamiento.rows[].pagado_al_inicio_periodo`        | Pagado al 31/12/<prev_year>                      | Already paid at start of period  | Money disbursed before the budget year started — useful to gauge progress.                                                                                                                                          |
| `etapas[i].solicitud_financiamiento.rows[].solicitado_periodo_actual`       | Solicitado para el año <budget_year>             | Requested for the budget year    | This year's funding ask.                                                                                                                                                                                            |
| `etapas[i].solicitud_financiamiento.rows[].solicitado_periodos_siguientes` | Solicitado años siguientes                       | Requested for subsequent years   | The tail of the funding ask.                                                                                                                                                                                        |
| `etapas[i].programacion_inversion.otros_aportes[]`                          | Otros Aportes                                   | In-kind / other contributions    | Often `APORTE BENEFICIARIOS` (beneficiary contribution), or partner contributions not running through SNI.                                                                                                          |

> **Currency convention:** every monetary field uses `M$` = thousands of CLP
> unless the row's `moneda` is `MUS$` (thousands of USD). The convention is
> consistent across the corpus.

---

## 8. How long does it take?

| JSON path                                                                         | Spanish (PDF)                       | English                         | Notes                                                                                                                                            |
| --------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `etapas[i].resumen_resultados.duracion_meses`                                     | Duración                            | Total duration (months)         | The headline duration of the etapa (e.g. 12, 24, 36 months).                                                                                     |
| `etapas[i].programacion_inversion.aportes_directos[].duracion_meses`              | Duración (per item)                 | Per-item duration               | Each line in the work plan has its own duration — useful for understanding sequencing.                                                          |
| `etapas[i].programacion_inversion.aportes_directos[].inicio` / `.termino`         | Inicio / Término                    | Item start / end                | FICHA convention: `{"mes": "ene", "anio_relativo": 1}` means "January of the project's first year". The dates are **relative to project start**, not calendar dates. |

---

## 9. Who runs it / partners?

| JSON path                                                            | Spanish (PDF)                              | English                                   | Notes                                                                                                                                                                              |
| -------------------------------------------------------------------- | ------------------------------------------ | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `etapas[i].instituciones_participantes.institucion_formuladora`      | Institución Formuladora de la Etapa        | Lead implementing agency                  | Who designed and is running this etapa. Typically a SEREMI (regional ministry office), a municipality, a state-owned enterprise (Metro S.A., EFE), or a public service (SERVIU, DGA). |
| `etapas[i].instituciones_participantes.instituciones_financieras`    | Instituciones Financieras                  | Financing institutions                    | Often the GORE (Gobierno Regional) or the relevant ministry. Multiple values possible.                                                                                             |
| `etapas[i].instituciones_participantes.instituciones_tecnicas`       | Instituciones Técnicas                     | Technical institutions                    | Specialised technical bodies brought in for design / supervision.                                                                                                                  |
| `etapas[i].funcionario_responsable.nombre`                           | Funcionario Responsable > Nombre           | Responsible officer                       | A real person — useful for direct outreach if you are doing primary research.                                                                                                      |
| `etapas[i].funcionario_responsable.institucion`                      | Institución                                | Officer's institution                     | Where the officer sits (often a regional SEREMI office).                                                                                                                           |
| `etapas[i].funcionario_responsable.cargo`                            | Cargo                                      | Officer's role                            | E.g. `"PROFESIONAL"`, `"DIRECTOR"`, `"JEFE DEPTO INVERSIONES"`.                                                                                                                   |
| `etapas[i].funcionario_responsable.fono`                             | Fono                                       | Phone number                              | Contact phone.                                                                                                                                                                     |
| `etapas[i].funcionario_responsable.correo_electronico`               | Correo Electrónico                         | Email                                     | Contact email. Populated for ~92% of etapas.                                                                                                                                       |

---

## 10. What does success mean? (indicators)

| JSON path                                                                    | Spanish (PDF)                       | English                              | Notes                                                                                                                                          |
| ---------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `etapas[i].resumen_resultados.indicadores.proposito`                         | Propósito                           | Purpose / strategic objective        | A sentence (or short numbered list) describing the change the project aims to produce.                                                         |
| `etapas[i].resumen_resultados.indicadores.indicadores_proposito`             | Indicadores de Propósito            | Purpose indicators                   | How that change will be measured. Often a single paragraph rather than discrete metrics — read it carefully for quantitative targets.         |
| `etapas[i].resumen_resultados.indicadores.componentes`                       | Componentes                         | Components                           | (See section 5 — same field.)                                                                                                                  |
| `etapas[i].resumen_resultados.indicadores.indicadores_componentes`          | Indicadores de Componentes          | Component indicators                 | Per-component success measures.                                                                                                                |

---

## 11. Was it approved? Was money actually spent?

### Approval (technical-economic review)

| JSON path                                       | Spanish (PDF)                                              | English                          | Notes                                                                                                                                                                                                       |
| ----------------------------------------------- | ---------------------------------------------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `etapas[i].iniciativa.rate.resultado`           | RATE (Resultado del Análisis Técnico Económico)            | Technical-economic review code   | **The single most important approval signal.** `RS` = Recomendado Satisfactorio (recommended, approved). `FI` = Falta Información (more info needed). `OT` = Objetado Técnicamente (technically objected). `RE` = Reevaluación. `IN` = Incumple. |
| `etapas[i].iniciativa.rate.fecha`               | Fecha (RATE)                                               | RATE date                        | When the review verdict was issued.                                                                                                                                                                          |
| `etapas[i].iniciativa.rate.institucion`         | Institución                                                | Reviewing institution            | Usually the Ministerio de Desarrollo Social y Familia (national) or a SEREMI Desarrollo Social (regional).                                                                                                 |
| `etapas[i].resultado_analisis[]`                | Resultado del Análisis Técnico Económico (table)           | Review history                   | One row per review pass. Each row has `rate`, `resultado`, `fecha`, `institucion_analisis`. Multi-row when a project bounced back and forth.                                                              |
| `etapas[i].conclusiones_analisis`               | Conclusiones del Análisis                                  | Reviewer's narrative conclusions | Free-text. Often empty.                                                                                                                                                                                      |
| `etapas[i].observaciones_admisibilidad`         | Observaciones de Admisibilidad / No Admisibilidad          | Admissibility observations       | Object with `admitido` (true/false), `preamble`, and a numbered list of `observaciones`. Tells you exactly what the reviewer asked for / objected to. Most useful for understanding why a project may have stalled or been rejected. |
| `etapas[i].header.admisibilidad`                | Admisibilidad (header)                                     | Admissibility flag               | `Si` / `No` / `null`.                                                                                                                                                                                        |
| `etapas[i].header.fecha_postulacion_sni`        | Fecha Postulación SNI                                      | SNI submission date              | When the FICHA entered the SNI system.                                                                                                                                                                       |
| `etapas[i].header.fecha_ingreso_sni`            | Fecha Ingreso SNI                                          | SNI entry date                   | When the FICHA was admitted.                                                                                                                                                                                 |

### Execution (actual spending)

| JSON path                                                                   | Spanish (PDF)                                                       | English                          | Notes                                                                                                                                  |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `etapas[i].historial_presupuesto.solicitudes_financiamiento[]`              | Historial > A. Solicitudes de Financiamiento                        | Year-by-year request history     | One row per budget year showing what was requested vs paid. Useful to see if a project was funded over multiple cycles or got cut.    |
| `etapas[i].historial_presupuesto.ejecucion_presupuestaria[]`                | Historial > B. Ejecución Presupuestaria                             | Actual budget execution          | One row per year × asignación showing money actually allocated and spent (`monto_vigente`, `gasto_total`). The "did it really happen" view. |
| `etapas[i].registro_sni[]`                                                  | Registro de Ingreso en el S.N.I. (table)                            | SNI submission log               | One row per submission cycle through the SNI. `recepcion`, `fecha`, `institucion_responsable`.                                        |

---

## A worked example — replicator's-eye view of one project

Source: `ambiente__bip_40060934_2024.json` (PROGRAMA, 2024, Region of
Valparaíso). The project produces a microbe-based bioinsumo to recover soils
degraded by wildfire — a climate-adaptation case study.

```
What is it
  Project name      TRANSFERENCIA PRODUCCIÓN DE BIOINSUMO PARA RECUPERAR
                    SUELOS DEGRADADOS DEL JARDÍN
  BIP code          40060934-0
  Type              PROGRAMA
  Stage             PERFIL (concept)
  Budget year       2024
  Status            NUEVA (new request)

Sector
  Sector            Recursos Naturales y Medio Ambiente
                    (Natural Resources & Environment)
  Sub-sector        Medio Ambiente (Environment)
  Analysis level    REGIONAL
  SEIA              NO CORRESPONDE (not subject to environmental review)

Where
  Region            Valparaíso

Why
  Justification     Wildfires have intensified due to human activity and
                    climate change. The Valparaíso region has lost over
                    4,000 hectares to fire. Burned soils need active
                    intervention to restore vegetation and ecosystem
                    services such as water regulation, carbon capture,
                    erosion prevention.

What it does
  Activities        Pilot facility at the Jardín Botánico Nacional
                    (Viña del Mar) producing microorganism-based bioinsumo
                    for application to wildfire-damaged soils. Targets
                    the 113 ha burned in December 2022.
  Components        1. Design and build microbe production systems
                    2. Produce microbes at 100-litre scale
                    3. Evaluate effect of microbe application
  Purpose           Pilot-scale microbe production + evaluation

Who benefits
  Beneficiaries     200,000 (split as Hombres 100,000 / Mujeres 100,000)
                    [unit: litres of bioinsumo, NOT people — read
                    descripcion_etapa for the unit]

How much
  Total cost        90,000 M$ ≈ 90,000,000 CLP ≈ ~105,847 USD
                    (at 850.25 CLP/USD)
  Source            F.N.D.R. (Regional Development Fund)
  Budget line       CONTRATACIÓN DEL PROGRAMA (programme implementation)
  Already paid      0
  Requested 2024    90,000 M$
  Requested 2025+   0

How long
  Duration          12 months
  Schedule          ene Año 1 → ene Año 2

Who runs it
  Lead              (not yet populated at PERFIL stage)
  Officer           (not yet populated)

Approval status
  RATE              null (not yet reviewed)
  Admisibilidad     null
  Observations      none
```

---

## What's NOT in the FICHA

A few things a replicator usually wants that are **not** in this dataset and
would need separate research:

- **GHG emission reductions / climate metrics** — Chile's SNI does not require
  these in the FICHA; you'd need to derive them from the activity description
  using sector-specific factors.
- **Geocoordinates** — section 13 GEORREFERENCIACIÓN exists as a label only;
  the actual coordinates live in the BIP system's map view, not the printed
  FICHA. Use `ubicacion.tipo` + `ubicacion.nombre` for region/comuna-level
  joins.
- **Procurement details / contractor names** — the FICHA describes the planned
  budget structure but not who won the tender. That data is in
  [mercadopublico.cl](https://mercadopublico.cl) once procurement happens.
- **Outcome evaluation** — the FICHA captures planned indicators; ex-post
  evaluation reports (when produced) live separately, usually with the
  Ministerio de Desarrollo Social y Familia.
- **Beneficiary unit** — see the caveat in section 6. You have to read the
  free-text description to know whether `total` refers to people, households,
  hectares, litres, etc.

---

## Quick lookup: where do I find …?

| You want …                                | JSON path                                                                  |
| ----------------------------------------- | -------------------------------------------------------------------------- |
| Climate driver / problem                  | `etapas[].narrative.justificacion`                                         |
| What activities they planned              | `etapas[].narrative.descripcion_etapa`                                     |
| Discrete components                       | `etapas[].resumen_resultados.indicadores.componentes`                      |
| Total budget in USD                       | `costo_total × 1000 / tipo_cambio_clp_per_usd`                             |
| Who funded it                             | `etapas[].solicitud_financiamiento.rows[].fuente`                          |
| Who is implementing it                    | `etapas[].instituciones_participantes.institucion_formuladora`             |
| Who to contact                            | `etapas[].funcionario_responsable.nombre / .correo_electronico`            |
| Region/comuna                             | `etapas[].ubicacion.tipo` + `.nombre`                                       |
| Approval status                           | `etapas[].iniciativa.rate.resultado`                                       |
| Was money actually spent?                 | `etapas[].historial_presupuesto.ejecucion_presupuestaria[]`                |
| Number of beneficiaries                   | `etapas[].resumen_resultados.beneficiarios_directos.total`                 |
| Project type (works vs programme)         | `etapas[].iniciativa.tipologia`                                            |
| Lifecycle stage                           | `etapas[].clasificacion.etapa_actual`                                      |
| Project ID for cross-referencing          | `etapas[].iniciativa.codigo_bip`                                            |

---

## A reading note on multi-etapa records

About 1.7% of records (124 PDFs in the v1 sample) print the same FICHA twice.
The schema captures both copies in `etapas[]`. A warning is emitted in
`extraction.warnings[]` with code `multi_etapa_identical_blocks`. Treat the
two etapas as a single project for case-study work.

---

## A reading note on Spanish characters

The dataset preserves Spanish accents and ñ. If you copy values into another
system (a spreadsheet, a database, a slide deck), make sure it's UTF-8.
