# Chile Beyond-NDC marginal abatement costs (cl-mma-ndc-macc)

Dataset review — **NOT PURSUED** (decision 2026-06-08). The CC BY bundle genuinely contains per-measure marginal abatement cost (USD/tCO₂eq, Chile-specific) + 2050 activity/emissions projections, but it is a **runnable research model, not a results table** — the costs are formulas, extractable only by running Pyplan/Analytica/SWITCH or reimplementing a ~1,400-node graph. **Decision: not worth that effort for an ordinal city ranking.** Cost axis stays on the global SPM.7 cost bins (already in the notebook). Reopen only if a Chile cost layer becomes essential AND a lower-effort source (e.g. a ready table in the MMA government NDC report) is found.

> Why it's shaped this way: it's an academic reproducibility deposit (the model), with the results published in the paper (CC BY-NC-ND, off-limits). Pyplan/Analytica store formulas not values by design. So it's the wrong *artifact type* for us — a simulation model, not the flat cost table we need — not bad data.
>
> Correction note: an earlier pass said "no cost data." Wrong — cost nodes were missed on a names-only scan. The data exists; the blocker is extraction effort, now judged not worth it.

Candidate origin: `cl-mma-ndc-macc` from `dataset-discovery/needs/2026-06-action-reduction-potential` (was *deprioritize*; upgraded to *investigate* 2026-06-08 after this review). Intended role: the **Chile national cost layer** for the city action-ranking methodology ([`methodology.md`](../../ipcc/ipcc-ar6-spm7-mitigation-potentials/methodology.md)) — i.e. replace the coarse, hole-y global SPM.7 cost bins with recent, Chile-specific marginal abatement costs (USD/tCO₂e), as a national-rate cost layer.

> **Naming note:** the id keeps the candidate's `cl-mma` lineage, but the usable source is **not** MMA — it's an academic study (GreenLab-UC / Climate Action Teams). Authorship recorded accurately below; rename the id/publisher if preferred.

## What it is

"**GHG Mitigation beyond the NDC in Chile: an assessment of alternatives**" — a multisector marginal-abatement-cost study: **47 mitigation actions** across transportation, buildings, industry & mining, IPPU, waste, electricity generation, forestry and agriculture, each with **marginal abatement cost (USD/tCO₂e)**, mitigation potential, and capital cost, built on an open multisector model (Pyplan/Analytica). Data is 2023 vintage.

- **Authors / publisher:** Climate Action Teams initiative; GreenLab and Centro Cambio Global, **Pontificia Universidad Católica de Chile** (with Vinken). Hosted via the Chilean Ministry of Energy (energia.gob.cl) and Mendeley Data.
- **Official-policy companion (separate):** the MMA NDC strengthening documents (cambioclimatico.mma.gob.cl) — public government materials; thinner on explicit MACC cost data; not the primary source here.

## Why we use it

- **Fills the IPCC cost holes.** SPM.7's global cost bins leave several big options *cost-unallocated* (EVs, demand-side) — see the cost test in `../../ipcc/ipcc-ar6-spm7-mitigation-potentials/action_ranking_calc.ipynb`. This study prices them, and at Chile-specific (not global) costs.
- **Recent + cross-sector + CL-specific** — a coherent national MACC over the same sectors we rank.

## Canonical sources

