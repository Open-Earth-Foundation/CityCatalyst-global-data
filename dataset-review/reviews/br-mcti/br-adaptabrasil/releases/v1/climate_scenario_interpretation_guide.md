# Climate Scenario Interpretation Guide

This release includes indicators across multiple climate scenario types.  
These scenarios are not interchangeable, and they answer different planning questions.

## Scenario groups in this dataset

- `SSP2-4.5` / `RCP4.5`: intermediate or moderate-emissions future (often labeled "optimistic" in relative terms).
- `SSP5-8.5` / `RCP8.5`: high-emissions, high-risk future (often labeled "pessimistic").
- `SWL1.5` / `SWL2.0`: specific warming-level scenarios (+1.5 C and +2.0 C worlds).

## 1) SSPs and RCPs: pathway-based scenarios

SSP/RCP scenarios describe **how the world evolves over time**:

- greenhouse gas emissions
- energy and technology transitions
- socioeconomic development
- mitigation effort

Use SSP/RCP scenarios to answer:

> "How does risk change over time under different development and emissions pathways?"

### RCPs (older generation)

RCP means **Representative Concentration Pathway** (widely used in CMIP5/IPCC AR5).

- `RCP4.5`: around 4.5 W/m² radiative forcing by 2100
- `RCP8.5`: around 8.5 W/m² radiative forcing by 2100

Higher forcing implies stronger warming pressure.

### SSPs (newer generation)

SSP means **Shared Socioeconomic Pathway** (used in CMIP6/IPCC AR6).

They combine:

- socioeconomic storyline
- emissions trajectory

Examples:

- `SSP1-2.6`: sustainability-oriented, lower emissions
- `SSP2-4.5`: middle-of-the-road, moderate emissions
- `SSP3-7.0`: fragmented world, high emissions
- `SSP5-8.5`: fossil-fuel intensive, very high emissions

## 2) SWLs: impact-at-temperature scenarios

SWL means **Specific Warming Level**.

SWLs are **not pathways**. They are temperature thresholds:

- `SWL1.5`: impacts in a +1.5 C world
- `SWL2.0`: impacts in a +2.0 C world

Use SWLs to answer:

> "What does risk look like once the climate reaches this warming level, regardless of exact year?"

## 3) Correct interpretation and mapping

### Related but not identical

- `RCP4.5` is broadly comparable to `SSP2-4.5`
- `RCP8.5` is broadly comparable to `SSP5-8.5`

However:

- RCPs are concentration/forcing-focused
- SSPs include socioeconomic narratives

So treat them as **aligned families**, not exact one-to-one equivalents.

### Pathway vs temperature framing

- **SSP/RCP** = "How do we get there?"
- **SWL** = "What happens at this level of warming?"

This is the key conceptual distinction for analysis and communication.

## 4) Practical use for adaptation and risk work

Recommended interpretation for planning:

- `SSP2-4.5`: moderate baseline for planning and prioritization
- `SSP5-8.5`: high-end stress test for robustness and contingency
- `SWL1.5`: lower warming threshold, often near-term relevance
- `SWL2.0`: stronger impact threshold for adaptation scaling

Useful mental model:

- SSP/RCP = the road humanity takes
- SWL = the temperature milestone reached along that road

## 5) Common mistakes to avoid

- Do not treat SWL values as if they were emission pathways.
- Do not assume SSP and RCP labels are numerically identical in all model outputs.
- Do not call `SSP2-4.5` "safe"; it is lower relative risk than high-end pathways, not no-risk.
- Do not use only one scenario for adaptation decisions; compare moderate, high-end, and warming-level views.

