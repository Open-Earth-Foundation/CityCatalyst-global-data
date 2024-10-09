INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT DISTINCT
    (MD5(CONCAT_WS('-', activity_name))::UUID) AS activity_id,
    replace(replace(lower(replace(activity_name, ' ','-')), '(', ''), ')', '') AS activity_name,
    null AS activity_units,
    null::uuid AS gpcmethod_id,
    null::jsonb as activity_subcategory_type
FROM 
     modelled.seeg_sector_emissions
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type
    ;