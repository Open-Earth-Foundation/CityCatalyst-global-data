# Review — AR6 SPM.7(a) mitigation potentials, release 2023

What this release's data can and cannot support. Dataset-level facts (license, provenance, parsing) live in the review README one level up.

## Scope and status

- `data/spm7a_mitigation_options_2030_clean.csv` — 31 mitigation options: 2030 global reduction potential, cost-bucket breakdown, uncertainty bounds.
- `data/spm7a_option_to_tef.csv` — curated option → TEF transition element links (house mapping schema), adjudicated 2026-06-05.
- `data/spm7a_option_to_action.csv` — curated option → city action links (102-action list from the SR1.5 feasibility review), adjudicated 2026-06-05.
- Produced by `spm7a_extract_clean.ipynb`, `spm7a_tef_mapping.ipynb`, and `spm7a_action_mapping.ipynb`.
- Status: research release; production approval tracked in `catalog/index.yaml`.

## What this data supports

Claim templates with their validity conditions:

- *"Globally, [option] sits in a higher 2030 mitigation-potential tier than [option]."* — valid when their uncertainty ranges don't overlap; check the bounds, don't assume.
- *"[Option] is among the largest global mitigation opportunities to 2030."* — valid for the clear top tier (Solar, reduced ecosystem conversion, Wind).
- *"Roughly [N] GtCO2e/yr of [option]'s potential is available below [cost threshold]."* — valid as a coarse tier; costs are 2015–2020 vintage, uncorrected for inflation.
- *"A substantial share of global 2030 potential costs less than US$20/tCO2e."* — supported; cheap potential concentrates in demand-side options.
- *"TE [element] addresses an option in the global top potential tier."* — via the mapping; link semantics only (see below).
- **Banding: three bands, no more.** The longest chain of options clearly separated by their uncertainty ranges is 3 deep, so three potential bands is the maximum the data certifies. Natural breaks give: **high — 5 options** (Solar, reduced ecosystem conversion, Wind, agricultural carbon sequestration, ecosystem restoration; 2.8–4.5 GtCO2e/yr), **medium — 25 options** (0.47–2.1), **low — 1 option** (CCU, 0.15). Through the TEF mapping: high band → 2 mapped options (Solar, Wind), 4 TEs; medium → 17 options, 107 TEs; low → unmapped. One TE (rooftop solar) spans two bands. Evidence: `spm7a_extract_clean.ipynb` §5.4–5.5.

## What this data does not support

