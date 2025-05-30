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
)
SELECT *
FROM tranport_units;