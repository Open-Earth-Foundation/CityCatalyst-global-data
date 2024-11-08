# Python dictionary to map GPC reference numbers to their scope and description

gpc_mappings = {
    "__doc__": """
    This dictionary maps GPC (Global Protocol for Community-Scale Greenhouse Gas Emission Inventories) reference numbers to their corresponding scopes and descriptions.

    The GPC reference numbers follow the format 'x.y.z'.

    'x' uses roman numerals and represents the sector of the emission source and is one of the following:
    - 'I' represents 'Stationary Energy'
    - 'II' represents 'Transportation'
    - 'III' represents 'Waste'
    - 'IV' represents 'Industrial Processes and Product Use (IPPU)'
    - 'V' represents 'Agriculture, forestry, and other land use (AFOLU)'
    - 'VI' represents 'Other Scope 3'

    'y' uses Arabic numerals and represents the subsector of the emission source within the sector and is one of the following:
    - for sector 'Stationary Energy'
        - '1' represents 'Residential Buildings'
        - '2' represents 'Commercial and institutional buildings and facilities'
        - '3' represents 'Manufacturing industries and construction'
        - '4' represents 'Energy industries'
        - '5' represents 'Agriculture, forestry and fishing activities'
        - '6' represents 'Non-specified sources'
        - '7' represents 'Fugitive emissions from mining, processing, storage, and Transportation of coal'
        - '8' represents 'Fugitive emissions from oil and natural gas systems'
    - for sector 'Transportation'
        - '1' represents 'On-road Transportation'
        - '2' represents 'Railways'
        - '3' represents 'Waterborne navigation'
        - '4' represents 'Aviation'
        - '5' represents 'Off-road Transportation'
    - for sector 'Waste'
        - '1' represents 'Solid waste disposal'
        - '2' represents 'Biological treatment of waste'
        - '3' represents 'Incineration and open burning'
        - '4' represents 'Wastewater treatment and discharge'

    'z' uses Arabic numerals and represents the scope of the emission source within the sector and the subsector and is one of the following:
    - '1' represents Scope 1 emissions, which are emissions within the city boundary
    - '2' represents Scope 2 emissions, which are emissions from grid-supplied energy consumed within the city boundary
    - '3' represents Scope 3 emissions, which are emissions from transmission and distribution losses from grid-supplied energy consumption

    There are certain assumptions made, that will always apply to the GPC reference numbers:
    - Combustion of fuels or consumption of fuels is always considered to be scope 1 emissions.
    - Grid-supplied energy like electricity, heat, cold and steam is always considered to be scope 2 emissions
    Those assumptions are to be followed over all other mappings you are provided with. 
    - Each activity data can only be associated with one single GPC reference number, and it can never be associated with multiple GPC reference numbers.

    Example entries:
    - "I.1.1": Represents emissions within the sector 'Stationary Energy' and the subsector 'Residential Buildings' from fuel combustion within the city boundary (Scope 1)
    - "II.2.2": Represents emissions within the sector 'Transportation' and the subsector 'Railways' from grid-supplied energy consumed within the city boundary (Scope 2)
    """,
    "I.1.1": {
        "Scope": 1,
        "Description": "Emissions from fuel combustion within the city boundary",
    },
    "I.1.2": {
        "Scope": 2,
        "Description": "Emissions from grid-supplied energy consumed within the city boundary",
    },
    "I.1.3": {
        "Scope": 3,
        "Description": "Emissions from transmission and distribution losses from grid-supplied energy consumption",
    },
    "I.2.1": {
        "Scope": 1,
        "Description": "Emissions from fuel combustion within the city boundary",
    },
    "I.2.2": {
        "Scope": 2,
        "Description": "Emissions from grid-supplied energy consumed within the city boundary",
    },
    "I.2.3": {
        "Scope": 3,
        "Description": "Emissions from transmission and distribution losses from grid-supplied energy consumption",
    },
    "I.3.1": {
        "Scope": 1,
        "Description": "Emissions from fuel combustion within the city boundary",
    },
    "I.3.2": {
        "Scope": 2,
        "Description": "Emissions from grid-supplied energy consumed within the city boundary",
    },
    "I.3.3": {
        "Scope": 3,
        "Description": "Emissions from transmission and distribution losses from grid-supplied energy consumption",
    },
    "I.4.1": {
        "Scope": 1,
        "Description": "Emissions from energy used in power plant auxiliary operations within the city boundary",
    },
    "I.4.2": {
        "Scope": 2,
        "Description": "Emissions from grid-supplied energy consumed in power plant auxiliary operations within the city boundary",
    },
    "I.4.3": {
        "Scope": 3,
        "Description": "Emissions from transmission and distribution losses from grid-supplied energy consumption in power plant auxiliary operations",
    },
    "I.4.4": {
        "Scope": 1,
        "Description": "Emissions from energy generation supplied to the grid",
    },
    "I.5.1": {
        "Scope": 1,
        "Description": "Emissions from fuel combustion within the city boundary",
    },
    "I.5.2": {
        "Scope": 2,
        "Description": "Emissions from grid-supplied energy consumed within the city boundary",
    },
    "I.5.3": {
        "Scope": 3,
        "Description": "Emissions from transmission and distribution losses from grid-supplied energy consumption",
    },
    "I.6.1": {
        "Scope": 1,
        "Description": "Emissions from fuel combustion within the city boundary",
    },
    "I.6.2": {
        "Scope": 2,
        "Description": "Emissions from grid-supplied energy consumed within the city boundary",
    },
    "I.6.3": {
        "Scope": 3,
        "Description": "Emissions from transmission and distribution losses from grid-supplied energy consumption",
    },
    "I.7.1": {
        "Scope": 1,
        "Description": "Emissions from fugitive emissions within the city boundary",
    },
    "I.8.1": {
        "Scope": 1,
        "Description": "Emissions from fugitive emissions within the city boundary",
    },
    "II.1.1": {
        "Scope": 1,
        "Description": "Emissions from fuel combustion on-road Transportation occurring within the city boundary",
    },
    "II.1.2": {
        "Scope": 2,
        "Description": "Emissions from grid-supplied energy consumed within the city boundary for on-road Transportation",
    },
    "II.1.3": {
        "Scope": 3,
        "Description": "Emissions from portion of transboundary journeys occurring outside the city boundary, and transmission and distribution losses from grid-supplied energy consumption",
    },
    "II.2.1": {
        "Scope": 1,
        "Description": "Emissions from fuel combustion for railway Transportation occurring within the city boundary",
    },
    "II.2.2": {
        "Scope": 2,
        "Description": "Emissions from grid-supplied energy consumed within the city boundary for railways",
    },
    "II.2.3": {
        "Scope": 3,
        "Description": "Emissions from portion of transboundary journeys occurring outside the city boundary, and transmission and distribution losses from grid-supplied energy consumption",
    },
    "II.3.1": {
        "Scope": 1,
        "Description": "Emissions from fuel combustion for waterborne navigation occurring within the city boundary",
    },
    "II.3.2": {
        "Scope": 2,
        "Description": "Emissions from grid-supplied energy consumed within the city boundary for waterborne navigation",
    },
    "II.3.3": {
        "Scope": 3,
        "Description": "Emissions from portion of transboundary journeys occurring outside the city boundary, and transmission and distribution losses from grid-supplied energy consumption",
    },
    "II.4.1": {
        "Scope": 1,
        "Description": "Emissions from fuel combustion for aviation occurring within the city boundary",
    },
    "II.4.2": {
        "Scope": 2,
        "Description": "Emissions from grid-supplied energy consumed within the city boundary for aviation",
    },
    "II.4.3": {
        "Scope": 3,
        "Description": "Emissions from portion of transboundary journeys occurring outside the city boundary, and transmission and distribution losses from grid-supplied energy consumption",
    },
    "II.5.1": {
        "Scope": 1,
        "Description": "Emissions from fuel combustion for off-road Transportation occurring within the city boundary",
    },
    "II.5.2": {
        "Scope": 2,
        "Description": "Emissions from grid-supplied energy consumed within the city boundary for off-road Transportation",
    },
    "III.1.1": {
        "Scope": 1,
        "Description": "Emissions from solid 'Waste' generated within the city boundary and disposed in landfills or open dumps within the city boundary",
    },
    "III.1.2": {
        "Scope": 3,
        "Description": "Emissions from solid 'Waste' generated within the city boundary but disposed in landfills or open dumps outside the city boundary",
    },
    "III.1.3": {
        "Scope": 1,
        "Description": "Emissions from 'Waste' generated outside the city boundary and disposed in landfills or open dumps within the city boundary",
    },
    "III.2.1": {
        "Scope": 1,
        "Description": "Emissions from solid 'Waste' generated within the city boundary that is treated biologically within the city boundary",
    },
    "III.2.2": {
        "Scope": 3,
        "Description": "Emissions from solid 'Waste' generated within the city boundary but treated biologically outside of the city boundary",
    },
    "III.2.3": {
        "Scope": 1,
        "Description": "Emissions from 'Waste' generated outside the city boundary but treated biologically within the city boundary",
    },
    "III.3.1": {
        "Scope": 1,
        "Description": "Emissions from solid 'Waste' generated and treated within the city boundary",
    },
    "III.3.2": {
        "Scope": 3,
        "Description": "Emissions from solid 'Waste' generated within the city boundary but treated outside of the city boundary",
    },
    "III.3.3": {
        "Scope": 1,
        "Description": "Emissions from 'Waste' generated outside the city boundary but treated within the city boundary",
    },
    "III.4.1": {
        "Scope": 1,
        "Description": "Emissions from 'Waste'water generated and treated within the city boundary",
    },
    "III.4.2": {
        "Scope": 3,
        "Description": "Emissions from 'Waste'water generated within the city boundary but treated outside of the city boundary",
    },
    "III.4.3": {
        "Scope": 1,
        "Description": "Emissions from 'Waste'water generated outside the city boundary but treated within the city boundary",
    },
    "IV.1": {
        "Scope": 1,
        "Description": "Emissions from industrial processes occurring within the city boundary",
    },
    "IV.2": {
        "Scope": 1,
        "Description": "Emissions from product use occurring within the city boundary",
    },
    "V.1": {
        "Scope": 1,
        "Description": "Emissions from livestock within the city boundary",
    },
    "V.2": {"Scope": 1, "Description": "Emissions from land within the city boundary"},
    "V.3": {
        "Scope": 1,
        "Description": "Emissions from aggregate sources and non-CO2 emission sources on land within the city boundary",
    },
    "VI.1": {
        "Scope": 3, 
        "Description": "Other Scope 3"},
}
