WITH adapta_indicators AS (
    SELECT 
        b.locode, 
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
    FROM 
        modelled.ccra_indicator_staging a 
    LEFT JOIN 
        modelled.city_polygon b 
    ON 
        REPLACE(LOWER(TRIM(a.city_name)), '-', ' ') = 
        CASE 
            WHEN LOWER(TRIM(b.city_name)) = 'amparo do são francisco' THEN 'amparo de são francisco'
            WHEN LOWER(TRIM(b.city_name)) = 'atílio vivácqua' THEN 'atílio vivacqua' 
            ELSE REPLACE(LOWER(TRIM(b.city_name)), '-', ' ') 
        END
    AND 
        a.region = b.region_code 
    AND 
        country_code = 'BR'
    WHERE 
        hazard_name NOT IN ('Availability', 'Access', 'Malaria', 'American Cutaneous Leishmaniasis', 'Visceral Leishmaniasis')
    AND 
        LOWER(a.key_impact_name) NOT IN (SELECT lower(keyimpact_name) FROM {{ df_2 }})
),
raw_risk AS (
    SELECT 
        (MD5(CONCAT_WS('-', keyimpact_name, hazard_name, indicator_year, scenario_name))::UUID) AS impact_id,
        locode AS actor_id,
        city_name,
        region AS region_code,
        NULL AS risk_score,
        0.01 + MAX(CASE WHEN category = 'hazard' THEN indicator_value END) * (0.99 - 0.01)  AS hazard_score,
        0.01 + MAX(CASE WHEN category = 'exposure' THEN indicator_value END) * (0.99 - 0.01)  AS exposure_score,
        0.01 + MAX(CASE WHEN category = 'vulnerability' THEN indicator_value END) * (0.99 - 0.01)  AS vulnerability_score,
        0.01 + MAX(CASE WHEN category = 'adaptive capacity' THEN indicator_value END) * (0.99 - 0.01)  AS adaptive_capacity_score,
        0.01 + MAX(CASE WHEN category = 'sensitivity' THEN indicator_value END) * (0.99 - 0.01)  AS sensitivity_score
    FROM adapta_indicators
    GROUP BY locode, city_name, region, keyimpact_name, hazard_name, indicator_year, scenario_name
),
risk_scores AS (
    SELECT
        impact_id,
        actor_id,
        city_name,
        region_code,
        hazard_score * exposure_score * vulnerability_score AS risk_score,
        hazard_score,
        exposure_score,
        vulnerability_score,
        adaptive_capacity_score,
        sensitivity_score
    FROM raw_risk
),
percentiles AS (
    SELECT
        impact_id,
        PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY risk_score) AS lower_limit,
        PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY risk_score) AS upper_limit
    FROM risk_scores
    GROUP BY impact_id
),
risk_scaled AS (
    SELECT
        rs.impact_id,
        rs.actor_id,
        rs.city_name,
        rs.region_code,
        CASE
            WHEN rs.risk_score < p.lower_limit THEN p.lower_limit
            WHEN rs.risk_score > p.upper_limit THEN p.upper_limit
            ELSE rs.risk_score
        END AS adjusted_risk_score,
        p.lower_limit AS risk_lower_limit,
        p.upper_limit AS risk_upper_limit,
        hazard_score,
        exposure_score,
        vulnerability_score,
        adaptive_capacity_score,
        sensitivity_score
    FROM risk_scores rs
    JOIN percentiles p ON rs.impact_id = p.impact_id
    WHERE rs.actor_id IS NOT NULL
)
INSERT INTO modelled.ccra_riskassessment (
    impact_id,
    actor_id,
    risk_score,
    hazard_score,
    exposure_score,
    vulnerability_score,
    adaptive_capacity_score,
    sensitivity_score,
    risk_lower_limit,
    risk_upper_limit
)
SELECT 
    impact_id,
    actor_id,
    0.01 + ( adjusted_risk_score - risk_lower_limit) * (0.99 - 0.01) / NULLIF( risk_upper_limit - risk_lower_limit, 0) AS risk_score,
    hazard_score,
    exposure_score,
    vulnerability_score,
    adaptive_capacity_score,
    sensitivity_score,
    risk_lower_limit,
    risk_upper_limit
FROM risk_scaled
ON CONFLICT (impact_id, actor_id) 
DO UPDATE SET
    risk_score = EXCLUDED.risk_score,
    hazard_score = EXCLUDED.hazard_score,
    exposure_score = EXCLUDED.exposure_score,
    vulnerability_score = EXCLUDED.vulnerability_score,
    adaptive_capacity_score = EXCLUDED.adaptive_capacity_score,
    sensitivity_score = EXCLUDED.sensitivity_score,
    risk_lower_limit = EXCLUDED.risk_lower_limit,
    risk_upper_limit = EXCLUDED.risk_upper_limit;