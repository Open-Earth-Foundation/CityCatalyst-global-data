WITH indicator_clean AS (
    SELECT DISTINCT
        TRIM(SPLIT_PART(_location, '-', 1)) AS city_name,
        TRIM(SPLIT_PART(_location, '-', 2)) AS region_code,
        indicator_name,
        variable_value::numeric AS indicator_score,
        units AS indicator_units,
--        CASE WHEN lower(units) = 'percentual' THEN variable_value::numeric / 100 
--        ELSE value_scaled END AS indicator_normalized_score,       
        REPLACE(series_year, 'serie.', '')::int AS indicator_year,
        'current' AS scenario_name,
        'IBGE' AS datasource
    FROM raw_data.ccra_ibge_indicator a
    WHERE NOT (variable_value IS NULL OR variable_value = '-' OR variable_value = '...')
),
percentiles AS (
    SELECT
        indicator_name, 
        scenario_name,
        PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY indicator_score) AS lower_limit,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY indicator_score) AS upper_limit
    FROM indicator_clean
    GROUP BY indicator_name, scenario_name
),
indicator_scaled AS (
    SELECT 
        i.city_name, 
        i.region_code, 
        i.indicator_name, 
        i.indicator_score, 
        indicator_year, 
        i.scenario_name, 
        i.indicator_units,
        datasource,
        CASE
            WHEN i.indicator_score < p.lower_limit THEN p.lower_limit
            WHEN i.indicator_score > p.upper_limit THEN p.upper_limit
            ELSE i.indicator_score
        END AS adjusted_indicator_score,
        p.lower_limit, 
        p.upper_limit
    FROM indicator_clean i
    JOIN percentiles p ON i.indicator_name = p.indicator_name AND i.scenario_name = p.scenario_name
    WHERE indicator_score IS NOT NULL 
),
upsert_data AS (
SELECT 
	(MD5(CONCAT_WS('-', b.locode, indicator_name, a.datasource, a.indicator_year, a.scenario_name))::UUID) AS id,
	b.locode as actor_id, 
    a.city_name,
    a.region_code,
    indicator_name,
    indicator_score,
    indicator_units,
    CASE WHEN lower(indicator_units) = 'percentual' THEN 0.01 + (indicator_score::numeric / 100) * (0.99 - 0.01)  
    ELSE  0.01 + (adjusted_indicator_score - lower_limit) * (0.99 - 0.01) / NULLIF(upper_limit - lower_limit, 0) end AS indicator_normalized_score,
    indicator_year,
    scenario_name,
    datasource    
FROM indicator_scaled a
INNER JOIN modelled.city_polygon b 
ON REPLACE(LOWER(TRIM(a.city_name)), '-', ' ') = REPLACE(LOWER(TRIM(b.city_name)), '-', ' ')
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
