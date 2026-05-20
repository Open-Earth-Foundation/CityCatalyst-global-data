INSERT INTO modelled.city_attribute (
    city_id,
    locode,
    country_code,
    region_name,
    attribute_type,
    attribute_value,
    attribute_units,
    datasource,
    datasource_date,
    attribute_category,
    dataset_id,
    release_id
)
SELECT
    cp.city_id,
    s.locode,
    cp.country_code,
    s.region_nombre         AS region_name,
    s.attribute_type,
    s.attribute_value,
    s.attribute_units,
    '{{ datasource_name }}' AS datasource,
    {{ reference_year }}    AS datasource_date,
    s.attribute_category,
    dr.dataset_id,
    dr.release_id
FROM raw_data.cl_mapbiomas_lulc_staging s
INNER JOIN modelled.city_polygon cp
    ON s.locode = cp.locode
CROSS JOIN (
    SELECT dr.release_id, dr.dataset_id
    FROM modelled.dataset_release dr
    JOIN modelled.publisher_datasource pd
        ON dr.dataset_id = pd.dataset_id
    WHERE pd.datasource_name = '{{ datasource_name }}'
      AND dr.version_label   = '{{ version_label }}'
) dr
ON CONFLICT (city_id, locode, attribute_type, datasource)
DO UPDATE SET
    attribute_value    = EXCLUDED.attribute_value,
    attribute_units    = EXCLUDED.attribute_units,
    datasource_date    = EXCLUDED.datasource_date,
    region_name        = EXCLUDED.region_name,
    country_code       = EXCLUDED.country_code,
    attribute_category = EXCLUDED.attribute_category,
    dataset_id         = EXCLUDED.dataset_id,
    release_id         = EXCLUDED.release_id;
