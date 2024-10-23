WITH adapta_indicators AS (
    SELECT b.locode AS actor_id, 
           a.city_name,
           a.region,
           LOWER(a.key_impact_name) AS keyimpact_name,
           LOWER(a.hazard_name) AS hazard_name,
           LOWER(a.hazard_name) || ' ' || REPLACE(a.indicator_level_name, ' score', '') AS indicator_name,
           a.scenario_name,
           REPLACE(a.indicator_level_name, ' score', '') AS category,
           a.indicator_value,
           CASE 
               WHEN a.indicator_year::int <= 2024 THEN 2024
               ELSE a.indicator_year::int 
           END AS indicator_year
    FROM modelled.ccra_indicator_staging a 
    LEFT JOIN modelled.city_polygon b 
    ON REPLACE(LOWER(TRIM(a.city_name)), '-', ' ') = (
       CASE 
           WHEN LOWER(TRIM(b.city_name)) = 'amparo do são francisco' THEN 'amparo de são francisco'
           WHEN LOWER(TRIM(b.city_name)) = 'atílio vivácqua' THEN 'atílio vivacqua'
           ELSE REPLACE(LOWER(TRIM(b.city_name)), '-', ' ') 
       END)
       AND a.region = b.region_code 
       AND b.country_code = 'BR'
    WHERE a.hazard_name NOT IN ('Availability', 'Access', 'Malaria', 'American Cutaneous Leishmaniasis', 'Visceral Leishmaniasis')
)
INSERT INTO modelled.ccra_impactchain_indicator (
    actor_id,
    impact_id,
    indicator_id,
    category,
    subcategory,
    indicator_score,
    indicator_weight,
    datasource
)
SELECT 
    actor_id AS actor_id,
    (MD5(CONCAT_WS('-', keyimpact_name, hazard_name, indicator_year, scenario_name))::UUID) AS impact_id,
    (MD5(CONCAT_WS('-', indicator_name))::UUID) AS indicator_id,
    CASE 
        WHEN category IN ('adaptive capacity', 'sensitivity') THEN 'vulnerability'
        ELSE category 
    END AS category,
    CASE 
        WHEN category IN ('adaptive capacity', 'sensitivity') THEN category
        ELSE NULL 
    END AS subcategory,
    indicator_value AS indicator_score,
    1 AS indicator_weight,
    'Adapta' AS datasource
FROM 
    adapta_indicators
WHERE 
    category != 'risk'
ON CONFLICT (actor_id, impact_id, category, subcategory, indicator_id) 
DO UPDATE SET 
    indicator_score = EXCLUDED.indicator_score,
    indicator_weight = EXCLUDED.indicator_weight,
    datasource = EXCLUDED.datasource;
