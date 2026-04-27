# Emissions Value Interpretation — Sector Context

This document helps someone unfamiliar with city-level emissions data make sense of
a value they are looking at. It is organised by GPC sector because the same number
means very different things depending on what sector produced it.

For machine-readable QA and MCP integration, use the companion rules file:
`sector-value-context.thresholds.yaml`.

**This is not a schema document.** For column definitions and table structure, see
`emissions-table.md`. This document is about what the *values themselves* mean —
whether a number is plausible, what it implies about a city, and what should make
you suspicious.

---

## Before reading any value

Three things must be known before a number is interpretable:

**Units and scale.** `emissions_value` is stored in tonnes of CO2-equivalent (tCO2e).
Check `emissions_units` to confirm. A value of `42000` in tCO2e is a small city's
annual residential heating — the same number in ktCO2e would be implausible for all
but the largest megacities in the most emissions-intensive sectors.

**Gas coverage.** Check the source documentation for whether the value includes
CO2 only, or a full gas basket (CO2 + CH4 + N2O ± F-gases). In waste and agriculture
sectors, methane dominates — a CO2-only figure for solid waste disposal would be a
fraction of the true total. Sources do not always document this clearly; when in doubt,
flag it.

**GWP basis.** When gases are combined into CO2-equivalent, a global warming potential
(GWP) factor is applied. Different IPCC Assessment Reports give different GWPs —
methane is 25 (AR4), 28 (AR5), or 27.9 (AR6). Most sources use AR5. A ~10% discrepancy
between two estimates in a methane-heavy sector is often explained by GWP basis alone
before any real difference in the underlying data.

---

## How to use this document

Each sector entry below provides:

- **What this covers** — which real-world activities and emission sources are included
- **Recommended normalisation** — what basis makes values comparable across cities
- **Expected range** — rough magnitude by city size `[TO RESEARCH — see note below]`
- **Drivers of variation** — what legitimately makes a value high or low
- **High value suggests** — what to infer about a city with an elevated figure
- **Low value suggests** — what to infer, or what data issues to consider
- **Plausibility flags** — specific conditions that should trigger a review


## Sector I — Stationary Energy

Stationary energy covers all fuel combustion and electricity use that is not transport.
It is typically the largest single sector in city inventories. The dominant subsectors
for most cities are residential buildings and commercial/institutional buildings.

---

### I.1 — Residential Buildings

**What this covers:** All energy use in homes — heating, cooling, cooking, lighting,
appliances. Includes grid electricity (as Scope 2) and direct fuel combustion (gas,
oil, biomass — Scope 1).

**Recommended normalisation:** Per capita (tCO2e per person per year). Residential
emissions are directly tied to population, making per-capita comparison the most
meaningful lens for cross-city comparison. Be cautious of cities with large seasonal
or transient populations (tourist cities, university towns) where resident population
understates actual energy demand.

**Expected range:**

| City size | Per capita (tCO2e/person/yr) |
|---|---|
| Small (< 500k population) | `[TO RESEARCH]` |
| Medium (500k – 2M) | `[TO RESEARCH]` |
| Large (> 2M) | `[TO RESEARCH]` |

> Research note: Stratify by climate zone (heating degree days) in addition to
> city size, as climate is likely the dominant driver of cross-city variation here.

**Drivers of variation:**
- Climate: cities with cold winters or hot summers have significantly higher energy demand for heating/cooling
- Grid carbon intensity: cities in high-renewables grids will show lower Scope 2 residential emissions
- Building stock age: older buildings are less insulated; emissions intensity is higher
- Fuel mix: cities reliant on oil or coal for heating have higher direct emissions than those using gas or heat pumps
- Household size: smaller average household size means higher per-capita floor area and energy use

**High value suggests:**
- Cold or hot climate with energy-intensive heating or cooling requirements
- Carbon-intensive electricity grid
- Older, less efficient building stock
- Low household density (detached housing vs apartments)
- Possible double-counting with I.2 if commercial and residential boundaries are unclear in the source

**Low value suggests:**
- Mild climate with low heating/cooling demand
- High share of renewables in the electricity grid
- Dense, multi-family housing with lower per-unit surface area
- Possible data gap: some sources exclude Scope 2 (electricity) from residential and only report direct fuel combustion, which substantially understates the total

**Plausibility flags:**
- A value of exactly zero is almost certainly a data gap — every city has residential energy use
- Values that are implausibly low relative to population may indicate the source only covers Scope 1 (direct combustion) and excludes electricity
- Cross-check: I.1 + I.2 combined should generally be the largest share of total city emissions unless the city has a dominant industrial or port sector

---

### I.2 — Commercial and Institutional Buildings

