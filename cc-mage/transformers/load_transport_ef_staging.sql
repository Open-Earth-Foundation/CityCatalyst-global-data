DROP TABLE IF EXISTS raw_data.ipcc_transport_ef2;

CREATE TABLE raw_data.ipcc_transport_ef2 AS
WITH conversions AS (
SELECT "_from" AS unit_from,"_to" AS unit_to,factor,fuel_type
FROM raw_data.ipcc_conversion_factor
),
tranport_units AS (
SELECT 	gpc_reference_number,
		activity_subcategory_type1,
		activity_subcategory_typename1,
		activity_subcategory_type2,
		activity_subcategory_typename2,
		gas_name,
		emissionfactor_value,
		units,
		actor_id,
		methodology_name
FROM raw_data.ipcc_transport_ef
UNION
SELECT 	gpc_reference_number,
		activity_subcategory_type1,
		activity_subcategory_typename1,
		activity_subcategory_type2,
		activity_subcategory_typename2,
		gas_name,
		factor * emissionfactor_value as emissionfactor_value,
		'kg/m3' as units,
		actor_id,
		methodology_name
FROM raw_data.ipcc_transport_ef a 
LEFT JOIN conversions b 
ON (CASE WHEN a.activity_subcategory_typename2 = 'fuel-type-diesel' THEN 'fuel-type-diesel-oil' 
WHEN a.activity_subcategory_typename2 = 'fuel-type-lpg' THEN 'fuel-type-liquefied-petroleum-gases'
ELSE a.activity_subcategory_typename2 END)  = b.fuel_type
AND unit_from = 'm³'
AND unit_to = 'TJ'
UNION
SELECT 	gpc_reference_number,
		activity_subcategory_type1,
		activity_subcategory_typename1,
		activity_subcategory_type2,
		activity_subcategory_typename2,
		gas_name,
		factor * emissionfactor_value as emissionfactor_value,
		'kg/kg' as units,
		actor_id,
		methodology_name
FROM raw_data.ipcc_transport_ef a 
INNER JOIN conversions b 
ON (CASE WHEN a.activity_subcategory_typename2 = 'fuel-type-diesel' THEN 'fuel-type-diesel-oil' 
WHEN a.activity_subcategory_typename2 = 'fuel-type-lpg' THEN 'fuel-type-liquefied-petroleum-gases'
ELSE a.activity_subcategory_typename2 END)  = b.fuel_type
AND unit_from = 'kg'
AND unit_to = 'TJ'
),
raw_data AS (
SELECT 	gpc_reference_number,
		activity_subcategory_type1,
		activity_subcategory_typename1,
		case when gpc_reference_number = 'II.3.1' then 'waterborne-navigation-fuel-type'
		when gpc_reference_number = 'II.4.1' then 'aviation-fuel-type'
		else activity_subcategory_type2 end as activity_subcategory_type2,
		activity_subcategory_typename2,
		gas_name,
		emissionfactor_value,
		units,
		actor_id,
		methodology_name
FROM tranport_units
),
method_data AS ( 
SELECT 	(MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID) AS method_id,
		methodology_name,
		gpc_reference_number,
		CASE 
	    WHEN gpc_reference_number IN ('II.5.1', 'II.4.1', 'II.3.1', 'II.1.1') THEN 'total-fuel-sold-in-gas-stations'
	    WHEN gpc_reference_number = 'II.2.1' THEN 'total-fuel-consumed'
	    ELSE 'unknown'
		END AS activity_name,
		jsonb_build_object(activity_subcategory_type1,activity_subcategory_typename1,activity_subcategory_type2,activity_subcategory_typename2) as activity_subcategory_type,
		activity_subcategory_type1,activity_subcategory_typename1,activity_subcategory_type2,activity_subcategory_typename2,
		gas_name,
		emissionfactor_value,
		units,
		trim(split_part(units, '/',2)) as activity_units,
		actor_id,
		'IPCC' as publisher_name,
		'https://www.ipcc.ch/,02359a57-1fd1-397f-9d75-692c569c8ed7' AS publisher_url,
		'IPCC' as datasource_name, 
		'IPCC Emission Factor Database (EFDB) [2006 IPCC Guidelines]' AS dataset_name,
		'https://www.ipcc-nggip.iges.or.jp/EFDB/main.php,02359a57-1fd1-397f-9d75-692c569c8ed7,6a508faa-80a8-3246-9941-90d8cc8dec85' AS dataset_url
FROM 	raw_data
WHERE  	emissionfactor_value IS NOT NULL
),
publisher_data AS (
SELECT 	method_id,
		methodology_name,
		gpc_reference_number,
		MD5(CONCAT_WS('-', activity_name, activity_units, activity_subcategory_type::TEXT, method_id))::UUID AS activity_id,
		activity_name,
		activity_units,
		activity_subcategory_type,
		activity_subcategory_type1,activity_subcategory_typename1,activity_subcategory_type2,activity_subcategory_typename2,
		(MD5(CONCAT_WS('-', publisher_name))::UUID) AS publisher_id,
		publisher_name,
		publisher_url,
		(MD5(CONCAT_WS('-', datasource_name, dataset_name, dataset_url))::UUID) AS dataset_id,
		datasource_name,
		dataset_name,
		dataset_url,
		gas_name,
		emissionfactor_value,
		actor_id,
		units
FROM 	method_data
)
SELECT 	method_id,
		methodology_name,
		gpc_reference_number,
		activity_id,
		activity_name,
		activity_units,
		activity_subcategory_type,
		activity_subcategory_type1,
		activity_subcategory_typename1,
		activity_subcategory_type2,
		activity_subcategory_typename2,
		publisher_id,
		publisher_name,
		publisher_url,
		dataset_id,
		datasource_name,
		dataset_name,
		dataset_url,
		MD5(CONCAT_WS('-', publisher_id, dataset_id, activity_id, units, gas_name, actor_id))::UUID AS emissionfactor_id,
		gas_name,
		emissionfactor_value,
		units,
		actor_id
FROM publisher_data