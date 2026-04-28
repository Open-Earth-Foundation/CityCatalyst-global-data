# AdaptaBrasil MCTI methodology review insights (v1 release)

This note reviews the official MCTI methodology documents collected in `methodology/` and consolidates strengths and limitations relevant for downstream ingestion and API serving.

## Scope and source set reviewed

Methodologies reviewed (official sector documents):

- `Teórico-metodológico_Recursos_Hidricos_2.0_19_08_2025.md`
- `Teorico-metodologico_Segurança_Alimentar-15_08_25.md`
- `Teórico-metodológico_Segurança_Energética_19_07_2023.md`
- `Teorico-metodologico_Malaria_LV_LTA_Arboviroses_25_10_2024.md`
- `Teorico_metodologico_Biodiversidade_Integridade_13_12_2024.md`
- `Teórico-metodológico_AdaptaBrasil_1-0-1 Desastres Geohidrológicos.md`
- `Teórico-metodológico_Infraestrutura_rodoviaria_30_10_2023.md`
- `Teórico-metodológico_Infraestrutura_ferroviaria_30_10_2023.md`
- `Teórico-metodológico_Infraestrutura_portuária_20_06_2022_versão_1.1.md`

## Advantages identified

### 1) Subnational resolution (municipal-first serving value)

- The methodology explicitly targets municipal interpretation in multiple sectors, including direct references to municipal normalization and index construction.
- Water resources documents explicitly describe municipal representation/aggregation (e.g., municipal representation of scarcity and basin-to-municipality association) and state that outputs are represented at municipal analysis level.
- Even where source data exists at other levels (subsystem/state), methods describe transformations/replication to support municipal-level platform display.

Why this matters for us: this supports city-centric product use cases and enables direct alignment with municipal adaptation workflows.

### 2) Standardized impact-chain / hierarchical framework

- Cross-sector methodological backbone is consistent: risk emerges from interaction of **Ameaça (Hazard)**, **Exposição (Exposure)**, and **Vulnerabilidade (Vulnerability)**, grounded in IPCC-aligned framing.
- Sector documents repeatedly use hierarchical composition of indicators/indices across levels, with explicit roll-up logic.
- Water and food-security methodologies explicitly use cascading/chain-impact framing (impactos em cascata / risco encadeado), matching the modeled `L1..L6` hierarchy used in this review release.

Why this matters for us: a stable semantic hierarchy enables reusable schema (`sector`, `risk`, `risk_component`, impact-chain nodes, base indicator) across sectors.

### 3) CCRA-style alignment (methodological fit for climate risk assessment)

- Methods are sector-based, scenario-based, and multi-horizon (present + future windows), which is consistent with climate change risk assessment practice.
- Documents ground methods in IPCC frameworks (AR5/AR6 references across sectors), with explicit treatment of uncertainty, adaptation relevance, and decision support.
- Several sectors include explicit scenario comparisons and horizon-based interpretation (e.g., 2030/2050 windows, optimistic/pessimistic labels tied to emissions pathways).

Why this matters for us: supports policy-facing interpretation and comparability with broader climate-risk assessment narratives.

## Limitations and caveats identified

### 1) Infrastructure sectors are not natively municipal in their core evidence model

- Port methodology is asset-based (coastal public ports; 21-port comparative analysis), not municipality-native.
- Road/rail methodologies are infrastructure-network impact models and include non-municipal components in their data logic.
- In practice, this creates a mismatch for strictly municipal serving patterns: not every infrastructure indicator should be interpreted as municipality-native signal.

Implication: infrastructure sectors should be tagged with explicit spatial-support metadata (asset/subsystem/state/municipal) in downstream tables.

### 2) Scenario coverage is heterogeneous across sectors

- Water resources v2.0 uses AR6 CMIP6 framing with SSP2-4.5 and SSP5-8.5, with baseline and future windows.
- Infrastructure methods (road/rail/ports) are tied to AR5-era RCP pathways (RCP4.5 and RCP8.5) with their own period mappings.
- Energy methodology uses Quarta Comunicação Nacional inputs and selects SWL2 where needed due to data availability constraints.

Implication: scenario identifiers are not uniform across sectors/versions; API contracts must preserve source scenario semantics and avoid forced cross-sector conflation.

### 3) Vintage inconsistency (method release dates and data windows vary)

- Methodology document versions span at least 2022 to 2025.
- Sector baselines and present/future windows differ (for example, AR5-era 1986-2005/2021-2040/2041-2060 mappings in infrastructure vs updated windows and AR6 references in water v2.0).
- Some sector methods are explicitly updated to 2.x while others remain in 1.x lineage.

Implication: any aggregated product should expose `methodology_version`, `source_vintage`, and `scenario_family` fields to prevent misleading cross-sector comparisons.

### 4) Why `Hazard/Exposure/Vulnerability` can be blank in some rows

- In some sector-risk branches, the hierarchy does not force a full `Hazard -> Exposure -> Vulnerability` decomposition for every base indicator.
- This is visible in Energy Security (`Access`, `Availability`), where some indicators are attached directly under the risk node in the modeled hierarchy.
- As a result, extraction tables can contain rows with valid base-indicator values while `risk_component_*` fields are empty.

Reason: this is a **structural hierarchy choice** from the source methodology/modeling (branch-specific design), not necessarily a missing-data error.

Practical interpretation rule:
- If component fields are empty but indicator values are present, treat as **structural null** (component not applicable to that indicator path).
- If indicator numeric value is empty and status is `Data unavailable`, treat as **data-gap null**.

## Recommended implementation guardrails

1. Keep the modeled hierarchy as the semantic serving layer, but include sector-specific metadata about spatial support and scenario family.
2. Do not assume every sector has equivalent municipal fidelity; flag infrastructure outputs as conditional/non-municipal where needed.
3. Preserve original scenario families (`SSP`, `RCP`, `SWL`) and avoid synthetic harmonization without documented conversion rules.
4. Add explicit provenance columns in serving tables:
   - `methodology_doc`
   - `methodology_version`
   - `scenario_family`
   - `scenario_label`
   - `baseline_period`
   - `projection_period`
   - `spatial_support_level`

## Bottom line

The official MCTI methodology set is strong for city-facing climate-risk products because it combines municipal interpretability, a standardized impact-chain logic, and policy-relevant scenario framing. The main operational risk is heterogeneity: infrastructure spatial granularity, scenario-family differences, and mixed methodological vintages must be represented explicitly in the data model rather than normalized away.
