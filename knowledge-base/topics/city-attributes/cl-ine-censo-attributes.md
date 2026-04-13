# City Attribute Interpretation: Chile INE Censo 2024

**Table:** `modelled.city_attribute`
**Datasource:** `cl-ine-censo`
**Publisher:** Instituto Nacional de Estadísticas (INE), Chile
**Release:** 2024
**Source URL:** https://censo2024.ine.gob.cl/resultados/
**Geographic coverage:** All Chilean comunas
**Spatial grain in `city_attribute`:** comuna (sub-city administrative unit)

---

## About this source

The INE Censo is Chile's official national population and housing census, conducted
approximately every 10 years. The 2024 census covers all ~346 comunas in Chile and is
the primary source for socioeconomic, housing, and employment indicators at the
local level.

This is a high-authority source (official national statistics) with full territorial
coverage and high spatial resolution. However, because it is a decennial census,
values will not change until the next census is conducted.

---

## The `attribute_category` scale for this dataset

Categories are quintile bands calculated across **all Chilean comunas** for each
indicator independently. They reflect relative standing within Chile — not an
international or absolute standard.

| Category | Meaning |
|---|---|
| `very low` | Bottom ~20% of Chilean comunas for this indicator |
| `low` | ~20th–40th percentile nationally |
| `medium` | ~40th–60th percentile nationally |
| `high` | ~60th–80th percentile nationally |
| `very high` | Top ~20% of Chilean comunas for this indicator |

> ⚠️ A `very low` category does **not** always mean a poor outcome. For `electricity_access`,
> nearly all comunas have 100% access, so a `very low` category may simply mean the comuna
> has the same universal access as most others — the distribution is compressed. Always
> read the numeric `attribute_value` alongside the category.

---

## Attribute definitions

### `electricity_access`

**What it measures:** The share of dwellings with access to any electricity source,
including grid, solar panel, generator, or other.

**Source variable:** `p9_fuente_elect` from the viviendas (dwellings) file.
- Values 1–5 = has electricity (any source)
- Value 6 = no electricity

**Interpretation of the value:** A value of `100.0` means all surveyed dwellings have
at least one electricity source. Values below 100 indicate a share of dwellings without
any power. In Chile, most comunas have near-universal access; low values typically appear
in isolated rural areas.

**Why `attribute_category` can be misleading here:** Because access is near-universal
across Chile, most comunas fall into `very low` or `low` — not because access is poor,
but because the distribution has little variation at the top. A `very low` category
here likely means "similar to the majority" rather than "worse than most."

**Climate and planning relevance:**
- Baseline for electrification planning and transport decarbonisation
- Comunas with below-100% access are candidates for off-grid renewable programmes
- Important context for electric vehicle adoption potential

---

### `home_ownership`

**What it measures:** The share of households that own their dwelling, either fully paid
off or still paying a mortgage.

**Source variable:** `p12_tenencia_viv` from the hogares (households) file.
- Value 1 = `Propia pagada` (fully owned)
- Value 2 = `Propia pagándose` (owned, mortgage ongoing)

**Interpretation of the value:** A value of `40.0` means 40% of households in that
comuna own their home. Higher values indicate more owner-occupier communities; lower
values indicate more renters or other tenure types (e.g. occupants without contract,
family arrangements).

**Climate and planning relevance:**
- Owner-occupiers are more likely to invest in energy efficiency improvements
  (insulation, solar panels, heat pumps) because they directly benefit from the savings
- Low ownership → higher renter share → split-incentive problem for efficiency retrofits
- Relevant to residential stationary energy emissions and building-stock transition

---

### `renter_share`

**What it measures:** The share of households renting their dwelling, either with or
without a formal contract.

**Source variable:** `p12_tenencia_viv` from the hogares (households) file.
- Value 3 = `Arrendada con contrato` (formal rental)
- Value 4 = `Arrendada sin contrato` (informal rental)

