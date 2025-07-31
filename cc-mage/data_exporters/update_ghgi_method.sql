WITH methodology AS (
    SELECT DISTINCT
        methodology_name,
        gpc_reference_number
    FROM raw_data.electricity_maps_staging
)
INSERT INTO modelled.ghgi_methodology 
    (method_id, methodology_name, methodology_description, gpc_reference_number)
SELECT
    (MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID) AS method_id,
    methodology_name,
    'The Grid Electricity Consumption methodology estimates GHG emissions from the use of electricity that is supplied through the grid. These emissions are calculated by multiplying the amount of electricity consumed by each subsector by the relevant grid emission factor.' AS methodology_description,
    gpc_reference_number
FROM methodology
ON CONFLICT (method_id) DO UPDATE SET
    methodology_name = EXCLUDED.methodology_name,
    methodology_description = EXCLUDED.methodology_description,
    gpc_reference_number = EXCLUDED.gpc_reference_number;