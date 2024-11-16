INSERT INTO modelled.emissions_factor 
    (emissionfactor_id, gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, active_from, active_to, actor_id)
SELECT DISTINCT (MD5(CONCAT_WS('-', gas_name, emissionsfactor_value, 'km', (MD5(CONCAT_WS('-', activity_name, activity_units, activity_subcategory_type, 'induced-activity'))::UUID), 'IPCC', actor_id))::UUID) AS emissionfactor_id,
		gas_name,
		emissionsfactor_value as emissionfactor_value,
		'km' as unit_denominator,
		(MD5(CONCAT_WS('-', activity_name, activity_units, activity_subcategory_type, 'induced-activity'))::UUID) AS activity_id,
		'IPCC' as datasource_name,
		null::date as active_from,
		null::date as active_to,
		actor_id
FROM 	raw_data.google_emissions
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
