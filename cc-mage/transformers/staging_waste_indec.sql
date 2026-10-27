DROP TABLE IF EXISTS raw_data.arg_solid_waste_indec;

CREATE TABLE raw_data.arg_solid_waste_indec AS 
WITH staging_data AS (
SELECT 	(MD5(CONCAT_WS('-', 'solid-waste-method-ct', gpc_reference_number))::UUID) AS method_id,
		'solid-waste-method-ct' as methodology_name,
		gpc_reference_number,
		activity_name,
		null as activity_subcategory_type,
		gas_name,
		(emission_factor::numeric / 1000) as emissionfactor_value,
		'kg' as emissions_factor_units,
		'kg' as activity_units,
		'INDEC' AS publisher_name,
		'https://www.indec.gob.ar/' AS publisher_url,
		'INDECv2022' AS datasource_name,
		'Misiones Censo 2022' AS dataset_name,
		'https://censo.gob.ar/index.php/datos_definitivos_misiones/' AS dataset_url,
		_year as emissions_year,
		(emissions_value::numeric * 1000) emissions_value,
		(MD5(CONCAT_WS('-', 'solid-waste-method-ct'))::UUID) as gpcmethod_id,
		(msw_t_year_::numeric * 1000) AS activity_value,
		actor_id,
		cp.city_id,
		null geometry_type,
		null geometry_id,
		null::geometry geometry
FROM raw_data.arg_solid_waste_staging a 
LEFT JOIN modelled.city_polygon cp 
ON a.actor_id = cp.locode
),
staging_activity AS (
SELECT 	*,
		MD5(CONCAT_WS('-', activity_name, activity_units, activity_subcategory_type::TEXT, method_id))::UUID AS activity_id,
		(MD5(CONCAT_WS('-', publisher_name))::UUID) AS publisher_id,
		(MD5(CONCAT_WS('-', datasource_name, dataset_name))::UUID) AS dataset_id
FROM 	staging_data
),
staging_ef as (
SELECT 	*,
		MD5(CONCAT_WS('-', publisher_id, dataset_id, activity_id, emissions_factor_units, gas_name, actor_id, emissions_year))::UUID AS emissionfactor_id
FROM 	staging_activity
)
SELECT 	*,
		(MD5(CONCAT_WS('-', actor_id, emissions_year, gpc_reference_number, gpcmethod_id, gas_name, emissionfactor_id, activity_id, geometry_id))::UUID) AS emissions_id
FROM 	staging_ef
