WITH ef AS (
    SELECT DISTINCT
        (MD5(CONCAT_WS('-', activity_name, activity_subcategory_type))::UUID) AS activity_id,
        gas_name,
        emissionsfactor_value,
        unit_denominator,
        actor_id
    FROM modelled.fugitivie_staging
)
INSERT INTO modelled.emissions_factor 
    (emissionfactor_id, gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, active_from, active_to, actor_id)
SELECT DISTINCT
    (MD5(CONCAT_WS('-', gas_name, emissionsfactor_value, unit_denominator, activity_id::TEXT, 'ClimateTRACEv2024', actor_id))::UUID) AS emissionfactor_id,
    gas_name,
    emissionsfactor_value AS emissionfactor_value,
    unit_denominator,
    activity_id,
    'ClimateTRACEv2024' AS datasource_name,
    --NULL::jsonb AS metadata,
    NULL::DATE AS active_from,
    NULL::DATE AS active_to,
    actor_id
FROM ef;