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
),
upsert AS (
SELECT 
    (MD5(CONCAT_WS('-', keyimpact_name, hazard_name, indicator_year, scenario_name))::UUID) AS impact_id,
    locode AS actor_id,
    city_name,
    region AS region_code,
    MAX(CASE WHEN category = 'risk' THEN indicator_value END) AS risk_score,
    MAX(CASE WHEN category = 'hazard' THEN indicator_value END) * 
    MAX(CASE WHEN category = 'exposure' THEN indicator_value END) *
    MAX(CASE WHEN category = 'vulnerability' THEN indicator_value END) AS risk_score_calc,
    MAX(CASE WHEN category = 'hazard' THEN indicator_value END) AS hazard_score,
    MAX(CASE WHEN category = 'exposure' THEN indicator_value END) AS exposure_score,
    MAX(CASE WHEN category = 'vulnerability' THEN indicator_value END) AS vulnerability_score,
    MAX(CASE WHEN category = 'sensitivity' THEN indicator_value END) AS sensitivity_score,
    MAX(CASE WHEN category = 'adaptive capacity' THEN indicator_value END) AS adaptive_capacity_score
FROM 
    adapta_indicators
GROUP BY 
    locode, city_name, region, keyimpact_name, hazard_name, indicator_year, scenario_name)
INSERT INTO modelled.ccra_riskassessment (
			  impact_id,
			  actor_id,
			  city_name,
			  region_code,
			  risk_score,
			  hazard_score,
			  exposure_score,
			  vulnerability_score,
			  adaptive_capacity_score,
		  sensitivity_score)	  
SELECT    	impact_id,
		  	actor_id,
		  	city_name,
		  	region_code,
		  	risk_score,
		  	hazard_score,
		  	exposure_score,
		  	vulnerability_score,
		  	adaptive_capacity_score,
		  	sensitivity_score
FROM 		upsert
ON CONFLICT (impact_id, actor_id) 
DO UPDATE SET
		city_name = EXCLUDED.city_name,
		region_code = EXCLUDED.region_code,
		risk_score = EXCLUDED.risk_score,
		hazard_score = EXCLUDED.hazard_score,
		exposure_score = EXCLUDED.exposure_score,
		vulnerability_score = EXCLUDED.vulnerability_score,
		adaptive_capacity_score = EXCLUDED.adaptive_capacity_score