- *"City [A] should prioritize [option]."* — potentials are global priors; local sector mix, grid intensity, and what an option displaces change the local answer (notably for Chile's fast-decarbonizing grid).
- *"Total opportunity = sum of options."* — potentials are explicitly non-additive; never sum them.
- A strict 1–31 ranking. Uncertainty ranges overlap heavily (top-5 options overlap 7–18 others); the data supports top/middle/tail tiers only.
- A five-band scale (very high / high / average / low / very low). Under quintile banding, 26/31 options' uncertainty ranges straddle a band edge — adjacent-band distinctions would be fake precision. Three bands is the ceiling (see above).
- *"[EVs / dietary shift / food-loss reduction / CCU] have low cost-effective potential."* — their costs are unallocated, not high; they vanish from cost-bucket views by artifact.
- *"TE [element] has a potential of [N]."* — the mapping links, it never attributes. Potential stays at option level; fan-out would double-count.
- Claims about post-2030 importance — the source warns relative importance shifts beyond 2030.

## Using it downstream

- Present rankings as tiers; show uncertainty bounds where present (absent bounds means "not stated", not zero).
- Pair with `ipcc-sr15-mitigation-feasibility` for the feasibility axis — SPM.7 deliberately excludes feasibility-beyond-cost, so the two combine without double-counting.
- Handle the four cost-unallocated options explicitly (e.g. a "cost unquantified" tier) in any MACC-style view.
- Unmapped options (12/31) are essentially the non-city-actionable set — treat TEF coverage as a city-relevance filter, and note only 19 options' evidence flows to TEs.
- Expect band labels on TEs to skew medium: 3 of the 5 high-band options are land-based and unmapped, so city-actionable evidence concentrates in the medium band. A TE labelled "medium" is not weak evidence — it's where most city levers live.
- Mapping coverage is a property of the target taxonomy, not this dataset: the action-list mapping reaches 25/31 options and 89/102 actions, with the high band reaching 16 actions (vs 4 TEs under TEF) because the action list is land/agriculture-rich. Compare both mappings before concluding anything about coverage.
- In the action mapping, "instrument" actions (certification, procurement, EPR, congestion pricing, urban form) carry `medium` by design — they drive options rather than being them. The 13 unreached actions (grid/T&D, governance instruments, cooking-fuel phase-out) get no potential evidence from this source; that is not a statement about their importance.

## Construction methodology and city-level adjustment

Added 2026-06-05 for need `2026-06-city-potential-modifiers`: can the global priors be adjusted with city parameters *using the methodology that built them*? Read against AR6 WGIII 12.2.1–12.2.2 + Table 12.3 notes (chapter text, verified) and the SPM.7 figure caption (verified). Answer: partially — decomposability differs by sector, and the split matters more than any average answer.

- **Reference point is recoverable** [verified]: potentials are measured against current-policy ~2019 baselines — WEO 2019 Current Policies for energy and buildings, SSP2/study-specific elsewhere; Table 12.2 gives the reference macro numbers (60 GtCO2e-yr median 2030 emissions). Any city adjustment must be stated relative to this baseline, which resolves the "what did the prior assume" question in principle.
- **Buildings — methodology-native rescaling** [verified from Ch.12 text; input tables inferred]: potentials were built as *regional % reductions per measure* from 67 studies, applied in the order sufficiency → efficiency → renewables with overlap correction (which also makes the buildings rows additive, unlike the rest of the dataset). The % structure means city potential ≈ regional % × city baseline buildings emissions — exactly the adjustment form the need wants, by construction. The per-region percentage tables live in Chapter 9 / its SM; extracting them is a follow-on review (see need candidates).
- **Energy supply + EVs — grid-EF adjustment endorsed by the source** [verified]: the caption states potential "will depend on the reference technology (and emissions) being displaced", and the EV row is published as "0.5–0.7 GtCO2e depending on the carbon intensity of the electricity supplied". The identity-class grid-EF modifier is not an external assumption — it is the source's own stated sensitivity.
- **CH4 (coal, oil and gas, waste, wastewater) + F-gases — go one level down** [citations verified; country resolution to confirm]: these rows aggregate country-resolved MACC datasets (Harmsen et al. 2019; US EPA 2019; Höglund-Isaksson et al. 2020/GAINS; IEA 2021). The underlying sources carry regional/country potentials directly — adjustment can skip the global-to-city jump by using them instead of rescaling the global number.
- **Transport mode-shift and demand avoidance — no recoverable structure** [verified]: ~10 sources, single global numbers, ±50%; "shift to public transport 0.5" has no published decomposition to rescale. City adjustment here requires external relationship evidence (elasticity literature) — a modelling step outside this dataset's methodology.
- **AFOLU and industry — out of city-adjustment reach** [verified]: AFOLU rows are 2020–2050 averages from 5–9 global studies (and mostly TEF-unmapped); industry rows are global per technology class. Treat as national context, not city-adjustable.
- Anti-claim: adjustment does not upgrade the data's epistemics — adjusted values remain ordinal-ranking inputs with ±20–60% uncertainty and non-additivity intact; never present them as city tCO2e potentials.

## Notes on non-obvious fields

- `smooth` (clean csv): the cost-bucket breakdown is an even-spread estimate, not measured — use the buckets of these 7 options as indicative only.
- `unc_low`/`unc_high`: missing for 10 options — "not stated", not zero.
- `mapping_confidence: none` (mapping csv): mapping was considered and found impossible; the rationale says why. These rows are kept on purpose.
- One mapped TE can serve two options (e.g. rooftop solar under both "Solar" and "Onsite renewables") — intentional many-to-many, mind it when grouping by TE.

## Traceability

- Source: IPCC DDC [doi:10.48490/3c86-xp02](https://doi.org/10.48490/3c86-xp02) (SYR); WGIII original [doi:10.48490/ayfg-tv12](https://doi.org/10.48490/ayfg-tv12).
- Construction methodology: AR6 WGIII [Chapter 12](https://www.ipcc.ch/report/ar6/wg3/chapter/chapter-12/) §12.2.1–12.2.2 + Table 12.3 notes; [figure SPM.7 caption](https://www.ipcc.ch/report/ar6/wg3/figures/summary-for-policymakers/figure-spm-7/); per-option source detail read from Supplementary Material 12.SM.1.2 (2026-06-05).
- Cross-cutting ranking methodology (how these potentials feed the city action ranking, incl. per-option source provenance): [`methodology.md`](../../methodology.md) at this review's root. Per-sector detail lives in the chapter reviews (`ipcc-ar6-ch9-buildings`, `ipcc-ar6-ch10-transport`).
- TEF catalog input: climateview-transition-elements release 2026-02-23 export (local-only, license pending — see that release's README).
- Mapping adjudication: Amanda, 2026-06-05 (recorded in `spm7a_tef_mapping.ipynb` findings).
