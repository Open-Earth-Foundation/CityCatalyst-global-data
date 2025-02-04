WITH activity_data AS (
    SELECT DISTINCT
        emissionfactor_id,
        activity_id,
        gas_name,
        emissionfactor_value as emissionsfactor_value,
        unit_denominator,
        country_code as actor_id
    FROM modelled.emissions_staging_full
)
INSERT INTO modelled.emissions_factor 
    (emissionfactor_id, gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, active_from, active_to, actor_id)
SELECT DISTINCT
    emissionfactor_id,
    gas_name,
    emissionsfactor_value,
    unit_denominator,
    activity_id,
    'ClimateTRACEv2024' AS datasource_name,
    --NULL::jsonb AS metadata,
    NULL::DATE AS active_from,
    NULL::DATE AS active_to,
    actor_id
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