INSERT INTO modelled.city_attribute (
    city_id,
    locode,
    country_code,
    attribute_type,
    attribute_category,
    attribute_units,
    datasource,
    datasource_date
)
SELECT DISTINCT
    city_id,
    locode,
    country_code,
    attribute_type,
    attribute_category,
    'categorical' AS attribute_units,
    datasource,
    datasource_date
FROM raw_data.city_emissions_zscore
ON CONFLICT (city_id, locode, attribute_type, datasource)
DO NOTHING;