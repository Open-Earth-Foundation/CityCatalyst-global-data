WITH formula_raw AS (
    SELECT DISTINCT
        gas,
        parameter_code,
        _parameter_name,
        gpc_refno,
        formula_input_value,
        formula_input_units,
        actor_id,
        methodology_name,
        formula_name,
        publisher_name,
        publisher_url,
        datasource_name,
        dataset_name,
        dataset_url
    FROM raw_data.waste_composition_staging
    WHERE formula_input_value IS NOT NULL
),
ids_data AS (
    SELECT *,
        MD5(CONCAT_WS('-', methodology_name, gpc_refno))::UUID AS method_id,
        MD5(CONCAT_WS('-', publisher_name, publisher_url))::UUID AS publisher_id,
        MD5(CONCAT_WS('-', datasource_name, dataset_name, dataset_url))::UUID AS dataset_id
    FROM formula_raw
)
INSERT INTO modelled.formula_input (
    formula_input_id,
    method_id, 
    publisher_id, 
    dataset_id, 
    gas_name,
    parameter_code,
    parameter_name,
    gpc_reference_number,
    formula_input_value,
    formula_input_units,
    metadata,
    actor_id
)
SELECT 
    MD5(CONCAT_WS('-', gas, parameter_code, gpc_refno, actor_id))::UUID AS formula_input_id,
    method_id, 
    publisher_id, 
    dataset_id, 
    gas,
    parameter_code,
    _parameter_name,
    gpc_refno,
    formula_input_value,
    formula_input_units,
    NULL::jsonb AS metadata,
    actor_id
FROM ids_data
ON CONFLICT (formula_input_id) DO UPDATE SET
    method_id = EXCLUDED.method_id, 
    publisher_id = EXCLUDED.publisher_id, 
    dataset_id = EXCLUDED.dataset_id, 
    gas_name = EXCLUDED.gas_name,
    parameter_code = EXCLUDED.parameter_code,
    parameter_name = EXCLUDED.parameter_name,
    gpc_reference_number = EXCLUDED.gpc_reference_number,
    formula_input_value = EXCLUDED.formula_input_value,
    formula_input_units = EXCLUDED.formula_input_units,
    metadata = EXCLUDED.metadata,
    actor_id = EXCLUDED.actor_id;