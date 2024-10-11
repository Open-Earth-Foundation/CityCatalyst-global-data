# Python dictionary to map the activity types and the important columns to conserve in a dataframe

white_list_mapping = {
    "__doc__": """
    This dictionary maps the most common Global Protocol for Community-Scale Greenhouse Gas Emission Inventories (GPC) activity data types 'fuel_sales', 'fuel_consumption' and 'electricity_consumption' and the important columns to conserve in a dataframe.
    Each activity data type has a description of what kind of data falls into that respective category and a list of columns with their data type and description.
    Each dataset con only be associated with on of the activity data types. This means, that only the described columns of one of the activity data types can be conserved in the dataframe.
    Do not mix columns of different activity data types in the same dataframe.

    Instructions for the LLM:
    - Names in datasets may not match these names below exactly but can be identified by their descriptions or examples.
    - Focus on identifying semantically similar terms, synonyms, or variations in dataset names.
    - The column names in this dictionary represent common terms. If a dataset uses different terminology for a concept (e.g., 'energy source' instead of 'energy type'), map accordingly.

    Examples:
    - from fuel sales datasets, we need to conserve the following columns: 'period', 'city', 'product', 'operator', 'user type', 'volume', 'units', 'coordinates', 'location'
    - from electricity consumption datasets, we need to conserve the following columns: 'date', 'region', 'energy type', 'final users', 'energy consumed', 'units', 'location'

    The names given in this dictionary are indicative and can be changed according to the specific dataset.
    """,
    "fuel_sales": {
        # Please check description and improve maybe for all 3 @ Mau
        "description": "This activity data type refers to data related to the sale of fuels (like propane, diesel, natural gases and so on).",
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
        "city": {
            "data_type": "string",
            "description": "The city where the data was collected or where the fuel was sold",
            "examples": ["New York", "Mendoza", "Sao Paulo"],
        },
        "locode": {
            "data_type": "string",
            "description": "The location code of the city where the data was collected or where the fuel was sold, according to the UN/LOCODE standard",
            "examples": ["US NYC", "AR-MZA", "BRSPO"],
        },
        "product": {
            "data_type": "string",
            "description": "The product sold (fuel type)",
            "examples": ["diesel", "petrol", "gasoline"],
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that sold the fuel. This can be also the company that distributes the fuel",
            "examples": ["YPF", "Shell", "Petrobras"],
        },
        "user_type": {
            "data_type": "string",
            "description": "Classifies the different sectors, users or channels through which fuel is sold, consumed or distributed in the city",
            "examples": [
                "fuel sales in gas stations",
                "Service stations, storage and distribution",
                "Freight transport",
            ],
        },
        "volume": {
            "data_type": "float",
            "description": "The volume of fuel sold",
            "examples": [1000, 20000, 300.9],
        },
        "units": {
            "data_type": "string",
            "description": "The units in which the volume of fuel is measured",
            "examples": ["liters", "gallons", "cubic meters", "L", "m3", "gal"],
        },
        "coordinates": {
            "data_type": "float",
            "description": "The coordinates of the location where the fuel was sold (latitude, longitude)",
            "examples": [-34.61, -58.38],
        },
        "location": {
            "data_type": "string",
            "description": "The location where the fuel was sold",
            "examples": [
                "Av. Corrientes 1234, Buenos Aires",
                "Av. Paulista 1234, Sao Paulo",
            ],
        },
    },
    "fuel_consumption": {
        "description": "This activity data type refers to data related to the consumption of fuels (like propane, diesel, natural gases and so on). E.g. burning those fuels or similar",  # Please check and improve @ Mau
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
        "city": {  # difference to 'region' below in electricity_consumption @ Mau?
            "data_type": "string",
            "description": "The city where the data was collected or where the fuel was consumed",
            "examples": ["New York", "Mendoza", "Sao Paulo"],
        },
        "product": {
            "data_type": "string",
            "description": "The fuel consumed (fuel type)",
            "examples": ["natural gas", "gasoline", "diesel"],
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that distributes the fuel",
            "examples": ["Metrogas", "Edenor", "Petrobras"],
        },
        "final_user": {
            "data_type": "string",
            "description": "The final user of the fuel or the sector where the fuel was consumed",
            "examples": ["residential", "commercial", "transportation", "industrial"],
        },
        "industry_type": {
            "data_type": "string",
            "description": "The type of industry where the fuel was consumed",
            "examples": [
                "Energy Industry",
                "Petroleum and Natural Gas Systems",
                "Power Plants",
            ],
        },
        "volume": {
            "data_type": "float",
            "description": "The volume of fuel consumed",
            "examples": [1000, 20000, 300.9],
        },
        "units": {
            "data_type": "string",
            "description": "The units in which the volume of fuel is measured",
            "examples": ["liters", "gallons", "cubic meters", "L", "m3", "gal"],
        },
        "location": {
            "data_type": "string",
            "description": "The location where the fuel was consumed",
            "examples": [
                "Av. Corrientes 1234, Buenos Aires",
                "Av. Paulista 1234, Sao Paulo",
            ],
        },
    },
    "electricity_consumption": {
        "description": "This activity data type refers to data related to the consumption of electricity (electric energy)",  # Please check and improve @ Mau
        "date": {
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
        "region": {  # does this include countries? @ Mau Also
            "data_type": "string",
            "description": "The region where the data was collected or where the energy was consumed",
            "examples": ["California", "Buenos Aires", "Sao Paulo"],
        },
        "locode": {
            "data_type": "string",
            "description": "The location code of the region where the data was collected or where the energy was consumed, according to the UN/LOCODE standard",
            "examples": ["US CA", "AR-BUE", "BRSPO"],
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that distributes the energy",
            "examples": ["Edison", "Enel", "AES"],
        },
        "facility_name": {
            "data_type": "string",
            "description": "The name of the facility where the fuel was consumed",
            "examples": ["Hospital de Clinicas", "Casa Rosada", "Estadio Monumental"],
        },
        "industry_type": {
            "data_type": "string",
            "description": "The type of industry where the fuel was consumed",
            "examples": [
                "Energy Industry",
                "Petroleum and Natural Gas Systems",
                "Power Plants",
            ],
        },
        "final_user": {
            "data_type": "string",
            "description": "The final user of the energy or the sector where the energy was consumed",
            "examples": ["residential", "commercial", "transportation"],
        },
        "electricity_consumed": {
            "data_type": "float",
            "description": "The amount of electricity consumed. This can be also final consumption or consumption",
            "examples": [1000, 20000, 300.9],
        },
        "units": {
            "data_type": "string",
            "description": "The units in which the electricity consumed is measured",
            "examples": ["kWh", "MWh", "GWh", "Joules"],
        },
        "location": {
            "data_type": "string",
            "description": "The location where the electricity was consumed",
            "examples": [
                "Av. Corrientes 1234, Buenos Aires",
                "Av. Paulista 1234, Sao Paulo",
            ],
        },
    },
}
