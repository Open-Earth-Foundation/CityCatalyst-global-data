# Need: city-level GHG inventories for Minnesota cities

**Status:** open

**Requested by / why:** OEF, in support of the RCA × NLC Concept Note Builder (Minnesota). The CNB assumes each cohort city's context — including a GHG inventory — is available to seed the agent (PRD §5.A). We need a source of city-level GHGI for MN cities, both to (a) provide that city context and (b) help choose the 3 cohort cities. A good source is also in scope for the core repo's GHGI pipeline (city emissions → GlobalAPI), so this need may serve two consumers.

**Use case & quality bar:** city context + cohort selection now; potentially production emissions later. City admin level is required (a state or metro total is not enough). Methodology must be documented and, ideally, mappable to GPC (CityCatalyst's framework) — the leading candidate (RII) uses its own energy/waste/travel model, so mapping cost is the key open question.

**Open questions:**
- License / terms of use for RII and GreenStep data (redistribution, derived works)?
- Mapping cost from RII's energy/waste/travel model to GPC sectors — is it tractable, or lossy?
- Recency and update cadence per city (RII is annual for ~30 cities; city-published inventories vary).
- Do the cohort cities (TBC) fall inside RII coverage? Most high-capacity MN cities do; Mankato notably may not.

**Outcome (to date):** candidates identified (see candidates.yaml). RII is the primary `investigate` → likely `promote`; GreenStep is a companion `investigate`; per-city CAP-embedded inventories are `deprioritize` (inconsistent, not a single dataset). Not yet promoted to review — access/license and GPC-mapping need confirming first.
