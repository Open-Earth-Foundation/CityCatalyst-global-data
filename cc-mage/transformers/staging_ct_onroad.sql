DROP TABLE IF EXISTS raw_data.ct_onroad_v2025_staging;

CREATE TABLE raw_data.ct_onroad_v2025_staging AS 
WITH staging_data AS (
SELECT  	(MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID) AS method_id,
			methodology_name,
			gpc_reference_number,
			activity_name,
			jsonb_build_object(activity_subcategory_typename,activity_subcategory_name) as activity_subcategory_type,
			activity_subcategory_typename,activity_subcategory_name,
			gas as gas_name,
			emissions_factor as emissionfactor_value,
			emissions_factor_units,
			activity_units,
			'ClimateTRACE' as publisher_name,
			'https://climatetrace.org/' as publisher_url,
			'ClimateTRACEv2025' as datasource_name,
			'On-road Transportation' as dataset_name,
			'https://downloads.climatetrace.org/v4.5.0/sector_packages/co2e_100yr/transportation.zip' AS dataset_url,
			_year as emissions_year,
			emissions_quantity as emissions_value,
			(MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID) AS gpcmethod_id,
			activity::numeric as activity_value,
			cp.locode as actor_id,
			cp.city_id,
			ST_GeometryType(ST_SetSRID(ST_MakePoint(a.lon, a.lat), 4326)) as geometry_type,
			ST_GeoHash(ST_SetSRID(ST_MakePoint(a.lon, a.lat), 4326), 20) AS geometry_id,
			ST_SetSRID(ST_MakePoint(a.lon, a.lat), 4326) as geometry
FROM 		raw_data.ct_onroad_v2025 a
INNER JOIN 	modelled.city_polygon cp
ON 			ST_Intersects(ST_SetSRID(ST_MakePoint(a.lon, a.lat), 4326), cp.geometry)
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