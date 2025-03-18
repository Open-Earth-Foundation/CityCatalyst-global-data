WITH activity_data AS (
    SELECT DISTINCT
        activity_name,  
        activity_units,
        activity_subcategory_type
    FROM modelled.fugitivie_staging
    WHERE activity_name IS NOT NULL
),
method_id AS (
    SELECT 
        gpcmethod_id
    FROM modelled.gpc_methodology
    WHERE methodology_name = 'custom-methodology'
    AND gpc_reference_number = 'I.7.1'
)
INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT 
    (MD5(CONCAT_WS('-', activity_name, activity_subcategory_type))::UUID) AS activity_id,
    a.activity_name,
    a.activity_units,
    m.gpcmethod_id,  
    a.activity_subcategory_type::jsonb
FROM activity_data a
CROSS JOIN method_id m 
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;