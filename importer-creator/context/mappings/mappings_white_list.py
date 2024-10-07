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
            "description": "The period of time the data refers to"
        },
        "city": {
            "data_type": "string",
            "description": "The city where the data was collected or where the fuel was sold"
        },
        "locode": {
            "data_type": "string",
            "description": "The location code of the city where the data was collected or where the fuel was sold, according to the UN/LOCODE standard"
        },
        "product": {
            "data_type": "string",
            "description": "The product sold, e.g. diesel, petrol, gasoline, etc."
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that sold the fuel"
        },
        "fuel type": {
            "data_type": "string",
            "description": "The type of fuel sold" ## ask Minh about this (same as product?)
        },
        "distribution channel": {
            "data_type": "string",
            "description": "Categorizes the different sectors or channels through which fuel is distributed or sold in the city"
        },
        "volume": {
            "data_type": "float",
            "description": "The volume of fuel sold"
        },
        "units": {
            "data_type": "string",
            "description": "The units in which the volume of fuel is measured"
        },
        "coordinates": {
            "data_type": "float",
            "description": "The coordinates of the location where the fuel was sold (latitude, longitude)"
        },
        "location": {
            "data_type": "string",
            "description": "The location where the fuel was sold"
        }
    },
    "fuel consumption": {
        "period": {
            "data_type": "datetime",
            "description": "The period of time the data refers to"
        },
        "city": {
            "data_type": "string",
            "description": "The city where the data was collected or where the fuel was consumed"
        },
        "product": {
            "data_type": "string",
            "description": "The product consumed, e.g. diesel, petrol, gasoline, etc."
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that distributes the fuel"
        },
        "fuel type": {
            "data_type": "string",
            "description": "The type of fuel consumed" 
        },
        "final user": {
            "data_type": "string",
            "description": "The final user of the fuel, e.g. residential, commercial, transportation, etc."
        },
        "facility name": {
            "data_type": "string",
            "description": "The name of the facility where the fuel was consumed"
        },
        "industry type": {
            "data_type": "string",
            "description": "The type of industry where the fuel was consumed"
        },
        "volume": {
            "data_type": "float",
            "description": "The volume of fuel consumed"
        },
        "units": {
            "data_type": "string",
            "description": "The units in which the volume of fuel is measured"
        },
        "location": {
            "data_type": "string",
            "description": "The location where the fuel was consumed"
        }
    },
    "energy consumption": {
        "date": {
            "data_type": "datetime",
            "description": "The period of time the data refers to"
        },
        "region": {
            "data_type": "string",
            "description": "The region where the data was collected or where the energy was consumed"
        },
        "locode": {
            "data_type": "string",
            "description": "The location code of the region where the data was collected or where the energy was consumed, according to the UN/LOCODE standard"
        },
        "energy type": {     ## this can be also "energy sources"
            "data_type": "string",
            "description": "The type of energy consumed"
        },
        "operator": {
            "data_type": "string",
            "description": "The company or entity that distributes the energy"
        },
        "facility name": {
            "data_type": "string",
            "description": "The name of the facility where the fuel was consumed"
        },
        "industry type": {
            "data_type": "string",
            "description": "The type of industry where the fuel was consumed"
        },
        "final users": {
            "data_type": "string",
            "description": "The final users of the energy, e.g. residential, commercial, transportation, etc."
        },
        "energy consumed": {    ## this can be also "final consumption" or "consumption"
            "data_type": "float",
            "description": "The amount of energy consumed"
        },
        "units": {
            "data_type": "string",
            "description": "The units in which the energy consumed is measured"
        },
        "location": {
            "data_type": "string",
            "description": "The location where the energy was consumed"
        }
    }
}