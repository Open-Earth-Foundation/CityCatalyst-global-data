INSERT INTO modelled.gpc_methodology 
    (gpcmethod_id, methodology_name, methodology_description, scope)
SELECT DISTINCT ON (methodology_name) 
    (MD5(CONCAT_WS('-', methodology_name))::UUID) AS gpcmethod_id,
    methodology_name,
    methodology_description,
    _scope AS scope   
FROM 
    modelled.gpc_method_staging
WHERE methodology_name IS NOT NULL
ON CONFLICT (gpcmethod_id)
DO UPDATE SET 
    methodology_name = EXCLUDED.methodology_name,
    methodology_description = EXCLUDED.methodology_description,
    scope = EXCLUDED.scope;