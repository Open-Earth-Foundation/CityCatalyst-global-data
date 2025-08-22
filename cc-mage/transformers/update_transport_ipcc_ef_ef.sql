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
    emissionfactor_value,
    units AS unit_denominator,  
    activity_id,
    datasource_name,  
    NULL::date AS active_from,      
    NULL::date AS active_to,        
    actor_id,
    publisher_id,
    dataset_id
FROM raw_data.ipcc_transport_ef2
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