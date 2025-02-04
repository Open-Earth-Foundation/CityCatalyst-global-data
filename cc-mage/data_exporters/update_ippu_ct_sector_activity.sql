WITH activity_data AS (
    SELECT DISTINCT
        activity_id,
        activity_name,  
        activity_units,
        gpcmethod_id,
        activity_subcategory_type
    FROM modelled.emissions_staging_full
    WHERE activity_name IS NOT NULL
)
-- Use the main INSERT INTO command with a SELECT from the CTE
INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT 
    activity_id,
    activity_name,
    activity_units,
    gpcmethod_id,  
    activity_subcategory_type::jsonb
FROM activity_data
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;