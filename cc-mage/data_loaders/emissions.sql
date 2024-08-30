CREATE TABLE IF NOT EXISTS modelled.emissions (
	emissions_id uuid PRIMARY KEY,
	datasource_name text NULL,
	actor_id varchar NULL,
	city_id text NULL,
	gpc_reference_number text NULL,
	emissions_value float8 NULL,
	emissions_year numeric NULL,
	emissions_units text NULL,
	gpcmethod_id uuid NULL,
	gas_name text NULL,
	emissionfactor_id uuid NULL,
	activity_id uuid NULL,
	activity_value text NULL,
	spatial_granularity text NOT NULL,
	geometry_type text NULL,
	geometry public.geometry NULL,
	geometry_id text NULL
);