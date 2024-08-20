CREATE TABLE IF NOT EXISTS modelled.gpc_methodology (
    gpcmethod_id UUID PRIMARY KEY,
    methodology_name TEXT,
    methodology_description TEXT,
    gpc_reference_number TEXT,
    scope int
);