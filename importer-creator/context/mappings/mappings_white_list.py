# Python dictionary to map the activity types and the important columns to conserve in a dataframe

white_list_mapping = {
    "__doc__": """
    This dictionary maps the most common activity data types and the important columns to conserve in a dataframe.

    Examples:
    - from fuel sales datasets, we need to conserve the following columns: 'period', 'city', 'product', 'operator', 'distribution channel', 'volume', 'units', 'transport_type'
    - from electricity consumption datasets, we need to conserve the following columns: 'date', 'region', 'energy type', 'final users', 'energy consumed', 'units'
    """,

    "fuel sales": {
        "period": "datetime",
        "city": "string",
        "product": "string",
        "operator": "string",
        "fuel type": "string",
        "distribution channel": "string",
        "volume": "float",
        "units": "string",
        "transport_type": "string",
        "coordinates": "float",
        "location": "string"
    },
    "fuel consumption": {
        "period": "datetime",
        "city": "string",
        "product": "string",
        "operator": "string",
        "fuel type": "string",
        "final user": "string",
        "volume": "float",
        "units": "string",
        "location": "string"
    },
    "energy consumption": {
        "date": "datetime",
        "region": "string",
        "energy type": "string",
        "operator": "string",
        "final users": "string",
        "energy consumed": "float",
        "units": "string",
        "location": "string"
    }
}