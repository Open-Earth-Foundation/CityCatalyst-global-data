WITH region_mapping AS (
    SELECT 'Acre' AS region_name, 'AC' AS region_code UNION ALL
    SELECT 'Alagoas', 'AL' UNION ALL
    SELECT 'Amapá', 'AP' UNION ALL
    SELECT 'Amazonas', 'AM' UNION ALL
    SELECT 'Bahia', 'BA' UNION ALL
    SELECT 'Ceará', 'CE' UNION ALL
    SELECT 'Distrito Federal', 'DF' UNION ALL
    SELECT 'Espírito Santo', 'ES' UNION ALL
    SELECT 'Goiás', 'GO' UNION ALL
    SELECT 'Maranhão', 'MA' UNION ALL
    SELECT 'Mato Grosso', 'MT' UNION ALL
    SELECT 'Mato Grosso do Sul', 'MS' UNION ALL
    SELECT 'Minas Gerais', 'MG' UNION ALL
    SELECT 'Paraná', 'PR' UNION ALL
    SELECT 'Paraíba', 'PB' UNION ALL
    SELECT 'Pará', 'PA' UNION ALL
    SELECT 'Pernambuco', 'PE' UNION ALL
    SELECT 'Piauí', 'PI' UNION ALL
    SELECT 'Rio de Janeiro', 'RJ' UNION ALL
    SELECT 'Rio Grande do Norte', 'RN' UNION ALL
    SELECT 'Rio Grande do Sul', 'RS' UNION ALL
    SELECT 'Rondônia', 'RO' UNION ALL
    SELECT 'Roraima', 'RR' UNION ALL
    SELECT 'Santa Catarina', 'SC' UNION ALL
    SELECT 'Sergipe', 'SE' UNION ALL
    SELECT 'São Paulo', 'SP' UNION ALL
    SELECT 'Tocantins', 'TO'
),
locode_data AS (
    SELECT 
        a.LOCODE AS locode,
        a._Name AS city_name,
        a.SubDiv AS region_code
    FROM raw_data.br_locode a
),
city_comparison AS (
    SELECT * FROM (
        VALUES
            ('Graccho Cardoso', 'SE', 'Gracho Cardoso', 'SE'),
            ('Amparo do São Francisco', 'SE', 'Amparo de São Francisco', 'SE'),
            ('Barão do Monte Alto', 'MG', 'Barão de Monte Alto', 'MG'),
            ('Santo Antônio de Leverger', 'MT', 'Santo Antônio do Leverger', 'MT'),
            ('Atílio Vivácqua', 'ES', 'Atilio Vivacqua', 'ES'),
            ('Santa Terezinha', 'BA', 'Santa Teresinha', 'BA')
    ) AS t(src_city_name, src_region_code, locode_city_name, locode_region)
),
staging_data AS (
    SELECT 
        ld.locode,        
        bb.city_name,
        rm.region_code,
        bb.geom
    FROM raw_data.br_city_polygon bb
    LEFT JOIN region_mapping rm 
    ON bb.region_name = rm.region_name
    LEFT JOIN city_comparison cc 
    ON bb.city_name = cc.src_city_name
    AND rm.region_code = cc.src_region_code
    LEFT JOIN locode_data ld 
    ON REPLACE(LOWER(COALESCE(cc.locode_city_name,bb.city_name)), '-', ' ') = REPLACE(LOWER(ld.city_name), '-', ' ')
    AND rm.region_code = ld.region_code
    WHERE ld.locode IS NOT NULL
)
-- Insert data into the main table
INSERT INTO modelled.city_polygon
(city_id, city_name, city_type, country_code, region_code, locode, osm_id, geometry, lat, lon, bbox_north, bbox_south, bbox_east, bbox_west)
SELECT
    ST_GeoHash(ST_Centroid(ST_SetSRID(ST_GeomFromWKB(decode(geom, 'hex')), 4326)), 20) AS city_id,
    city_name,
    'municipality' AS city_type,
    'BR' AS country_code,
    region_code,
    locode,
    NULL AS osm_id,
    ST_SetSRID(ST_GeomFromWKB(decode(geom, 'hex')), 4326) AS geometry,
    ST_Y(ST_Centroid(ST_SetSRID(ST_GeomFromWKB(decode(geom, 'hex')), 4326))) AS lat,
    ST_X(ST_Centroid(ST_SetSRID(ST_GeomFromWKB(decode(geom, 'hex')), 4326))) AS lon,
    ST_YMax(ST_Envelope(ST_SetSRID(ST_GeomFromWKB(decode(geom, 'hex')), 4326))) AS bbox_north,
    ST_YMin(ST_Envelope(ST_SetSRid(ST_GeomFromWKB(decode(geom, 'hex')), 4326))) AS bbox_south,
    ST_XMax(ST_Envelope(ST_SetSRid(ST_GeomFromWKB(decode(geom, 'hex')), 4326))) AS bbox_east,
    ST_XMin(ST_Envelope(ST_SetSRid(ST_GeomFromWKB(decode(geom, 'hex')), 4326))) AS bbox_west
FROM staging_data
ON CONFLICT (locode) DO UPDATE
SET
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

DROP TABLE raw_data.br_city_polygon;
DROP TABLE raw_data.br_locode;