**What this covers:** Energy use in offices, retail, hotels, hospitals, schools,
government buildings. Includes grid electricity (Scope 2) and direct fuel combustion
(Scope 1). Sometimes called "tertiary" or "services" sector.

**Recommended normalisation:** Per capita, or per unit of commercial floor area if
available. Per capita is the practical default for cross-city comparison.

**Expected range:**

| City size | Per capita (tCO2e/person/yr) |
|---|---|
| Small (< 500k population) | `[TO RESEARCH]` |
| Medium (500k – 2M) | `[TO RESEARCH]` |
| Large (> 2M) | `[TO RESEARCH]` |

> Research note: Capital cities and major business centres will have disproportionately
> high commercial emissions relative to their resident population — consider flagging
> this as a systematic pattern rather than an anomaly.

**Drivers of variation:**
- Economic structure: cities with large financial, government, or hospitality sectors have more commercial floor area per capita
- Climate: cooling load in hot climates drives electricity intensity of commercial buildings
- Grid carbon intensity
- Data boundary: some datasets bundle commercial with residential (I.1+I.2 combined) — check source documentation

**High value suggests:**
- City is a regional or national economic hub with high commercial activity relative to population
- Climate-driven cooling demand (hot cities)
- Possibly a reporting or bundling issue with I.1 — check if both I.1 and I.2 are elevated together

**Low value suggests:**
- City has limited commercial/institutional activity (residential or industrial profile)
- Source may only cover public buildings and exclude private commercial — check source scope
- Possible gap: some inventories skip I.2 entirely when data is unavailable

**Plausibility flags:**
- Zero values should be treated as data gaps unless the city is extremely small and primarily residential
- I.2 should not exceed I.1 in most residential cities; if it does, verify the source is not double-counting electricity

---

### I.3 — Manufacturing Industries and Construction

**What this covers:** Energy used by manufacturing plants, factories, and construction
activity within the city boundary. Scope 1 only (direct fuel combustion). Does not
include process emissions (those fall under Sector IV — IPPU).

**Recommended normalisation:** Per capita is less meaningful here — industrial output
or economic value added is a better denominator, but rarely available at city level.
Use per capita as a default but interpret alongside economic structure data.

**Expected range:**

| City size | Per capita (tCO2e/person/yr) |
|---|---|
| Small (< 500k population) | `[TO RESEARCH]` |
| Medium (500k – 2M) | `[TO RESEARCH]` |
| Large (> 2M) | `[TO RESEARCH]` |

> Research note: This will have high variance — industrial cities may be 5–10x the
> median; service-economy cities may be near zero. Report the distribution shape, not
> just central tendency.

**Drivers of variation:**
- Presence of energy-intensive industries (steel, cement, chemicals, paper) within city limits
- Whether the city boundary includes surrounding industrial zones or is drawn tightly around the urban core
- Fuel mix in industry (coal vs gas vs electricity)

**High value suggests:**
- City has significant manufacturing or heavy industry located within its administrative boundary
- May be a port city or industrial hub
- Worth cross-referencing with city-attribute `industry_construction_employment` to confirm

**Low value suggests:**
- Service economy or post-industrial city
- Industry may exist but be located outside the city boundary (e.g. in a surrounding municipality)
- Normal for most large metropolitan cores where industrial land use has been displaced

**Plausibility flags:**
- If I.3 is very high but the city has low industrial employment, suspect the source is using a wide geographic boundary that captures industrial zones not in the city proper
- Sector IV (IPPU) should be checked alongside I.3 — large industrial emitters often have both energy and process emissions

---

### I.4 — Energy Industries (Power Generation)

**What this covers:** Emissions from electricity generation, heat production, and fuel
transformation (refineries, gas processing) located within the city boundary. This
captures power plants physically located in the city, not the electricity consumed by
the city.

**Recommended normalisation:** This sector requires special care. A city that happens
to host a power plant serving a wider region will show very high I.4 emissions that
have nothing to do with the city's own energy consumption. Per-capita comparison is
almost meaningless here — always note whether a city is a net power exporter.

**Expected range:**

| City size | Per capita (tCO2e/person/yr) |
|---|---|
| Small (< 500k population) | `[TO RESEARCH]` |
| Medium (500k – 2M) | `[TO RESEARCH]` |
| Large (> 2M) | `[TO RESEARCH]` |

**Drivers of variation:**
- Whether a power plant is physically sited within the city boundary
- Type of generation (coal, gas, oil vs renewables)
- Whether the city is a net exporter of electricity to a wider grid

**High value suggests:**
- A power plant, refinery, or other energy facility is within the city limits
- This may represent a large share of regional or national generation — do not interpret as local consumption

