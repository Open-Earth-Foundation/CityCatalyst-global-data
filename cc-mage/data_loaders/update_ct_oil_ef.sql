  WITH ef AS (
    SELECT  
        gas_name,
        emissionfactor_value,
        unit_denominator,
        (MD5(CONCAT_WS('-', 
            activity_name, 
            'bpd', 
            json_build_object('facility_type', source_type, 'facility_name', source_name), 
            'custom-methodology'
        ))::UUID) AS activity_id,
        datasource_name,
        active_from::date AS active_from,
        active_to::date AS active_to,
        actor_id
    FROM  
        modelled.emissions_factor_staging
),
emissions_data AS (
    SELECT  
        (MD5(CONCAT_WS('-', gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, active_from, active_to, actor_id))::UUID) as emissionfactor_id,
        gas_name,
        emissionfactor_value,
        unit_denominator,
        activity_id,
        datasource_name,
        active_from,
        active_to,
        actor_id
    FROM  
        ef
)
INSERT INTO modelled.emissions_factor 
    (emissionfactor_id, gas_name, emissionfactor_value, unit_denominator, activity_id, datasource_name, active_from, active_to, actor_id)
SELECT 
    emissionfactor_id,
    gas_name,
    emissionfactor_value,
    unit_denominator,
    activity_id,
    datasource_name,
    active_from,
    active_to,
    actor_id
FROM 
    emissions_data
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


DROP TABLE modelled.emissions_factor_staging;