WITH ef_raw AS (
    SELECT DISTINCT
        gas_name,
        gpc_reference_number,
        emissionfactor_value,
        activity_units,
        methodology_name,
        activity_name, 
        locode AS actor_id
    FROM raw_data.biolog_treatment_eurostats_staging
    WHERE emissionfactor_value IS NOT NULL
),
ef_data AS (
    SELECT *,
        MD5(CONCAT_WS(
            '-', 
            'IPCC', 
            'https://www.ipcc.ch/'
            ))::UUID AS publisher_id,
        MD5(CONCAT_WS(
            '-', 
            'IPCC', 
            'IPCC Emission Factor Database (EFDB) [2006 IPCC Guidelines]', 
            'https://www.ipcc-nggip.iges.or.jp/EFDB/main.php'
            ))::UUID AS dataset_id,
        MD5(CONCAT_WS(
            '-', 
            activity_name, 
            activity_units, 
            jsonb_build_object(
                'biological-treatment-inboundary-waste-state', 'waste-state-wet-waste',
                'biological-treatment-inboundary-treatment-type', 'treatment-type-composting'
            )::TEXT, 
            MD5(CONCAT_WS(
                '-', 
                methodology_name, 
                gpc_reference_number
                ))::TEXT
        ))::UUID AS activity_id
    FROM ef_raw
)
INSERT INTO modelled.emissions_factor (
    emissionfactor_id, 
    publisher_id, 
    dataset_id,
    activity_id, 
    gas_name,
    emissionfactor_value,
    unit_denominator,
    active_to,
    active_from,
    actor_id
)
SELECT
    MD5(CONCAT_WS(
        '-', 
        publisher_id::TEXT, 
        dataset_id::TEXT, 
        activity_id::TEXT, 
        'kg', 
        gas_name, 
        actor_id, 
        2023
        ))::UUID AS emissionfactor_id,
    publisher_id,
    dataset_id,
    activity_id,
    gas_name,
    emissionfactor_value,
    'kg',
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
    unit_denominator = EXCLUDED.unit_denominator,
    active_to = EXCLUDED.active_to,
    active_from = EXCLUDED.active_from,
    actor_id = EXCLUDED.actor_id;
