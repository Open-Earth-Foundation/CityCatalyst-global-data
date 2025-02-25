WITH raw_index AS (
    SELECT  
        locode,
        'coverage rate of public urban drainage' as indicator_name,
        IN021 as indicator_score,
        null as indicator_units,
        2023 as indicator_year, 
        'current' as scenario_name,
        'SNIS' as datasource
    FROM raw_data.ccra_icare_urban_drainage a
    LEFT JOIN raw_data.icare_city_to_locode b 
    ON a.CD_MUN = b.municipality_code
    WHERE locode IS NOT NULL 
),
percentiles AS (
    SELECT
        indicator_name, 
        scenario_name,
        PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY indicator_score) AS lower_limit,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY indicator_score) AS upper_limit
    FROM 
        raw_index
    GROUP BY 
        indicator_name, 
        scenario_name
),
index_scaled AS (
    SELECT 
        i.locode,
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
        raw_index i
    JOIN 
        percentiles p ON i.indicator_name = p.indicator_name AND i.scenario_name = p.scenario_name
),
upsert_data AS (
    SELECT 
        (MD5(CONCAT_WS('-', a.locode, indicator_name, a.datasource, a.indicator_year, a.scenario_name))::UUID) AS id,
        a.locode AS actor_id, 
        indicator_name,
        indicator_score,
        a.indicator_units,
        0.01 + (adjusted_indicator_score - lower_limit) * (0.99 - 0.01) / NULLIF(upper_limit - lower_limit, 0) AS indicator_normalized_score,
        indicator_year,
        scenario_name,
        datasource    
    FROM 
        index_scaled a
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
