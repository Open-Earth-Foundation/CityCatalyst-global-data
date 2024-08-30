INSERT INTO modelled.emissions 
    (emissions_id, datasource_name, gpc_reference_number, actor_id, 
     gpcmethod_id, activity_id, activity_value, 
     gas_name, emissions_value, emissions_units, emissions_year, emissionfactor_id, 
     spatial_granularity, geometry_type, geometry)
SELECT 
    (MD5(CONCAT_WS('-', source_name, gpc_reference_number, actor_id, 
    (MD5(CONCAT_WS('-', activity_name,activity_units,activity_subcategory_type))::UUID),
    emissions_year))::UUID) AS emissions_id,
    source_name as datasource_name,
    gpc_reference_number,
    actor_id,
    (MD5(CONCAT_WS('-','II.1.1','induced-activity'))::UUID) as gpcmethod_id,
    (MD5(CONCAT_WS('-', activity_name,activity_units,activity_subcategory_type))::UUID) AS activity_id,
    activity_value,
    gas_name,
    emissions_value,
    emissions_units,
    emissions_year,
    emissions_factor_id::uuid as emissionfactor_id,
    'city' as spatial_granularity,
    geometry_type,
    geometry_value as geometry
FROM 
    modelled.emissions_staging
WHERE emissions_value > 0
ON CONFLICT ON CONSTRAINT emissions_pkey
DO UPDATE SET 
    datasource_name = EXCLUDED.datasource_name,
    gpc_reference_number = EXCLUDED.gpc_reference_number,
    actor_id = EXCLUDED.actor_id,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_id = EXCLUDED.activity_id,
    activity_value = EXCLUDED.activity_value,
    gas_name = EXCLUDED.gas_name,
    emissions_value = EXCLUDED.emissions_value,
    emissions_units = EXCLUDED.emissions_units,
    emissions_year = EXCLUDED.emissions_year,
    emissionfactor_id = EXCLUDED.emissionfactor_id,
    spatial_granularity = EXCLUDED.spatial_granularity,
    geometry_type = EXCLUDED.geometry_type,
    geometry = EXCLUDED.geometry;