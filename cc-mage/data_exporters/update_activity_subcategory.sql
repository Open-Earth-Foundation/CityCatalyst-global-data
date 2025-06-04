WITH activity_data AS (
    SELECT DISTINCT
        activity_name,
        activity_units,
        methodology_name,
        gpc_reference_number,
        fuel_type,
        MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID AS method_id
    FROM raw_data.ef_fuel_consumption_staging
    WHERE activity_name IS NOT NULL
)
INSERT INTO modelled.activity_subcategory (
    activity_id, 
    activity_name, 
    activity_units, 
    method_id, 
    activity_subcategory_type
)
SELECT 
    (MD5(CONCAT_WS('-', activity_name, activity_units, jsonb_build_object('fuel_type', fuel_type)::TEXT, method_id::TEXT))::UUID) AS activity_id,
    activity_name,
    activity_units,
    method_id,
    jsonb_build_object('fuel_type', fuel_type) AS activity_subcategory_type
FROM activity_data
ON CONFLICT (activity_id) DO UPDATE SET
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    method_id = EXCLUDED.method_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;