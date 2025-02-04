-- Step 1: Create Index on geometry_value if it does not exist
--CREATE INDEX IF NOT EXISTS idx_geom_emissions_staging ON raw_data.emissions_staging USING GIST (geometry_value);
DROP TABLE IF EXISTS modelled.emissions_staging_full;

CREATE TABLE modelled.emissions_staging_full AS
WITH emissions_ct AS (
    SELECT  
        'ClimateTRACEv2023' AS datasource_name,
        gpc_refno,
        b.iso2_code as country_code,
        emissions_year,
        emissions_value,
        emissions_units,
        unit_denominator,
        (MD5(CONCAT_WS('-', gpc_refno, 'custom-methodology'))::UUID) AS gpcmethod_id,
        gas_name,
        (MD5(CONCAT_WS('-', activity_name))::UUID) AS activity_id,
        activity_value,
        emissionsfactor_value AS emissionfactor_value,
        NULL::date AS active_from,
        NULL::date AS active_to,
        ST_GeometryType(ST_MakePoint(lon, lat)) AS geometry_type,
        ST_MakePoint(lon, lat) AS geometry
    FROM modelled.ippu_ct_staging a
    LEFT JOIN country_codes b 
	ON a.actor_id = b.iso3_code
)
SELECT  
    datasource_name,
    country_code,
    gpc_refno,
    emissions_value,
    emissions_year,
    emissions_units,
    gpcmethod_id,
    gas_name,
    (MD5(CONCAT_WS('-', gas_name, emissionfactor_value, unit_denominator, activity_id::TEXT, 'ClimateTRACEv2023', country_code))::UUID) AS emissionfactor_id,
    activity_id,
    activity_value,
    geometry_type,
    geometry,
    ST_GeoHash(geometry,20) as geometry_id
FROM emissions_ct;

CREATE INDEX IF NOT EXISTS idx_geom_temp ON modelled.emissions_staging_full USING GIST (geometry);
DROP TABLE modelled.country_codes;