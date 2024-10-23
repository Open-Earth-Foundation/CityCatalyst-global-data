WITH impact_assessment AS (
    SELECT unnest(ARRAY['water resources', 'food security', 'public health', 'energy security', 'biodiversity', 'port infrastructure','rail infrastructure', 'road infrastructure']) as key_impact,
           ARRAY['flooding','landslide','rain', 'drought', 'fire', 'sea level rise', 'heat wave'] as hazard,
           ARRAY[2024,2030,2050] as latest_year
),
year_assessment AS (
    SELECT trim(key_impact) as key_impact,
           hazard,
           unnest(latest_year) as latest_year
    FROM impact_assessment
),
hazard_assessment AS (
    SELECT key_impact,
           trim(unnest(hazard)) as hazard,
           latest_year,
           CASE 
               WHEN latest_year > 2024 THEN array['pesimistic','optimistic']
               ELSE array['current'] 
           END AS scenario_name
    FROM year_assessment
),
scenario_assessment as (
SELECT 
    (MD5(CONCAT_WS('-', key_impact, hazard, latest_year))::UUID) as id,
    key_impact as keyimpact_name,
    hazard as hazard_name,
    latest_year,
    unnest(scenario_name) as scenario_name
FROM hazard_assessment
)
INSERT INTO modelled.ccra_impactchain (
    id, 
    keyimpact_name,
    hazard_name,
    latest_year,
    scenario_name
)
SELECT 
    (MD5(CONCAT_WS('-', keyimpact_name, hazard_name, latest_year,scenario_name))::UUID) as id,
    keyimpact_name,
    hazard_name,
    latest_year,
    scenario_name
FROM scenario_assessment
ON CONFLICT (id) 
DO UPDATE SET 
    keyimpact_name = EXCLUDED.keyimpact_name,
    hazard_name = EXCLUDED.hazard_name,
    latest_year = EXCLUDED.latest_year,
    scenario_name = EXCLUDED.scenario_name;
