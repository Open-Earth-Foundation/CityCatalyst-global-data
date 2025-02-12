WITH activity_data AS (
    SELECT DISTINCT
        (MD5(CONCAT_WS('-', activity_name, gpcmethod_id, income_group, treatment_type, treatment_status, collection_status))::UUID) AS activity_id,
        gas_name,
        emissionfactor_value,
        unit_denominator
    FROM modelled.snis_staging
)
INSERT INTO modelled.emissions_factor 
    (emissionfactor_id, gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, active_from, active_to, actor_id)
SELECT DISTINCT
    (MD5(CONCAT_WS('-', gas_name, unit_denominator, activity_id::TEXT, 'IPCCv2006', 'BR'))::UUID) AS emissionfactor_id,
    gas_name,
    emissionfactor_value,
    unit_denominator,
    activity_id,
    'IPCCv2006' AS datasource_name,
    NULL::DATE AS active_from,
    NULL::DATE AS active_to,
    'BR' AS actor_id
FROM activity_data
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