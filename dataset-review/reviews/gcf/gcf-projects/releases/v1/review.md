# Review — gcf-projects, release v1 (Chile slice)

## Scope and status

Research release (not production-approved). The Chile slice of the Green Climate Fund project portfolio, hand-verified from the GCF Chile country page (2026-06-18) as a first cut pending a full API pull. Two committed outputs in `data/`: `gcf_chile_slice.csv` (the project dataset, 8 entries: 7 funded FPs plus one readiness grant) and `gcf_chile_to_actions.csv` (the project to action crosswalk). Built and validated in `gcf_chile_analysis.ipynb`. Dataset-level provenance, the access structure and the API are in the review README one level up.

## Visual summary

The notebook charts the eight entries by mapping confidence: three map to a city action, five do not. The funded portfolio is small but spans transport, forestry, energy and finance, with one genuinely city-facing programme (FP189 e-mobility).

## What this data supports

GCF has a real, city-relevant footprint in Chile. FP189, the regional E-Mobility Program for Sustainable Cities delivered by the IDB, finances electric buses and EV fleets and is the clearest city-facing international instrument in the portfolio. The Subnational Climate Fund (FP151/FP152) adds a subnational vehicle, and FP120 (REDD+ results-based payments) and FP017 (Tarapacá solar) are Chile-specific mitigation projects.

The access chain is the usable fact for a city. Every entry is reached through the National Designated Authority, the Ministerio de Hacienda, and an Accredited Entity such as the IDB, CAF or FAO; the Chilean direct-access entity is FYNSA. A city engages as a beneficiary or partner of an accredited entity, not as an applicant.

Three of the eight entries carry a high or medium action mapping: FP189 to zero-emission bus fleets, FP120 to reduce deforestation and degradation, and FP017 to solar generation.

## What this data does not support

The overclaim to guard against is reading a regional programme's headline as a Chile figure. FP189, FP151, FP152, FP254 and FP149 are multi-country; their financing totals cover all participating countries, so the US$450M behind FP189 is not Chile's allocation. Only FP017 and FP120 are Chile-specific.

It does not describe an open funding call. These are approved or under-implementation programmes, not application windows; GCF's own way in is a continuous, rolling project cycle through the accredited entity, so the records are outcomes, not opportunities a city applies to.

It is not a complete portfolio. This is a hand-verified eight-row slice; the full Chile set is whatever the API returns under a Chile filter, and the figures here should be refreshed from that pull.

## Using it downstream

Treat each row as intermediated precedent: carry the accredited entity and the national gatekeeper, and relate it to actions at the project grain, never splitting a multi-country amount across countries. The mitigation portfolio is the in-scope set; the adaptation entry (FP254, resilient water) is flagged out of scope, not a coverage gap.

## Benchmark values a city can use

These are comparator priors from a small slice, not guarantees, and the multi-country amounts are programme totals rather than Chile allocations. To understand the channel, the city-facing precedent is e-mobility (FP189), delivered by the IDB as accredited entity with national-government participation. To generalise, the Chile-specific instruments show the two routes that have actually closed: results-based payments for forests (FP120) and early equity for utility-scale solar plus storage (FP017). The delivery channel in every case is an accredited entity plus the Ministerio de Hacienda no-objection, which is the realistic access route a city should plan around.

## Notes on non-obvious fields

`chile_scope` separates Chile-specific entries (FP017, FP120, readiness) from multi-country programmes where Chile is one participant. `in_scope` marks the adaptation entry (FP254) as out of scope for the mitigation action list. `application_status` records that these are approved or under-implementation programmes, not open calls.

## Traceability

Source captured 2026-06-18 from the GCF Chile country page and the FP189 detail page; the canonical refresh path is a single call to the GCF Projects API (`http://api.gcfund.org/v1/projects`) filtered to Chile. Multi-country financing figures are verified as programme totals. License: public GCF programme information; confirm GCF terms before redistribution.

### References

- project dataset → `data/gcf_chile_slice.csv`
- crosswalk → `data/gcf_chile_to_actions.csv`
- notebook → `gcf_chile_analysis.ipynb`
- API + access structure → review README one level up
