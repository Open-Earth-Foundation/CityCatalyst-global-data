INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT DISTINCT
    (MD5(CONCAT_WS('-', activity_name, activity_units, activity_subcategory_type, 'induced-activity'))::UUID) AS activity_id,
    activity_name,
    activity_units,
    (MD5(CONCAT_WS('-', 'II.1.1', 'induced-activity'))::UUID) AS gpcmethod_id,
    activity_subcategory_type::jsonb
FROM 
    raw_data.google_emissions
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type
    ;
