# OEF — Chilean municipal technical-capacity tier

A four-tier technical-capacity classification for all **345 Chilean comunas**, derived from census population and two published rules. It is the *capacity* half of the city layer in the climate-action financial-feasibility work, separated out so that it stands on open data alone.

**At a glance**

- **Status:** research. Not production-approved, not in a pipeline, not yet catalog-registered.
- **Coverage:** 345 comunas, 16 regions, keyed on 5-digit CUT. One classification, no time series.
- **Licence:** **CC BY-SA 4.0**, following INE's explicit open-data terms. Commercial use is permitted with attribution and share-alike where the licence applies; the two rules are methodology supplied for this work, not an additional dataset.
- **Headline:** 39% of comunas fall in the second-lowest tier and 12% in the lowest, but those two tiers together hold 10% of the population. Low capacity is a majority-of-places, minority-of-people problem.

## What this is, and why it exists separately

The consuming feasibility model needs a per-comuna reading of institutional capacity: can this municipality formulate a project, pass the public-investment gate and manage a grant. That reading used to be a percentile blend of SINIM staffing indicators, which carried a non-commercial licence term and two documented data defects.

This dataset replaces it with a classification that no longer depends on SINIM at all. It exists as its own review, rather than as a step inside the model, for three reasons: its licence position deserves to be stated once, cleanly; the classification is reusable by anything that needs a coarse municipal capacity reading, not only by the feasibility score; and separating it gives the consuming model a source contract independent of the retired staffing extract.

## How it is built

Two published rules applied in sequence to one population figure.

**Rule 1, population to tramo.** The population brackets used by the MEED *Viabilidad Efectiva Municipal* adjustment.

| Tramo | Label | Population | Comunas |
| ----- | ----- | ----- | ----- |
| T1 | Grandes urbanas | > 100,000 | 57 |
| T2 | Medianas urbanas | 20,000 – 100,000 | 113 |
| T3 | Pequeñas semiurbanas | 5,000 – 20,000 | 133 |
| T4 | Rurales y aisladas | < 5,000 | 42 |

**Rule 2, tramo to capacity.** The MEED *Gobernanza Local* sub-criterion *Capacidad técnica e institucional*, on its native 0/25/50/100 scale and rescaled to a 0–1 axis for consumers that need one.

| Tramo | `gl_technical_capacity` | `capacity` | Stated basis |
| ----- | ----- | ----- | ----- |
| T1 | 100 | 1.00 | own planning unit (SECPLA) and confirmed public-investment execution |
| T2 | 50 | 0.50 | benchmark anchor, unadjusted |
| T3 | 25 | 0.25 | no own SECPLA, no public-investment history in the last three years |
| T4 | < 25 | **0.10** | additional degradation for absence of installed capacity; **value provisional** |

The T4 value is left undefined in the source rule ("menor a 25, a definir") and is filled provisionally at 0.10 here. Every T4 row is flagged with `t4_provisional` so a consumer cannot adopt it unknowingly.

**Output columns**

| Column | Meaning |
| ----- | ----- |
| `comuna_cut` | 5-digit zero-padded CUT, the join key |
| `comuna` | comuna name as published by INE |
| `population` | INE Censo 2024 count |
| `tramo` / `tramo_label` | VEM tier T1–T4 and its Spanish label |
| `gl_technical_capacity` | MEED GL sub-criterion score, 0–100 |
| `capacity` | the same value on a 0–1 axis |
| `capacity_basis` | which rule produced the value, so a consumer can tell this vintage from an earlier one |
| `t4_provisional` | true where the score depends on the undecided T4 band |

## Canonical downloads

There is nothing to download: this dataset is derived, not retrieved.

- **Population** comes from the INE census review already in this repo, `reviews/cl-ine/cl-ine-censo/releases/2024`, which carries its own provenance and re-download instructions.
- **The two rules** come from the MEED methodology documents of June 2026, held with the consuming model's release at `reviews/oef/cl-city-action-fundability/releases/v3/sample/` (gitignored).
- **Rebuild** by running `releases/v1/01_capacity_tier.ipynb` from a clean clone. Restart-and-run-all passes.

