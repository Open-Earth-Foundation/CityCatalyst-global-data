# SUBDERE / SIM — municipal income indicators (BEP)

Comuna-level municipal **income and fiscal-autonomy indicators** published by SUBDERE's Sistema de Información Municipal (SIM) from Contraloría budget-execution reporting. Adopted to replace SINIM as the source of the financial-autonomy axis, because SIM publishes the same indicator without SINIM's non-commercial restriction.

**At a glance**

- **Status:** research. Not production-approved, not in a pipeline, not yet catalog-registered.
- **Coverage:** 346 rows covering 345 comunas plus the Antarctic territory, keyed on 5-digit CUT. Annual workbook, revised in place.
- **Licence:** **commercial reuse supported**. No resource-specific terms are displayed; Chile's Gobierno Digital standard therefore applies **CC0-1.0 by default**. The CC0 assignment is a documented default, not an explicit statement in the workbook. *[verified with qualification]*
- **Headline:** recalculated FCM dependency and autonomy for all 345 project comunas, with no missing values, no median fill and no retired-source data in the release output.

## Why we use it

The financial-autonomy axis of the city-action fundability model has been the binding commercial-use constraint on that product, because its only input was SINIM, whose portal terms authorise use *sin fines comerciales*. SIM publishes the same underlying indicator from the same publisher, derived from Contraloría reporting, with no terms displayed and therefore CC0 by default.

What changes is the **publication surface, not the underlying data**. SIM and SINIM are both SUBDERE, and both ultimately rest on municipal budget-execution reporting. That is not a problem for the licence position, because terms attach to a publication rather than to facts, but the reasoning has to be stated plainly or it will not survive someone noticing the shared publisher. The claim is narrow and defensible: this workbook carries no restriction, so data taken from it carries none.

The indicator is **recalculated from the workbook's budget components**, not relabelled from previously extracted SINIM values. Relabelling would leave the SINIM extract as the true provenance while claiming a different licence, which is the failure mode this release exists to avoid.

## Canonical downloads

**Source:** SUBDERE's public SIM Ciudadano portal.

