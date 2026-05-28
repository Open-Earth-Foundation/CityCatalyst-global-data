# SR1.5 Mitigation Feasibility Priors

City-specific socioeconomic feasibility scores for the HIAP-MEED action
catalogue, derived from IPCC SR1.5 (Global Warming of 1.5°C) Chapter 4
Supplementary Material, Tables 4.SM.7 through 4.SM.15, combined with
city-level socioeconomic indicators via literature-cited bridges.

## Intended use

This dataset is designed as **one input feature** in a multi-feature
action ranking model. The full model is expected to combine signals from:

- **Socioeconomic feasibility** (this dataset) — "does the city's
  population profile support this action?"
- **Legal feasibility** — "can the city act here under its jurisdiction?"
- **Policy alignment** — "does this fit existing plans and political will?"
- **Emissions reduction potential** — "how much does it abate?"

Treated as one feature among several, this dataset is **v1-shippable**:
the output is an interpretable, traceable, literature-anchored signal
that complements rather than duplicates the other feasibility channels.
It should be used as an **ordinal** signal (relative ordering of actions
is more reliable than absolute values) and standardised alongside the
other features before downstream weighted combination.

**Design choices:**
- Archetype layer uses **SR1.5's native mitigation option names verbatim**
  (27 options across 9 SM tables). Every cell traces to a specific
  published IPCC table.
- City-data adjustment is gated by the **A/C rule**: only IPCC-coded
  directional findings receive city adjustment (see below).
- Bridges from SR1.5 indicators to city indicators are restricted to
  **strong, literature-cited** relationships only.

**Known scope:** the feature provides strongest discrimination on the
Economic, Socio-cultural, and (since the land-cover bridges were added)
Geophysical dimensions, where the bridges are conceptually robust. The
Environmental dimension is only partially active — `biodiversity` has
bridges through forest- and wetland-cover shares, but air-pollution and
toxic-waste channels still inherit the SR1.5 prior. The
non-`institutional_capacity` slice of the Institutional dimension also
inherits the prior. Downstream models should not expect this feature to
differentiate cities on those still-prior-only channels.


## Background — what is this dataset?

### What SR1.5 is

SR1.5 is the IPCC's *Special Report on Global Warming of 1.5°C*, published
in 2018. It established that limiting warming to 1.5°C requires global
emissions to roughly halve by 2030 and reach net-zero around 2050.

### What Chapter 4 does

Chapter 4, *Strengthening and Implementing the Global Response*, was the
first major IPCC chapter to address a question that previous reports had
ducked: not just *what mitigation options exist*, but **how feasible those
options are to actually deploy at scale**. Policymakers had been frustrated
that earlier reports listed solutions without saying how realistic each one
was to roll out.

### What the feasibility tables (4.SM.7–4.SM.15) actually contain

For each of ~25 mitigation options (Solar PV, Wind, Public transport,
Low/zero-energy buildings, Energy efficiency, Afforestation, etc.), the
Chapter 4 authors scored the option across **six kinds of barrier**:

- **Economic** — does it cost too much; do workers benefit
- **Technological** — is the tech mature; can it be scaled
- **Institutional** — will governments and regulators accept it
- **Socio-cultural** — will the public accept it; does it benefit health
- **Environmental** — does it have ecological co-benefits or trade-offs
- **Geophysical** — does the planet actually have the resources / land

For every option, on every dimension, they assessed multiple specific
indicators (like "cost-effectiveness", "technical scalability", "political
acceptability"). For each indicator they read the peer-reviewed literature
and coded the cell as **A** (real barrier), **B** (neutral), or **C** (no
barrier). Every cell carries citations.

So the document is essentially: *as of 2018, here is the global scientific
consensus on how hard each climate mitigation option is to deploy,
dimension by dimension, with the receipts.*

### What "priors" means

A **prior** is a statistical term for *what you believe before you look at
any specific case*. If someone asks "how feasible is residential retrofit
in city X?" and you have no information about city X yet, the IPCC table
is your best general guess — "globally, retrofit is economically feasible
on average, technologically high, institutionally medium, …". That global
guess is the prior.

When we then look at a specific city's data (its income, infrastructure,
governance), we *adjust* the prior to get a city-specific answer. The city
data doesn't replace the prior; it modifies it.

