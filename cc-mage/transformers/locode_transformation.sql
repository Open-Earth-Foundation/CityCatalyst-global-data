-- Step 1: Create Index on geometry_value if it does not exist
--CREATE INDEX IF NOT EXISTS idx_geom_emissions_staging ON raw_data.emissions_staging USING GIST (geometry_value);
DROP TABLE IF EXISTS modelled.emissions_staging_full;

CREATE TABLE modelled.emissions_staging_full AS
WITH emissions_ct AS (
    SELECT  
        'ClimateTRACEv2024' AS datasource_name,
        gpc_refno,
        b.iso2_code as country_code,
        emissions_year,
        sum(emissions_value) as emissions_value,
        emissions_units,
        unit_denominator,
        gas_name,
        (MD5(CONCAT_WS('-', activity_name, activity_subcategory_type))::UUID) AS activity_id,
        activity_name,
        activity_subcategory_type,
        max(activity_units) as activity_units,
        sum(activity_value) as activity_value,
        avg(emissionsfactor_value) as emissionsfactor_value,
        a.actor_id,
        NULL::date AS active_from,
        NULL::date AS active_to,
        ST_GeometryType(ST_MakePoint(lon, lat)) AS geometry_type,
        ST_SetSRID(ST_MakePoint(lon, lat), 4326) AS geometry
    FROM raw_data.ippu_ct_staging a
    LEFT JOIN raw_data.country_codes b 
	ON a.actor_id = b.iso3_code
    -- AE: we are only loading cement for now since it has processing and fuel combustion seperated
    WHERE a.industry = 'cement'
	GROUP BY actor_id, unit_denominator, emissions_units, gpc_refno, country_code, emissions_year, gas_name, activity_name, activity_subcategory_type, ST_MakePoint(lon, lat)
)
SELECT  
    datasource_name,
    country_code,
    gpc_refno,
    emissions_value,
    emissions_year,
    emissions_units,
    (MD5(CONCAT_WS('-', gpc_refno, 'custom-methodology'))::UUID) as gpcmethod_id,
    gas_name,
    (MD5(CONCAT_WS('-', gas_name, emissionsfactor_value, unit_denominator, activity_id::TEXT, 'ClimateTRACEv2024', actor_id))::UUID) AS emissionfactor_id,
    emissionsfactor_value AS emissionfactor_value,
    unit_denominator,
    activity_id,
    activity_name,
    activity_units,
    activity_subcategory_type,
    activity_value,
    geometry_type,
    geometry,
    ST_GeoHash(geometry,20) as geometry_id
FROM emissions_ct;

CREATE INDEX IF NOT EXISTS idx_geom_temp ON modelled.emissions_staging_full USING GIST (geometry);
DROP TABLE raw_data.country_codes;