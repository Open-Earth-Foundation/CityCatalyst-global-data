# CONAF Bosque Nativo fund awards (cl-conaf-bn-awards)

Project-level **award records** of CONAF's Fondo de Conservación, Recuperación y Manejo Sustentable del Bosque Nativo (Ley 20.283): the "who actually got funded" companion to the supply-side program review `cl-conaf/cl-conaf-fondos`. This release covers **ten annual cycles, Primer Concurso 2016–2025**, with **9,860 awarded projects** (one concurso per year) exported from the CONAF results portal. It is the first **awards / revealed-fundability** dataset in the repo, serving use case 2 of need `2026-06-cl-finance-opportunities` (help a city prioritise actions) and the "revealed fundability" roadmap item in the finance-inventory review.

This entry records *outcomes* (applications selected for a bonificación), distinct from `cl-conaf-fondos`, which records the *program* (what the fund is). Keep the two separate: supply versus awards is the core distinction (see the climate-finance concepts note).

## Canonical sources

- Results portal (current and previous cycles): https://concursolbn.conaf.cl/. The "Reporte" export is generated here.
- Program context, 2026 launch and totals: https://www.conaf.cl/abiertas-postulaciones-al-fondo-de-conservacion-de-la-ley-de-bosque-nativo-20-283/ and https://www.conaf.cl/990-proyectos-postularon-al-fondo-de-conservacion-recuperacion-y-manejo-del-bosque-nativo/ (2024 cycle: 990 projects, CLP 6.69 bn).
- Bonos Ley de Bosque Nativo: https://www.conaf.cl/manejo-de-ecosistemas/bosque-nativo/fondo-de-conservacion-y-manejo-sustentable-del-bosque-nativo/bonos-ley-de-bosque-nativo/

## Access

Manual export. The source file (`sample/extract.xlsx`, 9,860 rows × 36 cols, 1.55 MB, ten cycles 2016–2025) was downloaded by hand from `concursolbn.conaf.cl` and supplied by Amanda 2026-06. An earlier single-cycle export (`Reporte.xlsx`, Primer Concurso 2025 only) is now superseded by this 10-year file. No documented open API or bulk feed for the results was found, so re-download is a manual portal step. The raw export carries personal data and is **not committed** (see License); the committed `data/` holds only the de-identified derivatives produced by `releases/v1/extract_clean.ipynb`.

## License

This is public-interest government information (CONAF is a public body administering public funds), so the programme and award facts are public. **But the raw export contains personal data** (presenter name and email for 805/806 rows), so reuse is governed by Chile's data-protection rules, not just public-info reuse. Evidence tags: programme-fact reuse is **verified** (public); PII handling is **decided here**, namely strip it before commit or redistribution. No explicit open licence (such as CC BY) is attached to the portal export, unlike the BIDAT bulk data behind `cl-mdsfam/cl-bip-projects`.

## Spatial and temporal scope

National, **region-level only**: 15 of 16 regions appear across the decade, with no comuna and no predio location (`superficie_predios_postulante` is 100% blank). The data spans **ten annual cycles, 2016–2025** (one `Primer Concurso` / `concurso_id` per year), so it is now a genuine 10-year time series, with annual awards ranging 806–1,091. It still resolves only to region, not comuna.

## Interpretation warnings

Five things silently bite anyone reading these awards at face value: the currency unit, the gap between award and payment, who the named person really is, what the eligibility track means, and the region-level ceiling.

- **Amounts are in UTM, not CLP.** All `monto_*` and `aporte` fields are Unidades Tributarias Mensuales. Each cycle's `monto_total_utm` sums to 90,000–115,000 UTM, matching the announced CLP 6.7–7 bn annual fund at CLP 68,000/UTM. That cross-check, verified for all ten years in the notebook, is how the unit was established (the file states no unit). Convert with the UTM value for the relevant month, and treat any CLP figure as approximate.
- **This is the awarded/selected set, not the full applicant pool, and not yet "paid".** Rows are projects selected for a bonificación in each call (yearly monto_total sums to the fund total). Payment is a later execution stage (`tiene_bonificacion_saff`, `numero_bonos`). The executed-bono share rises with cohort age, from 39–46% for 2016–2019 cycles down to 14% for 2025 (35% overall), confirming a long award-to-payment lag. Read "awarded" or "committed", not "disbursed".
- **The named person is the *presenter*, not the landowner.** `presenter_type` = Extensionista (457), Consultor (148), Profesional de CONAF (146), Propietario que postula su propio predio (55). Only 7% of projects are self-presented by the owner; the rest run through technical intermediaries. This is a genuine *delivery-channel* finding (these awards require professional intermediation), but it means the dataset does **not** identify beneficiary landowners, and the PII it does carry is the intermediary's.
- **`tipo_concurso` is the eligibility track, not the actor.** Pequeños Propietarios (61%) and Otros Interesados (39%) are the two legal application lines, and both are private forest owners. No municipality appears as an awardee in any cycle.
- **Region-level only caps the city-prioritisation use.** The data supports a claim like "Bosque Nativo awards are active or strong in region X", but not "in comuna Y" from this file.

