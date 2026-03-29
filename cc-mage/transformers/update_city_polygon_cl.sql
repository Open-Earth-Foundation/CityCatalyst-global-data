-- Step 1: remove all existing Chile entries
DELETE FROM modelled.city_polygon
WHERE locode LIKE 'CL %';

-- Step 2: insert from staging, only where locode is not null
INSERT INTO modelled.city_polygon (
    city_id,
    city_name,
    city_type,
    country_code,
    region_code,
    locode,
    osm_id,
    geometry,
    lat,
    lon,
    bbox_north,
    bbox_south,
    bbox_east,
    bbox_west
)
SELECT
    ST_GeoHash(ST_Centroid(ST_GeomFromText(wkt_geom)), 20)  AS city_id,
    city_name,
    city_type,
    country_code,
    region_code,
    locode,
    osm_id::int,
    ST_GeomFromText(wkt_geom)                               AS geometry,
    lat,
    lon,
    bbox_north,
    bbox_south,
    bbox_east,
    bbox_west
FROM raw_data.city_polygon_staging
WHERE locode IS NOT NULL
ON CONFLICT (locode) DO UPDATE
    SET geometry     = EXCLUDED.geometry,
        city_name    = EXCLUDED.city_name,
        city_type    = EXCLUDED.city_type,
        country_code = EXCLUDED.country_code,
        region_code  = EXCLUDED.region_code,
        lat          = EXCLUDED.lat,
        lon          = EXCLUDED.lon,
        bbox_north   = EXCLUDED.bbox_north,
        bbox_south   = EXCLUDED.bbox_south,
        bbox_east    = EXCLUDED.bbox_east,
        bbox_west    = EXCLUDED.bbox_west;
