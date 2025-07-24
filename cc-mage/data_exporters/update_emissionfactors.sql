WITH ef_raw AS (
    SELECT DISTINCT
        gas,
        gpc_reference_number,
        emissions_per_activity,
        units,
        activity_units,
        methodology_name,
        actor_id,
        active_to,
        active_from,
        activity_name,
        fuel_type,
        publisher_name,
        datasource_name,
        dataset_name,
        publisher_url,
        dataset_url
    FROM raw_data.ef_fuel_consumption_staging
    WHERE emissions_per_activity IS NOT NULL
),
ef_data AS (
    SELECT *,
        MD5(CONCAT_WS('-', publisher_name, publisher_url))::UUID AS publisher_id,
        MD5(CONCAT_WS('-', datasource_name, dataset_name, dataset_url))::UUID AS dataset_id,
        
        -- Adapted activity_subcategory_type logic
        CASE gpc_reference_number
            WHEN 'I.1.1' THEN jsonb_build_object('residential-building-fuel-type', fuel_type)
            WHEN 'I.2.1' THEN jsonb_build_object('commercial-building-fuel-type', fuel_type)
            WHEN 'I.3.1' THEN jsonb_build_object('manufacturing-and-construction-fuel-type', fuel_type)
            WHEN 'I.4.1' THEN jsonb_build_object('energy-industries-fuel-type', fuel_type)
            WHEN 'I.5.1' THEN jsonb_build_object('agriculture-forestry-fishing-activities-fuel-type', fuel_type)
            WHEN 'I.6.1' THEN jsonb_build_object('non-specific-sources-fuel-type', fuel_type)
            ELSE jsonb_build_object('fuel_type', fuel_type)
        END AS activity_subcategory_type,

        -- Adapted activity_id logic using same structure
        (
            MD5(CONCAT_WS(
                '-',
                activity_name,
                activity_units,
                CASE gpc_reference_number
                    WHEN 'I.1.1' THEN jsonb_build_object('residential-building-fuel-type', fuel_type)::TEXT
                    WHEN 'I.2.1' THEN jsonb_build_object('commercial-building-fuel-type', fuel_type)::TEXT
                    WHEN 'I.3.1' THEN jsonb_build_object('manufacturing-and-construction-fuel-type', fuel_type)::TEXT
                    WHEN 'I.4.1' THEN jsonb_build_object('energy-industries-fuel-type', fuel_type)::TEXT
                    WHEN 'I.5.1' THEN jsonb_build_object('agriculture-forestry-fishing-activities-fuel-type', fuel_type)::TEXT
                    WHEN 'I.6.1' THEN jsonb_build_object('non-specific-sources-fuel-type', fuel_type)::TEXT
                    ELSE jsonb_build_object('fuel_type', fuel_type)::TEXT
                END,
                MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::TEXT
            ))
        )::UUID AS activity_id
    FROM ef_raw
)
INSERT INTO modelled.emissions_factor (
    emissionfactor_id,
    publisher_id,
    dataset_id,
    activity_id,
    gas_name,
    emissionfactor_value,
    units,
    active_to,
    active_from,
    actor_id
)
SELECT
    MD5(CONCAT_WS('-', publisher_id::TEXT, dataset_id::TEXT, activity_id::TEXT, units, gas, actor_id))::UUID AS emissionfactor_id,
    publisher_id,
    dataset_id,
    activity_id,
    gas AS gas_name,
    emissions_per_activity AS emissionfactor_value,
    units,
    NULL::DATE AS active_to,
    NULL::DATE AS active_from,
    actor_id
FROM ef_data
ON CONFLICT (emissionfactor_id) DO UPDATE SET
    publisher_id = EXCLUDED.publisher_id,
    dataset_id = EXCLUDED.dataset_id,
    activity_id = EXCLUDED.activity_id,
    gas_name = EXCLUDED.gas_name,
    emissionfactor_value = EXCLUDED.emissionfactor_value,
    units = EXCLUDED.units,
    active_to = EXCLUDED.active_to,
    active_from = EXCLUDED.active_from,
    actor_id = EXCLUDED.actor_id;