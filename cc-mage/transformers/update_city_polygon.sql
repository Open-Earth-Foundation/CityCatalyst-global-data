UPDATE modelled.city_polygon 
SET geometry = (SELECT ST_GeomFromText(wkt_geom) FROM raw_data.city_polygon_staging)
WHERE locode = '{{ locode }}'
;

-- UPDATE osm 
-- SET geometry = (SELECT wkt_geom FROM raw_data.city_polygon_staging)
-- WHERE locode = '{{ locode }}'
-- ;