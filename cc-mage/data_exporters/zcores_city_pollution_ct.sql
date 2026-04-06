DROP TABLE IF EXISTS raw_data.city_emissions_zscore;

CREATE TABLE raw_data.city_emissions_zscore AS
WITH city_totals AS (
    -- Step 1: total emissions per city and year
    SELECT
        city_id,
        locode,
        country_code,
        _year AS datasource_date,
        SUM(emissions_quantity) AS total_emissions
    FROM raw_data.pollution_with_city
    WHERE locode IS NOT NULL
    GROUP BY city_id, locode, country_code, _year
),
stats AS (
    -- Step 2: mean and std per year
    SELECT
        datasource_date,
        AVG(total_emissions) AS mean_emissions,
        STDDEV(total_emissions) AS stddev_emissions
    FROM city_totals
    GROUP BY datasource_date
),
z_scores AS (
    -- Step 3: compute z-score
    SELECT
        ct.city_id,
        ct.locode,
        ct.country_code,
        ct.datasource_date,
        (ct.total_emissions - s.mean_emissions) / s.stddev_emissions AS attribute_value
    FROM city_totals ct
    JOIN stats s
        ON ct.datasource_date = s.datasource_date
)

SELECT
    city_id,
    locode,
    country_code,
    attribute_value,
    datasource_date,
    'climateTRACE' AS datasource,
    'stationary pollution' AS attribute_type,

    CASE
        WHEN attribute_value < -1 THEN 'significantly below average stationary pollution'
        WHEN attribute_value >= -1 AND attribute_value < 0 THEN 'below average'
        WHEN attribute_value = 0 THEN 'average'
        WHEN attribute_value > 0 AND attribute_value <= 1 THEN 'above average'
        WHEN attribute_value > 1 THEN 'significantly above average stationary pollution'
    END AS attribute_category

FROM z_scores;