INSERT INTO modelled.emissions 
    (emissions_id, datasource_name, gpc_reference_number, actor_id, city_id,
     gpcmethod_id, activity_id, activity_value, 
     gas_name, emissions_value, emissions_units, emissions_year, emissionfactor_id, 
     spatial_granularity, geometry_type, geometry)
SELECT 	emissions_id, 
		datasource_name, 
		gpc_reference_number, 
		actor_id, 
		b.city_id as city_id,
     	method_id as gpcmethod_id, 
     	activity_id, 
     	null as activity_value, 
     	gas_name, 
     	emissions_value, 
     	emissions_units, 
     	emissions_year, 
     	null as emissionfactor_id, 
     	'city' as spatial_granularity, 
     	null as geometry_type, 
     	null as geometry
FROM raw_data.ct_wastewater_emissions_staging a 
LEFT JOIN modelled.city_polygon b 
ON a.actor_id = b.locode
ON CONFLICT ON CONSTRAINT emissions_pkey
DO UPDATE SET 
    datasource_name = EXCLUDED.datasource_name,
    gpc_reference_number = EXCLUDED.gpc_reference_number,
    actor_id = EXCLUDED.actor_id,
    city_id = EXCLUDED.city_id,
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