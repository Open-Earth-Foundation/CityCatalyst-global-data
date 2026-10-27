# Collection 2.0 reference data

| File | Purpose |
|------|---------|
| `legend_collection_02.csv` | MapBiomas pixel ID → English class labels ([official codes PDF](http://chile.mapbiomas.org/wp-content/uploads/sites/13/2025/10/Leyenda2025-LEYENDA-CODIGOS.pdf)) |
| `lulc_to_indicator_crosswalk.csv` | MapBiomas class → `indicator_group` (mutually exclusive) |
| `indicator_thresholds.csv` | National absolute `%` thresholds → quintile-style buckets per `*_share` indicator |
| `city_landuse_indicators.csv` | Long table: `comuna_code`, `comuna_name`, `year`, `indicator_group`, `area_pct` |
| `raw_data_cl_mapbiomas_lulc.csv` | INE-shaped export: `region`, `comuna`, `attribute_type`, `attribute_value`, `attribute_category`, … |

## Indicator groups

Each `lulc_class` maps to exactly one `indicator_group`. After GEE zonal stats, `exploration.ipynb` sums pixel shares by group per comuna.

Output columns: `comuna_code`, `comuna_name`, `year`, `indicator_group`, `area_pct` (% of all comuna pixels).

Groups in the crosswalk include `primary_forest`, `secondary_forest`, `silviculture`, `cropland`, `pasture`, `grassland`, `shrubland`, `wetland`, `urban_built`, `water`, `unmapped`, and others — see the CSV for the full list.

`unmapped` (clouds / no data) is included for QA; exclude from action matching if needed.
