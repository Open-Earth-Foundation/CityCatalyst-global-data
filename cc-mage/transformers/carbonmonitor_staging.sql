DROP TABLE IF EXISTS raw_data.carbonmonitor_staging;

CREATE TABLE raw_data.carbonmonitor_staging AS 
WITH cm_raw as (
SELECT 
  city,
  sector,
  EXTRACT(year FROM to_date(_date, 'DD/MM/YYYY')) AS emissions_year,
  'CO2' AS gas_name,
  SUM(_value::numeric) AS emissions_quantity,
  NULL AS activity,
  NULL AS emissions_factor,
  NULL AS activity_units,
  NULL AS emissions_factor_units
FROM raw_data.ghgi_carbon_monitor_emissions
WHERE EXTRACT(year FROM to_date(_date, 'DD/MM/YYYY')) < 2026
GROUP BY city, sector, EXTRACT(year FROM to_date(_date, 'DD/MM/YYYY'))
),
cm_activity AS (
SELECT 	a.city,
		a.sector,
		a.emissions_year,
		a.gas_name,
		a.emissions_quantity,
		a.activity,
		a.emissions_factor,
		a.activity_units,
		a.emissions_factor_units,
		b.gpc_reference_number,
		b.methodology_name,
		b.activity_name,
		b.activity_subcategoryname1,
		b.activity_subcategoryvalue1,
		b.activity_subcategoryname2,
		b.activity_subcategoryvalue2
FROM cm_raw a 
INNER JOIN raw_data.carbonmonitor_mapping b
ON a.sector = b.sector
WHERE b.mapping = 'Y'
)
SELECT
			methodology_name,
			gpc_reference_number,
			activity_name,
			jsonb_build_object(activity_subcategoryname1,activity_subcategoryvalue1,activity_subcategoryname2, activity_subcategoryvalue2) as activity_subcategory_type,
			gas_name,
			emissions_factor as emissionfactor_value,
			emissions_factor_units,
			activity_units,
			'CarbonMonitor' as publisher_name,
			'https://carbonmonitor.org/' as publisher_url,
			'CarbonMonitorv2025' as datasource_name,
			'CityLevelEmissions' as dataset_name,
			'https://cities.carbonmonitor.org/' as dataset_url,
			emissions_year,
			emissions_quantity as emissions_value,
			(MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID) AS gpcmethod_id,
			activity::numeric as activity_value,
			cp.locode as actor_id,
			cp.city_id,
			null as geometry_type,
			null AS geometry_id,
			null::geometry as geometry 	
FROM cm_activity a
INNER JOIN modelled.city_polygon cp 
ON lower(trim(city)) = trim(lower(cp.city_name))
WHERE lower(trim(city)) is not null;