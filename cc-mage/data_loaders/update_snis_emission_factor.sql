WITH activity_data AS (
    SELECT DISTINCT
        (MD5(CONCAT_WS('-', activity_name))::UUID) AS activity_id,
        gas_name,
        emissionfactor_value,
        unit_denominator
    FROM modelled.snis_staging
)
INSERT INTO modelled.emissions_factor 
    (emissionfactor_id, gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, metadata, active_from, active_to, actor_id)
SELECT DISTINCT
    (MD5(CONCAT_WS('-', gas_name, emissionfactor_value, unit_denominator, activity_id::TEXT, 'IPCC 2006', 'BR'))::UUID) AS emissionfactor_id,
    gas_name,
    emissionfactor_value,
    unit_denominator,
    activity_id,
    'IPCC 2006' AS datasource_name,
    NULL::jsonb AS metadata,
    NULL::DATE AS active_from,
    NULL::DATE AS active_to,
    'BR' AS actor_id
FROM activity_data;