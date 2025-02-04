WITH upsert AS (
    SELECT 
        c.locode AS actor_id,
        b.cluster_id,
        b.cluster_name::json,
        b.cluster_description::json,
        trim(unnest(string_to_array(b.gpc_sector, ','))) AS gpc_sector,
        2023 AS forecast_year,
        b.future_year,
        b.growth_rate / 100 AS growth_rate,
        'icare' AS datasource
    FROM raw_data.icare_city_topology a 
    LEFT JOIN raw_data.ghgi_icare_emissions_forecast_growth_rates b ON a.clusters = b.cluster_id
    LEFT JOIN raw_data.icare_city_to_locode c ON c.municipality_code = a.codmun
    WHERE locode IS NOT NULL 
)
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
    MD5(CONCAT_WS('-', actor_id, gpc_sector, forecast_year, future_year))::UUID AS id,
    actor_id,
    cluster_id,
    cluster_name,
    cluster_description,
    gpc_sector,
    forecast_year,
    future_year,
    growth_rate,
    'city' as spatial_granularity,
    datasource
FROM upsert
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

DROP TABLE IF EXISTS raw_data.icare_city_topology;
DROP TABLE IF EXISTS raw_data.ghgi_icare_emissions_forecast_growth_rates;
DROP TABLE IF EXISTS raw_data.icare_city_to_locode;
DROP TABLE IF EXISTS raw_data.ghgi_icare_emissions_forecast_historical_rates;