 WITH emissions AS (  
 SELECT source_name as datasource_name,
 		gpc_refno as gpc_reference_number,
 		actor_id,
 		(MD5(CONCAT_WS('-',gpc_refno,'fuel-combustion-consumption' ))::UUID) as gpcmethod_id,
 		(MD5(CONCAT_WS('-', 'fuel-consumption', activity_units, jsonb_build_object('fuel-type', subcategory), gpc_refno, 'fuel-combustion-consumption' ))::UUID) AS activity_id,
 		activity_value,
 		gas_name,
 		emissions_value,
 		emissions_units,
 		_year as emissions_year,
 		(MD5(CONCAT_WS('-', gas_name, emissionfactor_value, activity_units, 
 		 (MD5(CONCAT_WS('-', 'fuel-consumption', activity_units, jsonb_build_object('fuel-type', subcategory), gpc_refno, 'fuel-combustion-consumption' ))::UUID), 
 		 source_name, null::date, null::date, actor_id))::UUID) AS emissionfactor_id,
 		 'country' AS geometry_type,
 		 null::uuid AS geometry_id
FROM 	 modelled.emissions_staging)
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
    geometry_type,
    geometry,
    geometry_id
)
SELECT	(MD5(CONCAT_WS('-', actor_id, emissions_year, gpc_reference_number, gpcmethod_id, gas_name, emissionfactor_id, activity_id))::UUID) AS emissions_id,
		datasource_name,
		actor_id,
		null as city_id,
		gpc_reference_number,
		emissions_value,
		emissions_year,
		emissions_units,
		gpcmethod_id,
		gas_name,
		emissionfactor_id,
		activity_id,
		activity_value,
		geometry_type,
		null as geometry,
		null as geometry_id
FROM 	emissions
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
    geometry_type = EXCLUDED.geometry_type,
    geometry = EXCLUDED.geometry,
    geometry_id = EXCLUDED.geometry_id;