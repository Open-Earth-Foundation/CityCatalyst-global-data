# Python dictionary to map the activity types and the important columns to conserve in a dataframe

white_list_mapping = {
    "__doc__": """
    This dictionary maps the most common Global Protocol for Community-Scale Greenhouse Gas Emission Inventories (GPC) and the columns of interest to conserve in a dataframe. It is possible, that not all columns are present in the dataset.
    Each column name has a description of what kind of data falls into that respective column, the data type, and examples of the data.

    Hint:
    There are generally two types of energy sources: fuels - which contain all sorts of liquid and gas fuels - and energy - which refers to electric energy. 
    The terminology of 'energy' never refers to either fuel sales or fuel consumption.

    Instructions for the LLM:
    - Names in datasets may not match these names below exactly but can be identified by their descriptions or examples.
    - Focus on identifying semantically similar terms, synonyms, or variations in dataset names.
    - The column names in this dictionary represent common terms. If a dataset uses different terminology for a concept (e.g., 'energy source' instead of 'energy type'), map accordingly.

    Important:
    If you are unsure about the mapping of the columns and which ones to delete, do not delete any columns.
    
    Examples:
    ## now I'm not sure about the examples 
    - A dataset about fuel sales maps to the 'fuel_sales' 'activity data type' and should conserve the columns 'period', 'city', 'locode', 'product', 'operator', 'user_type', 'volume', 'units', 'coordinates', 'location'
    - A dataset about fuel consumption maps to the 'fuel_consumption' 'activity data type' and should conserve the columns 'period', 'city', 'product', 'operator', 'final_user', 'industry_type', 'volume', 'units', 'location'
    - A dataset about energy consumption maps to the 'electricity_consumption' 'activity data type' because electricity is considered energy and should conserve the columns 'date', 'region', 'locode', 'operator', 'facility_name', 'industry_type', 'final_user', 'electricity_consumed', 'units', 'location'

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
                "2020 January"
            ]
        },
        "region": {  
            "data_type": "string",
            "description": "The region where the data was collected, where the energy or fuel was consumed, or where the fuel was sold",
            "examples": [
                "California", 
                "Buenos Aires", 
                "Argentina"
            ]
        },
        "city": {
            "data_type": "string",
            "description": "The city where the data was collected, where the energy or fuel was consumed, or where the fuel was sold",
            "examples": [
                "New York", 
                "Mendoza", 
                "Sao Paulo"
            ]
        },
        "locode": {
            "data_type": "string",
            "description": "The location code of the city where the data was collected or where the fuel was sold, according to the UN/LOCODE standard",
            "examples": [
                "US NYC", 
                "AR-MZA", 
                "BRSPO",
                "AR"
            ]
        },
        "coordinates": {
            "data_type": "float",
            "description": "The coordinates of the location where the fuel was sold or consumed, also where the energy was consumed (latitude, longitude)",
            "examples": [
                -34.61, 
                -58.38
            ]
        },
        "location": {
            "data_type": "string",
            "description": "The location where the fuel was sold or consumed, also where the energy was consumed",
            "examples": [
                "Av. Corrientes 1234, Buenos Aires",
                "Av. Paulista 1234, Sao Paulo"
            ]
        },
        "product": {
            "data_type": "string",
            "description": "The name of the product sold or consumed (fuel type or electricity)",
            "examples": [
                "diesel", 
                "petrol", 
                "gasoline", 
                "electricity"
            ]
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that sold or distributes the fuel. This can also be the company that provides the electricity",
            "examples": [
                "YPF", 
                "Shell", 
                "Petrobras",
                "Edenor"
            ]
        },
        "user_type": {
            "data_type": "string",
            "description": "This category classifies the various sectors, users, or channels through which fuel is sold, consumed, or distributed within the city. It encompasses both the final consumers of fuel and the sectors where the fuel is utilized. This also includes end-users who consume electricity from the grid, those who utilize the electricity, and the specific sectors where the electricity is ultimately consumed.",
            "examples": [
                "fuel sales in gas stations",
                "Service stations, storage and distribution",
                "Freight transport",
                "Residential",
                "Commercial",
                "Power Plants"
            ]
        },
        "volume": {
            "data_type": "float",
            "description": "The volume or amount of fuel sold",
            "examples": [
                1000, 
                20000, 
                300.9
            ]
        },
        "units": {
            "data_type": "string",
            "description": "The units in which the volume of fuel is measured or the electricity consumption is quantified",
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
                "TEP"
            ]
        }
    }
}
