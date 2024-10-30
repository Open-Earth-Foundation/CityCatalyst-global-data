# Python dictionary to map the activity types and the important columns to conserve in a dataframe

white_list_mapping = {
    "__doc__": """
    This dictionary describes common Global Protocol for Community-Scale Greenhouse Gas Emission Inventories (GPC) columns found in datasets to retain in a dataframe. 
    The column names may vary across datasets, but the descriptions and examples provided will help identify equivalent or semantically similar terms. 
    Focus on mapping dataset columns to the appropriate terms based on meaning, not exact name matches.

    Instructions for the LLM:
    - The dataset column names may not match the names below exactly. Focus on identifying semantically similar terms, synonyms, or variations in column names.
    - Use the descriptions and examples provided for each key in the dictionary to find the closest match for the column names in the dataset.

    Example 1: Mendoza city dataset
    Input Dataset: ['Period', 'Operator', 'Registration Number', 'Brand/Flag', 'Deregistration Date', 'Tax ID', 'Business Type', 'Address', 'Locality', 'Province', 'Product', 'Marketing/Distribution Channel', 'Price without Taxes', 'Price with Taxes', 'Volume', 'Pump Price', 'No Movements', 'Exempt']
    Retained Columns: ['Period', 'Operator', 'Address', 'Province', 'Product', 'Marketing/Distribution Channel', 'Volume']

    Explanation:
    - Period: Retained because it corresponds to the "period" key in the dictionary, representing the date or time period the data refers to (e.g., "2020-01-01").
    - Operator: Retained as it matches the "operator" key, indicating the entity responsible for selling or distributing fuel, essential for understanding the source of emissions (e.g., "YPF").
    - Address: Retained since it aligns with the "location" key, providing the detailed location where the activity occurs (e.g., "Av. Corrientes 1234, Buenos Aires").
    - Province: Retained because it maps to the "region" key, specifying the region where the data was collected (e.g., "Tucumán").
    - Product: Retained as it corresponds to the "product" key, indicating the type of fuel associated with the emissions (e.g., "diesel").
    - Marketing/Distribution Channel: Retained because it aligns with the "user_type" key, classifying the distribution channels or sectors involved in the fuel sale (e.g., "Service stations").
    - Volume: Retained since it matches the "volume" key, representing the measured quantity of fuel sold or consumed (e.g., 1017.63).

    Registration Number, Brand/Flag, Deregistration Date, Tax ID, Business Type, Locality, Price without Taxes, Price with Taxes, Pump Price, No Movements, Exempt, Price without taxes, Price with taxes, Pump price: These columns were removed because they do not correspond to any keys in the dictionary or are not essential for calculating emissions. For instance, price-related columns are not needed for emissions quantification, and administrative details like registration numbers are outside the scope of activity data.

    Example 2: UAE dataset
    Input Dataset: ['STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'ACTION', 'REF_AREA', 'Reference area', 'FREQ', 'Frequency of observation', 'TIME_PERIOD', 'Time period', 'MEASURE', 'Measure', 'UNIT_MEASURE', 'Unit of measure', 'SOURCE_DETAIL', 'Source', 'COAL_PRODUCT', 'Coal Product', 'OG_PRODUCT', 'Oil and Gas Product Types', 'OG_SECTOR', 'Oil and Gas Variables', 'NG_SECTOR', 'Natural Gas Variables', 'NL_SECTOR', 'Natural Gas Liquids Variables', 'OG_COAL', 'Coal Variables', 'CO_INPUT', 'Refineries Input Type', 'OBS_VALUE', 'Observation value', 'OBS_STATUS', 'Observation status', 'UNIT_MULT', 'Unit multiplier', 'OBS_COMMENT', 'Footnotes', 'DECIMALS', 'Decimals'],
    Retained Columns: ['STRUCTURE_NAME', 'REF_AREA', 'Reference area', 'Frequency of observation', 'Unit of measure', 'TIME_PERIOD', 'Source', 'Oil and Gas Product Types', 'OBS_VALUE']
    
    Explanation:
    - STRUCTURE_NAME: Retained as it may provide important metadata about the data structure, aiding in understanding the dataset's context.
    - REF_AREA: Retained because it correspond to the "locode" key, indicating the UN/LOCODE associated with the data (e.g., "AR-BRC").
    - Reference area: Retained because it correspond to the "region" key, indicating the geographical area associated with the data (e.g., "California").
    - Frequency of observation: Retained as it provides temporal information related to the "period" key, indicating how often data points are recorded.
    - Unit of measure: Retained since it matches the "units" key, specifying the measurement units of the observed values (e.g., "Kilowatt-hours (kWh)").
    - TIME_PERIOD: Retained because it aligns with the "period" key, representing the specific time frame of the data (e.g., "2020-01").
    - Source: Retained as it may contain valuable information about the data's origin, which is useful for validation and traceability.
    - Oil and Gas Product Types: Retained since it corresponds to the "product" key, detailing the types of oil and gas products involved (e.g., "natural gas").
    - OBS_VALUE: Retained because it aligns with the "volume" key, representing the measured quantity of the energy product consumed or produced (e.g., 21080).
    """,
    "columns": {
        "period": {
            "data_type": "datetime",
            "description": "The date of the datapoint or the period of time the data refers to",
            "examples": [
                "2020-01-01",
                "2020-01-01 00:00:00",
                "2018",
                "2021-05",
                "2023 March",
            ],
        },
        "region": {
            "data_type": "string",
            "description": "The region (e.g. a country or state or province) where the data was collected, that the activity data (e.g. energy consumption or fuel consumption) is associated with",
            "examples": ["California", "Tucumán", "Argentina"],
        },
        "city": {
            "data_type": "string",
            "description": "The city where the data was collected, that the activity data (e.g. energy consumption or fuel consumption) is associated with",
            "examples": ["New York", "Bariloche", "Sao Paulo"],
        },
        "locode": {
            "data_type": "string",
            "description": "The location code of the city where the data was collected, that the activity data (e.g. energy consumption or fuel consumption) is associated with, according to the UN/LOCODE standard which has a 2 letter code for the country and a 5 letter code for the country and city",
            "examples": ["USNYC", "AR-BRC", "BR SAO", "USCAL", "ARTUC", "AR"],
        },
        "coordinates": {
            "data_type": "float",
            "description": "The coordinates (latitude, longitude) of the location where the data was collected, that the activity data (e.g. energy consumption or fuel consumption) is associated with",
            "examples": [(40.7128, -74.0060), (35.6762, 139.6503)],
        },
        "location": {
            "data_type": "string",
            "description": "The detailed location (e.g. the address) where the activity occurs (e.g fuel was sold or consumed, or energy was consumed)",
            "examples": [
                "Av. Corrientes 1234, Buenos Aires",
                "Av. Paulista 1234, Sao Paulo",
            ],
        },
        "product": {
            "data_type": "string",
            "description": "The name of the product that is associated with creating the emissions and which the activity data refers to (e.g fuel type or electricity)",
            "examples": ["diesel", "petrol", "gasoline", "electricity"],
        },
        "operator": {
            "data_type": "string",
            "description": "The responsible entity (e.g., a fuel distributor, energy provider, or waste management company) which is associated with the activity (e.g., operation or delivery of energy services)",
            "examples": ["YPF", "Shell", "Petrobras", "Edenor"],
        },
        "user_type": {
            "data_type": "string",
            "description": "This category classifies the various sectors, users, or distribution channels involved in the sale, consumption, or distribution of fuel or electricity within a city. It includes both the final consumers and the sectors where the energy is used. Additionally, it covers end-users who consume electricity from the grid, those who utilize that electricity, and the specific sectors associated with its consumption",
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
            "description": "It refers to the measured quantity or volume of the activity responsible for creating the emissions (refer to the 'product' key), such as fuel, energy or electricity. It represents the quantity sold, consumed or distributed",
            "examples": [1017.63, 21080, 300.9],
        },
        "units": {
            "data_type": "string",
            "description": "This refers to the units in which the data is measured, including volume, energy, or other metrics (refer to the 'volumne' key). The units in which the data is measured or quantified",
            "examples": [
                "Liters (L)",
                "Gallons (gal)",
                "Cubic meters (m³)",
                "Kilowatt-hours (kWh)",
                "Megawatt-hours (MWh)",
                "Kilojoules (kJ)",
                "Kilowatts (kW)",
                "Tonne of Oil Equivalent (TEP)",
            ],
        },
        "source": {
            "data_type": "string",
            "description": "The source of the data, which could be an organization, a publication, a database, or any other entity that provides the data",
            "examples": ["EIA", "BP Statistical Review", "IEA", "Local government"],
        },
    },
}
