WITH raw_biodiversity_index AS (
    SELECT 
        cd_mun municipailty_id,
        b.locode,
        -- nm_mun AS city_name, 
        -- uf AS region_code, 
        'biodiversity intactness index' as indicator_name,
        biodiversity_intactness_index__bii_::numeric as indicator_score,
        'Index' as indicator_units,
        2024 as indicator_year, 
        'current' as scenario_name,
        'EarthEngine' as datasource
    FROM raw_data.ccra_icare_biodiversity_index a 
    LEFT JOIN raw_data.icare_city_to_locode b 
    ON a.cd_mun = b.municipality_code
    WHERE locode IS NOT NULL
    AND cd_mun != 4300002
),
upsert_data AS (
    SELECT 
        (MD5(CONCAT_WS('-', a.locode, indicator_name, a.datasource, a.indicator_year, a.scenario_name))::UUID) AS id,
        a.locode AS actor_id, 
        -- a.city_name,
        -- a.region_code,
        indicator_name,
        indicator_score,
        a.indicator_units,
        0.01 + indicator_score * (0.99 - 0.01)  AS indicator_normalized_score,
        indicator_year,
        scenario_name,
        datasource    
    FROM 
        raw_biodiversity_index a
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
