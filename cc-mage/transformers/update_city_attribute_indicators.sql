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
        END AS category,
        a.datasource,
        a.indicator_year
    FROM modelled.ccra_indicator a
    JOIN Percentiles b ON a.indicator_name = b.indicator_name
    WHERE a.indicator_name IN ('population', 'population density', 'income', 'inadequate water access', 'inadequate sanitation')
        AND a.scenario_name = 'current'
),
UpsertIndicator AS (
    SELECT 
        cp.city_id, 
        a.actor_id AS locode,
        cp.region_code,
        cp.country_code, 
        a.indicator_name AS attribute_type,
        case when a.indicator_name in ('population', 'population density') then a.indicator_score::varchar
        else category end AS attribute_value, 
        NULL AS attribute_units, 
        a.datasource,
        a.indicator_year AS datasource_date
    FROM CategorizedScores a 
    INNER JOIN modelled.city_polygon cp 
    ON a.actor_id = cp.locode
),
CityBiomes AS (
    SELECT 
        cd_mun,
        nm_mun,
        nm_uf,
        CASE
            -- WHEN bioma = 'Amazônia' THEN 'Amazon rainforest'
            -- WHEN bioma = 'Mata Atlântica' THEN 'Atlantic Forest'
            WHEN bioma = 'Amazônia' THEN 'Tropical Rainforest'
            WHEN bioma = 'Caatinga' THEN 'Desert'
            WHEN bioma IN ('Cerrado', 'Pantanal', 'Pampa' ) THEN 'Grassland/Savanna'
            WHEN bioma = 'Mata Atlântica' THEN 'Tropical Rainforest'
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
    FROM CityBiomes a
    GROUP BY cd_mun, nm_mun, nm_uf
),
LookupRegionName AS (
    SELECT 		DISTINCT a.region_code, b.nm_uf as region_name
    FROM   		raw_data.icare_city_to_locode a 
    INNER JOIN 	raw_data.br_city_biome b
    ON 			a.municipality_code = b.cd_mun
),
AllData AS (
    SELECT city_id,
           locode,
           country_code,
           b.region_name,
           attribute_type,
           attribute_value,
           attribute_units,
           datasource,
           datasource_date  
    FROM UpsertIndicator a 
    INNER JOIN LookupRegionName b 
    ON trim(a.region_code) = trim(b.region_code)
    UNION ALL
    SELECT 
        cp.city_id, 
        a.locode, 
        cp.country_code AS country_code,
        b.nm_uf AS region_name,
        'main biome' AS attribute_type, 
        b.main_biome AS attribute_value, 
        NULL AS attribute_units,
        'IBGE' AS datasource, 
        2024 AS datasource_date
    FROM raw_data.icare_city_to_locode a
    LEFT JOIN AggregatedCityBiomes b ON a.municipality_code = b.cd_mun
    INNER JOIN modelled.city_polygon cp 
    ON a.locode = cp.locode
)
INSERT INTO modelled.city_attribute (
    city_id, locode, country_code, region_name, attribute_type, attribute_value, attribute_units, datasource, datasource_date
)
SELECT
    city_id, locode, country_code, region_name, attribute_type, lower(replace(attribute_value, ' ', '_')) as attribute_value, attribute_units, datasource, datasource_date
FROM AllData
ON CONFLICT (city_id, locode, attribute_type, datasource)
DO UPDATE SET
    attribute_value = EXCLUDED.attribute_value,
    attribute_units = EXCLUDED.attribute_units,
    datasource_date = EXCLUDED.datasource_date,
    region_name = EXCLUDED.region_name,
    country_code = EXCLUDED.country_code;