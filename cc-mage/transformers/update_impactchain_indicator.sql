WITH raw_impact_indicator AS (
SELECT  
        a.keyimpact_name,
        a.hazard_name,
        b.id as indicator_id,
        b.actor_id,
        a.component as category,
        null as subcategory,
        a.indicator_name,
        indicator_normalized_score as indicator_score,
        a.relationship,
        CASE WHEN b.indicator_year <=2024 THEN 2024 
        ELSE b.indicator_year END AS latest_year,
        b.scenario_name,
        b.datasource
FROM raw_data.keyimpact_hazard_indictor as a
LEFT JOIN  modelled.ccra_indicator b 
ON a.indicator_name = b.indicator_name AND a.datasource = b.datasource
),
upsert_data AS (
SELECT (MD5(CONCAT_WS('-', keyimpact_name, hazard_name, latest_year, scenario_name))::UUID) as impact_id,
        indicator_id,
        actor_id,
        category,
        coalesce(subcategory, 'none') as subcategory,
        indicator_name,
        indicator_score,
        1.0 / COUNT(*) OVER (PARTITION BY actor_id, keyimpact_name, hazard_name, latest_year, scenario_name, category) AS indicator_weight,
        relationship,
        datasource
FROM raw_impact_indicator
)
INSERT INTO modelled.ccra_impactchain_indicator (
  impact_id, indicator_id, actor_id, category, subcategory, indicator_name, indicator_score, indicator_weight, relationship, datasource
)
SELECT * 
FROM upsert_data
WHERE actor_id IS NOT NULL
ON CONFLICT (impact_id, indicator_id, category, subcategory)
DO UPDATE SET
  indicator_score = excluded.indicator_score,
  indicator_weight = excluded.indicator_weight,
  relationship = excluded.relationship,
  datasource = excluded.datasource;