DROP TABLE IF EXISTS raw_data.ct_wastewater_emissions_staging;

CREATE TABLE raw_data.ct_wastewater_emissions_staging AS
WITH all_data AS (
SELECT 	'wastewater-inside-methodology' as methodology_name,
		'III.4.1' as gpc_reference_number,
		'wastewater-inside-generated' as activity_name,
		'people' as activity_units,
        income_group, treatment_type, treatment_status, collection_status,
		json_build_object(
		            'wastewater-inside-domestic-calculator-income-group', income_group,
		            'wastewater-inside-domestic-calculator-treatment-name', treatment_type,
		            'wastewater-inside-domestic-calculator-treatment-status', treatment_status,
		            'wastewater-inside-domestic-calculator-collection-status', collection_status
		        ) AS activity_subcategory_type,
		 'ClimateTracev2024' as datasource_name,       
		 a.locode as actor_id, 
		 total_co2_emissions * scope_ratio as emissions_value,
		 2022 as emissions_year,
		 'kg' as emissions_units,
        'CO2' as gas_name		
FROM raw_data.br_wastewater_total_emissions a
LEFT JOIN raw_data.br_wastewater_scope_allocation b 
ON a.locode = b.locode
UNION ALL
SELECT 	'wastewater-inside-methodology' as methodology_name,
		'III.4.1' as gpc_reference_number,
		'wastewater-inside-generated' as activity_name,
		'people' as activity_units,
        income_group, treatment_type, treatment_status, collection_status,
		json_build_object(
		            'wastewater-inside-domestic-calculator-income-group', income_group,
		            'wastewater-inside-domestic-calculator-treatment-name', treatment_type,
		            'wastewater-inside-domestic-calculator-treatment-status', treatment_status,
		            'wastewater-inside-domestic-calculator-collection-status', collection_status
		        ) AS activity_subcategory_type,
		 'ClimateTracev2024' as datasource_name,       
		 a.locode as actor_id, 
		 total_n20_emissions * scope_ratio as emissions_value,
		 2022 as emissions_year,
		 'kg' as emissions_units,
        'N2O' as gas_name		
FROM raw_data.br_wastewater_total_emissions a
LEFT JOIN raw_data.br_wastewater_scope_allocation b 
ON a.locode = b.locode
UNION ALL
SELECT 	'wastewater-outside-methodology' as methodology_name,
		'III.4.2' as gpc_reference_number,
		'wastewater-outside-generated' as activity_name,
		'people' as activity_units,
        income_group, treatment_type, treatment_status, collection_status,
		json_build_object(
		            'wastewater-inside-domestic-calculator-income-group', income_group,
		            'wastewater-inside-domestic-calculator-treatment-name', treatment_type,
		            'wastewater-inside-domestic-calculator-treatment-status', treatment_status,
		            'wastewater-inside-domestic-calculator-collection-status', collection_status
		        ) AS activity_subcategory_type,
		 'ClimateTracev2024' as datasource_name,       
		 a.locode as actor_id, 
		 total_co2_emissions * (1-scope_ratio) as emissions_value,
		 2022 as emissions_year,
		 'kg' as emissions_units,
        'CO2' as gas_name		
FROM raw_data.br_wastewater_total_emissions a
LEFT JOIN raw_data.br_wastewater_scope_allocation b 
ON a.locode = b.locode
UNION ALL
SELECT 	'wastewater-outside-methodology' as methodology_name,
		'III.4.2' as gpc_reference_number,
		'wastewater-outside-generated' as activity_name,
		'people' as activity_units,
        income_group, treatment_type, treatment_status, collection_status,
		json_build_object(
		            'wastewater-inside-domestic-calculator-income-group', income_group,
		            'wastewater-inside-domestic-calculator-treatment-name', treatment_type,
		            'wastewater-inside-domestic-calculator-treatment-status', treatment_status,
		            'wastewater-inside-domestic-calculator-collection-status', collection_status
		        ) AS activity_subcategory_type,
		 'ClimateTracev2024' as datasource_name,       
		 a.locode as actor_id, 
		 total_n20_emissions * (1-scope_ratio) as emissions_value,
		 2022 as emissions_year,
		 'kg' as emissions_units,
        'N2O' as gas_name		
FROM raw_data.br_wastewater_total_emissions a
LEFT JOIN raw_data.br_wastewater_scope_allocation b 
ON a.locode = b.locode
),
data_methodid AS (
SELECT (MD5(CONCAT_WS('-', methodology_name, gpc_reference_number))::UUID) AS method_id, *
FROM all_data
WHERE emissions_value > 0
),
data_activityid AS (
SELECT (MD5(CONCAT_WS('-', method_id, activity_name, activity_units, activity_subcategory_type))::UUID) AS activity_id,
	   null as emission_factor_id,
	   null as geometry_value,
	   *
FROM   data_methodid
)
SELECT  (MD5(CONCAT_WS('-', datasource_name, gpc_reference_number, actor_id, emissions_year, method_id, gas_name, emission_factor_id, activity_id))::UUID) AS emissions_id,
		*
FROM    data_activityid
;