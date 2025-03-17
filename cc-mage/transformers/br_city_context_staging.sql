DROP TABLE IF EXISTS raw_data.br_city_context;

CREATE TABLE raw_data.br_city_context AS
WITH Percentiles AS (
    SELECT 
        indicator_name,
        PERCENTILE_CONT(0.2) WITHIN GROUP (ORDER BY indicator_score) AS p20,
        PERCENTILE_CONT(0.4) WITHIN GROUP (ORDER BY indicator_score) AS p40,
        PERCENTILE_CONT(0.6) WITHIN GROUP (ORDER BY indicator_score) AS p60,
        PERCENTILE_CONT(0.8) WITHIN GROUP (ORDER BY indicator_score) AS p80
    FROM modelled.ccra_indicator 
    WHERE indicator_name IN ('population', 'population density', 'income', 'inadequate water access', 'inadequate sanitation')
        AND scenario_name = 'current'
    GROUP BY indicator_name
),
CategorizedScores AS (
    SELECT 
        a.actor_id, 
        a.indicator_name, 
        a.indicator_score,
        CASE 
            WHEN a.indicator_score <= b.p20 THEN 'very low'
            WHEN a.indicator_score <= b.p40 THEN 'low'
            WHEN a.indicator_score <= b.p60 THEN 'moderate'
            WHEN a.indicator_score <= b.p80 THEN 'high'
            ELSE 'very high' 
        END AS category
    FROM modelled.ccra_indicator a
    JOIN Percentiles b ON a.indicator_name = b.indicator_name
    WHERE a.indicator_name IN ('population', 'population density', 'income', 'inadequate water access', 'inadequate sanitation')
        AND a.scenario_name = 'current'
),
IndicatorData AS (
SELECT
    actor_id,
    MAX(CASE WHEN indicator_name = 'population' THEN category ELSE NULL END) AS population_category,
    MAX(CASE WHEN indicator_name = 'population' THEN indicator_score ELSE NULL END) AS population_score,
    MAX(CASE WHEN indicator_name = 'population density' THEN category ELSE NULL END) AS population_density_category,
    MAX(CASE WHEN indicator_name = 'population density' THEN indicator_score ELSE NULL END) AS population_density_score,
    MAX(CASE WHEN indicator_name = 'income' THEN category ELSE NULL END) AS income_category,
    MAX(CASE WHEN indicator_name = 'income' THEN indicator_score ELSE NULL END) AS income_score,
    MAX(CASE WHEN indicator_name = 'inadequate water access' THEN category ELSE NULL END) AS inadequate_water_access_category,
    MAX(CASE WHEN indicator_name = 'inadequate water access' THEN indicator_score ELSE NULL END) AS inadequate_water_access_score,
    MAX(CASE WHEN indicator_name = 'inadequate sanitation' THEN category ELSE NULL END) AS inadequate_sanitation_category,
    MAX(CASE WHEN indicator_name = 'inadequate sanitation' THEN indicator_score ELSE NULL END) AS inadequate_sanitation_score
FROM CategorizedScores
GROUP BY actor_id
),
CityBiomes AS (
    SELECT 
        cd_mun,
        nm_mun,
        nm_uf,
        CASE
            WHEN bioma = 'Amazônia' THEN 'Amazon rainforest'
            WHEN bioma = 'Mata Atlântica' THEN 'Atlantic Forest'
            ELSE bioma 
        END AS biome, 
        biome_percentage,
        biome_rank
    FROM raw_data.br_city_biome
),
AggregatedCityBiomes AS (
    SELECT 
        cd_mun,
        nm_mun,
        nm_uf,
        MAX(CASE WHEN biome_rank = 1 THEN biome ELSE NULL END) AS main_biome,
        STRING_AGG(biome, ', ') AS all_biomes
    FROM CityBiomes
    GROUP BY cd_mun, nm_mun, nm_uf
)
SELECT
    a.locode,
    b.nm_mun AS city_name,
    a.region_code,
    b.nm_uf AS region_name,
    b.main_biome,
    b.all_biomes,
    id.population_category,
    id.population_score,
    id.population_density_category,
    id.population_density_score,
    id.income_category,
    id.income_score,
    id.inadequate_water_access_category,
    id.inadequate_water_access_score,
    id.inadequate_sanitation_category,
    id.inadequate_sanitation_score
FROM raw_data.icare_city_to_locode a
LEFT JOIN AggregatedCityBiomes b ON a.municipality_code = b.cd_mun
LEFT JOIN IndicatorData id ON a.locode = id.actor_id;
