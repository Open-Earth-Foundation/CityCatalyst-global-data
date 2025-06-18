CREATE TABLE raw_data.ct_staging AS
SELECT 
    ct.*,
    cp.city_id,
    cp.locode
FROM 
    raw_data.ct_staging1 ct
JOIN 
    modelled.city_polygon cp 
    ON ST_Intersects(
        ST_SetSRID(ST_MakePoint(ct.lon, ct.lat), 4326),
        cp.geometry
    )
WHERE 
    cp.country_code = 'CA';