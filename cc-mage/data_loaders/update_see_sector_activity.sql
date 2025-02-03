INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT 
    (MD5(CONCAT_WS('-', activity_name, activity_subcategory_type1, activity_subcategory_typename1, activity_subcategory_type2, activity_subcategory_typename2, activity_subcategory_type3, activity_subcategory_typename3))::UUID) AS activity_id,
    activity_name,
    NULL AS activity_units,
    NULL::UUID AS gpcmethod_id,
    CASE 
        WHEN activity_subcategory_type3 IS NOT NULL THEN 
            json_build_object(
                activity_subcategory_type1, activity_subcategory_typename1,
                activity_subcategory_type2, activity_subcategory_typename2,
                activity_subcategory_type3, activity_subcategory_typename3
            )
        WHEN activity_subcategory_type2 IS NOT NULL THEN 
            json_build_object(
                activity_subcategory_type1, activity_subcategory_typename1,
                activity_subcategory_type2, activity_subcategory_typename2
            )
        WHEN activity_subcategory_type1 IS NOT NULL THEN 
            json_build_object(
                activity_subcategory_type1, activity_subcategory_typename1
            )
        ELSE NULL::json
    END AS activity_subcategory_type
FROM (
    SELECT DISTINCT
        activity_name,
        activity_subcategory_type1, activity_subcategory_typename1,
        activity_subcategory_type2, activity_subcategory_typename2,
        activity_subcategory_type3, activity_subcategory_typename3
    FROM raw_data.seeg_sector_emissions
) AS distinct_data
ON CONFLICT (activity_id) DO UPDATE 
SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type;