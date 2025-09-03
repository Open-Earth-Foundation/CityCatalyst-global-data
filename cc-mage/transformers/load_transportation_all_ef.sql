DROP TABLE IF EXISTS raw_data.ipcc_transport_ef;

CREATE TABLE raw_data.ipcc_transport_ef AS
WITH ef_data AS (
SELECT 	ef_id,
		ipcc_code,
		gpc_reference_number,
		activity_subcategory_type1,
		activity_subcategory_typename1,
		activity_subcategory_type2,
		activity_subcategory_typename2,
		ipcc_name,
		gas_name,
		fuel_2006,
		type_parameter,
		description,
		technology,
		conditions,
		region,
		abatement,
		properties,
		(regexp_replace(ef_value, '[^\x20-\x7E]+', '', 'g'))::numeric as ef_value,
		unit,
		technical_reference_year,
		equation,
		ipcc_worksheet,
		technical_reference,
		data_source,
		data_provider,
		CASE 
        WHEN fuel_2006 LIKE 'Aviation Gasoline%' THEN 'fuel-type-aviation-gasoline'
        WHEN fuel_2006 LIKE 'Biogasoline%' THEN 'fuel-type-biofuel'
        WHEN fuel_2006 like 'Diesel Oil%' THEN 'fuel-type-diesel'
        WHEN fuel_2006 LIKE 'Gas Oil%' THEN 'fuel-type-gasoline'
        WHEN fuel_2006 LIKE 'Jet Gasoline%' THEN 'fuel-type-jet-gasoline'
        WHEN fuel_2006 LIKE 'Jet Kerosene%' THEN 'fuel-type-jet-kerosene'
        WHEN fuel_2006 LIKE 'Liquefied Petroleum Gases%' THEN 'fuel-type-liquefied-petroleum-gases'
        WHEN fuel_2006 LIKE 'Motor Gasoline%' THEN 'fuel-type-gasoline'
        WHEN fuel_2006 LIKE 'Natural Gas%' THEN 'fuel-type-cng'
        ELSE 'unknown' 
    END AS fuel_type
FROM raw_data.ipcc_ef
WHERE 1=1
AND gpc_reference_number like 'II.%'
AND gas_name IN ('CO2', 'CH4', 'N2O')
AND region IS null
AND NOT (regexp_replace(ef_value, '\s+', '', 'g') ~ '^\d+-\d+$')
),
rank_ef as (
SELECT 	ef_id,
		ipcc_code,
		gpc_reference_number,
		activity_subcategory_type1,
		activity_subcategory_typename1,
		activity_subcategory_type2,
		fuel_type as activity_subcategory_typename2,
		gas_name,
		description,
		technology,
		conditions,
		region,
		abatement,
		properties,
		ef_value,
		regexp_replace(unit, '\s+', '', 'g') as unit,
		technical_reference_year,
		technical_reference,
		data_provider,
		RANK() OVER (PARTITION BY ipcc_code, gpc_reference_number, activity_subcategory_type1,activity_subcategory_typename1, gas_name, fuel_type, unit 
		ORDER BY technical_reference_year DESC, technology) as rnk,
		RANK() over (partition by gpc_reference_number, activity_subcategory_type1,activity_subcategory_typename1, gas_name, fuel_type, unit 
		ORDER BY (CASE WHEN ipcc_code='1.A.3.e.ii' THEN 1 ELSE 2 END) DESC) as ipcc_rnk
FROM ef_data
WHERE ef_value > 0
AND description IN ('Default Emission Factor for Aircraft ', 'Road Transport Emission Factor ', 'Emission Factor for USA Vehicles ',
 'Default Emission Factor for the Most Common Used Fuels for Rail Transport ', 'Default Water-Bourne Navigation Emission Factor ', 'Default Emission Factors for Off-road Mobile Source and Machinery ')
AND unit = 'kg/TJ '
),
fuel_sales_nonco2 AS (
SELECT *
FROM rank_ef
WHERE rnk = 1
AND ipcc_rnk = 1
AND activity_subcategory_typename2 != 'unknown'
),
all_gases as (
SELECT a.*,
		b.ef_value AS co2_ef,
		b.ef_units AS co2_units
FROM fuel_sales_nonco2 a
LEFT JOIN raw_data.ipcc_transport_co2 b
ON a.activity_subcategory_typename2 = b.fuel_type
AND a.unit = b.ef_units
),
fuel_sales_ef AS (
SELECT 	gpc_reference_number,
		activity_subcategory_type1,
		'vehicle-type-all' as activity_subcategory_typename1,
		CASE WHEN gpc_reference_number = 'II.4.3' THEN 'aviation-fuel-type'
		WHEN gpc_reference_number = 'II.3.3' THEN 'waterborne-navigation-fuel-type'
		ELSE activity_subcategory_type2 END AS activity_subcategory_type2, 
		activity_subcategory_typename2,
		gas_name,
		ef_value as emissionfactor_value,
		unit as units,
		'world' as actor_id,
		'fuel-sales' as methodology_name
FROM all_gases
UNION
SELECT 	gpc_reference_number,
		activity_subcategory_type1,
		'vehicle-type-all' as activity_subcategory_typename1,
		CASE WHEN gpc_reference_number = 'II.4.3' THEN 'aviation-fuel-type'
		WHEN gpc_reference_number = 'II.3.3' THEN 'waterborne-navigation-fuel-type'
		ELSE activity_subcategory_type2 END AS activity_subcategory_type2, 
		activity_subcategory_typename2,
		'CO2' as gas_name,
		co2_ef as emissionfactor_value,
		co2_units as units,
		'world' as actor_id,
		'fuel-sales' as methodology_name
FROM all_gases
)
SELECT *
FROM fuel_sales_ef
ORDER BY gpc_reference_number,activity_subcategory_type1,activity_subcategory_typename1,activity_subcategory_type2,activity_subcategory_typename2,gas_name
