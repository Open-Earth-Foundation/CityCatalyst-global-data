WITH methodology AS (
    SELECT
        methodology_name,
        methodology_description,
        gpc_reference_number
    FROM raw_data.ghgi_methodology_staging
)
INSERT INTO modelled.ghgi_methodology 
    (method_id, methodology_name, methodology_description, gpc_reference_number)
SELECT
    (MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID) AS method_id,
    methodology_name,
    methodology_description,
    gpc_reference_number
FROM methodology