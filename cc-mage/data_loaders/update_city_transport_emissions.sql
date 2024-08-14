CREATE TABLE IF NOT EXISTS modelled.emissions (
    emissions_id UUID PRIMARY KEY,
    source_name TEXT NOT NULL,
    gpc_reference_number TEXT NOT NULL,
    actor_name TEXT,
    actor_id TEXT,
    temporal_granularity TEXT,
    gpcmethod_id UUID,
    activity_id UUID,
    activity_value NUMERIC,
    gas_name TEXT,
    emissions_value NUMERIC,
    emissions_units TEXT,
    emissions_year INTEGER,
    emissions_factor_id UUID,
    geometry_type TEXT,
    geometry_value TEXT
);


INSERT INTO modelled.emissions 
    (emissions_id, source_name, gpc_reference_number, actor_name, actor_id, temporal_granularity, 
     gpcmethod_id, activity_id, activity_value, 
     gas_name, emissions_value, emissions_units, emissions_year, emissions_factor_id, 
     geometry_type, geometry_value)
SELECT 
    (MD5(CONCAT_WS('-', source_name, gpc_reference_number, actor_id, 
    (MD5(CONCAT_WS('-', activity_name,activity_units,activity_subcategory_type))::UUID),
    emissions_year))::UUID) AS emissions_id,
    source_name,
    gpc_reference_number,
    actor_name,
    actor_id,
    temporal_granularity,
    (MD5(CONCAT_WS('-','II.1.1','Induced activity'))::UUID) as gpcmethod_id,
    (MD5(CONCAT_WS('-', activity_name,activity_units,activity_subcategory_type))::UUID) AS activity_id,
    activity_value,
    gas_name,
    emissions_value,
    emissions_units,
    emissions_year,
    emissions_factor_id::uuid as emissions_factor_id,
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
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_id = EXCLUDED.activity_id,
    activity_value = EXCLUDED.activity_value,
    gas_name = EXCLUDED.gas_name,
    emissions_value = EXCLUDED.emissions_value,
    emissions_units = EXCLUDED.emissions_units,
    emissions_year = EXCLUDED.emissions_year,
    emissions_factor_id = EXCLUDED.emissions_factor_id,
    geometry_type = EXCLUDED.geometry_type,
    geometry_value = EXCLUDED.geometry_value;