DROP TABLE IF EXISTS raw_data.ct_fossilfuels_staging;

CREATE TABLE raw_data.ct_fossilfuels_staging AS 
WITH data_raw AS (
SELECT 
  iso3_country,
  sector,
  subsector,
  EXTRACT(year FROM start_time) AS emissions_year,
  UPPER(gas) AS gas_name,
  lat,
  lon,
  sum(emissions_quantity::numeric) as emissions_quantity,
  max(source_name) as source_name,
  sum(activity::numeric) as activity,
  avg(emissions_factor::numeric) as emissions_factor,
  max(activity_units) as activity_units,
  max(emissions_factor_units) as emissions_factor_units
FROM raw_data.ct_fossilfuels
WHERE EXTRACT(year FROM start_time) < 2025
GROUP BY iso3_country,sector,subsector,EXTRACT(year FROM start_time),UPPER(gas), lat, lon
),
gpc_data AS (
SELECT 	a.sector,
		a.subsector,
		emissions_year,
		gas_name,
		lat,
		lon,
		emissions_quantity,
		source_name,
		activity,
		activity_units,
		emissions_factor,
		emissions_factor_units,
		trim(gpc_reference_number) as gpc_reference_number,
		methodology_name,
		activity_name,
		activity_subcategoryname1,
		activity_subcategoryvalue1,
		activity_subcategoryname2,
		activity_subcategoryvalue2
FROM data_raw a 
LEFT JOIN raw_data.ct_fossilfuels_mapping b 
ON a.sector = b.sector 
AND a.subsector = b.subsector
),
locode_data AS (
SELECT 		(MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID) AS method_id,
			methodology_name,
			gpc_reference_number,
			activity_name,
            (
			  CASE
			    WHEN activity_subcategoryname2 IS NOT NULL THEN
			      jsonb_build_object(
			        activity_subcategoryname1, activity_subcategoryvalue1,
			        activity_subcategoryname2, activity_subcategoryvalue2,
			        'data-source', source_name
			      )
			    ELSE
			      jsonb_build_object(
			        activity_subcategoryname1, activity_subcategoryvalue1,
			        'data-source', source_name
			      )
			  END
			) as activity_subcategory_type,
			gas_name,
			emissions_factor as emissionfactor_value,
			emissions_factor_units,
			activity_units,
			'ClimateTRACE' as publisher_name,
			'https://climatetrace.org/' as publisher_url,
			'ClimateTRACEv2025' as datasource_name,
			'Fossil Fuel Operations' as dataset_name,
			'https://climatetrace.org/data' as dataset_url,
			emissions_year,
			emissions_quantity as emissions_value,
			(MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID) AS gpcmethod_id,
			activity::numeric as activity_value,
			cp.locode as actor_id,
			cp.city_id,
			ST_GeometryType(ST_SetSRID(ST_MakePoint(a.lon, a.lat), 4326)) as geometry_type,
			ST_GeoHash(ST_SetSRID(ST_MakePoint(a.lon, a.lat), 4326), 20) AS geometry_id,
			ST_SetSRID(ST_MakePoint(a.lon, a.lat), 4326) as geometry			 
FROM 		gpc_data a
INNER JOIN 	modelled.city_polygon cp
ON 			ST_Intersects(ST_SetSRID(ST_MakePoint(a.lon, a.lat), 4326), cp.geometry)
)
SELECT 	method_id,
		methodology_name,
		gpc_reference_number,
		activity_name,
		activity_subcategory_type,
		gas_name,
		avg(emissionfactor_value) as emissionfactor_value,
		max(emissions_factor_units) as emissions_factor_units,
		max(activity_units) as activity_units,
		publisher_name,
		publisher_url,
		datasource_name,
		dataset_name,
		dataset_url,
		emissions_year,
		sum(emissions_value) as emissions_value,
		gpcmethod_id,
		sum(activity_value) as activity_value,
		actor_id,
		city_id,
        geometry_type,
        geometry_id,
        geometry
FROM 	locode_data
GROUP BY method_id,
		methodology_name,
		gpc_reference_number,
		activity_name,
		activity_subcategory_type,
		gas_name,
		publisher_name,
		publisher_url,
		datasource_name,
		dataset_name,
		dataset_url,
		emissions_year,
		gpcmethod_id,
		actor_id,
		city_id,
        geometry_type,
        geometry_id,
        geometry;