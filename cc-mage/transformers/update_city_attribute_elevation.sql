WITH LookupRegionName AS (
    SELECT 		DISTINCT region_code, b.nm_uf as region_name
    FROM   		raw_data.icare_city_to_locode a 
    INNER JOIN 	raw_data.br_city_biome b
    ON 			a.municipality_code = b.cd_mun
)
INSERT INTO modelled.city_attribute (
    city_id, 
    locode, 
    country_code, 
    region_name,
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
    b.region_name,
    'elevation' AS attribute_type,
    a.elevation AS attribute_value,
    'meters' AS attribute_units,
    'osm' AS datasource,
    '2025' AS datasource_date
FROM raw_data.city_elevation a
INNER JOIN modelled.city_polygon cp 
    ON a.locode = cp.locode
INNER JOIN LookupRegionName b 
ON cp.region_code = b.region_code
ON CONFLICT (city_id, locode, attribute_type, datasource)
DO UPDATE SET
    attribute_value = EXCLUDED.attribute_value,
    attribute_units = EXCLUDED.attribute_units,
    datasource_date = EXCLUDED.datasource_date,
    region_name = EXCLUDED.region_name,
    country_code = EXCLUDED.country_code;