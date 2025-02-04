-- Step 1: Create Index on geometry_value if it does not exist
--CREATE INDEX IF NOT EXISTS idx_geom_emissions_staging ON raw_data.emissions_staging USING GIST (geometry_value);
DROP TABLE IF EXISTS modelled.emissions_staging_full;

CREATE TABLE modelled.emissions_staging_full AS
WITH emissions_ct AS (
    SELECT
        -- AE: we had to take a group by here because we were still getting month records.   
        'ClimateTRACEv2024' AS datasource_name, -- AE: it's easier to query when there are no spaces and we can version with v and the year
        gpc_refno,
        b.iso2_code as country_code,
        emissions_year,
        SUM(emissions_value) AS emissions_value,
        MAX(emissions_units) AS emissions_units,
        MAX(unit_denominator) AS unit_denominator,
--        MAX((MD5(CONCAT_WS('-', gpc_refno, 'custom-methodology'))::UUID)) AS gpcmethod_id,
        gas_name,
--        (MD5(CONCAT_WS('-', activity_name, activity_subcategory_type))::UUID) AS activity_id,
        activity_name,
        activity_subcategory_type,
        MAX(activity_units) AS activity_units,
        SUM(activity_value) AS activity_value,
        AVG(emissionsfactor_value) AS emissionfactor_value,
        NULL::date AS active_from,
        NULL::date AS active_to,
        ST_GeometryType(ST_MakePoint(lon, lat)) AS geometry_type,
        ST_MakePoint(lon, lat) AS geometry
    FROM raw_data.ippu_ct_staging a
    LEFT JOIN raw_data.country_codes b 
	ON a.actor_id = b.iso3_code
	GROUP BY gpc_refno, country_code, emissions_year, gas_name, activity_name, activity_subcategory_type, ST_MakePoint(lon, lat)
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
    (MD5(CONCAT_WS('-', gas_name, emissionfactor_value, unit_denominator, activity_name, activity_subcategory_type, 'ClimateTRACEv2024'))::UUID) AS emissionfactor_id,
    emissionfactor_value,
    unit_denominator,
    (MD5(CONCAT_WS('-', activity_name, activity_subcategory_type))::UUID) AS activity_id,
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