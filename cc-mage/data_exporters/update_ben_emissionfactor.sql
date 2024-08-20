WITH 	emission_factor AS (
SELECT  DISTINCT
        gas_name,
        emissionfactor_value,
        activity_units AS unit_denominator,
        (MD5(CONCAT_WS('-', 'fuel-consumption', activity_units, jsonb_build_object('fuel-type', subcategory), gpc_refno, 'fuel-combustion-consumption' ))::UUID) AS activity_id,
        source_name as datasource_name,
       	null::date as active_from,
        null::date as active_to,
        actor_id
FROM 	modelled.emissions_staging)
INSERT INTO modelled.emissions_factor 
    (emissionfactor_id, gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, active_from, active_to, actor_id)
SELECT 	(MD5(CONCAT_WS('-', gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, active_from, active_to, actor_id))::UUID) AS emissionfactor_id,
		gas_name,
		emissionfactor_value,
		unit_denominator,
		activity_id,
		datasource_name,
		active_from,
		active_to,
		actor_id
FROM 	emission_factor
ON CONFLICT (emissionfactor_id) 
DO UPDATE SET 
    gas_name = EXCLUDED.gas_name,
    emissionfactor_value = EXCLUDED.emissionfactor_value,
    unit_denominator = EXCLUDED.unit_denominator,
    activity_id = EXCLUDED.activity_id,
    datasource_name = EXCLUDED.datasource_name,
    active_from = EXCLUDED.active_from,
    active_to = EXCLUDED.active_to,
    actor_id = EXCLUDED.actor_id;