INSERT INTO modelled.emissions 
    (emissions_id, datasource_name, gpc_reference_number, actor_id, 
     gpcmethod_id, activity_id, activity_value, 
     gas_name, emissions_value, emissions_units, emissions_year, emissionfactor_id, 
     spatial_granularity, geometry_type, geometry)
SELECT 
    (MD5(CONCAT_WS('-', 'EPE', gpc_reference_number, locode, 
    activity_id,
    emissions_year,gas_name))::UUID) AS emissions_id,
    'EPE' as datasource_name,
    gpc_reference_number,
    locode as actor_id,
    (MD5(CONCAT_WS('-', 'scaling'))::UUID)  as gpcmethod_id,
    activity_id,
    activity_value,
    gas_name,
    emissions_value,
    emissions_units,
    emissions_year,
    (MD5(CONCAT_WS('-', gas_name, emissionfactor_value, activity_units, activity_id, ef_datasource_name, locode))::UUID) AS emissionfactor_id,
    'city' as spatial_granularity,
    null as geometry_type,
    null as geometry
FROM 
    modelled.emissions_epe_staging
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