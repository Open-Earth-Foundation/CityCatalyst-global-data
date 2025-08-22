DROP TABLE IF EXISTS raw_data.br_wastewater_total_emissions;

CREATE TABLE raw_data.br_wastewater_total_emissions as
WITH income_data AS (
    SELECT 'treatment-name-none' AS treatment_type, 'urban_high_income' AS income_group, 0 AS utilisation_fraction, 0.057 AS emission_factor
    UNION ALL
    SELECT 'treatment-name-sewer', 'urban_high_income', 20, 0.0756
    UNION ALL
    SELECT 'treatment-name-septic-system', 'urban_high_income', 0, 0
    UNION ALL
    SELECT 'treatment-name-latrine', 'urban_high_income', 5, 0.15
    UNION ALL
    SELECT 'treatment-name-other', 'urban_high_income', 0, 0
    UNION ALL
    SELECT 'treatment-name-none', 'urban_low_income', 11.8, 0.057
    UNION ALL
    SELECT 'treatment-name-sewer', 'urban_low_income', 23.6, 0.0756
    UNION ALL
    SELECT 'treatment-name-septic-system', 'urban_low_income', 0, 0
    UNION ALL
    SELECT 'treatment-name-latrine', 'urban_low_income', 23.6, 0.15
    UNION ALL
    SELECT 'treatment-name-other', 'urban_low_income', 0, 0
    UNION ALL
    SELECT 'treatment-name-none', 'rural', 7, 0.057
    UNION ALL
    SELECT 'treatment-name-sewer', 'rural', 2, 0.0756
    UNION ALL
    SELECT 'treatment-name-septic-system', 'rural', 0, 0
    UNION ALL
    SELECT 'treatment-name-latrine', 'rural', 7, 0.15
    UNION ALL
    SELECT 'treatment-name-other', 'rural', 0, 0
),
income_factor AS (
SELECT treatment_type,income_group,utilisation_fraction/100 as utilisation_fraction,emission_factor
FROM income_data
WHERE utilisation_fraction > 0
),
raw_br_data AS (
SELECT DISTINCT municipal_code, municipality_name, uf, total_resident_population 
FROM raw_data.snis_br_wastewater
),
br_locode_data AS (
SELECT b.locode, b.geometry, a.total_resident_population, a.total_resident_population * 18.25 * 1.25 as total_organic_waste,
-- default values: protein = 33.58, Fnpr = 0.16, F_non_con = 1.4, F_ind_com = 1.25
a.total_resident_population *  33.58 * 0.16 * 1.4 * 1.25 n_effluent
FROM raw_br_data a
INNER JOIN modelled.city_polygon b
ON REPLACE(LOWER(TRIM(b.city_name)), '-', ' ') = REPLACE(LOWER(TRIM(a.municipality_name)), '-', ' ')
AND a.UF = b.region_code
)
SELECT 	a.locode,
		a.geometry,
		a.total_resident_population,
		a.total_organic_waste,
		b.utilisation_fraction * b.emission_factor * (a.total_organic_waste - 0) - 0 as total_co2_emissions,
		-- default values emissionfactor_value = 0.005
		b.utilisation_fraction * n_effluent * 0.005 * (44/28) AS total_n20_emissions,
		b.income_group,
		b.treatment_type,
		CASE 
            WHEN treatment_type = 'treatment-name-septic-system' THEN 'treatment-status-type-wastewater-treated'
            WHEN treatment_type = 'treatment-name-latrine' THEN 'treatment-status-type-wastewater-treated'
            WHEN treatment_type = 'treatment-name-other' THEN 'treatment-status-type-wastewater-treated'
            WHEN treatment_type = 'treatment-name-none' THEN 'treatment-status-type-wastewater-untreated'
            WHEN treatment_type = 'treatment-name-sewer' THEN 'treatment-status-type-wastewater-untreated'
            ELSE NULL
        END AS treatment_status,
        CASE 
            WHEN treatment_type = 'treatment-name-septic-system' THEN 'collection-status-type-wastewater-collected'
            WHEN treatment_type = 'treatment-name-latrine' THEN 'collection-status-type-wastewater-collected'
            WHEN treatment_type = 'treatment-name-other' THEN 'collection-status-type-wastewater-collected'
            WHEN treatment_type = 'treatment-name-none' THEN 'collection-status-type-wastewater-not-collected'
            WHEN treatment_type = 'treatment-name-sewer' THEN 'collection-status-type-wastewater-collected'
            ELSE NULL
        END AS collection_status
FROM br_locode_data a 
CROSS JOIN income_factor b
;