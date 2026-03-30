-- Step 1: remove all existing Chile entries
DELETE FROM modelled.city_polygon
WHERE locode LIKE 'CL %';

-- Step 2: insert from staging, joining dataset_id and release_id from the
-- tables populated by the upstream blocks (avoids inline MD5 recomputation)
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
    bbox_west,
    dataset_id,
    release_id
)
SELECT
    ST_GeoHash(ST_Centroid(ST_GeomFromText(s.wkt_geom)), 20)    AS city_id,
    s.city_name,
    s.city_type,
    s.country_code,
    s.region_code,
    s.locode,
    s.osm_id::int,
    ST_GeomFromText(s.wkt_geom)                                 AS geometry,
    s.lat,
    s.lon,
    s.bbox_north,
    s.bbox_south,
    s.bbox_east,
    s.bbox_west,
    dr.dataset_id,
    dr.release_id
FROM raw_data.city_polygon_staging s
CROSS JOIN (
    SELECT dr.release_id, dr.dataset_id
    FROM modelled.dataset_release dr
    JOIN modelled.publisher_datasource pd ON dr.dataset_id = pd.dataset_id
    WHERE pd.datasource_name = 'cl-ocha-ab'
      AND dr.version_label   = '2021'
) dr
WHERE s.locode IS NOT NULL
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
        bbox_west    = EXCLUDED.bbox_west,
        dataset_id   = EXCLUDED.dataset_id,
        release_id   = EXCLUDED.release_id;
