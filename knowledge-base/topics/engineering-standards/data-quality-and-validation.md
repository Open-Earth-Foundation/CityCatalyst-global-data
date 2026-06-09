# Data Quality & Validation

## Philosophy

Emissions and climate data is **estimated**, not measured. Two valid methodologies applied to the same city can produce legitimately different numbers. This means traditional validation — "check the value against the expected answer" — does not fully apply to our work.

Our validation goal is not to confirm correctness, but to detect anomalies and ensure consistency. We can credibly say:

- "This data is internally coherent"
- "This value is plausible given what we know about this context"
- "This looks unusual here is why we investigated and what we found"

What we cannot always say is "this is the right number." That is not a failure of our process it is an honest reflection of the nature of climate data. The standard we hold ourselves to is transparency and defensibility, not false precision.

When something unusual is found, the right response is often **documentation, not rejection**. A value that is 40% higher than last year is not automatically wrong but it needs a recorded explanation.

---

## Three Layers of Quality

### Layer 1 — Source Assessment

This happens before any pipeline work begins, in Phase 1 and Phase 2 of a project. It answers the question: *is this data source worth building with?*

**Methodology review** — a technical review of the source's documentation, assessing scientific credibility, alignment with GPC standards, known limitations, and fitness for our use case. Assumptions and limitations should be explicitly documented and carried forward into the dataset metadata.

**Data Scoring** — apply the [Data Scoring Framework](https://www.notion.so/openearth/Data-Scoring-Framework-233eb557728b806cb162cfd9fc66925a) to produce a categorical score across Technical Documentation, Activity Data, Emission Factors, Methodology, Spatial Granularity, Coverage, and Types of Gases. This score should be recorded in the project repo and referenced in the dataset metadata.

The outcome of Layer 1 is a documented decision: this source is fit for purpose, with these limitations, assessed to this score.

---

### Layer 2 — Structural Validation

This runs automatically at every pipeline execution. It answers the question: *does the data have the right shape?*

These checks are fully automatable using Mage test decorators and should be applied consistently at each stage boundary. A structural failure is a **hard fail** — the pipeline stops and the issue must be resolved before data progresses to the next stage.

**Checks to apply at every stage:**

- All expected columns are present with the correct names
- Column types match the schema (no numeric values stored as strings, etc.)
- No null values in required fields
- No duplicate records where uniqueness is expected
- Row count is non-zero and within a plausible range for the dataset

**Additional checks at specific stages:**

| Stage | Additional checks |
|---|---|
| `files` | File is readable and in the expected format; expected file structure matches |
| `raw_data` | All expected locodes are present; expected reporting years are covered; no values in columns that should be empty at this stage |
| `modelled` | All expected GPC sectors are present; `locode` values exist in the reference cities table; `reporting_year` is within expected range |
| `reporting` | Aggregation totals are consistent with modelled layer; no orphaned records |

---

### Layer 3 — Consistency & Plausibility Checks

These run as part of the pipeline but produce **flags for investigation**, not automatic hard failures. They answer the question: *do the values make sense?*

The distinction from Layer 2 is important: a plausibility flag means "this warrants a look," not necessarily "this is wrong." The response to a flag is investigation and documentation, not automatic rejection.

**Consistency checks** (can be largely automated):

- Sub-sector totals add up to sector totals within an acceptable tolerance
- Year-over-year change in emissions does not exceed a defined threshold without a documented reason (suggested: flag anything over 30% change)
- The same emission factor is applied consistently across all records where it should be identical
- No negative emissions values in sectors where the methodology does not allow for carbon sequestration
- Per-capita emissions fall within a broad plausible range for the city's population size and income context

**Plausibility checks** (require domain knowledge to define, per dataset):

These cannot be fully generalised — the valid range for an emission factor or activity metric depends on the sector, geography, and methodology. For each new dataset, the responsible team member should define the plausibility bounds, and these should be documented alongside the sample data.

Examples of what these look like in practice:
- Emission factors for a given fuel type fall within known approximate ranges from IPCC guidance
- Electricity emission factors are consistent with the country's grid mix and recent published values
- Transport activity figures are broadly consistent with population size and urban density

---

## Failure Handling

| Check type | On failure | Response |
|---|---|---|
| Structural (Layer 2) | Hard fail — pipeline stops | Fix the issue before re-running; do not manually override |
| Consistency / plausibility (Layer 3) | Soft flag — pipeline continues, flag is logged | Investigate, document the finding, confirm or escalate |

All flags should be recorded. If an investigation concludes the value is correct despite looking unusual, that conclusion and its reasoning should be written into the dataset notes or pipeline comments. Flags that are silently ignored are not acceptable — the investigation is part of the quality standard.

---

## Tooling

We currently use **Mage test decorators** for automated checks. The expectation is that all Layer 2 structural checks are implemented as test decorators on the relevant pipeline blocks. Layer 3 checks should also be implemented in Mage where possible, with output logged clearly as flags rather than failures.

There is no requirement to adopt additional validation tooling (e.g. Great Expectations, dbt tests) at this stage. If the complexity of validation grows, this decision should be revisited — but the framework above should be achievable with what we already have, applied more systematically than at present.
