WITH actions_en AS (
    SELECT *
    FROM 'https://raw.githubusercontent.com/Open-Earth-Foundation/CityCatalyst-global-data/refs/heads/develop/cc-mage/datasets/climate_actions/climate_actions_en.json'
),
actions_es AS (
    SELECT *
    FROM 'https://raw.githubusercontent.com/Open-Earth-Foundation/CityCatalyst-global-data/refs/heads/develop/cc-mage/datasets/climate_actions/climate_actions_es.json'
),
actions_pt AS (
    SELECT *
    FROM 'https://raw.githubusercontent.com/Open-Earth-Foundation/CityCatalyst-global-data/refs/heads/develop/cc-mage/datasets/climate_actions/climate_actions_pt.json'
)
SELECT
    a.ActionID AS action_id,
    json_object('en', a.ActionName, 'es', b.ActionName, 'pt', c.ActionName) AS action_name,
    a.ActionType AS action_type,
    a.Hazard AS hazard_name,
    a.Sector AS sector_names,
    a.Subsector AS subsector_names,
    a.PrimaryPurpose AS primary_purpose,
    json_object('en', a.Description, 'es', b.Description, 'pt', c.Description) AS description,
    a.CoBenefits.air_quality AS cobenefits_airquality,
    a.CoBenefits.water_quality AS cobenefits_waterquality,
    a.CoBenefits.habitat AS cobenefits_habitat,
    a.CoBenefits.cost_of_living AS cobenefits_costofliving,
    a.CoBenefits.housing AS cobenefits_housing,
    a.CoBenefits.mobility AS cobenefits_mobility,
    a.CoBenefits.stakeholder_engagement AS cobenefits_stakeholderengagement,
    json_object('en', a.EquityAndInclusionConsiderations, 'es', b.EquityAndInclusionConsiderations, 'pt', c.EquityAndInclusionConsiderations) AS equity_and_inclusion_considerations,
    a.GHGReductionPotential.stationary_energy AS ghgreduction_stationary_energy,
    a.GHGReductionPotential.transportation AS ghgreduction_transportation,
    a.GHGReductionPotential.waste AS ghgreduction_waste,
    a.GHGReductionPotential.ippu AS ghgreduction_ippu,
    a.GHGReductionPotential.afolu AS ghgreduction_afolu,
    a.AdaptationEffectiveness AS adaptation_effectiveness,
    a.CostInvestmentNeeded AS cost_investment_needed,
    a.TimelineForImplementation AS timeline_for_implementation,
    json_object('en', a.Dependencies, 'es', b.Dependencies, 'pt', c.Dependencies) AS dependencies,
    json_object('en', a.KeyPerformanceIndicators, 'es', b.KeyPerformanceIndicators, 'pt', c.KeyPerformanceIndicators) AS key_performance_indicators,
    a.PowersAndMandates as powers_and_mandates,
    a.AdaptationEffectivenessPerHazard.droughts AS adaptation_effectiveness_droughts,
    a.AdaptationEffectivenessPerHazard.heatwaves AS adaptation_effectiveness_heatwaves,
    a.AdaptationEffectivenessPerHazard.floods AS adaptation_effectiveness_floods,
    a.AdaptationEffectivenessPerHazard."sea-level-rise" AS adaptation_effectiveness_sealevelrise,
    a.AdaptationEffectivenessPerHazard.landslides AS adaptation_effectiveness_landslides,
    a.AdaptationEffectivenessPerHazard.storms AS adaptation_effectiveness_storms,
    a.AdaptationEffectivenessPerHazard.wildfires AS adaptation_effectiveness_wildfires,
    a.AdaptationEffectivenessPerHazard.diseases AS adaptation_effectiveness_diseases,
    a.biome
FROM actions_en a
LEFT JOIN actions_es b ON a.ActionID = b.ActionID
LEFT JOIN actions_pt c ON a.ActionID = c.ActionID;