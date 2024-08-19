WITH 	subcategory AS (
SELECT 	DISTINCT
    	'fuel-consumption' as activity_name,
    	'fuel-combustion-consumption' as methodology_name,
    	jsonb_build_object('fuel-type', subcategory) as activity_subcategory_type,
    	gpc_refno as gpc_reference_number,
    	activity_units
FROM 	modelled.emissions_staging)
INSERT INTO modelled.activity_subcategory 
    (activity_id, activity_name, activity_units, gpcmethod_id, activity_subcategory_type)
SELECT 	DISTINCT
    	(MD5(CONCAT_WS('-', activity_name, activity_units, activity_subcategory_type, gpc_reference_number, methodology_name))::UUID) AS activity_id,
    	activity_name,
    	activity_units,
    	(MD5(CONCAT_WS('-', gpc_reference_number, methodology_name))::UUID) AS gpcmethod_id,
    	activity_subcategory_type
FROM 	subcategory
ON CONFLICT (activity_id)
DO UPDATE SET 
    activity_name = EXCLUDED.activity_name,
    activity_units = EXCLUDED.activity_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type
    ;
