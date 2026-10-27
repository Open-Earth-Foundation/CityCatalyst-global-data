# SR1.5 Mitigation Feasibility Priors — release 2018-v2

City-specific socioeconomic feasibility scores for the HIAP-MEED action catalogue, derived from IPCC SR1.5 (Global Warming of 1.5°C) Chapter 4 Supplementary Material, Tables 4.SM.7 through 4.SM.15, combined with city-level socioeconomic indicators via literature-cited bridges.

## What 2018-v2 is

The underlying IPCC evidence base is unchanged: SR1.5 is still a 2018-vintage source, and the extracted A/B/C codes and the action mapping are byte-identical to the `2018` release. **2018-v2 is a scoring-methodology release, not a new publisher vintage.** It exists because the v1 scorer let one city measurement earn weight once per conceptual pathway it was bridged to. `poverty_rate` was bridged to `cost-effectiveness`, `distributional_effects` and `inclusiveness`, so on the transport actions it moved the score three times over. Review feedback on the City Fit report raised this as a High finding, on two grounds: the same indicator was effectively double- or triple-counted, and a reader had no way to see how the three uses were weighted against each other.

**The rule this release adopts is one city indicator, one channel.** Each city indicator now reaches an action score through at most one SR1.5 indicator. Six bridge rows were retired and one re-issued on a different channel to make that true; the retired rows stay in the dictionary with their literature lineage and a note recording why, so nothing is lost from the record. The scoring arithmetic is untouched — the whole change lives in the bridge dictionary, which is a place a reviewer can read. Full rationale and the channel-selection reasoning are under [Scoring an action for a city](#scoring-an-action-for-a-city).

This moves scores more than a reweighting would have. 492 of 1,032 (action × city) rows change, across 57 of 86 scoreable actions, in the range −0.083 to +0.063. Within-city ranking correlation with the 2018 release runs from 0.932 to 0.996, and five of the twelve sample comunas see their top ten change. **Treat 2018-v2 as a re-ranking, not a refinement**, and re-baseline anything downstream that was tuned against 2018 outputs.

The `2018` release stays in place as the pre-change baseline. Nothing points production at 2018-v2 until the chain table is reloaded and the `action_score` naming is ported into `CityCatalyst/global-api` — see [API contract](#api-contract).

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

**Known scope:** the feature provides strongest discrimination on the Economic, Socio-cultural and (since the land-cover bridges were added) Geophysical dimensions, where the bridges are conceptually robust. The Environmental dimension is inactive in practice: `biodiversity` has dictionary bridges through forest- and wetland-cover shares, but SR1.5 codes that cell B or NE everywhere they could apply, so none of them reaches a live cell. **As of 2018-v2 the Institutional dimension inherits the prior entirely** and no longer differentiates cities at all: its only bridged channel was `institutional_capacity`, whose three sector-employment bridges were consolidated onto `employment_productivity` under the one-channel rule. Downstream models should not expect this feature to differentiate cities on those prior-only channels.


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
| `data/sr15_indicator_to_city_indicator.csv` | 55 | canonical | Indicator-level bridge: 34 live bridges + 15 option-level constants + 6 rows retired under CC-718. Each row cites its literature lineage; retired rows also carry the reason they were retired in `status_note`. |
| `data/sr15_cell_bridge.csv` | 596 | regenerated | Cell-level bridge: one row per (option × dimension × indicator × city_indicator) once scope-matched bridges are attached. 108 rows carry a live bridge, down from 127 in the 2018 release. |
| `data/scoring_chain.csv` | 1,895 | regenerated | Full provenance chain — one flat row per (action × option × dimension × global_indicator × city_indicator), with `interpretation` text. Backs the API. New in 2018-v2: `release_id`. The notebook asserts that each (action, city indicator) pair appears on exactly one `global_indicator`, which is what makes a per-indicator filter of this file return one row per action. |
| `data/api/feasibility-api.md` | n/a | canonical | Endpoint specification for `GET /api/v1/cities/{locode}/action-mitigation-feasibility-scores`. |
| `data/api/example_response.json` | n/a | canonical | Full sample API payload mirroring the scoring-chain schema. |
| `scorer_simple.ipynb` | n/a | engine | Self-contained Jupyter notebook (release root). Reads the three canonical inputs in `data/` and the city-indicators file in `sample/`, then regenerates every derived artifact above, runs the CC-718 regression checks, and renders the before/after sensitivity. |

## City indicators used by the strong bridges

The 34 live bridges in `sr15_indicator_to_city_indicator.csv` reference 23 distinct city indicators. The sample `test_cities_indicators.csv` extracts all of them (plus `population` as context metadata).

Under the one-channel rule, `# bridges` above 1 no longer means an indicator can be counted twice within an action — it means the same channel applies at several sector scopes (`urban_built_share` on `physical_feasibility` across four families), or that two channels exist but never both carry an A/C verdict for the same option. The six indicators in the latter category are marked **†** and are watched by an assertion rather than curated; see [Bridges that are multi-channel but dormant](#bridges-that-are-multi-channel-but-dormant).

**Socioeconomic indicators (Chile sources — cl-casen 2022, cl-ine-censo 2024):**

| City indicator | Bridges to | # bridges | Changed in 2018-v2 |
|---|---|---|---|
| median_household_income | cost-effectiveness | 1 | |
| poverty_rate | cost-effectiveness | 1 | retired from `distributional_effects`, `inclusiveness` |
| unemployment_rate | employment_productivity | 1 | |
| employment_construction | employment_productivity | 1 | |
| employment_manufacturing | employment_productivity | 1 | retired from `institutional_capacity`, `technical_scalability` |
| employment_in_transport_and_logistics | employment_productivity | 1 | retired from `institutional_capacity` |
| employment_electricity_gas | employment_productivity | 1 | moved from `institutional_capacity` |
| electricity_access_rate | technical_scalability | 2 | |
| fixed_internet_household_share | technical_scalability | 2 | |
| home_ownership † | distributional_effects, public_acceptance | 2 | |
| renter_share † | distributional_effects, public_acceptance | 2 | |
| mean_years_schooling | human_capabilities | 1 | |
| literacy_rate | human_capabilities | 1 | |
| disability_prevalence | inclusiveness | 1 | |
| indigenous_identification_rate † | inclusiveness, public_acceptance | 2 | |

**Land-cover indicators (geospatial sources — ESA WorldCover / MapBiomas-style shares):**

| City indicator | Bridges to | # bridges |
|---|---|---|
| urban_built_share | physical_feasibility | 4 |
| cropland_share | physical_feasibility | 1 |
| pasture_share | physical_feasibility | 1 |
| grassland_share | physical_feasibility | 1 |
| shrubland_share | physical_feasibility | 1 |
| primary_forest_share † | physical_feasibility, biodiversity | 2 |
| secondary_forest_share † | physical_feasibility, limited_land_use | 2 |
| wetland_share † | physical_feasibility, biodiversity | 2 |

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

The scoring engine produces **one feasibility feature value per (action, city)** pair. The output is intended to be one input to a downstream multi-feature ranking model, not a final action ranking on its own.

The engine has two layers: the **SR1.5 prior** (the global verdict from IPCC) and the **city-data adjustment** (the local modification). Joins:

```
action_id  →  sr15_options                       (actions_to_sr15_mapping.csv)
sr15_option × dimension × indicator → A/B/C/...  (sr15_feasibility_per_cell.csv)
sr15_option × indicator × city_indicator → sign  (sr15_cell_bridge.csv)
city × city_indicator  →  city_value             (sample/test_cities_indicators.csv)
```

Only A/C cells are scored, per the A/C rule below. Each such cell blends its IPCC verdict with the city's bridged indicators 50/50, and cells roll up by unweighted mean within a dimension and then across dimensions:

```
sr15_signal      = +1 if C (supportive)  |  -1 if A (barrier)
city_capacity    = QUINT[city bucket]                          # 0.00 / 0.25 / 0.50 / 0.75 / 1.00
bridge_contrib   = bridge_sign × (2 × city_capacity − 1)       # −1 to +1
cell_score       = (sr15_signal + mean(bridge_contrib)) / 2    # = sr15_signal if the cell has no live bridge
cell_score_01    = (cell_score + 1) / 2                        # 0 to 1

raw_score        = mean over dimensions of (mean cell_score_01 within the dimension)
action_score     = 0.5 + STRENGTH_WEIGHT[match_strength] × (raw_score − 0.5)
```

The arithmetic is unchanged from the 2018 release. All of CC-718 lives in the bridge dictionary, so there is no weighting step to justify.

`STRENGTH_WEIGHT` shrinks the headline score toward neutral where the SR1.5 option only loosely describes the action: direct 1.00, partial 0.95, cross_cutting 0.90, weak 0.85, no_match 0.00. The per-dimension scores stay unshrunk, because they describe the IPCC-plus-city evidence and are independent of how confidently the action was mapped. Both values are published: `raw_score` and `score` in the ranked CSV, `raw_action_score` and `action_score` in the API payload.

Actions map to exactly one SR1.5 option in the current mapping. The multi-option averaging the earlier revision of this document described is not exercised by any row in `actions_to_sr15_mapping.csv`.

> **Correction, 2018-v2.** The `2018` revision of this section published `score = mean over dimensions of (sr15_avg_score / 3.0) × (1 + α · city_adjustment)`, an SR1.5-AVG-based formula with a multiplicative city term and a free parameter α. No release ever implemented it — the notebook, the API specification and the production SQL function have always run the signal-and-blend formula above. The formula shown here is the one the code runs.

### One indicator, one channel (CC-718)

**The problem.** A single city measurement could be bridged to several SR1.5 indicators, each of which is a separate cell in the rollup. `poverty_rate` was bridged to `cost-effectiveness`, `distributional_effects` and `inclusiveness`; `employment_manufacturing` to `employment_productivity`, `institutional_capacity` and `technical_scalability`. Every additional pathway added weight, so one measurement could move an action score two or three times over. Of 86 scoreable actions, 31 carried at least one repeated indicator, and in the worst case a single measurement commanded 0.125 of the 0–1 score range against 0.0625 for a single-channel indicator.

**The rule.** Each city indicator reaches an action score through at most one SR1.5 indicator. Six bridge rows were retired and one re-issued on a different channel. The retired rows stay in `sr15_indicator_to_city_indicator.csv` marked `status = retired_cc718`, with their original rationale and literature lineage intact and a `status_note` recording why they were retired; the scorer filters them out, and the notebook reconstructs the 2018 dictionary from them to measure the change.

**Why not weight the pathways instead.** The first draft of this release kept all three poverty pathways and normalised their combined weight down to what the strongest single pathway earned. It was arithmetically sound and the regression checks passed. It was rejected for two reasons. It left the City Fit report showing poverty three times with fractional weights attached, which is harder to read rather than easier — and the reviewer's complaint was as much about legibility as about arithmetic. And it answered the obvious follow-up question, *how much should poverty contribute through inclusiveness*, with a number the methodology cannot defend: the scorer's weights are face-valid defaults, not estimates. Removing the repetition removes the question.

**How the surviving channel was chosen — evidence strength, not influence.** Picking the channel that carried the most weight would have been circular. Weight here is an artifact of how many A/C cells a dimension happens to contain, so the largest channel is simply the one sitting in the sparsest dimension. Each indicator instead kept the channel with the strongest empirical lineage, which is a question the dictionary can already answer because every bridge carries its citations.

| City indicator | Channel kept | Channels retired | Reason |
|---|---|---|---|
| `poverty_rate` | `cost-effectiveness` | `distributional_effects`, `inclusiveness` | The energy-poverty literature on binding liquidity constraints (Bouzarovski; Bird & Hernández; Reames) is a measured mechanism. The other two rest on normative claims about who bears cost (Hallegatte; Markkanen & Anger-Kraavi), which are defensible readings but not measurements of the same kind. |
| `employment_manufacturing` | `employment_productivity` | `institutional_capacity`, `technical_scalability` | All three rationales restated one fact: an industrial workforce is present. `employment_productivity` is the channel the rest of the sector-employment family already used. |
| `employment_in_transport_and_logistics` | `employment_productivity` | `institutional_capacity` | Same family rule. |
| `employment_electricity_gas` | `employment_productivity` | `institutional_capacity` (moved, not dropped) | Was the family's lone exception. Moving it means one rule covers all four sector-employment indicators. |

**What it costs: the Institutional dimension no longer discriminates.** All three of `institutional_capacity`'s bridges were the sector-employment rows, so consolidating that family emptied the channel. Institutional still contributes its SR1.5 prior to the score, but in the sample its value is now identical across all twelve comunas for every action — 11 actions varied by city under the 2018 release, none do now. This was accepted knowingly: a dimension that discriminates on a proxy nobody can defend is worse than one that admits it has no city-level evidence. A national governance index (Worldwide Governance Indicators or similar) is the right way to give the dimension city-level discrimination back, and is the standing recommendation in the limitations below.

**Retiring a bridge is not the same as neutralising it.** A bridged A/C cell blends the IPCC verdict with city data 50/50; an unbridged one uses the verdict at full strength. So when a retired bridge was a cell's only bridge, that cell does not move to the middle — it moves to the *more extreme* prior, 1.0 for a C cell and 0.0 for an A cell. That is why the shift is larger than a reweighting and why it is asymmetric: 364 of the 492 changed rows went up and 128 went down, because A/C cells in this catalogue skew supportive. This asymmetry is a property of the existing cell formula, not of the curation, but the curation is what exposes it. It is recorded as a limitation below.

### Bridges that are multi-channel but dormant

Six indicators still appear on two SR1.5 indicators in the dictionary: `home_ownership` and `renter_share` (`distributional_effects` + `public_acceptance`), `indigenous_identification_rate` (`inclusiveness` + `public_acceptance`, with opposite signs), and `primary_forest_share`, `secondary_forest_share` and `wetland_share` (`physical_feasibility` + `biodiversity` or `limited_land_use`). None of them repeats within a single action today, though for two different reasons. For five of the six, the two channels never both carry an A/C verdict for the same option: the `biodiversity` pairs are dormant because SR1.5 codes that cell B or NE for every option the bridges could reach. `secondary_forest_share` is the exception — on *Enhanced weathering* both `physical_feasibility` and `limited_land_use` are coded C and both bridges attach, so the pair is live in `sr15_cell_bridge.csv`. It causes no repetition only because no catalogue action maps to Enhanced weathering. That is a weaker guarantee than the other five have, and it will break the moment an action is mapped there.

They were left in place rather than pre-emptively curated, because retiring one channel each would mean guessing at relative literature strength for pairs that cost nothing today. Instead the notebook asserts the one-channel invariant against the real cell set on every run, so an AR6 or AR7 code upgrade that activates one of these pairs fails the notebook and forces the curation decision at the point where it matters.

### What the rule moved

492 of 1,032 (action × city) rows changed, across 57 of 86 scoreable actions, in the range −0.0833 to +0.0625 with a mean absolute shift of 0.0200. By dimension:

| Dimension | Rows moved | Mean Δ |
|---|---|---|
| economic | 305 | +0.0060 |
| technological | 160 | +0.0169 |
| institutional | 114 | −0.0093 |
| socio_cultural | 54 | −0.0004 |
| environmental | 0 | 0 |
| geophysical | 0 | 0 |

The named cases from the issue, over the twelve sample comunas:

| Case | Action | Indicator channels retired | Mean 2018 | Mean 2018-v2 | Mean Δ | Max \|Δ\| |
|---|---|---|---|---|---|---|
| Public transport | `icare_0117` | `poverty_rate` 3→1, `employment_in_transport_and_logistics` 2→1 | 0.9058 | 0.9365 | +0.0308 | 0.0625 |
| Non-motorised transport (road space) | `ipcc_0105` | `poverty_rate` 3→1 | 0.9222 | 0.9413 | +0.0192 | 0.0443 |
| Non-motorised transport (bike sharing) | `icare_0121` | `poverty_rate` 3→1 | 0.9222 | 0.9413 | +0.0192 | 0.0443 |
| C&D waste regulation | `icare_0110` | `employment_manufacturing` 2→0 | 0.2787 | 0.2565 | −0.0221 | 0.0531 |
| Circular economy policy | `ipcc_0049` | `employment_manufacturing` 2→0 | 0.2395 | 0.2134 | −0.0260 | 0.0625 |

The two industrial-waste cases go to zero channels rather than one, because `employment_manufacturing`'s surviving `employment_productivity` channel is not coded A/C for those options — the indicator drops out of those actions entirely.

**Ranking is genuinely affected**, unlike the reweighting variant. Spearman correlation with the 2018 ordering runs from 0.932 (Río Bueno, `CL RBU`) to 0.996 (Valdivia, `CL ZAL`), the largest single rank move is 39 places (Mariquina, `CL MRQ`), and five comunas see their top ten change — Río Bueno by four actions, Corral (`CL CRR`) and Los Lagos (`CL LLG`) by three, Valdivia by two, La Unión (`CL LUN`) by one. Anything downstream that was calibrated against 2018 outputs needs re-baselining.

**Regression checks.** Step 8 of the notebook asserts five invariants and refuses to export if any fails. One channel per indicator: 102 actions checked, no city indicator on more than one A/C channel — asserted against the real cell set, not trusted from the dictionary. The 2018 baseline reproduces: scoring with the reconstructed 2018 dictionary returns the committed `2018` ranked output exactly, maximum difference 0.0, which is what makes the comparison above a true before-and-after. Only the curated rows differ: 23 cell bridges retired and 4 added, with zero other differences between the two cell-bridge tables, so nothing changed by accident. Sign symmetry: scoring a mirrored city (every bucket flipped about `medium`) negates the entire city adjustment, maximum error 4×10⁻¹⁶, so positive- and negative-sign bridges are handled symmetrically. And score bounds.

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

- Of the 547 cells in `sr15_feasibility_per_cell.csv`, **261 are A or C** (48%) and are eligible for city-data adjustment.
- Of those, **59 carry a scope-matched city bridge** that provides active discrimination (76 under the 2018 release). Those 59 cells hold **108 bridge rows** between them, because one cell can attach several *different* city indicators — what the one-channel rule forbids is one indicator appearing in more than one cell of the same action. The per-indicator counts later in this document are bridge rows, not cells.
- The remaining **202** A/C cells contribute to the score via the SR1.5 prior only, with no city adjustment. They appear in `sr15_cell_bridge.csv` with `city_indicator = '(no scope-matching bridge)'`.
- The B/NE/LE cells appear in `sr15_cell_bridge.csv` with a placeholder `city_indicator` value (e.g. `(SR1.5 code B: no directional evidence)`) to keep the chain fully enumerated for the API view.

> **Correction, 2018-v2.** The `2018` revision of this list reported 127 bridged cells and 134 prior-only cells, subtracting a bridge-row count from a cell count. Step 4 of the notebook now prints this census, so the document and the artifact cannot diverge again.
>
> The 2018 figures on the same basis are 76 bridged cells, 127 bridge rows and 185 prior-only cells.

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

- **Environmental**: entirely SR1.5 prior in practice. `biodiversity` has two bridges in the dictionary (`primary_forest_share` and `wetland_share`, both `nbs`-scoped), but neither reaches a live cell: SR1.5 codes the biodiversity cell B or NE for every option those bridges could apply to, so the channel carries zero cell-level bridges and does not appear in the bridge-count table below. The rows are kept as documented intent, ready to activate if AR6 or AR7 upgrades those codes. Air-pollution and toxic-waste channels have no bridges at all; closing them would need satellite air-quality or pollutant-inventory data.
- **Geophysical**: now partially active. `physical_feasibility` is the
  largest single channel in the bridge set (11 dictionary rows → 17
  cell-level bridges) and uses land-cover shares (`urban_built_share`,
  `cropland_share`, `pasture_share`, `grassland_share`, `shrubland_share`,
  `primary_forest_share`, `secondary_forest_share`, `wetland_share`)
  sourced from ESA WorldCover / MapBiomas-style products. The
  `limited_land_use`, `water_use`, and `limited_scarce_resources`
  channels still inherit the prior.
- **Institutional** (entirely, as of 2018-v2): `political_acceptability`, `legal_admin_acceptability` and `transparency_accountability` were already option-level, and `institutional_capacity` lost its three sector-employment bridges under the one-channel rule. The dimension now contributes the SR1.5 prior and nothing city-specific. A national governance index (Worldwide Governance Indicators) is the right source to restore discrimination here, and doing so is the highest-value open bridge work in this release.

Cities are discriminated primarily on the **Economic**, **Socio-cultural** and **Geophysical** dimensions, where the bridges are conceptually strong, and partially on **Technological**. **Environmental** and **Institutional** inherit the SR1.5 prior unchanged.

### Active bridge count by SR1.5 indicator

Counts of A/C cells with a scope-matched city bridge attached
(`sr15_cell_bridge.csv` filtered to `sr15_code ∈ {A, C}` and a real
`city_indicator`).

| SR1.5 indicator | 2018 | 2018-v2 |
|---|---|---|
| cost-effectiveness | 34 | 34 |
| physical_feasibility | 17 | 17 |
| human_capabilities | 14 | 14 |
| employment_productivity | 9 | 13 |
| technical_scalability | 16 | 12 |
| inclusiveness | 15 | 10 |
| public_acceptance | 3 | 3 |
| limited_land_use | 3 | 3 |
| distributional_effects | 9 | 2 |
| institutional_capacity | 7 | **0** |
| **Total** | **127** | **108** |

`employment_productivity` gains the sector-employment bridges consolidated onto it; `institutional_capacity` loses all of its, leaving the Institutional dimension with no city discrimination at all. `distributional_effects` and `inclusiveness` shrink to the bridges that were not poverty.

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
7. **Environmental dimension is inactive.** `biodiversity` carries two dictionary bridges (`primary_forest_share`, `wetland_share`) but zero live cell bridges, because SR1.5 codes that cell B or NE for every option they could reach; they are documented intent awaiting an AR6/AR7 code upgrade. `air_pollution`, `toxic_waste`, `social_co_benefits` and `absence_of_risk` have no bridges at all. Geophysical was the major v1 gap and is now substantially closed through the `physical_feasibility` land-cover bridges, but `water_use` and `limited_scarce_resources` remain prior-only and would benefit from hydrological or critical-minerals data.
8. **Quintile bucketing** of city indicators loses signal — a city at
   the 21st percentile and one at the 39th percentile both score `low`
   (0.25 capacity). For relative ranking within a country this is
   acceptable; for cross-country comparison the quintiles need
   re-calibration.
9. **Scoring math is heuristic.** The `(sr15_signal + bridge_mean)/2` averaging and the uniform per-dimension weight are face-valid defaults, not statistically derived. The downstream model should treat this feature's output as **ordinal** signal (relative ordering of actions) and standardise alongside the other features before weighted combination. Under the uniform weighting an indicator's influence still depends on how many A/C cells its dimension happens to contain, so an indicator in a sparse dimension has more leverage than one in a dense dimension. The one-channel rule stops an indicator being counted twice; it does not equalise leverage between dimensions. A deliberate per-dimension weighting is the next methodology question.
10. **Vintage.** SR1.5 is from 2018. Cite as the 2018-vintage prior in
    any reports; recheck when AR7 Special Report on Climate Change and
    Cities lands (expected early 2027).
11. **Retiring a bridge makes a cell more extreme, not more neutral.** A bridged A/C cell blends the IPCC verdict with city data 50/50; an unbridged one uses the verdict at full strength. So dropping a cell's only bridge moves it toward 1.0 (C) or 0.0 (A) rather than toward the middle. This is why 2018-v2 moved 364 rows up and only 128 down, and why the shift is larger than a reweighting would have produced. The asymmetry is a property of the cell formula, which predates this release; a cell formula that degraded gracefully to the prior would remove it, and is worth considering alongside the per-dimension weighting in caveat 9.
12. **Institutional no longer discriminates between cities.** As of 2018-v2 the dimension is entirely SR1.5 prior — its score is identical across all twelve sample comunas for every action. Downstream models should not read city-level institutional signal from this feature until a governance-index bridge lands.
13. **The production scorer is not in this folder.** The served scores come from a SQL function and modelled tables in `CityCatalyst/global-api`, loaded by `cc-mage`. Because the one-channel rule is a dictionary change, it propagates through a chain-table reload rather than a code change — but the `action_score` naming still needs porting, and until the reload happens the API serves `2018` behaviour. See [API contract](#api-contract) for the specific changes required.

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

The endpoint specification for the consumer-facing API (`GET /api/v1/cities/{locode}/action-mitigation-feasibility-scores`) lives at [`data/api/feasibility-api.md`](data/api/feasibility-api.md), with a full sample payload at [`data/api/example_response.json`](data/api/example_response.json). Both mirror the schema in `data/scoring_chain.csv`. The API replaces the earlier 510-row `action_socioeconomic` placeholder CSV and the HIAP-MEED `socioeconomicIndicators` block in `actions_api_mock.json`.

The sample payload is now generated by the notebook rather than exported from the database, so it cannot drift from the scorer. Regenerating it surfaced a stale artifact in the `2018` release: that payload carried 99 entries for 86 actions, duplicating the eight actions that mapped to more than one SR1.5 option under a mapping revision that `actions_to_sr15_mapping.csv` no longer contains. The 2018-v2 payload has one entry per action.

**Two changes the production implementation must absorb before it can serve 2018-v2**, both specified in `data/api/feasibility-api.md`:

1. **Reload the chain table.** The one-channel rule is a bridge-dictionary change, so the SQL scoring function itself needs no edit — but until `modelled.action_mitigation_feasibility_chain` is reloaded from this release's `scoring_chain.csv`, the served scores keep the retired bridges and stay on 2018 behaviour.
2. **`action_score` now carries the mapping-confidence shrinkage.** The `2018` payload exposed the unshrunk value under that name while the notebook and this document defined `action_score` as shrunk; the unshrunk value is now published alongside it as `raw_action_score`. Consumers reading `action_score` will see values move toward 0.5 for `partial`, `weak`, `cross_cutting` and `no_match` actions — for those rows a larger shift than CC-718 itself.

`city_indicators[]` needs no new fields: with one channel per indicator, each entry means exactly what it says, which was the point of the exercise.