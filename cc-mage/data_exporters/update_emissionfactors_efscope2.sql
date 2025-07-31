WITH ef_raw AS (
    SELECT DISTINCT
        gas,
        gpc_reference_number,
        emissions_per_activity,
        units,
        activity_units,
        methodology_name,
        actor_id,
        electricity_maps_staging._year,
        activity_name,
        publisher_name,
        datasource_name,
        dataset_name,
        publisher_url,
        dataset_url
    FROM raw_data.electricity_maps_staging
    WHERE emissions_per_activity IS NOT NULL
),
ef_data AS (
    SELECT *,
        MD5(CONCAT_WS('-', publisher_name, publisher_url))::UUID AS publisher_id,
        MD5(CONCAT_WS('-', datasource_name, dataset_name, dataset_url))::UUID AS dataset_id,
        NULL AS activity_subcategory_type,
        (MD5(CONCAT_WS(
            '-', 
            activity_name, 
            activity_units, 
            (MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::TEXT)
        )))::UUID AS activity_id,
        -- active period
        make_date(ef_raw._year, 1, 1) AS active_from,
        make_date(ef_raw._year, 12, 31) AS active_to
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
    -- ✅ Include year to generate unique IDs per year
    MD5(CONCAT_WS(
        '-', 
        publisher_id::TEXT, 
        dataset_id::TEXT, 
        activity_id::TEXT, 
        units, 
        gas, 
        actor_id, 
        ef_data._year::TEXT
    ))::UUID AS emissionfactor_id,
    publisher_id,
    dataset_id,
    activity_id,
    gas AS gas_name,
    emissions_per_activity AS emissionfactor_value,
    units,
    active_to,
    active_from,
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
