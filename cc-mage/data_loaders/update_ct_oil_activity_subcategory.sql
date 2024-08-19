INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT 	(MD5(CONCAT_WS('-', activity_name, activity_units, json_build_object('facility_type', source_type,'facility_name', source_name), 'custom-methodology'))::UUID) AS activity_id,
		activity_name, 
		activity_units, 
		(MD5(CONCAT_WS('-', gpc_refno, 'custom-methodology'))::UUID) AS gpcmethod_id,
		json_build_object('facility_type', source_type,'facility_name', source_name) as activity_subcategory_type
FROM 	modelled.activity_subcategory_staging
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type
    ;


DROP TABLE modelled.activity_subcategory_staging;