So the dataset in this folder is: **the global starting belief about how
feasible each option is, before we know anything about a specific city.**
The scoring engine takes that starting belief and adjusts it for the
actual city in question.

## Releases from IPCC — why SR1.5 (2018) is still the source

**For per-mitigation-option multidimensional feasibility, SR1.5 Ch.4
remains the most recent IPCC source.** AR6 WGIII (2022) chose a different
framing for mitigation — *cost and abatement potential* (Figure SPM.7 right
panel, dataset #6119) — so it didn't produce an updated equivalent. Adjacent
IPCC products since 2018:

- **AR6 WGII #5916 (2022)** — multidimensional feasibility for *adaptation*
  options. Use when the catalogue extends to adaptation.
- **AR6 WGIII Ch.3 §3.8 (2022)** — multidimensional feasibility at the
  *scenario* level (drawing on Brutschin et al. 2021). Complementary, not
  a per-option replacement.
- **AR6 WGIII Ch.17 (2022)** — enabling-conditions framing; better source
  for cross-cutting / strategic-planning archetypes than SR1.5.
- **AR6 SYR (2023) Figure SPM.7** — confirmed the asymmetric framing:
  adaptation = multidimensional feasibility, mitigation = cost & potential.

**Recheck triggers**: AR7 Special Report on Climate Change and Cities
(expected early 2027) is the most likely near-term IPCC product to update
this. AR7 WGIII follows ~2028.


## Files

Canonical inputs live in `data/`. A sample city-indicator input and the
notebook's ranked-action outputs live in `sample/`. The notebook
`scorer_simple.ipynb` sits at the release root.

| File | Rows | Status | Purpose |
|---|---|---|---|
| `data/actions_to_sr15_mapping.csv` | 102 | canonical | Each catalogue action mapped to one or more SR1.5 mitigation options. Includes `match_strength` and `mapping_rule`. |
| `data/sr15_feasibility_per_cell.csv` | 547 | canonical | Per-indicator A/B/C/NE/LE codes extracted from SR1.5 Ch.4 SM Tables 4.SM.7–15. |
| `data/sr15_indicator_to_city_indicator.csv` | 54 | canonical | Indicator-level bridge: 39 active bridges + 15 option-level constants. Each active row cites its literature lineage. |
| `data/sr15_cell_bridge.csv` | 598 | regenerated | Cell-level bridge: one row per (option × dimension × indicator × city_indicator) once scope-matched bridges are attached. |
| `data/scoring_chain.csv` | 1,900 | regenerated | Full provenance chain — one flat row per (action × option × dimension × global_indicator × city_indicator), with `interpretation` text. Backs the API. |
| `data/api/feasibility-api.md` | n/a | canonical | Endpoint specification for `GET /api/v1/cities/{locode}/action-mitigation-feasibility-scores`. |
| `data/api/example_response.json` | n/a | canonical | Full sample API payload mirroring the scoring-chain schema. |
| `scorer_simple.ipynb` | n/a | engine | Self-contained Jupyter notebook (release root). Reads the three canonical inputs in `data/` and the city-indicators file in `sample/`, then regenerates the four derived CSVs above. |
| `archive/actions_to_sr15_mapping.pre_single_primary.csv` | n/a | archive | Pre-single-primary snapshot of the action mapping, retained for diffing. |

## City indicators used by the strong bridges

The 39 active bridges in `sr15_indicator_to_city_indicator.csv` reference
23 distinct city indicators. The sample `test_cities_indicators.csv`
extracts all of them (plus `population` as context metadata).

**Socioeconomic indicators (Chile sources — cl-casen 2022, cl-ine-censo 2024):**

| City indicator | Bridges to | # bridges |
|---|---|---|
| median_household_income | cost-effectiveness | 1 |
| poverty_rate | cost-effectiveness, distributional_effects, inclusiveness | 3 |
| unemployment_rate | employment_productivity | 1 |
| employment_construction | employment_productivity | 1 |
| employment_manufacturing | employment_productivity, institutional_capacity, technical_scalability | 3 |
| employment_in_transport_and_logistics | employment_productivity, institutional_capacity | 2 |
| employment_electricity_gas | institutional_capacity | 1 |
| electricity_access_rate | technical_scalability | 2 |
| fixed_internet_household_share | technical_scalability | 2 |
| home_ownership | distributional_effects, public_acceptance | 2 |
| renter_share | distributional_effects, public_acceptance | 2 |
| mean_years_schooling | human_capabilities | 1 |
| literacy_rate | human_capabilities | 1 |
| disability_prevalence | inclusiveness | 1 |
| indigenous_identification_rate | inclusiveness, public_acceptance | 2 |

**Land-cover indicators (geospatial sources — ESA WorldCover / MapBiomas-style shares):**

| City indicator | Bridges to | # bridges |
|---|---|---|
| urban_built_share | physical_feasibility | 4 |
| cropland_share | physical_feasibility | 1 |
| pasture_share | physical_feasibility | 1 |
| grassland_share | physical_feasibility | 1 |
| shrubland_share | physical_feasibility | 1 |
| primary_forest_share | physical_feasibility, biodiversity | 2 |
| secondary_forest_share | physical_feasibility, limited_land_use | 2 |
| wetland_share | physical_feasibility, biodiversity | 2 |

`population` and several auxiliary land-cover shares (e.g.
`silviculture_share`, `water_share`, `beach_dune_share`, `ice_snow_share`,
`other_bare_share`) are extracted in `test_cities_indicators.csv` for
completeness but do not participate in any strong bridge — kept as
context metadata only.

**One signed-bridge tension worth noting.** `indigenous_identification_rate`
appears with opposite signs in two SR1.5 channels: **+1** for
`public_acceptance` in NBS contexts (cultural alignment with traditional
land management — Garnett et al. 2018, Fa et al. 2020), and **−1** for
`inclusiveness` across all options (historically marginalized groups need
explicit inclusion strategies — Whyte 2017, FAO 2021). Both signs are
defensible in their respective channels.

## How the SR1.5 AVG formula treats each code

SR1.5 Tables 4.SM.5 and 4.SM.6 define how indicator-level A/B/C/NA/NE/LE codes
aggregate to the dimension-level AVG score. Each code contributes differently:

| Code | Numerator contribution | Denominator contribution | Effect on dimension AVG |
|---|---|---|---|
| **A** (barrier) | 1 | 1 | Drags AVG down toward 1.0 |
| **B** (neutral) | 2 | 1 | Anchors AVG at the midpoint 2.0 |
| **C** (supportive) | 3 | 1 | Drags AVG up toward 3.0 |
| **NE** (no evidence) | 0 | 1 | Drags AVG down (each NE counts as worse than A) |
| **LE** (limited evidence) | 0 | 1 | Drags AVG down (same as NE) |
| **NA** (not applicable) | 0 | 0 | Does not contribute at all |

Two consequences worth knowing:

- **B is not "ignored."** A dimension full of B cells gets banded as `medium`
  (AVG = 2.0). The IPCC's neutral finding is itself a contribution to the score.
- **NE/LE are pessimistic.** Missing or limited evidence pulls the AVG *down*
  rather than being dropped. SR1.5's stance is that absence of evidence is not
  the same as evidence of feasibility. There is an overriding rule (4.SM.6): if
  more than 50% of effective indicators are NE/LE, the dimension is marked
  `insufficient_evidence` and the AVG is suppressed entirely.

## Scoring an action for a city

The scoring engine produces **one feasibility feature value per (action,
city)** pair. The output is intended to be one input to a downstream
multi-feature ranking model — not a final action ranking on its own.

The engine has two layers: the **SR1.5 prior** (global average from
IPCC) and the **city-data adjustment** (local modification). Joins:

```
action_id  →  sr15_options                       (actions_to_sr15_mapping.csv)
sr15_option × dimension × indicator → A/B/C/...  (sr15_feasibility_per_cell.csv)
sr15_option × indicator × city_indicator → sign  (sr15_cell_bridge.csv)
city × city_indicator  →  city_value             (sample/test_cities_indicators.csv)

dimension AVG = SR1.5 Table 4.SM.5 formula applied to the per-cell codes
                (computed inline by the notebook — no standalone CSV)

score = mean over dimensions of
          (sr15_avg_score / 3.0)                ← SR1.5 prior
          × (1 + α · city_adjustment)            ← city-data multiplier
```

If `sr15_options` contains multiple options separated by `|`, average their
priors across all listed options.

### The A/C rule for city-data adjustment

**City-data adjustments are only authorised on cells where SR1.5 found a
directional verdict** — i.e., cells coded A (barrier) or C (supportive).
Cells coded B, NE, LE, or NA do NOT receive city-data adjustment because:

- **B** — SR1.5 found no consistent directional effect in the global
  literature. We have no warrant to assert directionality from city data.
- **NE / LE** — SR1.5 found no or limited peer-reviewed evidence. We
  cannot author a directional bridge without primary literature.
- **NA** — IPCC marked the indicator not applicable to this option.

Under this rule:

- Of the 547 cells in `sr15_feasibility_per_cell.csv`, **261 are A or C**
  (48%) and are eligible for city-data adjustment.
- Of those, **127 currently have a scope-matched city bridge** that
  provides active discrimination.
- The remaining 134 A/C cells contribute to the score via the SR1.5 prior
  only — no city adjustment (they appear in `sr15_cell_bridge.csv` with
  `city_indicator = '(no scope-matching bridge)'`).
- The B/NE/LE cells appear in `sr15_cell_bridge.csv` with a placeholder
  `city_indicator` value (e.g. `(SR1.5 code B: no directional evidence)`)
  to keep the chain fully enumerated for the API view.

This is methodologically conservative but defensible: every city-data
adjustment in the system can be traced to an IPCC-published finding that
the indicator matters for this option.

### Quality threshold: strong bridges only

The bridges in `sr15_indicator_to_city_indicator.csv` are deliberately
restricted to **bridges with clear literature lineage**. Each active
bridge row cites canonical empirical work (e.g., split-incentive
literature for tenure → distributional_effects; energy-poverty literature
for poverty → cost-effectiveness; Sen's capability framework for
education → human_capabilities).

The decision rule was: a bridge stays if its sign claim is supported by
peer-reviewed empirical literature; otherwise it goes. The result is a
smaller but more defensible bridge set.

**Dimensions that mostly retain SR1.5 prior unmodified**:

- **Environmental**: largely unchanged — only `biodiversity` has active
  bridges (primary/secondary/wetland forest shares). Air-pollution and
  toxic-waste channels still inherit the SR1.5 prior; closing them would
  need satellite air-quality / pollutant-inventory data.
- **Geophysical**: now partially active. `physical_feasibility` is the
  largest single channel in the bridge set (11 dictionary rows → 17
  cell-level bridges) and uses land-cover shares (`urban_built_share`,
  `cropland_share`, `pasture_share`, `grassland_share`, `shrubland_share`,
  `primary_forest_share`, `secondary_forest_share`, `wetland_share`)
  sourced from ESA WorldCover / MapBiomas-style products. The
  `limited_land_use`, `water_use`, and `limited_scarce_resources`
  channels still inherit the prior.
- **Institutional** (mostly): `political_acceptability`,
  `legal_admin_acceptability`, `transparency_accountability` all
  retreated to option-level. Better source would be a national
  governance index (WGI). Only `institutional_capacity` retains active
  city bridges (sector-employment proxies for buildings, transport,
  manufacturing, and electricity/gas utilities).

Cities in the system are now discriminated primarily on the **Economic**,
**Socio-cultural**, and **Geophysical** dimensions, where the bridges are
conceptually strong. **Environmental** (apart from `biodiversity`) and the
non-capacity slice of **Institutional** inherit the SR1.5 prior largely
unchanged.

### Active bridge count by SR1.5 indicator

Counts of A/C cells with a scope-matched city bridge attached
(`sr15_cell_bridge.csv` filtered to `sr15_code ∈ {A, C}` and a real
`city_indicator`).

| SR1.5 indicator | Active cell-level bridges |
|---|---|
| cost-effectiveness | 34 |
| physical_feasibility | 17 |
| technical_scalability | 16 |
| inclusiveness | 15 |
| human_capabilities | 14 |
| distributional_effects | 9 |
| employment_productivity | 9 |
| institutional_capacity | 7 |
| public_acceptance | 3 |
| limited_land_use | 3 |
| **Total** | **127** |

The two new entries since the previous revision are `physical_feasibility`
(land-cover shares feeding the Geophysical dimension) and an expanded
`technical_scalability` channel; the `public_acceptance` count has tightened
as `home_ownership` / `renter_share` bridges were re-scoped to
`distributional_effects` where the literature is stronger.

## Match-strength distribution (102 actions)

- **direct (62)** — action's profile clearly maps to one SR1.5 option (includes 3 smart-grid actions reclassified from `rule_eff_renewable` to `Smart grids` via description-keyword matching)
- **partial (10)** — action maps but with a caveat (e.g., generic renewable channel averaged across Wind/Solar/Bioenergy)
- **weak (14)** — mostly waste actions; SR1.5 covers only food waste, so general MSW gets the food-waste prior with low confidence. Also includes 3 actions reclassified as scale-mismatch with Bioenergy: household biodigesters (`icare_0033`), pilot BECCS (`ipcc_0068`), and CCS-via-biogas (`icare_0082`) — the SR1.5 Bioenergy option assesses utility-scale and overstates land-use/water barriers for small-scale applications
- **cross_cutting (15)** — enabling, financial-instrument, and regulatory-standard actions that have no specific SR1.5 option. Use AR6 WGIII Ch.17 enabling-conditions framework instead
- **no_match (1)** — hydropower (not in SR1.5 Ch.4 SM mitigation options)

## SR1.5 color → code legend (Table 4.SM.6)

The cells in the SR1.5 SM tables encode A/B/C verdicts as colored bars, not
text. The decoded colors:

| Color (RGB ≈) | Code | Meaning |
|---|---|---|
| Dark brown (0.52, 0.24, 0.04) | C / AVG > 2.5 | Indicator does not pose a barrier |
| Medium orange (0.96, 0.69, 0.52) | B / 1.5 < AVG ≤ 2.5 | Neutral |
| Light peach (0.98, 0.89, 0.84) | A / AVG ≤ 1.5 | Indicator could block feasibility |
| Grey (0.68, 0.67, 0.67) | NA | Not applicable |
| White | NE/LE | No / limited evidence |

## Known limitations and caveats for downstream model use

Each limitation below is documented as a caveat for the downstream
ranking model rather than a blocker to shipping this feature.

1. **Delivery-mode collapse.** SR1.5 does not distinguish voluntary vs
   mandatory vs means-tested delivery of the same intervention. Retrofit
   archetypes with different delivery modes share the same prior. The
   downstream model should not expect this feature to differentiate
   delivery modes — that signal must come from policy alignment or a
   future v2 sub-archetype split.
2. **Targeting / equity dimension.** Low-income weatherisation gets the
   same prior as voluntary retrofit. Income-gradient evidence is a v2
   task; the equity channel is currently only partially captured (via
   the `inclusiveness` and `distributional_effects` indicators).
3. **Waste coverage is thin.** SR1.5 covers only food waste; municipal
   solid waste, recycling, PAYT not in the option set. 13 actions are
   flagged `match_strength = weak` on this basis — the downstream model
   should reduce confidence on those rows.
4. **Strategic / enabling actions** (15 actions) have no SR1.5 home and
   are excluded from the feature output. The downstream model should use
   policy alignment / legal feasibility features for these. AR6 WGIII
   Ch.17 enabling-conditions framework is the better future source.
5. **Urban NBS** (urban_green, wetland, peatland, fire_mgmt) are proxied
   onto Afforestation & reforestation with a weak-match flag.
6. **Hydropower** is not in SR1.5 Ch.4 SM (1 action excluded).
7. **Environmental dimension still mostly inactive** — only
   `biodiversity` now has city bridges (via primary/secondary/wetland
   forest shares). `air_pollution`, `toxic_waste`, `social_co_benefits`,
   and `absence_of_risk` channels still inherit the SR1.5 prior
   unmodified. Geophysical was the major v1 gap and is now substantially
   closed through the `physical_feasibility` land-cover bridges, but
   `water_use` and `limited_scarce_resources` remain prior-only and would
   benefit from hydrological / critical-minerals data in v1+.
8. **Quintile bucketing** of city indicators loses signal — a city at
   the 21st percentile and one at the 39th percentile both score `low`
   (0.25 capacity). For relative ranking within a country this is
   acceptable; for cross-country comparison the quintiles need
   re-calibration.
9. **Scoring math is heuristic.** The `(sr15_signal + bridge_mean)/2`
   averaging and the uniform per-dimension weight are face-valid
   defaults, not statistically derived. The downstream model should
   treat this feature's output as **ordinal** signal (relative ordering
   of actions) and standardise alongside the other features before
   weighted combination.