- **Workbook:** [indicadores-ingresos-municipales-2025.xlsx](https://municipalidades.subdere.gob.cl/descargas/indicadores-bep/indicadores-ingresos-municipales-2025.xlsx)
- **Public index page:** [Indicadores presupuestarios](https://ciudadano.subdere.gob.cl/indicadores-presupuestarios/), which lists annual workbooks without authentication.

**Re-download (this release):** raw lives in `releases/2025/sample/` (gitignored). Fetch the workbook URL above and place it there as `indicadores-ingresos-municipales-2025.xlsx`, then run the notebook. The direct file is anonymously accessible; use the public SIM Ciudadano page above as the canonical landing page rather than the municipality-admin route, which redirects to login.

**Vintage matters.** The workbook is **revised in place** at the same URL. The copy behind this release is stamped *Actualizado al 14-06-2026* in cell A1, and that stamp is carried into every output row as `source_vintage`. A later download can differ even though its URL and filename do not.

**Sheets**

| Sheet | Contents | Role |
| ----- | ----- | ----- |
| `2025` | 346 rows of income indicators, four-row header block | the data |
| `Cumplimiento_2025` | per-municipality monthly reporting compliance, headed *"Informado a Contraloría General de la República"* | provenance and completeness record, not an input |

**Columns used** (workbook label → cleaned column → meaning)

| Workbook label | Cleaned column | Meaning |
| ----- | ----- | ----- |
| IPP (M$) | `ipp_percibido_mclp` / `ipp_devengado_mclp` | permanent own income |
| FCM (M$) | `fcm_percibido_mclp` / `fcm_devengado_mclp` | Fondo Común Municipal received |
| IP (M$) (IPP + FCM) | `ip_percibido_mclp` / `ip_devengado_mclp` | own income including FCM |
| INGRESOS TOTALES (M$) | `ingresos_totales_percibido_mclp` / `..._devengado_mclp` | total income |
| Dependencia de Fondo Común Municipal (%) | recalculated as `fcm_dependency` | FCM ÷ IP, the autonomy input |
| Fondo Común Municipal en Ingresos Totales (%) | recalculated as `fcm_share_total_income` | FCM ÷ total income, a different measure |
| Relación entre Aportes Municipales y Recepción del FCM | `fcm_contribution_ratio` | carried unused; the net contributor or recipient reading |
| Autonomía Operacional Municipal (%) | `operational_autonomy` | carried unused |

**Cleaned output (`releases/2025/data/`):** `sim_municipal_income_2025.csv`, 345 × 16.

## Licence

> **Commercial reuse is supported.** The SIM workbook and public index page declare no contrary terms. Chile's Gobierno Digital open-data standard assigns **CC0-1.0 by default** when a State Administration body publishes a dataset without an explicit licence. This is an inferred application of the national default, not a resource-specific licence notice printed in the workbook. *[verified with qualification]*

The [Gobierno Digital open-data standard](https://wikiguias.digital.gob.cl/Est%C3%A1ndares/Datos-Abiertos) states that, absent an explicit assignment, datasets issued by State Administration bodies are opened under CC0 1.0. Neither the public SIM page nor the workbook displays a reuse, redistribution or commercial-use condition. Article 19 of [Ley 20.285](https://www.bcn.cl/leychile/navegar?idNorma=276363&idParte=8564036&idVersion=2025-07-11) also says delivery of copies under transparency law does not impose use restrictions unless another law provides one. Together these support commercial use, redistribution and derivatives; they do not amount to an explicit dataset-specific licence declaration by SUBDERE.

**Attribution is our convention, not a licence obligation.** CC0 imposes no credit requirement. Provenance is nonetheless recorded on every use, because the chain matters for anyone auditing the figures: *Contraloría General de la República (balance de ejecución presupuestaria), processed and published by SUBDERE's Sistema de Información Municipal.*

The `Fuente: CGR` line in the workbook banner and the compliance sheet's heading are what verify the Comptroller as upstream. The specific system name **SICOGEN II is not stated anywhere in the workbook or on the SIM pages** and is left out of the attribution line rather than asserted. *[unanswered]* SUBDERE's SIM programme page separately describes Dipres as a source for its budget reporting, so the full chain from municipality to workbook is not established; what is established is that the workbook names CGR.

For normal dataset review this is sufficient to mark `commercial_use: true`. If counsel or a customer requires an explicit owner statement rather than the government-wide default, request written confirmation from `sim@subdere.gov.cl`. *(Not legal advice.)*

## Spatial and temporal scope

Geography is the 345 comunas plus the Antarctic territory, keyed on the 5-digit CUT with leading zeros significant. The workbook is annual, one file per year, with earlier years available from the index page. Money is in thousands of nominal pesos (M$), so cross-year comparison needs deflating.

Each money figure appears on two accounting bases. **Percibido** is cash actually received; **devengado** is accrued. They are not interchangeable and can differ substantially, for example Antofagasta's total income of 149.6 bn percibido against 227.9 bn devengado. This release computes the indicator on **percibido**, which is the basis that reproduces the values already in production.

## Interpretation warnings

**Two different FCM ratios sit side by side, and confusing them is the easiest mistake here.** `fcm_dependency` is FCM over *own* income (IPP + FCM); `fcm_share_total_income` is FCM over *total* income. For Iquique they are 15.6% and 7.9%. The model's autonomy axis uses the first. A threshold set against one definition is meaningless against the other.

**The published ratio column can be stale; the components are authoritative.** For Cunco the workbook's stored `Dependencia de FCM` disagrees with its own budget lines by 0.045 pp. Small, but it is the reason this release recalculates rather than reads.

**Money is nominal and the workbook is revised in place.** Year-on-year deltas include inflation, and a re-download changes values without any change of URL or filename. Always carry `source_vintage`.

**The Antarctic row is not a comuna with zero income; it is a non-reporting territory.** It reports zero on every money column, which would compute a meaningless dependency ratio, so it is dropped rather than carried. This row is why the workbook holds 346 rows where the rest of the project holds 345, and it resolves a discrepancy that runs through the whole MEED document set.

**Migration audit: Padre Hurtado needs adjudication.** Before the retired source was removed, its dependency was recorded as 69.7% against 44.0% in this workbook, a 25.6 pp gap. The comparison values are not carried in this release, but the unresolved migration decision remains. *[unanswered]*

**Comunas sitting effectively on an archetype boundary should be read as indeterminate.** Natales has SIM/BEP dependency 0.500008, so its result depends on eight parts per million around the hard 0.5 split. That is a threshold-design issue, not a data defect.

**Devengado totals include accruals that percibido does not.** Using devengado would change the indicator for every comuna and is not what production currently reflects.

## Parsing notes

**Four-row header block, data starts at row 5.** Row 1 is a provenance banner with embedded tabs and newlines, row 2 a merged title, row 3 the column groups (merged across pairs), row 4 the percibido/devengado sub-header. Naive `read_excel` with a single header row returns nonsense.

**Merged cells across column pairs.** Each money measure spans two columns under one merged label, so column names have to be reconstructed positionally rather than read.

**CUT is a string.** Five digits, zero-padded. Read as an integer it silently corrupts every comuna in regions 1 through 9.

**Percentage columns are already fractions.** The columns labelled `(%)` hold values in 0 to 1, not 0 to 100. Multiplying by 100 a second time is the obvious trap.

**One row has null percentage cells.** The Antarctic row divides by zero and the workbook leaves those cells empty rather than writing a sentinel.

**The provenance banner lives in a cell, not in file metadata.** Cell A1 of the data sheet carries the vintage and the source; read it rather than trusting the filename.

## Current approved release

**2025** — research, not in `catalog/index.yaml` yet.

Promotion prerequisites are a spot check on Padre Hurtado, a decision on how boundary comunas such as Natales are treated, and the transformer change that swaps the autonomy input. Once the production indicator is regenerated from this workbook, SINIM is no longer the binding commercial-use restriction on the fundability product.
