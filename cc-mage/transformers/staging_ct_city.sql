DROP TABLE IF EXISTS raw_data.ct_city_staging;

CREATE TABLE raw_data.ct_city_staging AS 
WITH gpc_data AS (
SELECT 	a.sector,
		a.subsector,
		_year as emissions_year,
		upper(gas) as gas_name,
--		lat,
--		lon,
		emissions_quantity,
--		source_name,
		null::numeric as activity,
		null as activity_units,
		null::numeric as emissions_factor,
		null as emissions_factor_units,
		trim(gpc_reference_number) as gpc_reference_number,
		methodology_name,
		activity_name,
		activity_subcategoryname1,
		activity_subcategoryvalue1,
		activity_subcategoryname2,
		activity_subcategoryvalue2
FROM raw_data.ct_city_emissions a 
INNER JOIN raw_data.ct_city_mapping b 
ON a.sector = b.sector 
AND a.subsector = b.subsector
WHERE a.emissions_quantity > 0
AND b.mapping = 'Y'
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
			        activity_subcategoryname2, activity_subcategoryvalue2
			      )
			    ELSE
			      jsonb_build_object(
			        activity_subcategoryname1, activity_subcategoryvalue1
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
			'ClimateTrace City API' as dataset_name,
			'https://climatetrace.org/data' as dataset_url,
			emissions_year,
			emissions_quantity as emissions_value,
			(MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID) AS gpcmethod_id,
			activity::numeric as activity_value,
			'{{locode}}' as actor_id,
			(select city_id from modelled.city_polygon where locode = '{{locode}}') as city_id,
			null as geometry_type,
			null AS geometry_id,
			null::geometry as geometry 			 
FROM 		gpc_data a
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