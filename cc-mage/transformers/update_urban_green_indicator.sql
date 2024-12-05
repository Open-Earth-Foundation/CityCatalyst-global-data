WITH raw_biodiversity_index AS (
    SELECT 
        cod_municipio municipailty_id,
        TRIM(SPLIT_PART(b.municipality, '(', 1)) AS city_name, 
        b._state AS region_code,  
        'forest and non-forest natural cover' as indicator_name,
        urban_green_areas__::numeric + vegetetation_supression__::numeric as indicator_score,
        'percent' as indicator_units,
        2022 as indicator_year, 
        'current' as scenario_name,
        'MapBiomass' as datasource
    FROM raw_data.ccra_icare_urban_green_areas a
    LEFT JOIN raw_data.ccra_ips_indicator b 
    ON a.cod_municipio = b.municipality_code
),
upsert_data AS (
    SELECT 
        (MD5(CONCAT_WS('-', b.locode, indicator_name, a.datasource, a.indicator_year, a.scenario_name))::UUID) AS id,
        b.locode AS actor_id, 
        a.city_name,
        a.region_code,
        indicator_name,
        indicator_score,
        a.indicator_units,
        0.01 + indicator_score * (0.99 - 0.01) AS indicator_normalized_score,
        indicator_year,
        scenario_name,
        datasource    
    FROM 
        raw_biodiversity_index a
    INNER JOIN 
        modelled.city_polygon b ON REPLACE(LOWER(TRIM(a.city_name)), '-', ' ') = REPLACE(LOWER(TRIM(b.city_name)), '-', ' ')
        AND a.region_code = b.region_code
        AND b.country_code = 'BR'
)
INSERT INTO modelled.ccra_indicator (
    id,
    actor_id,
    indicator_name,
    indicator_score,
    indicator_units,
    indicator_normalized_score,
    indicator_year,
    scenario_name,
    datasource
)
SELECT 
    id,
    actor_id,
    indicator_name,
    indicator_score,
    indicator_units,
    indicator_normalized_score,
    indicator_year,
    scenario_name,
    datasource
FROM upsert_data
ON CONFLICT (id) 
DO UPDATE SET
    indicator_score = EXCLUDED.indicator_score,
    indicator_units = EXCLUDED.indicator_units,
    indicator_normalized_score = EXCLUDED.indicator_normalized_score;

