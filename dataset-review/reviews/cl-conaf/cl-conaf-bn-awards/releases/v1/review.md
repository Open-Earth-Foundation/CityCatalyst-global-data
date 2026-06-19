# Review — cl-conaf-bn-awards, release v1

## Scope and status

Research release, not production-approved. These are award records for CONAF's Fondo de Conservación, Recuperación y Manejo Sustentable del Bosque Nativo (Ley 20.283), covering ten annual cycles (Primer Concurso 2016–2025) and 9,860 awarded projects. They were produced by the cleaning notebook, which drops all personal data and cleans the hand-exported source file. The committed artifact is a single project-level table (9,860 rows, de-identified, pipeline-ready); the aggregates are rendered as charts inline in the notebook (not saved as image files), and this review carries the precise figures as tables. Dataset-level facts (provenance, license, parsing) sit in the README one level up. This is the repo's first awards / revealed-fundability dataset, and now a 10-year time series.

### References

- cleaning notebook (also renders the charts inline) → `releases/v1/extract_clean.ipynb`
- raw export (not committed, PII) → `sample/extract.xlsx`
- project-level table (pipeline raw) → `data/cl_conaf_bn_awards_projects.csv`

## Visual summary

The notebook renders these aggregates as clean charts inline (run it to see them); the precise figures live in the tables further down. The shape in brief: demand is durable, at roughly 810–1,090 awards a year for a decade, with total committed UTM stepping up to about 115k from 2020. Awards concentrate in south-central regions and barely touch the north or Metropolitana. The management mix is a stable timber skew (79% literal C), and unit intensity tracks the legal caps at about 9 UTM/ha for timber down to 5 for preservation. The executed-bono share lags badly, from about 40% in the older cohorts to 14% for 2025, so awarded is not disbursed.

## What this data supports

These are claims an analyst could lift into a report, each backed by the de-identified data and the charts under "Visual summary". They cluster around three things: how much gets funded, where, and what kind of work the fund rewards.

- "CONAF awarded roughly 810–1,090 native-forest projects per year over 2016–2025 (9,860 in total), with stable demand and no collapse." See the by-year chart in the notebook.
- "Awards concentrate in south-central regions: La Araucanía 20%, Los Ríos 15%, Los Lagos 15%, Maule 13%, Aysén/Biobío 9%, consistently across the decade." See the by-region chart in the notebook.
- "Awards skew to timber-production management (literal C, 79%) over non-timber (B, 17%) and preservation (A, 4%), and to small owners (61%), and these shares are stable over ten years."
- "Most awards go through technical intermediaries; only a small minority are self-presented by the owner." (`presenter_type`: extensionista 68%, consultor 15%.)
- "Typical award size and the owner co-contribution can be characterised in UTM per project and per hectare." Useful as priors for action unit-economics (use case 1), subject to the UTM caveat.

## Mapping to actions

`data/cl_conaf_bn_awards_to_actions.csv` (built by the self-contained `map_actions.ipynb`, separate from the PII-dependent extract notebook) maps awards to the city action list at the **`objetivo_manejo` grain** (= `literal` A/B/C — the field that names what the bonificación funds). This is the **cleanest mapping in the repo: 100% of awards** get a high-confidence primary action, because the classification directly names the activity. Three objetivos → two primary actions: producción maderera + no maderera (9,463) → **sustainable forest management (`ipcc_0054`)**; preservación/xerofíticas de alto valor (397) → **reduce deforestation & degradation (`ipcc_0052`)**; with medium secondary links to forest restoration (`ipcc_0053`) and sustainable wood products (`ipcc_0071`). Link, don't attribute; medium rows await human adjudication.

Caveat: the bonificación funds management of *existing* native forest, not new planting, so afforestation/reforestation (`ipcc_0053`) is only a partial secondary. This deepens AFOLU forest-management precedent rather than adding new sectors — complementary to the FPA awards (which add waste/energy/wetlands).

## What this data does not support

The overclaims to guard against all come from reading the awarded set as something it is not: paid money, a city's own funding, comuna-level geography, or a measure of need.

- "These amounts are in CLP." No: they are UTM, converted at the month's UTM value, so any CLP figure is derived and approximate.
- "These projects were paid or disbursed." No: they are awarded and committed; only 35% show an executed bonificación overall (`tiene_bonificacion_saff=Si`), and that share falls to 14% for the most recent (2025) cohort.
- "A city or municipality won these funds." No: awardees are private forest owners on two legal tracks, and no municipality appears. For a city this is mobilisation and facilitation evidence, not direct fundability.
- "We can see which comuna each award is in." No: the data resolves to region only, with no comuna or predio location.
- "This shows where forest restoration is most needed." No: it shows where the program awarded, which reflects selection and where the fund operates, not latent need.
- "This is the full applicant pool or a success rate." No: it is the awarded set only; non-selected applications are not in the export, so award odds cannot be computed from it alone.

## Using it downstream

Using the awarded set without overreading it comes down to a few translation rules.

