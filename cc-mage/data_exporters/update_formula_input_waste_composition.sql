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
publisher_ids AS (
    SELECT DISTINCT
        publisher_id,
        publisher_name,
        dataset_id,
        dataset_name
    FROM modelled.publisher_datasource
),
-- Match with known publisher/dataset IDs
ids_data AS (
    SELECT
        fr.*,
        MD5(CONCAT_WS('-', fr.methodology_name, fr.gpc_refno))::UUID AS method_id,
        pid.publisher_id,
        pid.dataset_id
    FROM formula_raw fr
    LEFT JOIN publisher_ids pid
      ON fr.publisher_name = pid.publisher_name
     AND fr.dataset_name = pid.dataset_name
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
    actor_id,
    formula_name
)
SELECT 
    MD5(CONCAT_WS('-', fr.formula_name, fr.gas, fr.parameter_code, fr.gpc_refno, fr.actor_id))::UUID AS formula_input_id,
    fr.method_id, 
    fr.publisher_id, 
    fr.dataset_id, 
    fr.gas,
    fr.parameter_code,
    fr._parameter_name AS parameter_name,
    fr.gpc_refno AS gpc_reference_number,
    fr.formula_input_value,
    fr.formula_input_units,
    NULL::jsonb AS metadata,
    fr.actor_id,
    fr.formula_name
FROM ids_data fr
WHERE fr.publisher_id IS NOT NULL AND fr.dataset_id IS NOT NULL
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
    actor_id = EXCLUDED.actor_id,
    formula_name = EXCLUDED.formula_name;