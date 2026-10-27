INSERT INTO modelled.emissions_factor (
    emissionfactor_id, 
    gas_name, 
    emissionfactor_value,
    unit_denominator,
    activity_id,
    datasource_name,
    active_from,
    active_to,
    actor_id,
    publisher_id,
    dataset_id
)
SELECT emissionfactor_id, 
    gas_name,
    avg(emissionfactor_value) as emissionfactor_value, -- have to take the average because ef changes each month
    emissions_factor_units AS unit_denominator,  
    activity_id,
    datasource_name,  
    DATE(emissions_year || '-01-01')  AS active_from,      
    DATE(emissions_year || '-12-31') AS active_to,        
    actor_id,
    publisher_id,
    dataset_id
FROM raw_data.ct_staging_v2025
GROUP BY emissionfactor_id, gas_name, emissions_factor_units, activity_id, datasource_name, emissions_year, actor_id, publisher_id, dataset_id
ON CONFLICT (emissionfactor_id)
DO UPDATE SET
    gas_name = EXCLUDED.gas_name,
    emissionfactor_value = EXCLUDED.emissionfactor_value,
    unit_denominator = EXCLUDED.unit_denominator,
    activity_id = EXCLUDED.activity_id,
    datasource_name = COALESCE(EXCLUDED.datasource_name, emissions_factor.datasource_name),
    active_from = COALESCE(EXCLUDED.active_from, emissions_factor.active_from),
    active_to = COALESCE(EXCLUDED.active_to, emissions_factor.active_to),
    actor_id = EXCLUDED.actor_id,
    publisher_id = EXCLUDED.publisher_id,
    dataset_id = EXCLUDED.dataset_id;