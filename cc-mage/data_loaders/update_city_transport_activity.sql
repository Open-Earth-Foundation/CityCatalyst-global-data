
CREATE TABLE IF NOT EXISTS modelled.activity_subcategory (
    activity_id UUID PRIMARY KEY,
    activity_name TEXT,
    activity_units TEXT,
    gpcmethod_id UUID,
    activity_subcategory_type JSONB
);


INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT DISTINCT
    (MD5(CONCAT_WS('-', activity_name, activity_units, activity_subcategory_type))::UUID) AS activity_id,
    activity_name,
    activity_units,
    (MD5(CONCAT_WS('-', 'II.1.1', 'Induced activity'))::UUID) AS gpcmethod_id,
    activity_subcategory_type::jsonb
FROM 
    modelled.emissions_staging
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type
    ;


