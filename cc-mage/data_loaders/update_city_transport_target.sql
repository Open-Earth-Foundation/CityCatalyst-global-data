CREATE TABLE IF NOT EXISTS modelled.emissions (
    emissions_id UUID PRIMARY KEY,
    source_name TEXT NOT NULL,
    gpc_reference_number TEXT NOT NULL,
    actor_name TEXT,
    actor_id TEXT,
    temporal_granularity TEXT,
    method_name TEXT,
    activity_name TEXT,
    activity_subcategory_type TEXT,
    activity_value NUMERIC,
    activity_units TEXT,
    gas_name TEXT,
    emissions_value NUMERIC,
    emissions_units TEXT,
    emissions_year INTEGER,
    emissions_factor_id TEXT,
    geometry_type TEXT,
    geometry_value TEXT
);


INSERT INTO modelled.emissions 
    (emissions_id, source_name, gpc_reference_number, actor_name, actor_id, temporal_granularity, 
     method_name, activity_name, activity_subcategory_type, activity_value, activity_units, 
     gas_name, emissions_value, emissions_units, emissions_year, emissions_factor_id, 
     geometry_type, geometry_value)
SELECT 
    (MD5(CONCAT_WS('-', source_name, gpc_reference_number, actor_id, activity_name, 
                   activity_subcategory_type, emissions_year))::UUID) AS emissions_id,
    source_name,
    gpc_reference_number,
    actor_name,
    actor_id,
    temporal_granularity,
    method_name,
    --(MD5(CONCAT_WS('-', activity_name,activity_units, activity_subcategory_type))::UUID) AS activity_id,
    activity_name,
    activity_subcategory_type,
    activity_value,
    activity_units,
    gas_name,
    emissions_value,
    emissions_units,
    emissions_year,
    emissions_factor_id,
    geometry_type,
    geometry_value
FROM 
    modelled.emissions_staging
ON CONFLICT ON CONSTRAINT emissions_pkey
DO UPDATE SET 
    source_name = EXCLUDED.source_name,
    gpc_reference_number = EXCLUDED.gpc_reference_number,
    actor_name = EXCLUDED.actor_name,
    actor_id = EXCLUDED.actor_id,
    temporal_granularity = EXCLUDED.temporal_granularity,
    method_name = EXCLUDED.method_name,
    activity_name = EXCLUDED.activity_name,
    activity_subcategory_type = EXCLUDED.activity_subcategory_type,
    activity_value = EXCLUDED.activity_value,
    activity_units = EXCLUDED.activity_units,
    gas_name = EXCLUDED.gas_name,
    emissions_value = EXCLUDED.emissions_value,
    emissions_units = EXCLUDED.emissions_units,
    emissions_year = EXCLUDED.emissions_year,
    emissions_factor_id = EXCLUDED.emissions_factor_id,
    geometry_type = EXCLUDED.geometry_type,
    geometry_value = EXCLUDED.geometry_value;
