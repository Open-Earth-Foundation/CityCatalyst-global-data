INSERT INTO modelled.city_attribute (
    city_id,
    locode,
    country_code,
    attribute_type,
    attribute_value,
    attribute_units,
    datasource,
    datasource_date,
    attribute_category,
    dataset_id,
    release_id
)
SELECT DISTINCT
    cez.city_id,
    cez.locode,
    cez.country_code,
    cez.attribute_type,
    cez.attribute_value,
    'categorical' AS attribute_units,
    cez.datasource,
    cez.datasource_date,
    cez.attribute_category,
    MD5('ClimateTRACE-High Resolution Visualization of PM2.5 Impacts on Surrounding Population-https://downloads.climatetrace.org/latest/country_packages/pm2_5/TCD.zip')::UUID AS dataset_id,
    MD5('ClimateTRACE-PM2.5-v5_3_0')::UUID AS release_id
FROM raw_data.city_emissions_zscore cez
ON CONFLICT (city_id, locode, attribute_type, datasource, datasource_date)
DO UPDATE SET
    country_code = EXCLUDED.country_code,
    attribute_value = EXCLUDED.attribute_value,
    attribute_units = EXCLUDED.attribute_units,
    datasource_date = EXCLUDED.datasource_date,
    attribute_category = EXCLUDED.attribute_category,
    dataset_id = EXCLUDED.dataset_id,
    release_id = EXCLUDED.release_id;