**Low value suggests:**
- No major power generation infrastructure within the city
- Normal for most cities that consume electricity produced elsewhere

**Plausibility flags:**
- Very high I.4 in a small city almost always means a power plant is in the boundary — verify before treating as anomaly
- Some sources exclude I.4 from city totals on the grounds that the city is not the "consumer" — always check whether totals include or exclude this subsector

---

## Sector II — Transportation

Transportation is typically the second or third largest sector in city inventories.
For car-dependent cities in high-income countries it often exceeds stationary energy.

---

### II.1 — On-Road Transportation

**What this covers:** All vehicles using public roads within the city boundary —
private cars, buses, trucks, motorcycles, delivery vehicles. Includes both resident
vehicles and pass-through traffic. Scope 1 (direct tailpipe combustion).

**Recommended normalisation:** Per capita (tCO2e per person per year). Can also be
normalised by vehicle kilometres travelled (VKT) if available, which better isolates
emission intensity from travel demand.

**Expected range:**

| City size | Per capita (tCO2e/person/yr) |
|---|---|
| Small (< 500k population) | `[TO RESEARCH]` |
| Medium (500k – 2M) | `[TO RESEARCH]` |
| Large (> 2M) | `[TO RESEARCH]` |

> Research note: Also consider stratifying by density (compact vs sprawling) and
> transit investment level as secondary dimensions — both are strong predictors.

**Drivers of variation:**
- Urban density: compact, walkable cities have substantially lower per-capita transport emissions
- Public transit availability and modal share
- Freight intensity: port cities and logistics hubs have high truck traffic through the boundary
- Highway pass-through traffic: a city on a major freight corridor will absorb emissions from vehicles that neither start nor end their trip there
- EV adoption rate (becomes significant after ~15–20% fleet share)

**High value suggests:**
- Car-dependent city with low transit investment and low density
- Significant freight or highway pass-through traffic
- Limited active transport infrastructure
- Possibly a sprawling metropolitan area where surrounding car-dependent suburbs contribute

**Low value suggests:**
- Dense, transit-rich city with high modal share on public transport or active modes
- High EV penetration in a jurisdiction with clean electricity
- Possible data gap: some sources use top-down national disaggregation that understimates city-level traffic if the national model is not calibrated to local road networks

**Plausibility flags:**
- II.1 is the most frequently reported transport subsector — if it is zero or missing, assume data gap
- Very high values relative to a dense city may indicate pass-through freight is being captured in the boundary; check if the city is on a major highway or port corridor
- Compare with city-attribute `transport_logistics_employment` — high logistics employment + low transport emissions warrants investigation

---

### II.2–II.5 — Other Transport (Rail, Water, Aviation, Off-Road)

**What this covers:** Railways (II.2), waterborne navigation including ports (II.3),
aviation (II.4), and off-road vehicles including construction and agricultural
machinery (II.5).

**Recommended normalisation:** Per capita for overview; absolute values when assessing
port or airport impact specifically.

**Expected range:** `[TO RESEARCH]` — Note: these subsectors are frequently missing
from city inventories because data is harder to collect. A zero or null value is as
likely to mean "not reported" as "zero emissions." Always check source documentation
before treating as zero.

**Drivers of variation:**
- II.2 (Rail): presence of freight rail lines through city; electrification of rail
- II.3 (Water): whether the city is a port; size and type of port activity (container, bulk, passenger)
- II.4 (Aviation): whether an airport falls within the city boundary; LTO (landing and takeoff) cycles vs full flight
- II.5 (Off-road): construction activity cycles; presence of mining or agricultural equipment within city limits

**Plausibility flags:**
- For II.4 specifically: some sources include only LTO (landing and takeoff) emissions within the city boundary; others include cruise altitude emissions allocated to the departure airport. These can differ by an order of magnitude — always check methodology
- Port cities with II.3 emissions should cross-reference with known port throughput data to sense-check magnitude

---

## Sector III — Waste

Waste is dominated by methane from landfills and wastewater, making GWP basis
(see preamble) especially important here. A CO2-only figure for this sector is
almost certainly incomplete.

---

### III.1 — Solid Waste Disposal

**What this covers:** Methane (and some CO2) from organic matter decomposing in
landfills and open dumps located within or attributed to the city. This includes
legacy emissions from closed landfills that continue to produce gas for decades.

**Recommended normalisation:** Per capita (tCO2e per person per year). Also useful to
compare against known waste generation rates (kg/person/day) if available.

**Expected range:**

| City size | Per capita (tCO2e/person/yr) |
|---|---|
| Small (< 500k population) | `[TO RESEARCH]` |
| Medium (500k – 2M) | `[TO RESEARCH]` |
| Large (> 2M) | `[TO RESEARCH]` |

