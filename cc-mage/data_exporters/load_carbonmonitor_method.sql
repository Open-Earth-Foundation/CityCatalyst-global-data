WITH methodology AS (
    SELECT DISTINCT
        gpcmethod_id as method_id,
        methodology_name,
        null as methodology_description,
        gpc_reference_number
    FROM raw_data.carbonmonitor_staging_v2025
)
INSERT INTO modelled.ghgi_methodology 
    (method_id, methodology_name, methodology_description, gpc_reference_number)
SELECT
    method_id,
    methodology_name,
    methodology_description,
    gpc_reference_number
FROM methodology
ON CONFLICT (method_id) DO UPDATE SET
    methodology_name = EXCLUDED.methodology_name,
    methodology_description = EXCLUDED.methodology_description,
    gpc_reference_number = EXCLUDED.gpc_reference_number;