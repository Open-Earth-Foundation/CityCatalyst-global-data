DROP TABLE modelled.city_polygon;

CREATE TABLE modelled.city_polygon AS 
SELECT 	city_id,city_name,city_type,country_code,region_code,locode,osm_id,geometry,lat,lon,bbox_north,bbox_south,bbox_east,bbox_west
FROM 	(
SELECT 	ST_GeoHash(ST_Centroid(st_geomfromtext(geometry)),20) AS city_id,
		name AS city_name,
		addresstype AS city_type,
		substring(locode,0,3) AS country_code,
		NULL AS region_code,
		locode,
		osm_id,
		st_geomfromtext(geometry) AS geometry,
		lat,
		lon,
		bbox_north,
		bbox_south,
		bbox_east,
		bbox_west,
		RANK() OVER(PARTITION BY ST_GeoHash(ST_Centroid(st_geomfromtext(geometry)),20) ORDER BY locode DESC) AS city_order
FROM 	osm )  a
WHERE 	city_order = 1;

CREATE INDEX IF NOT EXISTS idx_city_geom ON modelled.city_polygon USING GIST (geometry);