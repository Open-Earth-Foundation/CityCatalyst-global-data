# Python dictionary to map the activity types and the important columns to conserve in a dataframe

white_list_mapping = {
    "__doc__": """
    This dictionary maps the most common activity data types and the important columns to conserve in a dataframe.

    Examples:
    - from fuel sales datasets, we need to conserve the following columns: 'period', 'city', 'product', 'operator', 'distribution channel', 'volume', 'units', 'transport_type'
    - from electricity consumption datasets, we need to conserve the following columns: 'date', 'region', 'energy type', 'final users', 'energy consumed', 'units'
    """,

    "fuel sales": {
        "period": {
            "data_type": "datetime",
            "description": "The period of time the data refers to",
            "examples": ["2020-01-01", "2020-01-01 00:00:00", "2020", "2020-01", "2020 January"]
        },
        "city": {
            "data_type": "string",
            "description": "The city where the data was collected or where the fuel was sold",
            "examples": ["New York", "Mendoza", "Sao Paulo"]
        },
        "locode": {
            "data_type": "string",
            "description": "The location code of the city where the data was collected or where the fuel was sold, according to the UN/LOCODE standard",
            "examples": ["US NYC", "AR MZA", "BR SPO"]
        },
        "product": {
            "data_type": "string",
            "description": "The product sold",
            "examples": ["diesel", "petrol", "gasoline"]
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that sold the fuel",
            "examples": ["YPF", "Shell", "Petrobras"]
        },
        "distribution channel": {
            "data_type": "string",
            "description": "Categorizes the different sectors or channels through which fuel is distributed or sold in the city",
            "examples": ["fuel sales in gas stations", "Service stations, storage and distribution", "Freight transport"]
        },
        "volume": {
            "data_type": "float",
            "description": "The volume of fuel sold",
            "examples": [1000, 20000, 300.9]
        },
        "units": {
            "data_type": "string",
            "description": "The units in which the volume of fuel is measured",
            "examples": ["liters", "gallons", "cubic meters", "L", "m3", "gal"] 
        },
        "coordinates": {
            "data_type": "float",
            "description": "The coordinates of the location where the fuel was sold (latitude, longitude)",
            "examples": [-34.61, -58.38]
        },
        "location": {
            "data_type": "string",
            "description": "The location where the fuel was sold",
            "examples": ["Av. Corrientes 1234, Buenos Aires", "Av. Paulista 1234, Sao Paulo"]
        }
    },
    "fuel consumption": {
        "period": {
            "data_type": "datetime",
            "description": "The period of time the data refers to",
            "examples": ["2020-01-01", "2020-01-01 00:00:00", "2020", "2020-01", "2020 January"]
        },
        "city": {
            "data_type": "string",
            "description": "The city where the data was collected or where the fuel was consumed",
            "examples": ["New York", "Mendoza", "Sao Paulo"]
        },
        "product": {
            "data_type": "string",
            "description": "The product consumed",
            "examples": ["natural gas", "gasoline"]
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that distributes the fuel",
            "examples": ["Metrogas", "Edenor", "Petrobras"]
        },
        "final user": {
            "data_type": "string",
            "description": "The final user of the fuel",
            "examples": ["residential", "commercial", "transportation"]
        },
        "industry type": {
            "data_type": "string",
            "description": "The type of industry where the fuel was consumed",
            "examples": ["Energy Industry", "Petroleum and Natural Gas Systems", "Power Plants"]
        },
        "volume": {
            "data_type": "float",
            "description": "The volume of fuel consumed",
            "examples": [1000, 20000, 300.9]
        },
        "units": {
            "data_type": "string",
            "description": "The units in which the volume of fuel is measured",
            "examples": ["liters", "gallons", "cubic meters", "L", "m3", "gal"]
        },
        "location": {
            "data_type": "string",
            "description": "The location where the fuel was consumed",
            "examples": ["Av. Corrientes 1234, Buenos Aires", "Av. Paulista 1234, Sao Paulo"]
        }
    },
    "energy consumption": {
        "date": {
            "data_type": "datetime",
            "description": "The period of time the data refers to",
            "examples": ["2020-01-01", "2020-01-01 00:00:00", "2020", "2020-01", "2020 January"]
        },
        "region": {
            "data_type": "string",
            "description": "The region where the data was collected or where the energy was consumed",
            "examples": ["California", "Buenos Aires", "Sao Paulo"]
        },
        "locode": {
            "data_type": "string",
            "description": "The location code of the region where the data was collected or where the energy was consumed, according to the UN/LOCODE standard",
            "examples": ["US CA", "AR BUE", "BR SPO"]
        },
        "energy type": {   
            "description": "The type of energy consumed, this can be also energy sources",
            "data_type": "string",
            "examples": ["electricity", "electric power", "heating", "steam", "cooling"]
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that distributes the energy",
            "examples": ["Edison", "Enel", "AES"]
        },
        "facility name": {
            "data_type": "string",
            "description": "The name of the facility where the fuel was consumed",
            "examples": ["Hospital de Clinicas", "Casa Rosada", "Estadio Monumental"]
        },
        "industry type": {
            "data_type": "string",
            "description": "The type of industry where the fuel was consumed",
            "examples": ["Energy Industry", "Petroleum and Natural Gas Systems", "Power Plants"]
        },
        "final users": {
            "data_type": "string",
            "description": "The final users of the energy, e.g. residential, commercial, transportation, etc.",
            "examples": ["residential", "commercial", "transportation"]
        },
        "energy consumed": {    ## 
            "data_type": "float",
            "description": "The amount of energy consumed. This can be also final consumption or consumption",
            "examples": [1000, 20000, 300.9]
        },
        "units": {
            "data_type": "string",
            "description": "The units in which the energy consumed is measured",
            "examples": ["kWh", "MWh", "GWh", "Joules"]
        },
        "location": {
            "data_type": "string",
            "description": "The location where the energy was consumed",
            "examples": ["Av. Corrientes 1234, Buenos Aires", "Av. Paulista 1234, Sao Paulo"]
        }
    }
}