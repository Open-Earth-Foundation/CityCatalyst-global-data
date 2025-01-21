WITH activity_data AS (
    SELECT DISTINCT
        (MD5(CONCAT_WS('-', activity_name))::UUID) AS activity_id,
        activity_name,  
        activity_units,
        activity_subcategory_type
    FROM modelled.ippu_ct_staging
    WHERE activity_name IS NOT NULL 
)
INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT DISTINCT ON (activity_id) 
    activity_id,
    replace(replace(lower(replace(activity_name, ' ', '-')), '(', ''), ')', '') AS activity_name,
    activity_units,
    'c6d07ec2-0518-3f40-1ff9-3b77bf8b8fd4'::UUID AS gpcmethod_id,  
    activity_subcategory_type::jsonb
FROM activity_data
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;