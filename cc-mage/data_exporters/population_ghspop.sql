WITH dataset_data AS (
    SELECT DISTINCT
        publisher_name,
        publisher_url,
        datasource_name, 
        dataset_name, 
        dataset_url,
        locode,
        population,
        _year::INTEGER AS year, 
        population_source,
        geographical_level
    FROM raw_data.ghs_pop_staging
)

INSERT INTO modelled.population (
    population_id,
    publisher_id,
    dataset_id,
    population_value,
    actor_id,
    year,
    population_source,
    geographical_level
)

SELECT DISTINCT

    MD5(CONCAT_WS(
        '-', 
        publisher_name,
        publisher_url,
        datasource_name,
        dataset_name,
        dataset_url,
        year,
        locode
    ))::UUID AS population_id,

    MD5(CONCAT_WS('-', publisher_name, publisher_url))::UUID AS publisher_id,
    MD5(CONCAT_WS('-', datasource_name, dataset_name, dataset_url))::UUID AS dataset_id,

    ROUND(population)::BIGINT AS population_value,
    locode AS actor_id,
    year,
    population_source,
    geographical_level

FROM dataset_data

ON CONFLICT (publisher_id, dataset_id, year, actor_id)
DO UPDATE SET
    population_value = EXCLUDED.population_value,
    population_source = EXCLUDED.population_source,
    geographical_level = EXCLUDED.geographical_level;