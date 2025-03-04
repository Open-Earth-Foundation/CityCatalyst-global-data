WITH data_raw AS (
SELECT City,Country,Region,Boundary,Year_calendar, Population,Area,GDP, "I.1.1"::varchar as "I.1.1","I.1.2"::varchar as "I.1.2","I.1.3","I.2.1","I.2.2"::varchar as "I.2.2","I.2.3","I.3.1","I.3.2","I.3.3","I.4.1","I.4.2","I.4.3","I.4.4","I.5.1","I.5.2","I.5.3","I.6.1","I.6.2","I.6.3","I.7.1","I.8.1","II.1.1"::varchar as "II.1.1","II.1.2","II.1.3","II.2.1","II.2.2","II.2.3","II.3.1","II.3.2","II.3.3","II.4.1","II.4.2","II.4.3","II.5.1","II.5.2","II.5.3","III.1.1","III.1.2","III.1.3","III.2.1","III.2.2","III.2.3","III.3.1","III.3.2","III.3.3","III.4.1","III.4.2","III.4.3","IV.1","IV.2","V.1","V.2","V.3","VI.1"
FROM {{df_1}}
),
flattened_data AS (
SELECT
    city,
    country,
    region,
    boundary,
    year_calendar as emissions_year,
    population,
    area,
    GDP,
    gpc_reference_number,
    emissions as emissions_value,
    'tonnes' as emissions_units,
    'co2eq' as gas_name
FROM
    data_raw
UNPIVOT (
    emissions FOR gpc_reference_number IN (
        "I.1.1", "I.1.2", "I.1.3", "I.2.1", "I.2.2", "I.2.3", "I.3.1", "I.3.2", "I.3.3", "I.4.1", "I.4.2", "I.4.3", "I.4.4", "I.5.1", "I.5.2", "I.5.3", "I.6.1", "I.6.2", "I.6.3", "I.7.1", "I.8.1",
        "II.1.1", "II.1.2", "II.1.3", "II.2.1", "II.2.2", "II.2.3", "II.3.1", "II.3.2", "II.3.3", "II.4.1", "II.4.2", "II.4.3", "II.5.1", "II.5.2", "II.5.3",
        "III.1.1", "III.1.2", "III.1.3", "III.2.1", "III.2.2", "III.2.3", "III.3.1", "III.3.2", "III.3.3", "III.4.1", "III.4.2", "III.4.3",
        "IV.1", "IV.2",
        "V.1", "V.2", "V.3",
        "VI.1"
    )
)
)
SELECT 	city,country,region,boundary,emissions_year,--population,area,GDP,
		gpc_reference_number,
		emissions_value::numeric*1000 as emissions_value,
		'kg'emissions_units,
		gas_name
FROM flattened_data
WHERE boundary NOT IN ('Province / District / State', 'County', 'Whole area of the TMG jurisdiction including island area', 'Multnomah County', 'Comprehensive Land Use Plan (CLUP)')
AND trim(emissions_value) NOT IN ('NO', 'NE', 'IE (II.1.1)', 'IE (I.1.1)', 'IE', 'C')