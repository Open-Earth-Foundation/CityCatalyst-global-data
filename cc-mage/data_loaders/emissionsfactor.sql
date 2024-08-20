CREATE TABLE IF NOT EXISTS modelled.emissions_factor (
	emissionfactor_id uuid NOT NULL,
	gas_name text NULL,
	emissionfactor_value float8 NULL,
	unit_denominator text NULL,
	activity_id uuid NULL,
	datasource_name text NULL,
	active_from date NULL,
	active_to date NULL,
	actor_id text NULL,
	CONSTRAINT emissions_factor_pkey PRIMARY KEY (emissionfactor_id)
);