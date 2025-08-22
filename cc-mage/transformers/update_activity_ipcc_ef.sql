WITH distinct_activities AS (
    SELECT DISTINCT 
        activity_id, 
        activity_name, 
        activity_units, 
        method_id::uuid AS gpcmethod_id, 
        activity_subcategory_type::varchar
    FROM raw_data.ipcc_transport_ef2
)
INSERT INTO modelled.activity_subcategory (
    activity_id, 
    activity_name, 
    activity_units, 
    gpcmethod_id, 
    activity_subcategory_type
)
SELECT 
    activity_id, 
    activity_name, 
    activity_units, 
    gpcmethod_id, 
    activity_subcategory_type::json
FROM distinct_activities
ON CONFLICT (activity_id) DO UPDATE SET
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;
