WITH raw_datasus AS (
    SELECT 
        co_mun AS municipailty_id, 
        no_mun AS muncipailty_name, 
        ano AS indicator_year, 
        variavel AS indicator_units, 
        SUM(valor) AS count_cases,
        RANK() OVER (PARTITION BY co_mun ORDER BY ano DESC) AS rnk
    FROM raw_data.ccra_datosgov_indicator
    GROUP BY co_mun, no_mun, ano, variavel
),
raw_datasus_latest AS (
    SELECT 
        municipailty_id, 
        TRIM(SPLIT_PART(b.municipality, '(', 1)) AS city_name, 
        b._state AS region_code, 
        'health establishments' AS indicator_name, 
        count_cases AS indicator_score, 
        indicator_year,
        a.indicator_units,		
        'current' AS scenario_name,
        'DatosGov' AS datasource
    FROM 
        raw_datasus a 
    LEFT JOIN 
        raw_data.ccra_ips_indicator b ON a.municipailty_id = b.municipality_code
    WHERE 
        rnk = 1
),
percentiles AS (
    SELECT
        indicator_name, 
        scenario_name,
        PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY indicator_score) AS lower_limit,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY indicator_score) AS upper_limit
    FROM 
        raw_datasus_latest
    GROUP BY 
        indicator_name, 
        scenario_name
),
ipc_scaled AS (
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
    FROM 
        raw_datasus_latest i
    JOIN 
        percentiles p ON i.indicator_name = p.indicator_name AND i.scenario_name = p.scenario_name
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
        0.01 + (adjusted_indicator_score - lower_limit) * (0.99 - 0.01) / NULLIF(upper_limit - lower_limit, 0) AS indicator_normalized_score,
        indicator_year,
        scenario_name,
        datasource    
    FROM 
        ipc_scaled a
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