## Licence

**CC BY-SA 4.0. Commercial use permitted, with attribution and share-alike.**

The only data input is the INE Censo 2024 population count. INE's [Terms of use and open-data licence](https://www.ine.gob.cl/terminos-de-uso-y-licencia-de-datos-abiertos) apply Creative Commons Attribution-ShareAlike 4.0 International to its open data. That licence permits commercial use and adaptation, requires appropriate credit, and requires adaptations to be shared under the same licence. The two rules applied to population are methodology supplied for this work rather than another copied dataset.

This is a deliberate change of position from the capacity measure it replaces. The earlier measure read SINIM personnel indicators, whose portal terms authorise use *sin fines comerciales* with attribution. This release reads only the INE census table, so it carries no non-commercial source term.

The v3 feasibility city profile pairs this table with SUBDERE SIM/BEP rather than SINIM. The release contains no copied SINIM validation table; structural assertions validate the population brackets directly. Clearing these two city inputs does not clear unrelated finance inputs with their own non-commercial terms. *(Not legal advice.)*

**Attribution:** *Fuente: Censo de Población y Vivienda 2024, Instituto Nacional de Estadísticas (INE), Chile.*

## Spatial and temporal scope

Geography is the 345 comunas of Chile across 16 regions, keyed on the 5-digit CUT with leading zeros preserved. There is no time dimension: this is one classification, from one census. It changes when the census does, or when either published rule is revised, and both are infrequent. A comuna near a bracket boundary can change tier on a small population revision, which is the main way this dataset moves between vintages.

## Interpretation warnings

The traps worth knowing before using a field.

**The tier is population under another name.** It does not measure any comuna's actual staff, budget, systems or delivery record. Two comunas in the same tier score identically by construction, and the staffing data this replaced showed the real within-tier spread is wide.

**T1 asserts more than the data evidences.** The published rule conditions the T1 score on a confirmed planning unit and public-investment execution history. No such evidence is joined here, so T1 is assigned on population alone. Reading a T1 score as proof that a comuna has a SECPLA is reading in a claim that is not there.

**The T4 score is not settled.** It is provisional at 0.10 and flagged per row. In the consuming model this is consequential rather than cosmetic: at 0.10 every action type, including a bare regulation, escalates to needing technical assistance in all 42 T4 comunas.

**Tiers are not a ranking.** The data supports four bands and nothing finer. There is no defensible ordering of comunas within a band, and no basis for reading the gap between bands as a measured quantity.

**Low capacity is not low value.** A low tier means an action is harder to deliver locally or needs an external route. It is a reason to attach support, never a reason to score an action's climate impact lower.

**Most low-capacity comunas are small.** T3 and T4 together are 51% of comunas but 10% of the population. Any national aggregate weighted by comuna rather than by population will overstate how much of Chile sits in the low tiers.

## Parsing notes

**CUT is a string.** Five digits, zero-padded, leading zeros significant. Read as an integer it silently corrupts every Region 1 through 9 comuna.

**Some methodology examples number tramo backwards.** The consultant workbook numbers its raw tramo column 1 to 4 with **1 as rural**, the opposite of the VEM convention used here and throughout the MEED. This release does not ingest that workbook; it applies the documented brackets directly to INE population.

**The census release is long-format.** Population is one `attribute_type` among sixteen; filter before reshaping.

**Comuna counts disagree between sources.** The source methodology note describes 346 comunas throughout, while its own workbook holds 345 and the census holds 345. This release covers 345 and that is the number to quote.

**Bracket edges are exclusive at the top.** T1 is strictly greater than 100,000 and T2 starts at exactly 20,000. Cabildo's census count is 19,983, only 17 people below the T2 boundary, so a small population revision can change its tier without an institutional change.

## Current approved release

**v1** — research, not in `catalog/index.yaml` yet.

Promotion prerequisites are a decision on the T4 band from SSG/OEF, and a decision on whether the T1 score stays population-assigned or becomes evidence-gated on SECPLA and public-investment history. Neither is a data question.
