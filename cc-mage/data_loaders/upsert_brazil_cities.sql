INSERT INTO modelled.city_polygon
(city_id, city_name, city_type, country_code, region_code, locode, osm_id, geometry, lat, lon, bbox_north, bbox_south, bbox_east, bbox_west)
SELECT
    ST_GeoHash(ST_Centroid(ST_GeomFromText(geometry)), 20) AS city_id,
    city AS city_name,
    'municipality' AS city_type,
    'BR' AS country_code,
    region AS region_code,
    locode,
    REPLACE(osm_id,'R','')::int AS osm_id,
    geometry,
    ST_Y(ST_Centroid(geometry)) AS lat,
    ST_X(ST_Centroid(geometry)) AS lon,
    ST_YMax(ST_Envelope(geometry)) AS bbox_north,
    ST_YMin(ST_Envelope(geometry)) AS bbox_south,
    ST_XMax(ST_Envelope(geometry)) AS bbox_east,
    ST_XMin(ST_Envelope(geometry)) AS bbox_west
FROM modelled.city_polygon_staging
ON CONFLICT (locode)
DO UPDATE set
	city_id = EXCLUDED.city_id,
    city_name = EXCLUDED.city_name,
    city_type = EXCLUDED.city_type,
    region_code = EXCLUDED.region_code,
    osm_id = EXCLUDED.osm_id,
    locode = EXCLUDED.locode,
    geometry = EXCLUDED.geometry,
    lat = EXCLUDED.lat,
    lon = EXCLUDED.lon,
    bbox_north = EXCLUDED.bbox_north,
    bbox_south = EXCLUDED.bbox_south,
    bbox_east = EXCLUDED.bbox_east,
    bbox_west = EXCLUDED.bbox_west;

DROP TABLE modelled.city_polygon_staging;