> Research note: High variation expected between high-income cities (managed landfills
> with gas capture, or landfill diversion) and lower-income cities (open dumps, high
> organic fraction). Treat as two distinct reference populations.

**Drivers of variation:**
- Waste composition: high organic fraction (food waste) produces more methane
- Landfill management: gas capture and flaring dramatically reduce net emissions; open dumping maximises them
- Landfill boundary attribution: the physical landfill may be outside city limits but serve the city's waste — attribution practices vary by source
- Legacy emissions: old closed landfills continue emitting for 20–40 years after closure
- GDP level: higher-income cities have more packaging waste (less organic) and better landfill management

**High value suggests:**
- Open dumping or unmanaged landfill within or attributed to the city
- High organic fraction in waste stream (food-heavy diets, low packaging)
- Large legacy landfill with no gas capture
- Regional landfill that serves neighbouring municipalities counted in the city's boundary

**Low value suggests:**
- High landfill diversion (recycling, composting, incineration)
- Active landfill gas capture and flaring or energy recovery
- Possibly: the landfill is outside city limits and has not been attributed to the city — check methodology

**Plausibility flags:**
- If GWP basis is AR4 (CH4 = 25) vs AR5 (CH4 = 28), the same physical emissions will differ by ~12% — always check before comparing two sources
- A very low or zero value in a city without documented landfill gas capture or high diversion rates is suspicious
- Regional landfill attribution is one of the most common sources of apparent discrepancy between city-reported inventories and top-down source estimates

---

### III.4 — Wastewater Treatment and Discharge

**What this covers:** Methane and nitrous oxide from treatment of sewage and
industrial wastewater, including emissions from treatment plants and discharge
into water bodies.

**Recommended normalisation:** Per capita.

**Expected range:**

| City size | Per capita (tCO2e/person/yr) |
|---|---|
| Small (< 500k population) | `[TO RESEARCH]` |
| Medium (500k – 2M) | `[TO RESEARCH]` |
| Large (> 2M) | `[TO RESEARCH]` |

**Drivers of variation:**
- Treatment type: anaerobic treatment produces more methane than aerobic; advanced treatment plants often capture it
- Sewage connection rate: cities with low sewerage coverage have different emission profiles from open or septic systems
- Industrial wastewater load: food processing, brewing, and other organic-rich industrial effluents increase emissions

**High value suggests:**
- Large or inefficient treatment plants with no methane capture
- High industrial organic effluent load
- Significant informal or unconnected population using pit latrines or open drainage (different emission profile, but still significant)

**Low value suggests:**
- High-efficiency treatment with gas capture and energy recovery
- Possible data gap — wastewater is one of the subsectors most frequently missing from city inventories

**Plausibility flags:**
- N2O from wastewater can be significant but is often not reported separately — check if the source includes it
- Zero values are a common data gap indicator here

---

## Sector IV — Industrial Processes and Product Use (IPPU)

**What this covers:** Emissions from industrial chemical reactions that are not
combustion — cement calcination, steel making, chemical production, refrigerants
(F-gases). This is separate from the energy used to power those same processes
(which sits in Sector I).

**Recommended normalisation:** Not meaningful on a per-capita basis for most cities.
Useful as an absolute value or as a share of total city emissions.

**Expected range:** Highly variable. Most cities will have near-zero IPPU. Cities
with cement plants, steel mills, or large chemical facilities will have values that
can dwarf all other sectors. `[TO RESEARCH — but flag that this is a bimodal
distribution, not a normal one]`

**Plausibility flags:**
- High IPPU + high I.3 together confirm a genuine industrial city profile; high IPPU alone with low I.3 is worth investigating
- F-gas (refrigerant) emissions are frequently underreported at city level — absence does not mean zero

---

## Sector V — Agriculture, Forestry and Land Use (AFOLU)

**What this covers:** Methane from livestock, nitrous oxide from soils and
fertiliser, and CO2 from land use change and forestry within city limits. Can also
include carbon sinks (urban forests, green space) as negative values.

**Note:** AFOLU is rarely significant in dense urban cores. It becomes important for
cities with large peri-urban agricultural areas within their administrative boundary,
or cities that explicitly include their surrounding rural hinterland in their
inventory boundary.

**Expected range:** Near zero for most dense cities. Potentially significant for
cities with large administrative areas that include rural and agricultural land.
`[TO RESEARCH — but distinguish urban-core cities from cities with wide administrative
boundaries]`

**Plausibility flags:**
- A large AFOLU figure from a city known to be densely urban suggests a wide boundary definition or a boundary misclassification
- Negative AFOLU values (carbon sequestration) are valid but rare — they require credible forestry or land-use accounting methodology

---