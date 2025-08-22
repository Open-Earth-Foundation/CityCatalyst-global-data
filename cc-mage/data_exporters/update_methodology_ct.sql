INSERT INTO modelled.ghgi_methodology 
    (method_id, methodology_name, methodology_description, gpc_reference_number)
SELECT DISTINCT ON (gpc_refno)
    (MD5(CONCAT_WS('-', methodology_name, gpc_refno))::UUID) AS method_id,
    methodology_name,
    methodology_description,
    gpc_refno AS gpc_reference_number 
FROM 
    raw_data.ct_staging
WHERE methodology_name IS NOT NULL
ON CONFLICT (method_id)
DO UPDATE SET 
    methodology_name = EXCLUDED.methodology_name,
    methodology_description = EXCLUDED.methodology_description,
    gpc_reference_number = EXCLUDED.gpc_reference_number