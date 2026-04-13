# `modelled.city_attribute` — Table Context

This document explains how to read and interpret rows from the `modelled.city_attribute` table.
It is intended as context for AI-assisted data querying and interpretation.

---

## Purpose

`city_attribute` is a long-format (EAV) table that stores socioeconomic, infrastructure,
and demographic indicators at the city or sub-city level. Each row describes a single
indicator for a single place.

These attributes are used as:
- Context indicators for city-level climate action planning
- Inputs to vulnerability and equity assessments
- Proxies for activity data in emissions modelling (e.g. renter share as an efficiency proxy)

---

## Schema

| Column | Type | Description |
|---|---|---|
| `city_id` | varchar (PK) | Internal city identifier |
| `locode` | varchar (PK) | UN/LOCODE identifier for the city or region |
| `country_code` | varchar | ISO 3166-1 alpha-2 country code |
| `region_name` | varchar | Name of the administrative region |
| `attribute_type` | varchar (PK) | The indicator name (snake_case) |
| `attribute_value` | varchar | The numeric or categorical value of the indicator |
| `attribute_units` | varchar | Units for the value (e.g. `percent`, `count`, `index`) |
| `attribute_category` | varchar | Relative classification of the value (see scale below) |
| `datasource` | varchar (PK) | Identifier of the source dataset |
| `datasource_date` | integer | Year of the source data |
| `dataset_id` | uuid | FK to `modelled.publisher_datasource` |
| `release_id` | uuid | FK to `modelled.dataset_release` |

> The composite primary key is `(city_id, locode, attribute_type, datasource)`, meaning
> the same indicator can exist from multiple sources for the same city.

---

## How to read a row

**Example:**
```
locode:             CL-IQQ
attribute_type:     home_ownership
attribute_value:    40.0
attribute_units:    percent
attribute_category: very low
datasource:         cl-ine-censo
datasource_date:    2024
```

**Plain-language interpretation:**
> In Iquique (CL-IQQ), 40% of households own their dwelling, according to Chile's 2024
> national census. This places Iquique in the bottom quintile nationally for home ownership
> among Chilean comunas.

---

## The `attribute_category` scale

`attribute_category` is a **relative classification** of the value compared to all cities
or sub-units in the same country/dataset for that indicator. It is not an absolute standard.

| Value | Meaning |
|---|---|
| `very low` | Bottom ~20% of comparable units |
| `low` | ~20th–40th percentile |
| `medium` | ~40th–60th percentile |
| `high` | ~60th–80th percentile |
| `very high` | Top ~20% of comparable units |

> ⚠️ **Important:** Categories are relative within a dataset's reference population.
> "Very low electricity access" in a dataset where all cities have >95% access is very
> different from the same label in a dataset with wide variation. Always check the
> `datasource` and refer to the dataset-specific interpretation guide.

---

## Interpreting `attribute_value`

`attribute_value` is stored as `varchar` to accommodate both numeric and categorical source
data. When numeric, parse as float. Units are in `attribute_units`.

Common unit types:
- `percent` — a share of the relevant population or dwelling stock (0–100 scale)
- `count` — an absolute count
- `index` — a normalised score (typically 0–1 or 0–100, dataset-specific)

---

## Dataset-specific interpretation guides

For deeper interpretation of specific `attribute_type` values — including how indicators
were derived, source variable mappings, and climate relevance — refer to the
dataset-specific documents in this folder:

| Dataset | Guide |
|---|---|
| Chile INE Censo 2024 | [cl-ine-censo-attributes.md](./cl-ine-censo-attributes.md) |

---

## Common query patterns

**All attributes for a city:**
```sql
SELECT attribute_type, attribute_value, attribute_units, attribute_category, datasource_date
FROM modelled.city_attribute
WHERE locode = 'CL-IQQ'
ORDER BY attribute_type;
```

**Compare one indicator across cities:**
```sql
SELECT locode, region_name, attribute_value, attribute_category
FROM modelled.city_attribute
WHERE attribute_type = 'home_ownership'
  AND datasource = 'cl-ine-censo'
ORDER BY attribute_value::float DESC;
```

**Find cities with high vulnerability signals:**
```sql
SELECT locode, region_name, attribute_type, attribute_value, attribute_category
FROM modelled.city_attribute
WHERE attribute_category IN ('very high', 'high')
  AND attribute_type IN ('renter_share', 'industry_construction_employment')
ORDER BY locode, attribute_type;
```
