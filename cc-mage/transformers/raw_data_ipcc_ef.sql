WITH ef_multi_columns AS (
SELECT 	ef_id,
--		ipcc_1996_sector,
		REPLACE(REGEXP_REPLACE(ipcc_2006_sector, '\n', '|'), CHR(10), '|') AS ipcc_sector_multi,
		REPLACE(REGEXP_REPLACE(gas_name, '\n', '|'), CHR(10), '|')  AS gas_multi,
--		fuel_1996,
		fuel_2006,
		type_parameter,
		description,
		technology,
		conditions,
		region,
		abatement,
		properties,
		ef_value,
		unit,
		equation,
		ipcc_worksheet,
		technical_reference,
		data_source,
		data_provider
FROM {{ df_2 }} a
WHERE ef_id IS NOT NULL
),
ef_split_sector AS (
SELECT 	ef_id,
		UNNEST(STRING_SPLIT(ipcc_sector_multi, '|')) AS ipcc_sector,
		gas_multi,
		fuel_2006,
		type_parameter,
		description,
		technology,
		conditions,
		region,
		abatement,
		properties,
		ef_value,
		unit,
		equation,
		ipcc_worksheet,
		technical_reference,
		data_source,
		data_provider
FROM ef_multi_columns
),
ef_split_gas AS (
SELECT 	ef_id,
		ipcc_sector,
		UNNEST(STRING_SPLIT(gas_multi, '|')) AS gas_name,
		fuel_2006,
		type_parameter,
		description,
		technology,
		conditions,
		region,
		abatement,
		properties,
		ef_value,
		unit,
		equation,
		ipcc_worksheet,
		technical_reference,
		data_source,
		data_provider
FROM ef_split_sector
WHERE ipcc_sector != ''
),
ipcc_to_gpc_mapping AS (
SELECT *
FROM {{ df_1 }}
),
ef_clean AS (
SELECT 	ef_id,
		TRIM(STRING_SPLIT(ipcc_sector, '-')[1]) as ipcc_code,
		TRIM(STRING_SPLIT(ipcc_sector, '-')[2]) as ipcc_name,
		CASE WHEN gas_name = 'CARBON DIOXIDE' THEN 'CO2'
		WHEN gas_name = 'NITROUS OXIDE' THEN 'N2O'
		WHEN gas_name = 'METHANE' THEN 'CH4' 
		ELSE gas_name END AS gas_name,
		fuel_2006,
		type_parameter,
		description,
		technology,
		conditions,
		region,
		abatement,
		properties,
		ef_value,
		unit,
		CASE WHEN regexp_extract(technical_reference, '([0-9]{4})') = '' OR regexp_extract(technical_reference, '([0-9]{4})') IS NULL THEN regexp_extract(type_parameter, '([0-9]{4})')
        ELSE regexp_extract(technical_reference, '([0-9]{4})')
        END AS technical_reference_year,
		equation,
		ipcc_worksheet,
		technical_reference,
		data_source,
		data_provider
FROM ef_split_gas a 
WHERE gas_name != ''
),
gpc_ef AS (
SELECT 	ef_id,
		ipcc_code,
		case when b.gpc_mapping = 'II.4.3' then 'II.4.1'
		when b.gpc_mapping = 'II.3.3' then 'II.3.1'
		else b.gpc_mapping end as gpc_reference_number,
		activity_subcategory_type1,activity_subcategory_typename1,activity_subcategory_type2,activity_subcategory_typename2,
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
		ef_value,
		unit,
		technical_reference_year,
		equation,
		ipcc_worksheet,
		technical_reference,
		data_source,
		data_provider
FROM ef_clean a 
LEFT JOIN ipcc_to_gpc_mapping b 
ON a.ipcc_code = b.ipcc_sector
)
SELECT *
FROM gpc_ef