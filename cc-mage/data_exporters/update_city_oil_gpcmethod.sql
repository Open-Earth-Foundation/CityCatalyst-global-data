INSERT INTO modelled.gpc_methodology 
    (gpcmethod_id, methodology_name, methodology_description, gpc_reference_number, scope)
SELECT DISTINCT
    (MD5(CONCAT_WS('-', gpc_refno, 'custom-methodology'))::UUID) AS gpcmethod_id,
    'custom-methodology' as methodology_name,
    'No direct relationship to gpc methodologies' AS methodology_description,
    gpc_refno as gpc_reference_number,
    1 as scope
FROM 
    modelled.emissions_staging
ON CONFLICT (gpcmethod_id)
DO UPDATE SET 
    methodology_name = EXCLUDED.methodology_name,
    methodology_description = EXCLUDED.methodology_description,
    gpc_reference_number = EXCLUDED.gpc_reference_number,
    scope = EXCLUDED.scope
    ;