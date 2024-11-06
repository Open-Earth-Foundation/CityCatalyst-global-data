WITH indicator_clean AS (
    SELECT 
        TRIM(SPLIT_PART(_location, '-', 1)) AS city_name,
        TRIM(SPLIT_PART(_location, '-', 2)) AS region_code,
        indicator_name,
        variable_value::numeric AS indicator_score,
        units AS indicator_units,
        CASE WHEN lower(units) = 'percentual' THEN variable_value::numeric / 100 
        ELSE value_scaled END AS indicator_normalized_score,       
        REPLACE(series_year, 'serie.', '')::int AS indicator_year,
        'current' AS scenario_name,
        'IBGE' AS datasource
    FROM raw_data.ccra_ibge_indicator a
    WHERE variable_value IS NOT NULL 
),
upsert_data AS (
    SELECT
        (MD5(CONCAT_WS('-', b.locode, indicator_name, a.datasource, a.indicator_year, a.scenario_name))::UUID) AS id, 
        b.locode as actor_id, 
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
    indicator_normalized_score = EXCLUDED.indicator_normalized_score;
