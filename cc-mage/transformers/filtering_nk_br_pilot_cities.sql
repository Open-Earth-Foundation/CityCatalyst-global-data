-- Add geometry column
ALTER TABLE raw_data.nk_staging 
ADD COLUMN IF NOT EXISTS geom geometry(Point, 4326);

-- Update geometry column with spatial data
UPDATE raw_data.nk_staging
SET geom = ST_SetSRID(ST_GeomFromText(geometry), 4326)
WHERE geom IS NULL;

-- Create a new table with filtered data
CREATE TABLE IF NOT EXISTS raw_data.nk_br_pilot_cities AS
SELECT ns.*, subquery.locode
FROM raw_data.nk_staging ns
JOIN (
    SELECT cp.locode, cp.geometry
    FROM modelled.city_polygon cp
    JOIN raw_data.brazil_pilot_cities pc ON cp.locode = pc.locode
) subquery 
ON ST_Within(ns.geom, subquery.geometry);