10. **Vintage.** SR1.5 is from 2018. Cite as the 2018-vintage prior in
    any reports; recheck when AR7 Special Report on Climate Change and
    Cities lands (expected early 2027).

## Methodology summary

1. **Extracted** A/B/C/NA codes from the colored cell encoding in SR1.5
   Ch.4 SM Tables 4.SM.7–4.SM.15 using `pdfplumber`. Color palette and
   thresholds per Table 4.SM.6.
2. **Aggregated** per-indicator codes to dimension-level AVG scores using
   the SR1.5 formula.
3. **Mapped** each catalogue action to one or more SR1.5 options via rules
   over `primary_outcome`, `primary_intervention`, `primary_channel`, and
   description-text disambiguation for the new-build-vs-retrofit case.
4. **Verified** spot-checks against rendered PDF pages 32 and 35–36 — all
   sampled cells matched.

## Citation

de Coninck, H., Revi, A., Babiker, M. et al. (2018). Strengthening and
Implementing the Global Response. In: IPCC, *Global Warming of 1.5°C*
(SR1.5), Chapter 4, Supplementary Material.
https://www.ipcc.ch/sr15/

## API contract

The endpoint specification for the consumer-facing API
(`GET /api/v1/cities/{locode}/action-mitigation-feasibility-scores`) lives
at [`data/api/feasibility-api.md`](data/api/feasibility-api.md), with a
full sample payload at
[`data/api/example_response.json`](data/api/example_response.json). Both
mirror the schema in `data/scoring_chain.csv`. The API replaces the
earlier 510-row `action_socioeconomic` placeholder CSV and the
HIAP-MEED `socioeconomicIndicators` block in `actions_api_mock.json`.