## Parsing notes

- Single sheet "Worksheet"; **row 0 is blank**, the header is on **row 1**, and data starts at row 2. `read_excel(..., header=1)` handles it, but a naive default-header read will be wrong.
- **Rename by EXACT column name, not prefix.** Several columns share a prefix (`rptpro_superficie` vs `rptpro_superficie_plan`/`_bonos`; `rptpro_tipo_presenta` vs `rptpro_tipo_presentacion`), so `startswith` matching collides and silently duplicates columns. The notebook learned this the hard way and now maps exact names, asserting that all expected source columns are present.
- Blank-heavy SAFF/execution columns are blank by design (they populate only as projects reach execution); they are not data-quality errors.
- PII columns `rptpro_presentado_por` and `rptpro_email_presenta` are dropped at load; `rptpro_tipo_presenta` is kept (channel, non-identifying).

## How this was produced (extraction & refresh)

Source: hand-downloaded `sample/extract.xlsx` from `concursolbn.conaf.cl` (ten cycles 2016–2025). Cleaning is done by **`releases/v1/extract_clean.ipynb`** (a Phase-B notebook, block-structured for Mage portability: load → de-identify → rename/type → validate → export → visualise). The steps: read with `header=1` (blank row 0); **drop all PII** (presenter name and email), keeping only `presenter_type`; rename `monto_*` to `*_utm`; add a region short-name; and assert per-year counts, UTM-total bands, uniqueness, and no-PII before exporting. The single committed data output is `data/cl_conaf_bn_awards_projects.csv` (9,860 rows, de-identified, pipeline-ready); **aggregates are rendered as charts inline in the notebook** (not saved as image files), with the precise figures carried as tables in `review.md`. To refresh: drop the next cycle's export into `sample/`, re-run the notebook (restart-and-run-all), and commit the regenerated `data/`.

## Relationship to other datasets

- **`cl-conaf/cl-conaf-fondos`**: the supply side (what the fund is). This is its awards side; join on the fund, not on a key.
- **`cl-mdsfam/cl-bip-projects`** (BIP/SNI): the *public-investment* outcomes pipeline, with **no record overlap** (verified: 0 shared ids, 0 CONAF-financed BIP rows). BIP is public bodies' investment projects evaluated for RATE; this is private-owner forestry bonifications outside the SNI. They are complementary awards layers for different actor universes, so relate them only at the (comuna/region, sector) aggregate level.

## Mapping to actions

`releases/v1/data/cl_conaf_bn_awards_to_actions.csv` (built by `map_actions.ipynb`, self-contained — reads the committed projects CSV, not the PII raw) maps awards to the city action list at the **`objetivo_manejo` grain** (= `literal` A/B/C). It's the cleanest mapping in the repo — **100% of awards** take a high-confidence primary action: producción maderera + no maderera → sustainable forest management (`ipcc_0054`); preservación/xerofíticas → reduce deforestation & degradation (`ipcc_0052`); medium secondaries to restoration (`ipcc_0053`) and sustainable wood products (`ipcc_0071`). All AFOLU/native-forest — it deepens forest-management precedent rather than adding sectors. Caveat: funds management of *existing* forest, not new planting, so afforestation is only a partial secondary. Medium rows await adjudication.

## Current approved release

Not promoted (research). First release **v1** in `releases/v1/`: `extract_clean.ipynb` (renders the aggregate charts inline — awards by year, by region, composition, UTM/ha by literal, execution lag), the pipeline-ready `data/cl_conaf_bn_awards_projects.csv` (9,860 rows, de-identified), `map_actions.ipynb` + `data/cl_conaf_bn_awards_to_actions.csv` (the objetivo→action crosswalk, self-contained, restart-and-run-all passes), and `review.md`. Raw `sample/extract.xlsx` is deliberately not committed (PII). Evidence tags: structure and coverage **verified** (the notebook asserts per-year counts, uniqueness, no-PII, and a restart-and-run-all pass); UTM unit **verified** (the fund-total cross-check holds for all ten years); the awarded-not-paid reading **inferred** (from the execution-flag pattern, now corroborated by the cohort-age lag); license public-fact **verified**, PII handling **decided** (dropped).
