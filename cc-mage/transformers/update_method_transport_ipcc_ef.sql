WITH methodology AS (
    SELECT DISTINCT
        method_id,
        methodology_name,
        null as methodology_description,
        gpc_reference_number
    FROM raw_data.ipcc_transport_ef2
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