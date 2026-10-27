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
    FROM raw_data.incineration_eurostats_staging
    WHERE emissions_value IS NOT NULL
),
ids AS (
    SELECT *,
        -- Create gpcmethod_id
        MD5(CONCAT_WS(
            '-',
            methodology_name,
            gpc_reference_number
        ))::UUID AS gpcmethod_id,

        -- Create publisher_id
        MD5(CONCAT_WS(
            '-', 
            'IPCC', 
            'https://www.ipcc.ch/'
        ))::UUID AS publisher_id,

        -- Create dataset_id
        MD5(CONCAT_WS(
            '-', 
            'IPCC', 
            'IPCC Emission Factor Database (EFDB) [2006 IPCC Guidelines]', 
            'https://www.ipcc-nggip.iges.or.jp/EFDB/main.php'
        ))::UUID AS dataset_id
    FROM emissions_data
),
with_activity AS (
    SELECT *,
        -- Create activity_id
        MD5(CONCAT_WS(
            '-',
            activity_name,
            activity_units,
            jsonb_build_object(
                'biological-treatment-inboundary-waste-state', 'waste-state-wet-waste',
                'biological-treatment-inboundary-treatment-type', 'treatment-type-composting'
            )::TEXT,
            gpcmethod_id::TEXT
        ))::UUID AS activity_id
    FROM ids
),
with_emissionfactor AS (
    SELECT *,
        CASE
            WHEN gas_name IN ('CH4', 'N2O') THEN MD5(CONCAT_WS(
                '-', 
                publisher_id::TEXT, 
                dataset_id::TEXT, 
                activity_id::TEXT, 
                'kg', 
                gas_name, 
                actor_id, 
                '2023'
            ))::UUID
            ELSE NULL
        END AS emissionfactor_id
    FROM with_activity
),
final_data AS (
    SELECT *,
        -- Create emissions_id using all relevant pieces
        MD5(CONCAT_WS(
            '-', 
            'EuroStat',
            gpc_reference_number,
            actor_id,
            '2023',
            gpcmethod_id::TEXT,
            gas_name,
            emissionfactor_id::TEXT
        ))::UUID AS emissions_id
    FROM with_emissionfactor
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
    emissions_id,
    'EuroStat' AS datasource_name,
    gpc_reference_number,
    actor_id,
    city_id,
    2023 AS emissions_year,
    emissions_value,
    emissions_units,
    gpcmethod_id,
    gas_name,
    emissionfactor_id,
    activity_id,
    total_waste AS activity_value,
    'city' AS spatial_granularity,
    NULL AS geometry_type,
    NULL AS geometry,
    NULL AS geometry_id

FROM final_data

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
