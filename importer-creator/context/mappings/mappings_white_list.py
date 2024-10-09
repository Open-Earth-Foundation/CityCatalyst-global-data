# Python dictionary to map the activity types and the important columns to conserve in a dataframe

white_list_mapping = {
    "__doc__": """
    This dictionary maps the most common activity data types 'fuel_sales', 'fuel_consumption' and 'energy_consumption' and the important columns to conserve in a dataframe.
    Each activity data type has a description of what kind of data falls into that respective category and a list of columns with their data type and description.

    Instructions for the LLM:
    - Names in datasets may not match these names below exactly but can be identified by their descriptions.
    - Focus on identifying semantically similar terms, synonyms, or variations in dataset names.
    - The column names in this dictionary represent common terms. If a dataset uses different terminology for a concept (e.g., 'energy source' instead of 'energy type'), map accordingly.

    Examples:
    - from fuel sales datasets, we need to conserve the following columns: 'period', 'city', 'product', 'operator', 'distribution channel', 'volume', 'units', 'transport_type'
    - from electricity consumption datasets, we need to conserve the following columns: 'date', 'region', 'energy type', 'final users', 'energy consumed', 'units'

    The names given in this dictionary are indicative and can be changed according to the specific dataset.
    """,
    "fuel_sales": {
        "description": "Mapping of columns relevant for fuel sales data, which typically includes sales of products like diesel or gasoline. Common variations may include ...",
        "period": {
            "data_type": "datetime",
            "description": "The period of time the data refers to",
        },
        "city": {
            "data_type": "string",
            "description": "The city where the data was collected or where the fuel was sold",
        },
        "locode": {
            "data_type": "string",
            "description": "The location code of the city where the data was collected or where the fuel was sold, according to the UN/LOCODE standard",
        },
        "product": {
            "data_type": "string",
            "description": "The product sold, e.g. diesel, petrol, gasoline, etc.",
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that sold the fuel",
        },
        "fuel_type": {
            "data_type": "string",
            "description": "The type of fuel sold",  ## ask Minh about this (same as product?)
        },
        "distribution channel": {
            "data_type": "string",
            "description": "Categorizes the different sectors or channels through which fuel is distributed or sold in the city",
        },
        "volume": {"data_type": "float", "description": "The volume of fuel sold"},
        "units": {
            "data_type": "string",
            "description": "The units in which the volume of fuel is measured",
        },
        "coordinates": {
            "data_type": "float",
            "description": "The coordinates of the location where the fuel was sold (latitude, longitude)",
        },
        "location": {
            "data_type": "string",
            "description": "The location where the fuel was sold",
        },
    },
    "fuel_consumption": {
        "description": "Mapping of columns relevant for fuel consumption data like liquid fuels consumption and gas consumption, including the consumption of different fuel types by various users. Common variations may include ...",
        "period": {
            "data_type": "datetime",
            "description": "The period of time the data refers to",
        },
        "city": {
            "data_type": "string",
            "description": "The city where the data was collected or where the fuel was consumed",
        },
        "product": {
            "data_type": "string",
            "description": "The product consumed, e.g. diesel, petrol, gasoline, etc.",
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that distributes the fuel",
        },
        "fuel_type": {
            "data_type": "string",
            "description": "The type of fuel consumed",
        },
        "final_user": {
            "data_type": "string",
            "description": "The final user of the fuel, e.g. residential, commercial, transportation, etc.",
        },
        "facility_name": {
            "data_type": "string",
            "description": "The name of the facility where the fuel was consumed",
        },
        "industry_type": {
            "data_type": "string",
            "description": "The type of industry where the fuel was consumed",
        },
        "volume": {"data_type": "float", "description": "The volume of fuel consumed"},
        "units": {
            "data_type": "string",
            "description": "The units in which the volume of fuel is measured",
        },
        "location": {
            "data_type": "string",
            "description": "The location where the fuel was consumed",
        },
    },
    "energy_consumption": {
        "description": "Mapping of columns relevant for energy consumption data, focusing on the consumption of energy types like electricity, steam, and/or heating/cooling across regions and sectors. Common variations may include ...",
        "date": {
            "data_type": "datetime",
            "description": "The period of time the data refers to",
        },
        "region": {
            "data_type": "string",
            "description": "The region where the data was collected or where the energy was consumed",
        },
        "locode": {
            "data_type": "string",
            "description": "The location code of the region where the data was collected or where the energy was consumed, according to the UN/LOCODE standard",
        },
        "energy_type": {  ## this can be also "energy sources"
            "data_type": "string",
            "description": "The type of energy consumed",
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that distributes the energy",
        },
        "facility_name": {
            "data_type": "string",
            "description": "The name of the facility where the fuel was consumed",
        },
        "industry_type": {
            "data_type": "string",
            "description": "The type of industry where the fuel was consumed",
        },
        "final_users": {
            "data_type": "string",
            "description": "The final users of the energy, e.g. residential, commercial, transportation, etc.",
        },
        "energy_consumed": {  ## this can be also "final consumption" or "consumption"
            "data_type": "float",
            "description": "The amount of energy consumed",
        },
        "units": {
            "data_type": "string",
            "description": "The units in which the energy consumed is measured",
        },
        "location": {
            "data_type": "string",
            "description": "The location where the energy was consumed",
        },
    },
}
