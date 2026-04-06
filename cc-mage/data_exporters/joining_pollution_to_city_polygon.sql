CREATE TABLE raw_data.pollution_with_city AS
SELECT
    ps.*,
    cp.city_id,
    cp.country_code,
    cp.locode,
    cp.geometry
FROM raw_data.pollution_staging ps
JOIN modelled.city_polygon cp
    ON ST_Within(
        ST_SetSRID(ST_MakePoint(ps.lon, ps.lat), 4326),
        cp.geometry
    )
WHERE cp.country_code = 'CL';