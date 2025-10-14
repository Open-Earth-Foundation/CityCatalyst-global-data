WITH nk_data AS (
    SELECT 
        a.country_code, 
        a.locode, 
        b.gpc_reference_number, 
        COUNT(*) AS number_sites
    FROM 
        modelled.city_polygon a 
    LEFT JOIN 
        raw_data.ghgi_notation_key b 
    ON 
        ST_Intersects(a.geometry, ST_SetSRID(ST_Point(longitude, latitude), 4326))
    WHERE 
        a.country_code = 'BR'
    GROUP BY 
        a.country_code, 
        a.locode, 
        b.gpc_reference_number
),
all_data AS (
    SELECT DISTINCT 
        locode, 
        gpc_reference_number
    FROM 
        modelled.city_polygon
    CROSS JOIN 
        (SELECT DISTINCT gpc_reference_number FROM raw_data.ghgi_notation_key)
    WHERE 
        country_code = 'BR'
    ORDER BY 
        locode, 
        gpc_reference_number
),
data_source AS (
    SELECT DISTINCT 
        gpc_reference_number, 
        datasource_year, 
        datasource_code, 
        datasource_name
    FROM 
        raw_data.ghgi_notation_key
)
SELECT  
    a.locode, 
    a.gpc_reference_number,
    COALESCE(b.number_sites, 0) AS number_sites,
    c.datasource_year,
    c.datasource_code as publisher_id,
    c.datasource_name
FROM 
    all_data a 
LEFT JOIN 
    nk_data b 
ON 
    a.locode = b.locode
    AND a.gpc_reference_number = b.gpc_reference_number
LEFT JOIN 
    data_source c
ON 
    a.gpc_reference_number = c.gpc_reference_number;