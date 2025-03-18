WITH raw_indicator AS (
    SELECT 
        cod_municipio municipailty_id,
        TRIM(SPLIT_PART(b.municipality, '(', 1)) AS city_name,
        b.locode, 
        b.region_code AS region_code,  
        'deforested area' as indicator_name,
        deforested_area__::numeric as indicator_score,
        'percent' as indicator_units,
        2022 as indicator_year, 
        'current' as scenario_name,
        'IPS' as datasource
    FROM raw_data.ccra_icare_deforested_area a
    LEFT JOIN raw_data.icare_city_to_locode b 
    ON a.cod_municipio = b.municipality_code
    WHERE locode IS NOT NULL 
),
upsert_data AS (
    SELECT 
        (MD5(CONCAT_WS('-', locode, indicator_name, a.datasource, a.indicator_year, a.scenario_name))::UUID) AS id,
        locode AS actor_id, 
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
        raw_indicator a
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
    indicator_normalized_score = EXCLUDED.indicator_normalized_score,
    scenario_name = EXCLUDED.scenario_name,
    datasource = EXCLUDED.datasource

