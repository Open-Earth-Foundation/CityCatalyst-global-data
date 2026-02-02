WITH emissions_data AS (
    SELECT DISTINCT
        city_id,
        locode AS actor_id,
        total_waste,
        emissions_value,
        gas_name,
        emissions_units,
        gpc_reference_number,
        activity_name,
        activity_units,
        methodology_name  
    FROM raw_data.mc_eurostats_staging
    WHERE emissions_value IS NOT NULL
)

INSERT INTO modelled.emissions (
    emissions_id,
    datasource_name, 
    gpc_reference_number, 
    actor_id,
    city_id, 
    emissions_year,
    emissions_value,
    emissions_units,
    gpcmethod_id,
    gas_name,
    emissionfactor_id,
    activity_id,
    activity_value,
    spatial_granularity,
    geometry_type,
    geometry,
    geometry_id
)

SELECT DISTINCT
    -- ✅ emissions_id using all required components (excluding EF and geometry)
    MD5(CONCAT_WS(
        '-', 
        'EuroStat',
        gpc_reference_number,
        actor_id,
        '2023',
        MD5(CONCAT_WS(
            '-',
            methodology_name,
            gpc_reference_number
        ))::TEXT,
        gas_name,
        MD5(CONCAT_WS(
            '-',
            activity_name,
            activity_units,
            jsonb_build_object(
                'methane-commitment-solid-waste-inboundary-oxidation-factor', 'oxidation-factor-well-managed-landfill'
            )::TEXT,
            MD5(CONCAT_WS(
                '-',
                methodology_name,
                gpc_reference_number
            ))::TEXT
        ))::TEXT
    ))::UUID AS emissions_id,

    'EuroStat' AS datasource_name,
    gpc_reference_number,
    actor_id,
    city_id,
    2023 AS emissions_year,
    emissions_value,
    emissions_units,
    MD5(CONCAT_WS(
        '-',
        methodology_name,
        gpc_reference_number
    ))::UUID AS gpcmethod_id,
    gas_name,
    NULL::UUID AS emissionfactor_id,

    MD5(CONCAT_WS(
        '-',
        activity_name,
        activity_units,
        jsonb_build_object(
            'methane-commitment-solid-waste-inboundary-oxidation-factor', 'oxidation-factor-well-managed-landfill'
        )::TEXT,
        MD5(CONCAT_WS(
            '-',
            methodology_name,
            gpc_reference_number
        ))::TEXT
    ))::UUID AS activity_id,

    total_waste AS activity_value,
    'city' AS spatial_granularity,
    NULL AS geometry_type,
    NULL AS geometry,
    NULL AS geometry_id

FROM emissions_data

ON CONFLICT (emissions_id) DO UPDATE SET
    datasource_name = EXCLUDED.datasource_name, 
    gpc_reference_number = EXCLUDED.gpc_reference_number, 
    actor_id = EXCLUDED.actor_id,
    city_id = EXCLUDED.city_id, 
    emissions_year = EXCLUDED.emissions_year,
    emissions_value = EXCLUDED.emissions_value,
    emissions_units = EXCLUDED.emissions_units,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    gas_name = EXCLUDED.gas_name,
    emissionfactor_id = EXCLUDED.emissionfactor_id,
    activity_id = EXCLUDED.activity_id,
    activity_value = EXCLUDED.activity_value,
    spatial_granularity = EXCLUDED.spatial_granularity,
    geometry_type = EXCLUDED.geometry_type,
    geometry = EXCLUDED.geometry,
    geometry_id = EXCLUDED.geometry_id;
