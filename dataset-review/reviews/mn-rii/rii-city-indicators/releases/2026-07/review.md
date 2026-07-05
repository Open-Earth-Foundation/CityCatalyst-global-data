# Review — RII city indicators, release 2026-07

## Scope and status

This release holds the 2024 GHG-emissions data for participating Minnesota cities, drawn from four Tableau exports of the Regional Indicators Initiative (residential energy, commercial/industrial energy, on-road transport, and waste), together with the mapping that aligns RII's emission categories to GPC reference numbers and the per-city totals that result. Everything downstream of the raw exports is produced by one notebook, `rii_extract_clean.ipynb`, which loads the exports, cleans them, confirms the units, maps to GPC, and assembles the city results. The status is research, not production-approved: promotion is blocked on a redistribution licence from LHB and on re-exporting an unfiltered energy view, both recorded in the review README one level up. Dataset-level facts — licence, provenance, the Tableau-export quirks — live in that README and are not repeated here; this document is only about what the 2024 numbers can and cannot carry.

## Visual summary

The notebook's charts show three things. Coverage is deeply uneven across indicators: transport reaches 117 cities, waste 70, and energy only 28, so the picture narrows sharply as you ask for more sectors. Across the fifteen need-target cities, transport dominates the sectors we can see, and only three targets (Rochester, Minnetonka, Saint Louis Park) show all three sectors stacked; the rest show transport, or transport plus waste, with an empty energy band. Per-capita transport emissions for the targets sit in a tight 2.2–5.2 tCO₂e band, with the larger core cities (Minneapolis, Saint Paul, Hopkins) at the low end and outer suburbs (Minnetonka, Richfield, Bloomington) higher — the signature of the in-boundary method counting through-traffic. Run the notebook for the rendered charts; the precise figures are in the tables below and in the committed CSVs.

## What this data supports

These claims are mostly about single-city, single-sector 2024 emissions and cross-city comparison *within RII*, and the load-bearing caveat is that "an RII city total" almost never means a whole-inventory total. Within those bounds the data is solid.

A city covered for a sector has a usable 2024 emissions figure in that sector. "Rochester's 2024 on-road transport emissions are about 337,000 tCO₂e, and its stationary-energy emissions about 1,181,000 tCO₂e" is a supported sentence. The figures are bottom-up from utility, MnDOT, and MPCA data, consistent in method across cities and years.

Cross-city comparison is valid when both cities are in RII and you compare the same sector. "Among RII cities, Minnetonka's per-capita on-road transport emissions (5.2 tCO₂e) are higher than Minneapolis's (2.2)" is supported and is exactly the kind of signal cohort selection needs. RII is explicitly built for this internal comparability.

A three-sector city total is supported only for the 28 cities flagged `complete_basic3`, and only as an RII-basis figure. "Rochester's 2024 energy + transport + waste emissions total about 1.55 million tCO₂e" is supportable with the completeness flag attached; the same sentence for Minneapolis is not, because Minneapolis has no energy figure in this export.

The residential/commercial energy split maps to GPC I.1 and I.2, so for the 28 energy cities the data supports a stationary-energy breakdown by building type and fuel, at scope 1 (combustion) and scope 2 (electricity) separately.

## What this data does not support

The overclaim to watch is treating a `basic_partial_tco2e` number as a city's GPC BASIC inventory, or comparing an RII city to a non-RII one.

It does not support a GPC BASIC total for any city. Even the complete-3 cities omit wastewater (III.4), composting (III.2), rail, aviation and off-road transport (II.2/II.4/II.5), and energy-industry own use (I.4); the waste sector is accounted on RII's methane-commitment basis, not GPC's first-order-of-decay. "This city's GPC BASIC emissions are X" cannot be said from this release — `basic_partial_tco2e` is an RII-basis, three-sector figure aligned to GPC sectors, not a certified inventory.

It does not support comparison with any inventory produced outside RII. "City A (from RII) emits more than City B (from Metro Climate Stats / the MPCA statewide inventory / the city's own CAP)" is invalid; the methodologies differ enough that the methodology document itself forbids mixing them, including using one for a baseline and another for tracking.

It does not support reading a missing sector as a low-emitting sector. Duluth and Mankato have transport but no waste figure, and most cities have no energy figure; a blank is "not covered by this export", never "near zero". The filtered 28-city energy slice in particular is a Tableau selection artifact, not evidence about which cities have low energy emissions.

It does not support splitting RII's commercial/industrial energy between GPC I.2 and I.3. The source reports one combined bucket (including street lighting); the mapping links it to both codes without dividing the value, so any per-code industrial-vs-commercial number would be invented precision.

It does not support summing RII waste into a GPC total without restatement. The methane-commitment basis measures the future emissions of this year's landfilled waste, which is a different quantity from GPC's this-year emissions; the two are not interchangeable.

## Using it downstream

Read `basic_partial_tco2e` only alongside `complete_basic3` and `sectors_present` — the total is a subset sum whenever a city lacks a sector, and silently treating it as whole is the main way this data gets misused. For a city with only transport, quote the transport figure, not the "total".

Pair this release with the Minnesota Sustainability Index for the who/where of inventories (it says which cities have an inventory and links to it; RII supplies the numbers), and treat Metro Climate Stats as the GPC-conformant alternative for Twin Cities metro cities when a need genuinely requires GPC BASIC rather than RII-basis figures. Do not blend the two.

For CityCatalyst / GPC ingestion, use `rii_gpc_emissions.csv`: it carries the GPC code and scope per city-unit with the value un-split. Handle the combined `I.2+I.3` rows explicitly — either keep them as a merged commercial+industrial stationary-energy line or hold them pending an RII breakdown; do not divide them. Carry the AR4-GWP and methane-commitment-waste caveats into any inventory that consumes these values.

## Notes on non-obvious fields

`gpc_code_applied` holds a combined value like `I.2.1+I.3.1` for RII's commercial/industrial energy — this is intentional, marking a source quantity that spans two GPC sub-sectors and must not be split, not a data error. `mapping_confidence` of `medium` on a row is a flag that a human has yet to adjudicate the mapping, not a statement about the emissions figure's accuracy. In the emissions table, waste `Recycled` is absent (it is zero by protocol and dropped from the GPC output); its all-zero presence in the raw export is what proved the values are emissions rather than tonnage. `basic_partial_tco2e` is a subset sum, not a BASIC total — the `complete_basic3` boolean is the field that tells you whether all three sectors are present.

## Traceability

Source: Regional Indicators Initiative, 2024 emissions views, exported from the Tableau Public workbook `CITYSUMMARIES` on 2026-07-05 (per-view exports in `sample/`, gitignored; re-export steps in the review README). Methodology: RII Methodology, February 2026. GPC reference notation: `knowledge-base/topics/gpc-framework.md`. Mapping adjudication: the medium and none rows were drafted by the agent on 2026-07-05 and await human adjudication — the three judgment clusters (combined commercial/industrial bucket, "Other" fuels as scope 1, waste basis) are listed in the notebook Findings; record the adjudicator and date there and here when settled.
