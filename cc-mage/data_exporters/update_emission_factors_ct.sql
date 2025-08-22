WITH ef_raw AS (
    SELECT DISTINCT
        gas_name,
        gpc_refno,
        emissionfactor_value,
        units,
        activity_units,
        methodology_name,
        activity_name, 
        source_name,
        "livestock_species",
        "livestock_activity_type",
        "livestock_subactivity_type",
        publisher_name,
        datasource_name,
        dataset_name,
        publisher_url,
        dataset_url,
        locode,
        emissions_year
    FROM raw_data.ct_staging
    WHERE emissionfactor_value IS NOT NULL
),
ef_data AS (
    SELECT *,
        MD5(CONCAT_WS(
            '-', 
            publisher_name, 
            publisher_url
            ))::UUID AS publisher_id,
        MD5(CONCAT_WS(
            '-', 
            datasource_name, 
            dataset_name, 
            dataset_url
            ))::UUID AS dataset_id,
        MD5(CONCAT_WS(
            '-', 
            activity_name, 
            activity_units, 
            jsonb_build_object(
				'data-source', "source_name",
                'livestock-species', "livestock_species",
                'livestock-activity-type', "livestock_activity_type",
                'livestock-subactivity-type', "livestock_subactivity_type"
            )::TEXT, 
            MD5(CONCAT_WS(
                '-', 
                methodology_name, 
                gpc_refno
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
    units,
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
        units, 
        gas_name, 
        locode, 
        emissions_year
        ))::UUID AS emissionfactor_id,
    publisher_id,
    dataset_id,
    activity_id,
    gas_name,
    emissionfactor_value,
    units,
    NULL::DATE AS active_to,
    NULL::DATE AS active_from,
    locode AS actor_id
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