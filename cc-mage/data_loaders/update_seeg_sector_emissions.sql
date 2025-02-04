WITH seeg_city_emissions AS (
    SELECT 
        gpc_reference_number,
        gas_name,
        activity_name,
        activity_subcategory_type1, activity_subcategory_typename1,
        activity_subcategory_type2, activity_subcategory_typename2,
        activity_subcategory_type3, activity_subcategory_typename3,
        locode,
        city_id,
        emissions_2015,
        emissions_2016,
        emissions_2017,
        emissions_2018,
        emissions_2019,
        emissions_2020,
        emissions_2021,
        emissions_2022,
        emissions_2023
    FROM 
        raw_data.seeg_sector_emissions e 
    LEFT JOIN 
        modelled.city_polygon c ON 
            LOWER(TRIM(e.city)) = LOWER(TRIM(c.city_name)) AND
            e.region = c.region_code AND
            country_code = 'BR'
    WHERE 
        e.city != 'NA'
),
seeg_city_emissions_year AS (
    SELECT 
        gpc_reference_number,
        activity_name,
        activity_subcategory_type1, activity_subcategory_typename1,
        activity_subcategory_type2, activity_subcategory_typename2,
        activity_subcategory_type3, activity_subcategory_typename3,
        gas_name,
        locode,
        city_id,
        year AS emissions_year,
        emissions_value::numeric * 1000 AS emissions_value,
        'kg' AS emissions_units
    FROM 
        (SELECT 
            gpc_reference_number,
            gas_name,
            activity_name,
            activity_subcategory_type1, activity_subcategory_typename1,
            activity_subcategory_type2, activity_subcategory_typename2,
            activity_subcategory_type3, activity_subcategory_typename3,
            locode,
            city_id,
            emissions_2015,
            emissions_2016,
            emissions_2017,
            emissions_2018,
            emissions_2019,
            emissions_2020,
            emissions_2021,
            emissions_2022,
            emissions_2023
        FROM 
            seeg_city_emissions
        GROUP BY 
            gpc_reference_number,
            gas_name,
            activity_name,
            activity_subcategory_type1, activity_subcategory_typename1,
            activity_subcategory_type2, activity_subcategory_typename2,
            activity_subcategory_type3, activity_subcategory_typename3,
            locode,
            city_id,
            emissions_2015,
            emissions_2016,
            emissions_2017,
            emissions_2018,
            emissions_2019,
            emissions_2020,
            emissions_2021,
            emissions_2022,
            emissions_2023
        ) AS source
    CROSS JOIN LATERAL (
        VALUES
            ('2015', emissions_2015),
            ('2016', emissions_2016),
            ('2017', emissions_2017),
            ('2018', emissions_2018),
            ('2019', emissions_2019),
            ('2020', emissions_2020),
            ('2021', emissions_2021),
            ('2022', emissions_2022),
            ('2023', emissions_2023)
    ) AS unpivoted(year, emissions_value)
)
INSERT INTO modelled.emissions 
    (emissions_id, datasource_name, gpc_reference_number, actor_id, city_id,
     gpcmethod_id, activity_id, activity_value, 
     gas_name, emissions_value, emissions_units, emissions_year, emissionfactor_id, 
     spatial_granularity, geometry_type, geometry)
SELECT 
    (MD5(CONCAT_WS('-', 'SEEGv2023', gpc_reference_number, locode,activity_name,activity_subcategory_typename1, activity_subcategory_type2, activity_subcategory_typename2, activity_subcategory_type3, activity_subcategory_typename3,
    emissions_year, gas_name))::UUID) AS emissions_id,
    'SEEGv2023' AS datasource_name,
    gpc_reference_number,
    locode AS actor_id,
    city_id,
    NULL::UUID AS gpcmethod_id,
    (MD5(CONCAT_WS('-', activity_name, activity_subcategory_type1, activity_subcategory_typename1, activity_subcategory_type2, activity_subcategory_typename2, activity_subcategory_type3, activity_subcategory_typename3))::UUID) AS activity_id,
    NULL AS activity_value,
    gas_name,
    emissions_value,
    emissions_units,
    emissions_year::numeric AS emissions_year,
    NULL::UUID AS emissionfactor_id,
    'city' AS spatial_granularity,
    NULL AS geometry_type,
    NULL AS geometry
FROM 
    seeg_city_emissions_year
WHERE 
    emissions_value > 0
AND locode IS NOT NULL
ON CONFLICT ON CONSTRAINT emissions_pkey
DO UPDATE SET 
    datasource_name = EXCLUDED.datasource_name,
    gpc_reference_number = EXCLUDED.gpc_reference_number,
    actor_id = EXCLUDED.actor_id,
    city_id = EXCLUDED.city_id,
    gpcmethod_id = EXCLUDED.gpcmethod_id,
    activity_id = EXCLUDED.activity_id,
    activity_value = EXCLUDED.activity_value,
    gas_name = EXCLUDED.gas_name,
    emissions_value = EXCLUDED.emissions_value,
    emissions_units = EXCLUDED.emissions_units,
    emissions_year = EXCLUDED.emissions_year,
    emissionfactor_id = EXCLUDED.emissionfactor_id,
    spatial_granularity = EXCLUDED.spatial_granularity,
    geometry_type = EXCLUDED.geometry_type,
    geometry = EXCLUDED.geometry;