**Interpretation of the value:** A value of `43.48` means approximately 43% of households
are renters. Note that `home_ownership + renter_share` will typically not sum to 100%
because there are other tenure types (e.g. gifted housing, occupants without title).

**Relationship to `home_ownership`:** These are complementary indicators from the same
source variable but they are not strict complements — the gap is occupied by other
tenure types.

**Climate and planning relevance:**
- High renter share is a key vulnerability proxy: renters often have lower income,
  less housing security, and limited ability to improve their dwelling conditions
- Informal renters (no contract) are especially exposed to displacement risk from
  climate adaptation works
- Relevant to equity analysis in climate action planning

---

### `industry_construction_employment`

**What it measures:** The share of the employed population working in mining,
manufacturing, or construction sectors.

**Source variable:** `cod_caenes` from the personas (persons) file, filtered to
employed persons (`sit_fuerza_trabajo = 1`).
- CAENES code B = Mining and quarrying
- CAENES code C = Manufacturing
- CAENES code F = Construction

**Interpretation of the value:** A value of `22.79` means approximately 23% of employed
residents work in these combined industrial sectors. High values indicate an industrial
economic base in the local labour force.

**Important caveat:** This measures where residents *work*, not where industrial
activity *occurs*. A high value in a residential suburb could reflect workers who
commute to nearby industrial zones.

**Climate and planning relevance:**
- Proxy for local economic exposure to industrial sector emissions (Scope 1 stationary
  energy, IPPU)
- Useful context when cross-referencing with GPC emissions data — high employment in
  industry may correlate with local political economy constraints on emission reductions
- Relevant to just-transition planning: high industrial employment = higher workforce
  dependence on sectors targeted for decarbonisation

---

### `transport_logistics_employment`

**What it measures:** The share of the employed population working in transport,
storage, and logistics.

**Source variable:** `cod_caenes` from the personas (persons) file, filtered to
employed persons (`sit_fuerza_trabajo = 1`).
- CAENES code H = Transporte y almacenamiento (transport and storage)

**Interpretation of the value:** A value of `7.35` means approximately 7% of employed
residents work in transport or logistics. Higher values suggest significant freight,
distribution, or passenger transport activity in the local economy.

**Climate and planning relevance:**
- Proxy for the significance of the transport sector in the local economy
- May correlate with higher road freight emissions (GPC sector II) and associated
  air quality impacts
- Useful for targeting transport decarbonisation interventions and assessing workforce
  exposure to EV/freight transition

---

## Indicators reviewed but not currently mapped

The following indicators from the Censo are identified in the dataset review as
potentially useful but are not yet mapped into `city_attribute`:

| Potential indicator | Source variable | Status |
|---|---|---|
| Vehicle ownership rate | `p45_medio_transporte` (commute mode proxy only) | Not directly available; proxy under review |
| Urban vs. rural population split | `area` field | Not yet extracted |
| Household size | Derived from hogares + personas records | Not yet extracted |

---

## Known limitations

- **Decennial frequency:** Values reflect 2024 conditions and will not update until
  the next census (expected ~2034)
- **Employment sector definition:** CAENES codes may differ from labour survey
  (ENE) definitions, so comparisons with labour market data should be treated carefully
- **Resident vs. workplace geography:** Employment indicators reflect where people
  *live*, not where industry *operates*
- **Vehicle ownership gap:** Direct vehicle ownership data is not available at
  the required level of detail; commute mode (`p45_medio_transporte`) is a proxy only
- **Category compression at 100%:** For `electricity_access`, near-universal access
  compresses the distribution, making quintile categories less informative than the
  raw value

---

## Related files

- Dataset review: `dataset-review/reviews/cl-ine/cl-ine-censo/README.md`
- Release review: `dataset-review/reviews/cl-ine/cl-ine-censo/releases/2024/review.yaml`
- Variable dictionaries: `dataset-review/reviews/cl-ine/cl-ine-censo/releases/2024/sample/dictionary_*.csv`
- Generic table guide: `domain-knowledge/topics/city-attributes/city_attribute-table.md`
