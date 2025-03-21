WITH impact_assessment AS (
SELECT 	hazard,
		keyimpact,
		ARRAY[2024,2030,2050] as latest_year
FROM (
    VALUES 
    ('droughts', ARRAY['Water Resources', 'Food Security', 'Energy Security', 'Biodiversity']),
    ('heatwaves', ARRAY['Public Health', 'Infrastructure', 'Biodiversity', 'Energy Security']),
    ('diseases', ARRAY['Public Health']),
    ('landslides', ARRAY['Infrastructure', 'Public Health']),
    ('floods', ARRAY['Infrastructure', 'Food Security', 'Public Health']),
    ('wildfires', ARRAY['Infrastructure', 'Biodiversity', 'Public Health']),
    ('sea-level-rise', ARRAY['Infrastructure'])
) AS t(hazard, keyimpact)
),
year_assessment AS (
    SELECT keyimpact as key_impact,
           hazard,
           unnest(latest_year) as latest_year
    FROM impact_assessment
),
hazard_assessment AS (
    SELECT lower(trim(unnest(key_impact))) as key_impact,
    	   lower(hazard) as hazard,
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
