WITH indicator_clean AS (
SELECT  DISTINCT
        TRIM(SPLIT_PART("_name", '/', 1)) AS city_name,
        TRIM(SPLIT_PART("_name", '/', 2)) AS region_code,
        case when indicator_name = 'Dias consecutivos secos' then 'consecutive dry days'
        	when indicator_name = 'Índice de precipitação-evapotranspiração padronizado' then 'standardized precipitation evapotranspiration index'
        	end AS indicator_name,
        null::numeric AS indicator_score,
        null::numeric AS indicator_units,
        _value as indicator_normalized_score,
        _year AS indicator_year,
        CASE 
        WHEN scenario_id IS NULL THEN 'current'
        WHEN scenario_id = 1 THEN 'optimistic'
        WHEN scenario_id = 2 THEN 'pesimistic'
        ELSE NULL 
    	END AS scenario_name,
        'Adapta' AS datasource
FROM 	raw_data.ccra_adapta_indicator
),
upsert_data AS (
    SELECT 
        (MD5(CONCAT_WS('-', b.locode, indicator_name, a.datasource, a.indicator_year, a.scenario_name))::UUID) AS id,
        b.locode as actor_id, 
        a.city_name,
        indicator_name,
        a.indicator_score,
        a.indicator_units,
        a.indicator_normalized_score,
        a.indicator_year,
        a.scenario_name,
        a.datasource
    FROM 
        indicator_clean a 
    INNER JOIN 
        modelled.city_polygon b 
    ON 
        REPLACE(LOWER(TRIM(a.city_name)), '-', ' ') = REPLACE(LOWER(TRIM(b.city_name)), '-', ' ')
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
    indicator_normalized_score = EXCLUDED.indicator_normalized_score
