WITH sinir_staging AS (
    SELECT
        e.activity_value, 
        e.actor_name, 
        e.gas_name,
        e.emissionfactor_value, 
        e.emissionfactor_units, 
        e.emissions_value,
        e.emissions_units, 
        e.activity_name, 
        e.GPC_refno,
        e.emissions_year,
        e.gpcmethod_id,
        c.locode,
        c.city_id,
        (MD5(CONCAT_WS('-', activity_name, activity_subcategory_type))::UUID) AS activity_id
    FROM 
        raw_data.sinir_staging e 
    LEFT JOIN 
        modelled.city_polygon c
        ON REPLACE(LOWER(TRIM(e.actor_name)), '-', ' ') = REPLACE(LOWER(TRIM(c.city_name)), '-', ' ')
		AND e.sending_region_code = c.region_code
    WHERE 
        e.actor_name IS NOT NULL
),
staging_with_activity AS (
    SELECT
        activity_id,
        activity_value,
        gas_name,
        emissionfactor_value,
        activity_name,
        GPC_refno,
        emissions_year,
        locode,
        city_id,
        actor_name,
        emissions_value,
        emissions_units,
        gpcmethod_id,
        (MD5(CONCAT_WS('-', gas_name, emissionfactor_value, 't', activity_id::TEXT, 'IPCCv2006', 'BR'))::UUID) AS emissionfactor_id
    FROM 
        sinir_staging
)
INSERT INTO modelled.emissions 
    (emissions_id, datasource_name, gpc_reference_number, actor_id, city_id,
     gpcmethod_id, activity_id, activity_value, 
     gas_name, emissions_value, emissions_units, emissions_year, emissionfactor_id, 
     spatial_granularity, geometry_type, geometry)
SELECT DISTINCT
    (MD5(CONCAT_WS('-', 'SINIR', GPC_refno, actor_name, locode, city_id, activity_name, activity_value, emissionfactor_value, emissions_year, gas_name))::UUID) AS emissions_id,
    'SINIR' AS datasource_name,
    GPC_refno AS gpc_reference_number,
    locode AS actor_id,
    city_id,
    gpcmethod_id::UUID,
    activity_id,
    activity_value,
    gas_name,
    emissions_value,
    emissions_units,
    emissions_year::numeric AS emissions_year,
    emissionfactor_id,
    'city' AS spatial_granularity,
    NULL AS geometry_type,
    NULL::text[]  AS geometry
FROM 
    staging_with_activity
WHERE 
    emissions_value > 0
AND locode IS NOT NULL
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