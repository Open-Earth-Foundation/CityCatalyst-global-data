TRUNCATE TABLE modelled.cap_climate_action;

WITH raw_data AS (
    SELECT 
        action_id,
        action_name::json AS action_name,
        ARRAY(SELECT jsonb_array_elements_text(action_type)) AS action_type,
        ARRAY(SELECT jsonb_array_elements_text(hazard_name)) AS hazard_name,
        ARRAY(SELECT jsonb_array_elements_text(sector_names)) AS sector_names,
        ARRAY(SELECT jsonb_array_elements_text(subsector_names)) AS subsector_names,
        ARRAY(SELECT jsonb_array_elements_text(primary_purpose)) AS primary_purpose,
        CASE WHEN description IS NULL OR description = '' THEN NULL ELSE description::json END AS description,
        cobenefits_airquality::integer AS cobenefits_airquality,
        cobenefits_waterquality::integer AS cobenefits_waterquality,
        cobenefits_habitat::integer AS cobenefits_habitat,
        cobenefits_costofliving::integer AS cobenefits_costofliving,
        cobenefits_housing::integer AS cobenefits_housing,
        cobenefits_mobility::integer AS cobenefits_mobility,
        cobenefits_stakeholderengagement::integer AS cobenefits_stakeholderengagement,
        CASE WHEN equity_and_inclusion_considerations IS NULL OR equity_and_inclusion_considerations = '' THEN NULL ELSE equity_and_inclusion_considerations::json END AS equity_and_inclusion_considerations,
        TRIM(REPLACE(REPLACE(ghgreduction_stationary_energy, '"', ''), CHR(39), '')) AS ghgreduction_stationary_energy,
        TRIM(REPLACE(REPLACE(ghgreduction_transportation, '"', ''), CHR(39), '')) AS ghgreduction_transportation,
        TRIM(REPLACE(REPLACE(ghgreduction_waste, '"', ''), CHR(39), '')) AS ghgreduction_waste,
        TRIM(REPLACE(REPLACE(ghgreduction_ippu, '"', ''), CHR(39), '')) AS ghgreduction_ippu,
        TRIM(REPLACE(REPLACE(ghgreduction_afolu, '"', ''), CHR(39), '')) AS ghgreduction_afolu,
        LOWER(TRIM(REPLACE(REPLACE(adaptation_effectiveness, '"', ''), CHR(39), ''))) AS adaptation_effectiveness,
        LOWER(TRIM(REPLACE(REPLACE(cost_investment_needed, '"', ''), CHR(39), ''))) AS cost_investment_needed,
        TRIM(REPLACE(REPLACE(timeline_for_implementation, '"', ''), CHR(39), '')) AS timeline_for_implementation,
        CASE WHEN dependencies IS NULL OR dependencies = '' THEN NULL ELSE dependencies::json END AS dependencies,
        CASE WHEN key_performance_indicators IS NULL OR key_performance_indicators = '' THEN NULL ELSE key_performance_indicators::json END AS key_performance_indicators,
        ARRAY(SELECT jsonb_array_elements_text(powers_and_mandates)) AS powers_and_mandates,
        LOWER(TRIM(REPLACE(REPLACE(adaptation_effectiveness_droughts, '"', ''), CHR(39), ''))) AS adaptation_effectiveness_droughts,
        LOWER(TRIM(REPLACE(REPLACE(adaptation_effectiveness_heatwaves, '"', ''), CHR(39), ''))) AS adaptation_effectiveness_heatwaves,
        LOWER(TRIM(REPLACE(REPLACE(adaptation_effectiveness_floods, '"', ''), CHR(39), ''))) AS adaptation_effectiveness_floods,
        LOWER(TRIM(REPLACE(REPLACE(adaptation_effectiveness_sealevelrise, '"', ''), CHR(39), ''))) AS adaptation_effectiveness_sealevelrise,
        LOWER(TRIM(REPLACE(REPLACE(adaptation_effectiveness_landslides, '"', ''), CHR(39), ''))) AS adaptation_effectiveness_landslides,
        LOWER(TRIM(REPLACE(REPLACE(adaptation_effectiveness_storms, '"', ''), CHR(39), ''))) AS adaptation_effectiveness_storms,
        LOWER(TRIM(REPLACE(REPLACE(adaptation_effectiveness_wildfires, '"', ''), CHR(39), ''))) AS adaptation_effectiveness_wildfires,
        LOWER(TRIM(REPLACE(REPLACE(adaptation_effectiveness_diseases, '"', ''), CHR(39), ''))) AS adaptation_effectiveness_diseases,
        CASE WHEN biome IS NULL OR biome = '' OR biome = 'none' THEN NULL ELSE biome END AS biome
    FROM raw_data.cap_climate_action
)
INSERT INTO modelled.cap_climate_action (
    action_id,action_name,action_type,hazard_name,sector_names,subsector_names,primary_purpose,description,cobenefits_airquality,cobenefits_waterquality,cobenefits_habitat,cobenefits_costofliving,cobenefits_housing,cobenefits_mobility,cobenefits_stakeholderengagement,equity_and_inclusion_considerations,ghgreduction_stationary_energy,ghgreduction_transportation,ghgreduction_waste,ghgreduction_ippu,ghgreduction_afolu,adaptation_effectiveness,cost_investment_needed,timeline_for_implementation,dependencies,key_performance_indicators,powers_and_mandates,adaptation_effectiveness_droughts,adaptation_effectiveness_heatwaves,adaptation_effectiveness_floods,adaptation_effectiveness_sealevelrise,adaptation_effectiveness_landslides,adaptation_effectiveness_storms,adaptation_effectiveness_wildfires,adaptation_effectiveness_diseases,biome
)
SELECT * FROM raw_data
ON CONFLICT (action_id) DO UPDATE SET
    action_name=EXCLUDED.action_name,action_type=EXCLUDED.action_type,hazard_name=EXCLUDED.hazard_name,sector_names=EXCLUDED.sector_names,subsector_names=EXCLUDED.subsector_names,primary_purpose=EXCLUDED.primary_purpose,description=EXCLUDED.description,cobenefits_airquality=EXCLUDED.cobenefits_airquality,cobenefits_waterquality=EXCLUDED.cobenefits_waterquality,cobenefits_habitat=EXCLUDED.cobenefits_habitat,cobenefits_costofliving=EXCLUDED.cobenefits_costofliving,cobenefits_housing=EXCLUDED.cobenefits_housing,cobenefits_mobility=EXCLUDED.cobenefits_mobility,cobenefits_stakeholderengagement=EXCLUDED.cobenefits_stakeholderengagement,equity_and_inclusion_considerations=EXCLUDED.equity_and_inclusion_considerations,ghgreduction_stationary_energy=EXCLUDED.ghgreduction_stationary_energy,ghgreduction_transportation=EXCLUDED.ghgreduction_transportation,ghgreduction_waste=EXCLUDED.ghgreduction_waste,ghgreduction_ippu=EXCLUDED.ghgreduction_ippu,ghgreduction_afolu=EXCLUDED.ghgreduction_afolu,adaptation_effectiveness=EXCLUDED.adaptation_effectiveness,cost_investment_needed=EXCLUDED.cost_investment_needed,timeline_for_implementation=EXCLUDED.timeline_for_implementation,dependencies=EXCLUDED.dependencies,key_performance_indicators=EXCLUDED.key_performance_indicators,powers_and_mandates=EXCLUDED.powers_and_mandates,adaptation_effectiveness_droughts=EXCLUDED.adaptation_effectiveness_droughts,adaptation_effectiveness_heatwaves=EXCLUDED.adaptation_effectiveness_heatwaves,adaptation_effectiveness_floods=EXCLUDED.adaptation_effectiveness_floods,adaptation_effectiveness_sealevelrise=EXCLUDED.adaptation_effectiveness_sealevelrise,adaptation_effectiveness_landslides=EXCLUDED.adaptation_effectiveness_landslides,adaptation_effectiveness_storms=EXCLUDED.adaptation_effectiveness_storms,adaptation_effectiveness_wildfires=EXCLUDED.adaptation_effectiveness_wildfires,adaptation_effectiveness_diseases=EXCLUDED.adaptation_effectiveness_diseases,biome=EXCLUDED.biome;