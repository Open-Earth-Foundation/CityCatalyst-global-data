INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT DISTINCT ON (activity_id) 
    (MD5(CONCAT_WS('-', activity_name, activity_subcategory_type))::UUID) AS activity_id,
    replace(replace(lower(replace(activity_name, ' ', '-')), '(', ''), ')', '') AS activity_name,
    activity_units,                         
    gpcmethod_id::UUID,             
    activity_subcategory_type::jsonb        
FROM 
    raw_data.sinir_staging
WHERE activity_name IS NOT NULL
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;