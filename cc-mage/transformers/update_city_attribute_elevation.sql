INSERT INTO modelled.city_attribute (
    city_id, 
    locode, 
    country_code, 
    attribute_type, 
    attribute_value, 
    attribute_units, 
    datasource, 
    datasource_date
)
SELECT 
    cp.city_id, 
    a.locode,
    cp.country_code, 
    'elevation' AS attribute_type,
    a.elevation AS attribute_value,
    'meters' AS attribute_units,
    'osm' AS datasource,
    '2025' AS datasource_date
FROM raw_data.city_elevation a
INNER JOIN modelled.city_polygon cp 
    ON a.locode = cp.locode
ON CONFLICT (city_id, locode, attribute_type, datasource)
DO UPDATE SET
    attribute_value = EXCLUDED.attribute_value,
    attribute_units = EXCLUDED.attribute_units,
    datasource_date = EXCLUDED.datasource_date;