- For the **prioritisation** use case, treat it as *city-as-enabler mobilisation potential*, not city-as-applicant fundability: a region with many active awards is one where a city can credibly steer local owners to the fund. Keep this signal separate from BIP (city-as-applicant); see the climate-finance concepts note.
- For **understanding actions**, use the per-project superficie, monto, and aporte fields and the objetivo_manejo split as empirical priors for native-forest action archetypes and cost.
- Aggregate to (region, literal) before presenting, and do not surface project rows in a product (they derive from PII-bearing source records and resolve only to region anyway).
- Pair with `cl-conaf-fondos` (supply) for the full picture of this fund; relate to `cl-bip-projects` only at the aggregate (region, sector) level, never a row join.

## Benchmark values a city can use

What a city can reuse from this awarded set to understand, replicate, generalise, or take learnings from the fund. Figures cover all ten cycles (2016–2025) unless noted, and are **comparator priors** (region-level, amounts in UTM at about CLP 68,000): order-of-magnitude planning anchors rather than guarantees.

To understand or size it, the typical values fall out by management type. Each forest is managed under one *literal* (A, B, or C), and the three differ in how common they are, how large the award is, and how much they pay per hectare.

| Management type (literal) | Share of awards | Median award (UTM) | Unit rate (UTM/ha) |
|---|---|---|---|
| Timber production (C) | 79% | 52 | 9.3 |
| Non-timber (B) | 17% | 39 | 5.6 |
| Preservation (A) | 4% | 36 | 5.0 |

Across all types the median award is about 49 UTM per project (around CLP 3.3 M), with an interquartile range of 24–105 UTM. The unit rate is the single most reusable figure: it tracks the legal caps and is stable across years, so a city can size an action as hectares × rate.

*Worked example: a city steering owners toward 100 ha of timber management (literal C) can expect on the order of 100 × 9.3 ≈ 930 UTM in bonificaciones, about CLP 63 M at CLP 68,000/UTM.*

The two application tracks differ mainly in parcel size, with small owners working smaller plots:

| Applicant track | Share of awards | Median parcel (ha) |
|---|---|---|
| Pequeños Propietarios (small owners) | 61% | 5.0 |
| Otros Interesados | 39% | 11.1 |

The overall median parcel is 6.3 ha (interquartile range 3.1–14.4).

To replicate it (design conditions that show up in the data):

- **Near-fully subsidised:** only 25% of awards carry any owner co-contribution (`aporte`). Replicating this kind of action needs little owner cash; the barrier is access, not co-finance.
- **Technical intermediation is effectively required:** the large majority of awards were filed by a professional (extensionista 68%, consultor 15%), not the owner. The replicable enabling step is brokering technical support, not just informing owners.
- **Award-to-payment lag:** the executed-bono share rises with cohort age (39–46% for 2016–2019, 14% for 2025; 35% overall), so plan for a long, conditional gap between award and disbursement.

To generalise or take learnings:

- **Where the route is proven:** awards concentrate in south-central regions (La Araucanía 20%, Los Ríos 15%, Los Lagos 15%, Maule 13%, Aysén/Biobío 9%), consistently over the decade. A city there has strong precedent; a northern or central city has almost none, so generalise with care.
- **What the fund actually funds:** the management-type table above tells the story, with timber production dominating and small owners taking the larger share, stable over ten years. The learning is that this instrument flows overwhelmingly to *productive* management, so if a city's objective is conservation or forest-carbon, that is a goal-versus-instrument mismatch to flag rather than assume away.
- **Demand is durable:** roughly 810–1,090 awards every year for a decade, a reliable recurring route rather than a one-off.

## Notes on non-obvious fields

- `monto_*_utm` and `aporte_propietario_utm`: UTM, not CLP (unit established by the fund-total cross-check; the source states no unit).
- `tiene_plan_saff`, `tiene_bonificacion_saff`, `numero_bonos`: execution-stage flags. Blank does not mean missing, it means not yet at that stage; `tiene_bonificacion_saff=Si` is the closest thing to "paid".
- `tipo_concurso`: legal eligibility track (Pequeños Propietarios / Otros Interesados), both private owners, not the GPC actor.
- `presenter_type`: who submitted (extensionista, consultor, CONAF professional, or owner), a delivery-channel signal kept after the identifying name and email were dropped.
- `literal` A/B/C maps to objetivo_manejo (A = preservation, B = non-timber, C = timber).

## Traceability

Source: `sample/extract.xlsx` (Primer Concurso 2016–2025, 9,860 rows) exported from concursolbn.conaf.cl, supplied 2026-06; raw not committed (PII). Produced by `extract_clean.ipynb` (restart-and-run-all passes; asserts per-year counts, award_id uniqueness, no-PII, and per-year UTM-total bands). Cross-checks: each cycle's monto_total sum (90k–115k UTM) against the announced CLP 6.7–7 bn annual fund, and an overlap test against `cl-mdsfam/cl-bip-projects` (0 shared ids). Profiled and extracted 2026-06-17.
