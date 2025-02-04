INSERT INTO modelled.gpc_methodology 
    (gpcmethod_id, methodology_name, methodology_description, gpc_reference_number, scope)
SELECT DISTINCT ON (gpc_refno)
    (MD5(CONCAT_WS('-', methodology_name, gpc_refno))::UUID) AS gpcmethod_id,
    methodology_name,
    methodology_description,
    gpc_refno AS gpc_reference_number,
    last_no AS scope   
FROM 
    modelled.gpc_method_staging
WHERE methodology_name IS NOT NULL
ON CONFLICT (gpcmethod_id)
DO UPDATE SET 
    methodology_name = EXCLUDED.methodology_name,
    methodology_description = EXCLUDED.methodology_description,
    gpc_reference_number = EXCLUDED.gpc_reference_number,
    scope = EXCLUDED.scope;