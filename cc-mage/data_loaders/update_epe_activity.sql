INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT DISTINCT
    activity_id,
    activity_name,
    activity_units,
    (MD5(CONCAT_WS('-', 'scaling'))::UUID) AS gpcmethod_id,
    null::jsonb as activity_subcategory_type
FROM 
    modelled.emissions_epe_staging
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type
    ;
