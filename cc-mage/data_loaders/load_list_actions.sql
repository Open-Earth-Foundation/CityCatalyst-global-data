WITH actions_en AS (
    SELECT 
        *,
        replace(cobenefits, CHR(39), '"')::json as cobenefits_json,
        replace(GHGReductionPotential, CHR(39), '"')::json as ghg_reduction_json,
        replace(AdaptationEffectivenessPerHazard, CHR(39), '"')::json as adaptation_effectiveness_json
    FROM {{df_1}}
),
actions_es AS (
    SELECT 
        *
    FROM {{df_3}}
),
actions_pt AS (
    SELECT 
        *
    FROM {{df_2}}
)
select replace(GHGReductionPotential, CHR(39), '"')
from actions_en a
-- SELECT
--     a.ActionID AS action_id,
--     json_object('en', a.ActionName, 'es', b.ActionName, 'pt', c.ActionName) AS action_name,
--     a.ActionType AS action_type,
--     a.Hazard AS hazard_name,
--     a.Sector AS sector_names,
--     a.Subsector AS subsector_names,
--     a.PrimaryPurpose AS primary_purpose,
--     json_object('en', a.Description, 'es', b.Description, 'pt', c.Description) AS description,
--     a.cobenefits_json.air_quality AS cobenefits_airquality,
--     a.cobenefits_json.water_quality AS cobenefits_waterquality,
--     a.cobenefits_json.habitat AS cobenefits_habitat,
--     a.cobenefits_json.cost_of_living AS cobenefits_costofliving,
--     a.cobenefits_json.housing AS cobenefits_housing,
--     a.cobenefits_json.mobility AS cobenefits_mobility,
--     a.cobenefits_json.stakeholder_engagement AS cobenefits_stakeholderengagement,
--     json_object('en', a.EquityAndInclusionConsiderations, 'es', b.EquityAndInclusionConsiderations, 'pt', c.EquityAndInclusionConsiderations) AS equity_and_inclusion_considerations,
--     a.GHGReductionPotential.stationary_energy AS ghgreduction_stationary_energy,
--     a.GHGReductionPotential.transportation AS ghgreduction_transportation,
--     a.GHGReductionPotential.waste AS ghgreduction_waste,
--     a.GHGReductionPotential.ippu AS ghgreduction_ippu,
--     a.GHGReductionPotential.afolu AS ghgreduction_afolu,
--     a.AdaptationEffectiveness AS adaptation_effectiveness,
--     a.CostInvestmentNeeded AS cost_investment_needed,
--     a.TimelineForImplementation AS timeline_for_implementation,
--     json_object('en', a.Dependencies, 'es', b.Dependencies, 'pt', c.Dependencies) AS dependencies,
--     json_object('en', a.KeyPerformanceIndicators, 'es', b.KeyPerformanceIndicators, 'pt', c.KeyPerformanceIndicators) AS key_performance_indicators,
--     a.PowersAndMandates as powers_and_mandates,
--     a.AdaptationEffectivenessPerHazard.droughts AS adaptation_effectiveness_droughts,
--     a.AdaptationEffectivenessPerHazard.heatwaves AS adaptation_effectiveness_heatwaves,
--     a.AdaptationEffectivenessPerHazard.floods AS adaptation_effectiveness_floods,
--     a.AdaptationEffectivenessPerHazard."sea-level-rise" AS adaptation_effectiveness_sealevelrise,
--     a.AdaptationEffectivenessPerHazard.landslides AS adaptation_effectiveness_landslides,
--     a.AdaptationEffectivenessPerHazard.storms AS adaptation_effectiveness_storms,
--     a.AdaptationEffectivenessPerHazard.wildfires AS adaptation_effectiveness_wildfires,
--     a.AdaptationEffectivenessPerHazard.diseases AS adaptation_effectiveness_diseases,
--     a.biome
-- FROM actions_en a
-- LEFT JOIN actions_es b ON a.ActionID = b.ActionID
-- LEFT JOIN actions_pt c ON a.ActionID = c.ActionID;