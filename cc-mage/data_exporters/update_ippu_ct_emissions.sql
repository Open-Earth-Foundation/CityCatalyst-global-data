INSERT INTO modelled.emissions (
    emissions_id,
    datasource_name,
    actor_id,
    city_id,
    gpc_reference_number,
    emissions_value,
    emissions_year,
    emissions_units,
    gpcmethod_id,
    gas_name,
    emissionfactor_id,
    activity_id,
    activity_value,
    spatial_granularity,
    geometry_type,
    geometry,
    geometry_id
)
 SELECT 
    (MD5(CONCAT_WS('-', locode, emissions_year, gpc_refno, gpcmethod_id, gas_name, emissionfactor_id, activity_id, geometry_id))::UUID) AS emissions_id,
    'ClimateTRACEv2024' as datasource_name,
    b.locode as actor_id,
    b.city_id,
    gpc_refno as gpc_reference_number,
    emissions_value,
    emissions_year,
    emissions_units,
    gpcmethod_id,
    gas_name,
    emissionfactor_id,
    activity_id,
    activity_value,
    'city' as spatial_granularity,
    ST_GeometryType(a.geometry) AS geometry_type,
    a.geometry,
    geometry_id
FROM modelled.city_polygon b 
INNER JOIN modelled.emissions_staging_full a
ON ST_Intersects(b.geometry, a.geometry)
AND a.country_code = b.country_code 
ON CONFLICT (emissions_id) DO UPDATE SET
    datasource_name = EXCLUDED.datasource_name,
    actor_id = EXCLUDED.actor_id,
    city_id = EXCLUDED.city_id,
    gpc_reference_number = EXCLUDED.gpc_reference_number,
    emissions_value = EXCLUDED.emissions_value,
    emissions_year = EXCLUDED.emissions_year,
    emissions_units = EXCLUDED.emissions_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    gas_name = EXCLUDED.gas_name,
    emissionfactor_id = EXCLUDED.emissionfactor_id,
    activity_id = EXCLUDED.activity_id,
    activity_value = EXCLUDED.activity_value,
    spatial_granularity = EXCLUDED.spatial_granularity,
    geometry_type = EXCLUDED.geometry_type,
    geometry = EXCLUDED.geometry,
    geometry_id = EXCLUDED.geometry_id;


DROP TABLE modelled.emissions_staging_full;
DROP TABLE raw_data.ippu_ct_staging;