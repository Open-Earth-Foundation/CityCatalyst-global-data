DROP TABLE IF EXISTS raw_data.ipcc_transport_co2;

CREATE TABLE raw_data.ipcc_transport_co2 AS
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
        WHEN fuel_2006 LIKE 'Liquefied Petroleum Gases%' THEN 'fuel-type-lpg'
        WHEN fuel_2006 LIKE 'Motor Gasoline%' THEN 'fuel-type-gasoline'
        WHEN fuel_2006 LIKE 'Natural Gas%' THEN 'fuel-type-natural-gas-liquids'
        ELSE 'unknown' 
    END AS fuel_type
FROM raw_data.ipcc_ef
WHERE 1=1
--AND gpc_reference_number like 'II.%'
AND gas_name IN ('CO2', 'CH4', 'N2O')
AND region IS null
and description in ('Carbon Content ', 'Net Calorific Value (NCV) ')
AND NOT (regexp_replace(ef_value, '\s+', '', 'g') ~ '^\d+-\d+$')
),
--- these are to be used for co2 since it doesn't depend on the transport types they are the same for all
-- need to Emissions (kg CO₂) = Fuel Energy (GJ) × Carbon Content (kg/GJ) × (44/12) 
co2_ef AS (
SELECT ipcc_code, gpc_reference_number, activity_subcategory_type1,activity_subcategory_typename1, gas_name, fuel_type,
max(case when description = 'Carbon Content ' then ef_value end) as carbon_content,
max(case when description = 'Carbon Content ' then unit end) as carbon_content_unit,
max(case when description = 'Net Calorific Value (NCV) ' then ef_value end) as ncv,
max(case when description = 'Net Calorific Value (NCV) ' then unit end) as ncv_unit 
FROM ef_data
WHERE gas_name = 'CO2'
AND fuel_type != 'unknown'
GROUP BY ipcc_code, gpc_reference_number, activity_subcategory_type1,activity_subcategory_typename1, gas_name, fuel_type
)
SELECT 	ipcc_code,
		gpc_reference_number,
		activity_subcategory_type1,
		activity_subcategory_typename1,
		gas_name,
		fuel_type,
--		carbon_content,
--		carbon_content_unit,
--		ncv,
--		ncv_unit,
		carbon_content * (44/12) * 1000 AS ef_value,
		'kg/TJ' AS ef_units
FROM co2_ef
-- UNION
-- SELECT 	ipcc_code,
-- 		gpc_reference_number,
-- 		activity_subcategory_type1,
-- 		activity_subcategory_typename1,
-- 		gas_name,
-- 		fuel_type,
-- --		carbon_content,
-- --		carbon_content_unit,
-- --		ncv,
-- --		ncv_unit,
-- 		(ncv * 1000 * carbon_content * (44/12)) / 1000 AS ef_value1,
-- 		'kg/kg' AS ef_units2
-- FROM co2_ef