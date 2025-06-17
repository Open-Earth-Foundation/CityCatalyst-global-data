DROP TABLE IF EXISTS raw_data.br_wastewater_scope_allocation;

CREATE TABLE raw_data.br_wastewater_scope_allocation as
WITH raw_br_data AS (
SELECT DISTINCT municipal_code, municipality_name, uf, total_resident_population 
FROM raw_data.snis_br_wastewater
),
br_locode_data AS (
SELECT b.locode, b.geometry, a.total_resident_population
FROM raw_br_data a
INNER JOIN modelled.city_polygon b
ON REPLACE(LOWER(TRIM(b.city_name)), '-', ' ') = REPLACE(LOWER(TRIM(a.municipality_name)), '-', ' ')
AND a.UF = b.region_code
),
ct_sites AS (
SELECT MAX(b.activity) AS activity, MAX(b.activity_units) AS activity_units, ST_SetSRID(ST_Point(b.lon, b.lat), 4326) as wastewater_treatment_site
FROM raw_data.ct_wastewater b
WHERE date_part('YEAR', start_time::date) = 2022
GROUP BY  ST_SetSRID(ST_Point(b.lon, b.lat), 4326)
),
ct_scope_input as (
SELECT a.locode, MAX(a.total_resident_population) as total_resident_population, SUM(b.activity) as population_served 
FROM br_locode_data a 
LEFT JOIN ct_sites b
ON ST_Intersects(a.geometry, b.wastewater_treatment_site)
GROUP BY a.locode
)
SELECT 	locode, 
		least((coalesce(population_served,0)/total_resident_population), 1) as scope_ratio
FROM ct_scope_input
;