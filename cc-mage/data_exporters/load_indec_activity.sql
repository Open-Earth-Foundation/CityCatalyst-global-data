WITH activity_data AS (
    SELECT DISTINCT
        MD5(CONCAT_WS(
        '-',
        activity_name,
        activity_subcategory_type::TEXT,
        method_id::TEXT
    ))::UUID AS activity_id,
        activity_name,
        activity_units,
        method_id,
        activity_subcategory_type
    FROM raw_data.arg_solid_waste_indec
)
INSERT INTO modelled.activity_subcategory (
    activity_id, 
    activity_name, 
    activity_units, 
    gpcmethod_id, 
    activity_subcategory_type
)
SELECT  activity_id,
        activity_name,
        activity_units,
        method_id as gpcmethod_id,
        activity_subcategory_type::json
FROM activity_data
ON CONFLICT (activity_id) DO UPDATE SET
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;