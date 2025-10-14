SELECT  DISTINCT
        'Power Plan' as facility_type,
        'I.4.1' as gpc_reference_number,
        latitude, longitude,
        2024 as datasource_year,
        'WRI' as datasource_code,
        'World Resources Institue' as datasource_name
FROM {{ df_5 }}
WHERE 
(primary_fuel IN ('Coal', 'Gas', 'Oil', 'Petcoke')
OR 
other_fuel1 IN ('Coal', 'Gas', 'Oil', 'Petcoke')
OR
other_fuel2 IN ('Coal', 'Gas', 'Oil', 'Petcoke')
OR 
other_fuel3 IN ('Coal', 'Gas', 'Oil', 'Petcoke')
)
UNION
SELECT  DISTINCT 
        'Coal Mine'  as facility_type,
        'I.7.1' as gpc_reference_number,
        latitude, longitude,
        2025 as datasource_year,
        'globalenergymonitor' as datasource_code,
        'Global Energy Monitor' as datasource_name
FROM {{ df_2 }}
UNION
SELECT  'Airport' as facility_type,
        'II.4.1' as gpc_reference_number,
        latitude_deg as latitude, longitude_deg as longitude,
        2025 as datasource_year,
        'OurAirports' as datasource_code,
        'OurAirports' as datasource_name
FROM {{df_3}}
UNION
SELECT  DISTINCT
        'Oil and Gas Plant' as facility_type,
        'I.8.1' as gpc_reference_number,
        latitude, longitude,
        2025 as datasource_year,
        'OGIM' as datasource_code,
        'Oil and Gas Infrastructure Mapping' as datasource_name
FROM {{ df_4 }}
WHERE _status NOT IN ('decommissioned', 'abandoned', 'shut in', 'cancelled', 'exploration')
UNION
SELECT  DISTINCT
        'LNG Terminal' as facility_type,
        'I.8.1' as gpc_reference_number,
        latitude, longitude,
        2025 as datasource_year,
        'OGIM' as datasource_code,
        'Oil and Gas Infrastructure Mapping' as datasource_name
FROM {{ df_1 }}