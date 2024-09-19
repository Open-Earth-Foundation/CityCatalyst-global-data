INSERT INTO modelled.gpc_methodology 
    (gpcmethod_id, methodology_name, methodology_description, gpc_reference_number, scope)
SELECT DISTINCT
    (MD5(CONCAT_WS('-', 'II.1.1', 'induced-activity'))::UUID) AS gpcmethod_id,
    'induced-activity' as methodology_name,
    '50% inbound, 50% outbound, and 100% in-boundary trips' AS methodology_description,
    gpc_reference_number,
    1 as scope
FROM 
    raw_data.google_emissions
ON CONFLICT (gpcmethod_id)
DO UPDATE SET 
    methodology_name = EXCLUDED.methodology_name,
    methodology_description = EXCLUDED.methodology_description,
    gpc_reference_number = EXCLUDED.gpc_reference_number,
    scope = EXCLUDED.scope
    ;