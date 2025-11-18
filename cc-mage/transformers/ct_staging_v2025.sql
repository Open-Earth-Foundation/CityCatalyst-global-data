DROP TABLE IF EXISTS raw_data.ct_staging_v2025;

CREATE TABLE raw_data.ct_staging_v2025 AS 
WITH staging_data AS (
SELECT *
FROM raw_data.ct_buildings_staging
UNION 
SELECT *
FROM raw_data.ct_transportation_staging
UNION
SELECT *
FROM raw_data.ct_manufactoring_staging
UNION
SELECT *
FROM raw_data.ct_fossilfuels_staging
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