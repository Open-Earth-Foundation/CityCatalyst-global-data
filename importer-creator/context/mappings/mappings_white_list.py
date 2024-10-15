# Python dictionary to map the activity types and the important columns to conserve in a dataframe

white_list_mapping = {
    "__doc__": """
    This dictionary maps the most common Global Protocol for Community-Scale Greenhouse Gas Emission Inventories (GPC) and the columns of interest to conserve in a dataframe. It is possible, that not all columns are present in the dataset.
    Each column name has a description of what kind of data falls into that respective column, the data type, and examples of the data.

    Instructions for the LLM:
    - Names in datasets may not match these names below exactly but can be identified by their descriptions or examples.
    - Focus on identifying semantically similar terms, synonyms, or variations in dataset names.
    - The column names in this dictionary represent common terms. If a dataset uses different terminology for a concept (e.g., 'energy source' instead of 'energy type'), map accordingly.

    Important:
    If you are unsure about the mapping of the columns and which ones to delete, do not delete any columns.
    
    Examples:
    - example1: a dataset from Mendoza city has the following list of input columns ['Period', 'Operator', 'Registration Number', 'Brand/Flag', 'Deregistration Date', 'Tax ID', 'Business Type', 'Address', 'Locality', 'Province', 'Product', 'Marketing/Distribution Channel', 'Price without Taxes', 'Price with Taxes', 'Volume', 'Pump Price', 'No Movements', 'Exempt', 'Price without taxes', 'Price with taxes', 'Pump price'], 
    but the columns to conserve are ['Period', 'Operator', 'Address', 'Province', 'Product', 'Marketing/Distribution Channel', 'Volume']
    - example2: a dataset from UEA has the following list of input columns ['STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'ACTION', 'REF_AREA', 'Reference area', 'FREQ', 'Frequency of observation', 'TIME_PERIOD', 'Time period', 'MEASURE', 'Measure', 'UNIT_MEASURE', 'Unit of measure', 'SOURCE_DETAIL', 'Source', 'COAL_PRODUCT', 'Coal Product', 'OG_PRODUCT', 'Oil and Gas Product Types', 'OG_SECTOR', 'Oil and Gas Variables', 'NG_SECTOR', 'Natural Gas Variables', 'NL_SECTOR', 'Natural Gas Liquids Variables', 'OG_COAL', 'Coal Variables', 'CO_INPUT', 'Refineries Input Type', 'OBS_VALUE', 'Observation value', 'OBS_STATUS', 'Observation status', 'UNIT_MULT', 'Unit multiplier', 'OBS_COMMENT', 'Footnotes', 'DECIMALS', 'Decimals'],
    but the columns to conserve are ['STRUCTURE_NAME', 'REF_AREA', 'Reference area', 'Frequency of observation', 'Unit of measure', 'TIME_PERIOD', 'Source', 'Oil and Gas Product Types', 'OBS_VALUE']
    
    The names given in this dictionary are indicative and can be changed according to the specific dataset.
    """,
    "columns": {
        "period": {
            "data_type": "datetime",
            "description": "The period of time the data refers to",
            "examples": [
                "2020-01-01",
                "2020-01-01 00:00:00",
                "2020",
                "2020-01",
                "2020 January",
            ],
        },
        "region": {
            "data_type": "string",
            "description": "The region (e.g. a country or state or province) where the data was collected, that the activity data (e.g. energy consumption or fuel consumption) is associated with",
            "examples": [
                "California",
                "Tucumán", 
                "Argentina"
                ],
        },
        "city": {
            "data_type": "string",
            "description": "The city where the data was collected, that the activity data (e.g. energy consumption or fuel consumption) is associated with",
            "examples": [
                "New York", 
                "Bariloche", 
                "Sao Paulo"
                ],
        },
        "locode": {
            "data_type": "string",
            "description": "The location code of the city where the data was collected, that the activity data (e.g. energy consumption or fuel consumption) is associated with, according to the UN/LOCODE standard",
            "examples": [
                "USNY",
                "AR-BRC",
                "BR SAO",
                "USCAL",
                "ARTUC",
                "AR"
                ],
        },
        "coordinates": {
            "data_type": "float",
            "description": "The coordinates of the location where the data was collected, that the activity data (e.g. energy consumption or fuel consumption) is associated with (latitude, longitude)",
            "examples": [
                -34.61, 
                -58.38
                ],
        },
        "location": {
            "data_type": "string",
            "description": "The location where the actvity occurs (e.g fuel was sold or consumed, also where the energy was consumed)",
            "examples": [
                "Av. Corrientes 1234, Buenos Aires",
                "Av. Paulista 1234, Sao Paulo",
            ],
        },
        "product": {
            "data_type": "string",
            "description": "The name of the product to which the data refers (e.g fuel type or electricity)",
            "examples": ["diesel", "petrol", "gasoline", "electricity"],
        },
        "operator": {
            "data_type": "string",
            "description": "The entity (e.g., a company or organization) responsible for selling or distributing fuel or electricity, associated with the operation or delivery of energy services.",
            "examples": [
                "YPF", 
                "Shell", 
                "Petrobras", 
                "Edenor"
                ],
        },
        "user_type": {
            "data_type": "string",
            "description": "This category classifies the various sectors, users, or distribution channels involved in the sale, consumption, or distribution of fuel or electricity within a city. It includes both the final consumers and the sectors where the energy is used. Additionally, it covers end-users who consume electricity from the grid, those who utilize that electricity, and the specific sectors associated with its consumption.",
            "examples": [
                "fuel sales in gas stations",
                "Service stations, storage and distribution",
                "Freight transport",
                "Residential",
                "Commercial",
                "Power Plants",
            ],
        },
        "volume": {
            "data_type": "float",
            "description": "It refers to the measured quantity or volume of the data to which it refers, such as fuel, energy or electricity. It represents the quantity sold, consumed or distributed.",
            "examples": [
                1000, 
                20000, 
                300.9
                ],
        },
        "units": {
            "data_type": "string",
            "description": "This refers to the units in which the data is expressed. The units in which the data is measured or quantified",
            "examples": [
                "liters",
                "gallons",
                "cubic meters",
                "L",
                "m3",
                "gal",
                "kWh",
                "MWh",
                "kilojoules",
                "kilowatts",
                "TEP",
            ],
        },
    },
}
