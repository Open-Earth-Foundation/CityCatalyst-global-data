SELECT  'Google EIE' AS source_name,
        'II.1.1' as gpc_reference_number,
        '{{ city_name }}' as actor_name,
        '{{locode}}' as actor_id,
        'annual' as temporal_granularity,
        'Induced activity' as method_name,
        'VKT' as activity_name,
        lower(_mode) as tranportation_mode,
        lower(travel_bounds) as trip_direction,
        gpc_distance_km as activity_value,
        CASE WHEN lower(_mode) = 'bus' THEN 'Bus - Standard'
        WHEN lower(_mode) = 'automobile' THEN 'Passenger Automobiles'
        WHEN lower(_mode) = 'motorcycle' THEN 'Motorcycle' END as transportation_mode_curb,
        CASE WHEN lower(_mode) = 'bus' THEN 'Heavy Duty Trucks and Buses'
        WHEN lower(_mode) = 'automobile' THEN 'Passenger Automobiles'
        WHEN lower(_mode) = 'motorcycle' THEN 'Motorcycle' END as transportation_mode_ef,
        'km' as activity_units,
        'co2e' as gas_name,
        gpc_co2e_tons*1000 as emissions_value,
        'kg' as emissions_units,
        _year as emissions_year,
        '{{country}}' as emissions_country,
        null as geometry_type,
        null as geometry_value  
FROM {{ df_1 }}
WHERE lower(travel_bounds) != 'total'
AND gpc_co2e_tons > 0
