WITH emissions_raw AS (
    SELECT DISTINCT
        gas_name,
        gpc_refno,
        emissionfactor_value,
        units,
        activity_units,
        methodology_name,
        activity_name, 
        source_name,
        "livestock_species",
        "livestock_activity_type",
        "livestock_subactivity_type",
        publisher_name,
        publisher_url,
        datasource_name,
        dataset_name,
        dataset_url,
        lat,
        lon,
        city_id,
        locode,
        emissions_year,
        emissions_value,
        emissions_units, 
        activity_value
    FROM raw_data.ct_staging
    WHERE emissions_value IS NOT NULL
),
step1_ids AS (
    SELECT *,
        -- Create publisher_id 
        MD5(CONCAT_WS(
            '-', 
            publisher_name, 
            publisher_url
            ))::UUID AS publisher_id,

        -- Create dataset_id
        MD5(CONCAT_WS(
            '-', 
            datasource_name, 
            dataset_name, 
            dataset_url
            ))::UUID AS dataset_id,
        
        -- Create gpcmethod_id
        MD5(CONCAT_WS(
            '-', 
            methodology_name, 
            gpc_refno
            ))::UUID AS gpcmethod_id,
        
        -- Create activity_id
        MD5(CONCAT_WS('-',
            activity_name,
            activity_units,
            jsonb_build_object(
                'data-source', source_name,
                'livestock-species', livestock_species,
                'livestock-activity-type', livestock_activity_type,
                'livestock-subactivity-type', livestock_subactivity_type
            )::TEXT,
            MD5(CONCAT_WS('-', methodology_name, gpc_refno))::TEXT
        ))::UUID AS activity_id
    FROM emissions_raw
),
step2_final_ids AS (
    SELECT *,
        MD5(CONCAT_WS('-',
            publisher_id::TEXT,
            dataset_id::TEXT,
            activity_id::TEXT,
            units,
            gas_name,
            locode,
            emissions_year
        ))::UUID AS emissionfactor_id
    FROM step1_ids
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
SELECT
    MD5(CONCAT_WS(
        '-', 
        city_id, 
        emissions_year, 
        gpc_refno, 
        gpcmethod_id, 
        gas_name, 
        emissionfactor_id, 
        activity_id, 
        MD5(CONCAT_WS(
            '-', 
            ST_AsText(ST_SetSRID(ST_MakePoint(lon, lat), 4326)), 
            ST_GeometryType(ST_MakePoint(lon, lat)))
            )::TEXT
    ))::UUID AS emissions_id,

    datasource_name, 
    gpc_refno AS gpc_reference_number, 
    locode AS actor_id,
    city_id, 
    emissions_year,
    emissions_value,
    emissions_units,
    gpcmethod_id,
    gas_name,
    emissionfactor_id,
    activity_id,
    activity_value,
    'city' AS spatial_granularity,
    ST_GeometryType(ST_MakePoint(lon, lat)) AS geometry_type,
    ST_SetSRID(ST_MakePoint(lon, lat), 4326) AS geometry,

    -- Create geometry_id
    MD5(CONCAT_WS(
        '-', 
        ST_AsText(ST_SetSRID(ST_MakePoint(lon, lat), 4326)), 
        ST_GeometryType(ST_MakePoint(lon, lat))
    ))::UUID AS geometry_id
FROM step2_final_ids

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