WITH activity_data AS (
    SELECT DISTINCT
        (MD5(CONCAT_WS('-', activity_name, activity_subcategory_type))::UUID) AS activity_id,
        gas_name,
        emissionfactor_value,
        actor_id
    FROM raw_data.sinir_staging
)
INSERT INTO modelled.emissions_factor 
    (emissionfactor_id, gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, active_from, active_to, actor_id)
SELECT DISTINCT
    (MD5(CONCAT_WS('-', gas_name, emissionfactor_value, 't', activity_id::TEXT, 'IPCCv2006', actor_id))::UUID) AS emissionfactor_id,
    gas_name,
    emissionfactor_value,
    't' AS unit_denominator,
    activity_id,
    'IPCCv2006' AS datasource_name,
    --NULL::jsonb AS metadata,
    NULL::DATE AS active_from,
    NULL::DATE AS active_to,
    actor_id
FROM activity_data
WHERE emissionfactor_value > 0
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