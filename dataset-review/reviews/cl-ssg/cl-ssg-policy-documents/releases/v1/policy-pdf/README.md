# Sample data — Chile policy document inventory (2026)

| File | Description |
|------|-------------|
| `data_requirements_local_codes.csv` | Chile region / province / comuna codes (INE-style), source for the join keys. |
| `data_requirements_general_policies.csv` | Curated manifest: policy name, type, governance body, territorial scale and codes, and source `link` (URL or placeholder text). |
| `data_requirements_combined.csv` | **Long join:** every Chile comuna × each policy whose `territory_code` applies to that comuna. **snake_case** columns; geography first, then document fields. `record_source` = `comuna_policy`. |

**Encoding:** UTF-8.

**`data_requirements_general_policies.csv` columns:** empty first column, `Territory_code`, `Policy name`, `Type of Policy`, `Governance`, `Scale`, `Scale level_code`, `Region_code`, `Communal_Code`, `Sector_code`, `link`.

**`data_requirements_combined.csv` column order:** `record_source`, then INE geography (`codigo_region`, `nombre_region`, `abreviatura_region`, `codigo_provincia`, `nombre_provincia`, `codigo_comuna_2018`, `nombre_comuna`), then policy fields (`territory_code`, `policy_name`, `type_of_policy`, `governance`, `scale`, `scale_level_code`, `region_code`, `communal_code`, `sector_code`, `link`). On each row, `region_code` / `communal_code` are filled from `territory_code` when it encodes a regional or communal scope.

**Territory matching (for the join):** `1_*_*` national (`1_00_00`) → all comunas; `2_00_00` → all comunas (generic regional instrument placeholders); `2_XX_*` with `XX` not `00` → comunas in region `XX` (zero-padded); `3_XX_YYYYY` → comuna `YYYYY` in region `XX`; `4_*_*` inter-communal → all comunas (broad applicability).

**Parsing note:** The general-policies source file splits `Scale level_code` across commas; the builder rejoins those segments into `scale_level_code`.

**Regenerate:** from this release folder run `python3 build_combined_csv.py` (writes `sample/data_requirements_combined.csv`).

**Note:** Some `link` values are not URLs (e.g. `*1 per Region*`, `In process`). Treat as metadata until resolved to concrete sources.
