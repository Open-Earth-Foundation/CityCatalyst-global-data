# OEF — Brazil city finance feasibility (br-city-finance-feasibility)

The Brazil counterpart of the Chile city-action fundability model: for a Brazilian municipality and an adaptation intervention, how realistically can the city pay for and deliver it, and through which funding route. This entry holds the OEF-built city profile and, as they are built, the route-eligibility model and fund-supply inventory. It is an internal derived product: the source reviews (CAPAG, MUNIC) remain authoritative for provenance and licence, and this entry re-grants nothing.

Status: release v1 contains the pilot city profile only — 50 pilot cities joined to the CAPAG credit screen and the MUNIC finance-push components, the two city-side signals the methodology's recommended starting configuration requires. The intervention-side inputs (cost band, type, sector tag), the fund-supply inventory, and the per-intervention legal verdicts are not yet built; the model logic that combines them is specified in `methodology.md` but not yet implemented.

## Why we use it

- Feeds the Feasibility pillar (Financing component) of the adaptation action prioritisation methodology for Brazil.
- Gives the pilot a scoreable city profile now: every one of the 50 pilot cities carries a CAPAG state and a full finance-push breakdown with zero missing records.

## Licence

Inherits the most restrictive upstream licence. CAPAG is ODbL with STN attribution; MUNIC is public with IBGE attribution and no named licence instrument. Nothing in this entry may be redistributed under terms looser than its sources.

## Current approved release

No release is production-approved. Release **v1** (pilot city profile) is under review.

### References

- Working methodology → `methodology.md`
- Pilot profile notebook → `releases/v1/01_city_profile_pilot.ipynb`
- Pilot profile table → `releases/v1/data/br_city_finance_profile_pilot.csv`
- Feasibility pillar pre-read (source of the model design) → https://docs.google.com/document/d/1TyCqsRmjyqFGu3gwL4JEjCWWGPoaf1p377QZPnbkiUk/edit
- Chile precedent → `dataset-review/reviews/oef/cl-city-action-fundability/`
