WITH 
transport_emission_factor_ex AS (
    SELECT 
        ef_id,
        UNNEST(STRING_SPLIT(ipcc_sector_multi, '|')) AS ipcc_sector,
        gas_multi,
        fuel_1996,
        fuel_2006,
        type_parameter,
        Description,
        technologies_paractises,
        parameters_conditions,
        region,
        control_paractises,
        properties,
        emissionsfactor_value,
        emissionsfactor_units,
        ipcc_equation,
        data_source,
        ipcc_worksheet,
        technical_reference,
        dataset_name
    FROM {{ df_1 }} 
),
transport_emission_factor_ex2 AS (
    SELECT 
        ef_id,
        ipcc_sector,
        UNNEST(STRING_SPLIT(gas_multi, '|')) AS gas,
        fuel_1996,
        fuel_2006,
        type_parameter,
        Description,
        technologies_paractises,
        parameters_conditions,
        region,
        control_paractises,
        properties,
        emissionsfactor_value,
        emissionsfactor_units,
        ipcc_equation,
        data_source,
        ipcc_worksheet,
        technical_reference,
        dataset_name
    FROM transport_emission_factor_ex
    WHERE TRIM(ipcc_sector) <> ''
),
transport_emission_factor_clean AS (
    SELECT 
        CASE 
            WHEN ipcc_sector = '1A3b1 - Cars' THEN 'Passenger Automobiles'
            WHEN ipcc_sector = '1A3b4 - Motorcycles' THEN 'Motorcycle'
            WHEN ipcc_sector = '1A3b - Road Transportation' THEN 'Heavy Duty Trucks and Buses, Light Duty Truck, Motorcycle, Passenger Automobiles'
            WHEN ipcc_sector = '1A3b2 - Light Duty Trucks' THEN 'Light Duty Truck'
            WHEN ipcc_sector = '1A3b3 - Heavy Duty Trucks and Buses' THEN 'Heavy Duty Trucks and Buses'
        END AS vehicle_type,
        fuel_2006 AS fuel_type,
        CASE
            WHEN gas = 'METHANE' THEN 'CH4'
            WHEN gas = 'NITROUS OXIDE' THEN 'N2O'
            WHEN gas = 'CARBON DIOXIDE' THEN 'CO2'
        END AS gas,
        CASE
            WHEN REGEXP_MATCHES(emissionsfactor_value, '(\d+\.?\d*)\s*-\s*(\d+\.?\d*)') THEN
                ROUND((
                    NULLIF(SPLIT_PART(REGEXP_EXTRACT(emissionsfactor_value, '(\d+\.?\d*)\s*-\s*(\d+\.?\d*)'), '-', 1), '')::decimal +
                    NULLIF(SPLIT_PART(REGEXP_EXTRACT(emissionsfactor_value, '(\d+\.?\d*)\s*-\s*(\d+\.?\d*)'), '-', 2), '')::decimal
                ) / 2.0::decimal, 3)
            WHEN NOT REGEXP_MATCHES(emissionsfactor_value, '[a-zA-Z]') THEN
                emissionsfactor_value::numeric
            ELSE NULL
        END AS emissionsfactor_value,
        emissionsfactor_units
    FROM transport_emission_factor_ex2
    WHERE gas IN ('METHANE', 'CARBON DIOXIDE', 'NITROUS OXIDE')
    AND emissionsfactor_units LIKE '%km%'
    AND type_parameter LIKE '%IPCC%'
    AND region IS NULL
),
transport_emission_factor_clean2 AS (
    SELECT 
        TRIM(vehicle_type) AS vehicle_type,
        fuel_type,
        gas, 
        CASE 
            WHEN emissionsfactor_units = 'mg/km' THEN emissionsfactor_value / 1000 
            ELSE emissionsfactor_value 
        END AS emissionsfactor_value,
        'g/km' AS emissionsfactor_units
    FROM (
        SELECT 
            UNNEST(STRING_SPLIT(vehicle_type, ',')) AS vehicle_type,
            fuel_type,
            gas,
            emissionsfactor_value,
            emissionsfactor_units
        FROM transport_emission_factor_clean
    )
),
transport_emission_factor_clean3 AS (
    SELECT 
        vehicle_type,
        fuel_type,
        gas, 
        emissionsfactor_value / 1000 AS emissionsfactor_value,
        'kg/km' AS units
    FROM transport_emission_factor_clean2
)
SELECT 
    vehicle_type,
    fuel_type,
    gas, 
    AVG(emissionsfactor_value) AS emissionsfactor_value,
    'kg/km' AS units
FROM transport_emission_factor_clean3
GROUP BY vehicle_type, fuel_type, gas
ORDER BY vehicle_type, fuel_type, gas;
