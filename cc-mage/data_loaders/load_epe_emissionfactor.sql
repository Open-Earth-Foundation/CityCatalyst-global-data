INSERT INTO modelled.emissions_factor 
    (emissionfactor_id, gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, active_from, active_to, actor_id)
SELECT DISTINCT (MD5(CONCAT_WS('-', gas_name, emissionfactor_value, activity_units, activity_id, ef_datasource_name, locode))::UUID) AS emissionfactor_id,
		gas_name,
		emissionfactor_value as emissionfactor_value,
		activity_units as unit_denominator,
		activity_id,
		ef_datasource_name as datasource_name,
		DATE (emissions_year || '-01-01') as active_from,
		DATE (emissions_year || '-12-31') as active_to,
		locode as actor_id
FROM 	modelled.emissions_epe_staging
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

