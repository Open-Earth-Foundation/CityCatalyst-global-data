WITH ad AS (
    SELECT DISTINCT
        e.datasource_name_x, 
        e.actor_id,
        e.city_id,
        e.gpc_reference_number,
        e.emissions_value,
        e.emissions_year, 
        e.emissions_units, 
        e.gas_name, 
        e.activity_id,
        e.activity_value, 
        e.geometry_type,
        e.geometry, 
        e.geometry_id, 
        e.spatial_granularity,
        e.emissionfactor_value,
        e.unit_denominator,
        c.gpcmethod_id  
    FROM modelled.scope3_staging_epe e
    LEFT JOIN 
        modelled.gpc_methodology c 
        ON e.gpc_reference_number = c.gpc_reference_number
),
ad_with_emissionfactor_id AS (
    SELECT DISTINCT
        *,
        (MD5(CONCAT_WS('-', gas_name, emissionfactor_value, unit_denominator, activity_id::TEXT, 'World Bank', actor_id))::UUID) AS emissionfactor_id
    FROM ad
)
INSERT INTO modelled.emissions 
    (emissions_id, datasource_name, gpc_reference_number, actor_id, city_id,
     gpcmethod_id, activity_id, activity_value, 
     gas_name, emissions_value, emissions_units, emissions_year, emissionfactor_id, 
     spatial_granularity, geometry_type, geometry)
SELECT DISTINCT ON (emissions_id)
    (MD5(CONCAT_WS('-', datasource_name_x, gpc_reference_number, actor_id, activity_value, emissions_year, gas_name, emissionfactor_id::TEXT))::UUID) AS emissions_id,
    datasource_name_x AS datasource_name,
    gpc_reference_number,
    actor_id,
    city_id,
    gpcmethod_id::UUID,  
    activity_id::UUID,
    activity_value,
    gas_name,
    emissions_value,
    emissions_units,
    emissions_year::numeric AS emissions_year,
    emissionfactor_id,
    'city' AS spatial_granularity,
    geometry_type,
    geometry
FROM 
    ad_with_emissionfactor_id
WHERE 
    emissions_value > 0
AND actor_id IS NOT NULL
ON CONFLICT ON CONSTRAINT emissions_pkey
DO UPDATE SET 
    datasource_name = EXCLUDED.datasource_name,
    gpc_reference_number = EXCLUDED.gpc_reference_number,
    actor_id = EXCLUDED.actor_id,
    city_id = EXCLUDED.city_id,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_id = EXCLUDED.activity_id,
    activity_value = EXCLUDED.activity_value,
    gas_name = EXCLUDED.gas_name,
    emissions_value = EXCLUDED.emissions_value,
    emissions_units = EXCLUDED.emissions_units,
    emissions_year = EXCLUDED.emissions_year,
    emissionfactor_id = EXCLUDED.emissionfactor_id,
    spatial_granularity = EXCLUDED.spatial_granularity,
    geometry_type = EXCLUDED.geometry_type,
    geometry = EXCLUDED.geometry;
