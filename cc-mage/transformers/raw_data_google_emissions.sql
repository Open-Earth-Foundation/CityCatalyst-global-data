DROP TABLE IF EXISTS raw_data.google_emissions;

CREATE TABLE raw_data.google_emissions AS 
SELECT 
    e.source_name,
    e.gpc_reference_number,
    e.actor_name,
    e.actor_id,
    e.temporal_granularity,
    e.method_name,
    e.activity_name,
    e.tranportation_mode,
    e.trip_direction,
    json_build_object('tranportation_mode', tranportation_mode,
    				'trip_direction', trip_direction,
    				'fuel_type', ef.fuel_type) as activity_subcategory_type,
    e.activity_value AS total_vkt,
    e.activity_units,
    e.activity_value * c.pct_value AS activity_value,
    e.emissions_value AS total_co2eq,
    e.activity_value * c.pct_value * ef.emissionsfactor_value AS emissions_value,
    e.emissions_units,
    e.emissions_year,
    c.pct_value AS pct_fuel_type,
    ef.fuel_type,
    ef.gas as gas_name,
    ef.emissionsfactor_value,
    ef.units AS emissionfactor_units
FROM 
    modelled.emissions_staging e
LEFT JOIN 
    modelled.curb_transport_staging c 
ON 
    e.transportation_mode_curb = c.vehicle_type
    AND e.emissions_country = LOWER(c.country)
    AND c.pct_value > 0
LEFT JOIN 
    modelled.ipcc_transport_staging ef 
ON 
    (CASE 
        WHEN c.fuel_type = 'Compressed Natural Gas (CNG)' THEN 'Natural Gas'
        WHEN c.fuel_type = 'Motor Gasoline (Petrol)' THEN 'Motor Gasoline'
        WHEN c.fuel_type = 'Liquefied Petroleum Gas (LPG)' THEN 'Liquefied Petroleum Gases'
        ELSE c.fuel_type 
    END) = ef.fuel_type
    AND 
    (CASE 
        WHEN c.vehicle_type = 'Bus - Standard' THEN 'Heavy Duty Trucks and Buses'
        ELSE c.vehicle_type 
    END) = TRIM(ef.vehicle_type);

