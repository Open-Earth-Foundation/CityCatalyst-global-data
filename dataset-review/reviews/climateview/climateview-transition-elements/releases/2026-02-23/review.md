# Glossary for `export-2026-02-23/transition_elements.csv`

This glossary explains the key terms and fields used in the TEF `transition_elements.csv` export.

## Row-level concept

- **Transition Element (TE)**: One mitigation intervention option. Each row is one TE with an identifier, classification, and relationship fields (what it acts on, and what it shifts to).

## Field glossary (data dictionary)

- **`stable_id`**: Machine-friendly unique key for the transition element.
  - Example: `shift_to_electric_vehicles`
  - Use for joins and programmatic references.

- **`short_label`**: Human-readable label that includes TE code and name.
  - Example: `T-1A1a-TE-1 - Shift to electric cars`

- **`description`**: Narrative description of the intervention and intended change.
  - Notes: Some rows contain truncated or templated text.

- **`sector_id`**: Top-level sector code.
  - Observed values: `1-transport`, `2-industry`, `3-afolu`, `4-buildings`, `5-energy`, `6-waste`

- **`sector_path`**: Hierarchical taxonomy path for the intervention area.
  - Example: `Transport > Mobility > Road > Light Duty Vehicles`

- **`type`**: Intervention logic type.
  - `shift`: moves activity/demand/fuel/technology from one state to another
  - `improve`: increases efficiency or lowers emissions intensity without explicit from-to transfer

- **`sustainability_class`**: TE color class used as a qualitative sustainability signal.
  - Observed values: `green`, `amber`, `red` (some rows blank)
  - Practical interpretation:
    - `green`: typically lower-carbon / co-benefit-aligned options
    - `amber`: transitional or context-dependent options
    - `red`: higher-carbon options (for baseline/mix modeling context)

- **`co_benefits`**: JSON-style array of additional expected benefits.
  - Example values: `air_quality`, `reduced_noise`, `job_creation`, `less_congestion`
  - Stored as stringified list in CSV (not normalized table format).

- **`ipcc_ref`**: Reference slug to an IPCC-style mitigation concept.
  - Example: `1a-12-electric-technologies`
  - Notes: Some rows are empty.

- **`acts_on_labels`**: JSON-style array of baseline technologies/activities the TE acts on.
  - Example: `["petrol vehicles", "diesel vehicles"]`
  - Think of this as the "from" side.

- **`shifts_to_labels`**: JSON-style array of destination technologies/activities.
  - Example: `["battery electric vehicles"]`
  - Mostly populated for `shift` rows; often empty for `improve` rows.
  - Think of this as the "to" side.

- **`status`**: Lifecycle state of the TE record.
  - Observed value: `active`

- **`version_introduced`**: Export/release date when this TE version appears.
  - Observed format: `YYYY-MM-DD` (example: `2026-02-23`)

- **`version_deprecated`**: Date when a TE is retired/replaced.
  - Often empty in this extract.

## TE code anatomy in `short_label`

Pattern example: `T-1A1a-TE-1`

- **`T`**: Transition element namespace.
- **`1A1a`**: Hierarchical sector/subsector code aligned with TE taxonomy.
- **`TE`**: Transition Element marker.
- **`1`**: Sequence number within that code group.

## Common terms in this dataset

- **Modal shift**: Moving mobility demand from one mode to another (e.g., cars to rail).
- **Fuel shift**: Changing fuel source (e.g., diesel to electricity, gas to biogas).
- **Electrification**: Replacing direct fossil fuel use with electricity-based technologies.
- **Retrofitting**: Improving existing stock (buildings, vehicles, systems) for efficiency.
- **District heating/cooling**: Centralized thermal supply replacing individual systems.
- **CHP (Combined Heat Power)**: Co-generation of heat and electricity from one process.

## Data quality notes for analysts

- Some `description` values are incomplete, placeholder-based, or templated.
- Some `sustainability_class` and `ipcc_ref` fields are blank.
- Arrays are embedded as stringified JSON-like lists in CSV cells.
- Spelling/casing is not fully standardized across labels (for example "commerical", "busses").

Use `stable_id` as the reliable key and treat descriptive text as semi-structured metadata.
