WITH 	gpc_method AS (
SELECT 	DISTINCT
    	'fuel-combustion-consumption' as methodology_name,
    	gpc_refno as gpc_reference_number
FROM 	modelled.emissions_staging)
INSERT INTO modelled.gpc_methodology 
    (gpcmethod_id, methodology_name, methodology_description, gpc_reference_number, scope)
SELECT 	DISTINCT
    	(MD5(CONCAT_WS('-', gpc_reference_number, methodology_name))::UUID) AS gpcmethod_id,
    	methodology_name,
    	'This method calculates emissions using fuel consumption data and specific emission factors' as methodology_description,
    	gpc_reference_number,
   	 	1 as scope
FROM 	gpc_method
ON CONFLICT (gpcmethod_id)
DO UPDATE SET 
    methodology_name = EXCLUDED.methodology_name,
    methodology_description = EXCLUDED.methodology_description,
    gpc_reference_number = EXCLUDED.gpc_reference_number,
    scope = EXCLUDED.scope
    ;