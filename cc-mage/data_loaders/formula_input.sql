CREATE TABLE IF NOT EXISTS modelled.formula_input (
    formula_input_id uuid NOT NULL,
    method_id uuid NULL, 
    publisher_id uuid NULL, 
    dataset_id uuid NULL, 
    gas_name varchar NULL,
    parameter_code varchar NULL,
    parameter_name varchar NULL,
    gpc_reference_number varchar NULL,
    formula_input_value float8 NULL,
    formula_input_units varchar NULL,
    metadata jsonb,
    actor_id varchar NULL,
	CONSTRAINT formula_input_pkey PRIMARY KEY (formula_input_id)
);