- **Data + model (USE THIS):** Mendeley Data, *"GHG Mitigation beyond the NDC in Chile — Pyplan Models"*, [doi:10.17632/jtp6dcyp78](https://data.mendeley.com/datasets/jtp6dcyp78) (v5, 2023-06-06). Sectoral emission projections + mitigation actions + abatement cost.
- **Report (DO NOT reuse content):** Climate Action Teams discussion paper, energia.gob.cl / SSRN [10.2139/ssrn.4168343](http://dx.doi.org/10.2139/ssrn.4168343).

## License — the decisive finding [verified 2026-06-08]

The two pieces have **different** licenses, and only one is usable for the commercial/clean-room build:

- **Discussion-paper report:** **CC BY-NC-ND 4.0** — NonCommercial *and* NoDerivatives. **Disqualifying.** Do not use its text, figures, or numbers-as-published in the deliverable, and don't add it to the repo.
- **Mendeley model + data:** **CC BY 4.0** — commercially usable with attribution. ✅ This is the path: take the abatement-cost data from the Mendeley dataset, cite it.

Facts (the cost values themselves) aren't copyrightable, but to stay clean we source them from the CC BY dataset, not the NC-ND report.

## Access obstacle (not a license problem) [to verify at Step 2]

The Mendeley files are **Pyplan/Analytica model files**, not necessarily plain tables. If "Download All" yields `.ana`/Pyplan exports, the per-action cost table must be **exported to CSV/XLSX from Pyplan or Analytica first**. Confirm file formats when the data is dropped in; if only model files exist, that export is the gating step.

## Spatial / temporal scope

- **Geography:** Chile **national** — not city. Enters the ranking as a *national-rate cost layer* (same treatment as industry abatement), not a city-differentiated one.
- **Time:** 2023 study; actions to 2030 (NDC) / beyond-NDC scenarios.

## Step 2 — what the data actually is [verified 2026-06-08]

The CC BY Mendeley download (~999 MB) is a **runnable multisector model**, with two kinds of content:

- **Stored data (directly extractable):** activity & emissions projections to 2050 — transport consumption/emissions (`Energy Demand/*.xlsx`, 100k+ rows), waste generation/composition & wastewater (`IPPU and Waste/*.xlsx`), population & GDP. These are the model *inputs/baseline* (the 2050 values visible in the Excels).
- **Computed-but-not-stored (per-measure cost & mitigation):** the Pyplan `.ppl` models contain explicit per-measure cost nodes — e.g. **FOLU has 6 `Costo de Mitigación` nodes in USD/tCO₂eq** (forestation, fire, protected areas, kelp, PDM, average); Agriculture & IPPU carry CAPEX/OPEX/NPV build-ups. **But every such node is a formula, not a value** — 0 of ~1,400 nodes across the `.ppl` files cache any result. The numbers only exist after the model is evaluated.
- Electricity is the separate **SWITCH** model (inputs/outputs, `Reference_NDC` scenario); Analytica `.ana` sectors are binary.

So per-measure marginal abatement cost (USD/tCO₂eq) **is present, Chile-specific, and CC BY** — but as model logic to run, not a table to read.

## Fit verdict: fit in content, gated on extraction

It's the right data (CC BY, Chile, per-measure USD/tCO₂eq + potential), but extracting numbers needs **model evaluation**. Paths, in effort order:

1. **Run the models** in Pyplan + Analytica (and SWITCH for electricity) → export the per-measure cost table → ideal CC-BY Chile cost layer. Best if the tooling is available.
2. **Reimplement the Pyplan node graph in Python** (formulas are readable xarray; inputs are in the bundle) for the `.ppl` sectors (FOLU, Agriculture, IPPU) → moderate engineering, partial (excludes Analytica + electricity).
3. **Extract only the stored activity/emissions projections** (easy, CC BY) as a Chile baseline/potential layer, and keep cost on the global SPM.7 bins.
4. Cross-check the **MMA government NDC report** for a ready results table (simplest if present).

Reopen/advance when a path is chosen. This is *not* a flat CSV join.

## Housekeeping

The 999 MB bundle was **removed from the repo** (it included a 422 MB dispatch CSV; far over the large-file convention). Re-download if ever needed from the Mendeley DOI above. Do not commit the bundle or the NC-ND report.

## The live lead: MMA government NDC report (re-points this candidate)

The two "Chile NDC MACC" sources are different things, and the **government** one is the right fit for the `cl-mma` publisher:

- **GreenLab-UC / Climate Action Teams (Mendeley)** — the academic study profiled above. **Not fit** (model not results; results NC-ND). Dead end, recorded.
- **MMA *Fortalecimiento de la NDC* (Nov 2022)** — `cambioclimatico.mma.gob.cl/wp-content/uploads/2023/01/Chile-Fortalecimiento-NDC-nov22.pdf`. **Government, public.** Reported (web search, **not yet verified firsthand**) to contain a cost-effectiveness analysis and a **per-measure MACC in USD/tCO₂, sector by sector** (most measures negative-cost by 2050). This is the promising cost-layer source.

**Access obstacle:** the MMA PDF is large and **times out on fetch** in this environment (180 s). To verify and extract the per-measure cost table it needs to be **downloaded and dropped into `releases/2023/data/`** (same as the Ch.9 PDF), after which: confirm the table is present, extract a clean `cl_macc_costs.csv` (measure, sector, USD/tCO₂, potential), map measures to our `calc_options`, and write `review.md`.

**Verdict if the MMA table checks out:** promote as the **Chile national-rate cost layer** — public-government licence, fully-allocated per-measure costs, fills the SPM.7 unallocated gaps. National, not city (national-rate, like industry abatement).

Fallback if it doesn't pan out: stay on the **global SPM.7 cost bins** (already in the notebook), accepting the unallocated-option gaps.
