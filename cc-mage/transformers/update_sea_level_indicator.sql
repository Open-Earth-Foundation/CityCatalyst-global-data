WITH raw_sealevel AS (
    SELECT 
        municipailty_id,
        b.locode,
        -- TRIM(SPLIT_PART(b.municipality, '(', 1)) AS city_name, 
        -- b._state AS region_code, 
        indicator_name,
        variable_value as indicator_score,
        null as indicator_units,
        indicator_year, 
        scenario as scenario_name,
        'SeaLevelRiseProjection' as datasource
    FROM raw_data.ccra_icare_sea_level a
    LEFT JOIN raw_data.icare_city_to_locode b 
    ON a.municipailty_id = b.municipality_code
    WHERE locode IS NOT NULL
),
percentiles AS (
    SELECT
        indicator_name, 
        scenario_name,
        PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY indicator_score) AS lower_limit,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY indicator_score) AS upper_limit
    FROM 
        raw_sealevel
    GROUP BY 
        indicator_name, 
        scenario_name
),
sealevel_scaled AS (
    SELECT 
        i.locode, 
        -- i.region_code, 
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
    FROM 
        raw_sealevel i
    JOIN 
        percentiles p ON i.indicator_name = p.indicator_name AND i.scenario_name = p.scenario_name
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
        0.01 + (adjusted_indicator_score - lower_limit) * (0.99 - 0.01) / NULLIF(upper_limit - lower_limit, 0) AS indicator_normalized_score,
        indicator_year,
        scenario_name,
        datasource    
    FROM 
        sealevel_scaled a
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

DROP TABLE raw_data.ccra_icare_sea_level;