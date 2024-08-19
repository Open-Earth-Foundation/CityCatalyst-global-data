CREATE TABLE IF NOT EXISTS modelled.activity_subcategory (
    activity_id UUID PRIMARY KEY,
    activity_name TEXT,
    activity_units TEXT,
    gpcmethod_id UUID,
    activity_subcategory_type JSONB
);