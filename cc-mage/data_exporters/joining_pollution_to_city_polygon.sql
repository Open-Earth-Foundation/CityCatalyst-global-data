DROP TABLE raw_data.pollution_with_city;

CREATE TABLE raw_data.pollution_with_city AS
SELECT
    ps.*,
    cp.city_id,
    cp.country_code,
    cp.locode,
    ST_SetSRID(cp.geometry, 4326) AS geometry
FROM raw_data.pollution_staging ps
JOIN modelled.city_polygon cp
    ON ST_Within(
        ST_SetSRID(ST_MakePoint(ps.lon, ps.lat), 4326),
        ST_SetSRID(cp.geometry, 4326)
    )
WHERE cp.country_code = 'CL';