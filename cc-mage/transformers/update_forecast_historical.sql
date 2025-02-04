WITH base_data AS (
    SELECT DISTINCT
        b.locode AS actor_id, 
        c.clusters AS cluster_id,
        CASE 
            WHEN sector_en = 'Waste' THEN 'III'
            WHEN sector_en = 'Energy' THEN 'I, II'
            WHEN sector_en = 'Agriculture' THEN 'V.1, V.3'
            WHEN sector_en = 'Industrial Processes' THEN 'IV'
            WHEN sector_en = 'Land Use Change and Forestry' THEN 'V.2'
        END AS gpc_sector,
        a.growth_rate_2019,
        a.growth_rate_2020,
        a.growth_rate_2021,
        a.growth_rate_2022,
        a.growth_rate_2023
    FROM 
        raw_data.ghgi_icare_emissions_forecast_historical_rates a
    LEFT JOIN 
        raw_data.icare_city_to_locode b ON a.city_name = TRIM(SPLIT_PART(b.municipality, '(', 1)) 
        AND a.region_code = b.region_code 
    LEFT JOIN 
        raw_data.icare_city_topology c ON b.municipality_code = c.codmun 
    WHERE b.locode is not null
),
history_rates AS (
    SELECT DISTINCT
        actor_id, 
        cluster_id, 
        gpc_sector, 
        '2019' AS year, 
        growth_rate_2019 AS growth_rate 
    FROM base_data
    UNION ALL
    SELECT 
        actor_id, 
        cluster_id, 
        gpc_sector, 
        '2020' AS year, 
        growth_rate_2020 AS growth_rate 
    FROM base_data
    UNION ALL
    SELECT 
        actor_id, 
        cluster_id, 
        gpc_sector, 
        '2021' AS year, 
        growth_rate_2021 AS growth_rate 
    FROM base_data
    UNION ALL
    SELECT 
        actor_id, 
        cluster_id, 
        gpc_sector, 
        '2022' AS year, 
        growth_rate_2022 AS growth_rate 
    FROM base_data
    UNION ALL
    SELECT 
        actor_id, 
        cluster_id, 
        gpc_sector, 
        '2023' AS year, 
        growth_rate_2023 AS growth_rate 
    FROM base_data
),
cluster_desc AS (
    SELECT DISTINCT cluster_id, cluster_name, cluster_description
    FROM raw_data.ghgi_icare_emissions_forecast_growth_rates
)
-- Insert into the target table
INSERT INTO modelled.ghgi_emission_forecast (
    id,
    actor_id,
    cluster_id,
    cluster_name,
    cluster_description,
    gpc_sector,
    forecast_year,
    future_year,
    growth_rate,
    spatial_granularity,
    datasource
)
SELECT 
    MD5(CONCAT_WS('-', h.actor_id, TRIM(unnest(string_to_array(h.gpc_sector, ','))), 2023, h.year))::UUID AS id,  -- Generate ID
    h.actor_id,
    h.cluster_id,
    cd.cluster_name::json,
    cd.cluster_description::json,
    TRIM(unnest(string_to_array(h.gpc_sector, ','))) AS gpc_sector,
    2023 AS forecast_year,
    h.year::int AS future_year,
    COALESCE(h.growth_rate, 0) AS growth_rate,
    'city' AS spatial_granularity,
    'SEEG' AS datasource   -- Updated to use a static value or variable if needed
FROM 
    history_rates h  -- Source for growth rates
LEFT JOIN 
    cluster_desc cd ON cd.cluster_id = h.cluster_id  -- Joining with cluster description
ON CONFLICT (id) DO UPDATE SET
    actor_id = EXCLUDED.actor_id,
    cluster_id = EXCLUDED.cluster_id,
    cluster_name = EXCLUDED.cluster_name,
    cluster_description = EXCLUDED.cluster_description,
    gpc_sector = EXCLUDED.gpc_sector,
    forecast_year = EXCLUDED.forecast_year,
    future_year = EXCLUDED.future_year,
    growth_rate = EXCLUDED.growth_rate,
    datasource = EXCLUDED.datasource;