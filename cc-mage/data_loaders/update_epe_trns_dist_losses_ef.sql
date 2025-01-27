WITH ef AS (
    SELECT DISTINCT
    gas_name, 
    emissionfactor_value,
    unit_denominator, 
    activity_id, 
    datasource_name, 
    active_from,
    active_to, 
    actor_id
    FROM modelled.ef_staging_epe
)
INSERT INTO modelled.emissions_factor 
    (emissionfactor_id, gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, active_from, active_to, actor_id)
SELECT DISTINCT
    (MD5(CONCAT_WS('-', gas_name, emissionfactor_value, unit_denominator, activity_id::TEXT, datasource_name, actor_id))::UUID) AS emissionfactor_id,
    gas_name,
    emissionfactor_value,
    unit_denominator,
    activity_id::UUID,
    datasource_name,
    --NULL::jsonb AS metadata,
    active_from,
    active_to,
    actor_id
FROM ef
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