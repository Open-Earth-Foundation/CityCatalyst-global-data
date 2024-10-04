# Python dictionary to map the activity types and the important columns to conserve in a dataframe

white_list_mapping = {
    "__doc__": """
    This dictionary maps the most common activity data types and the important columns to conserve in a dataframe.

    Examples:
    - from fuel sales datasets, we need to conserve the following columns: 'period', 'city', 'product', 'operator', 'distribution channel', 'volume', 'units', 'transport_type'
    - from electricity consumption datasets, we need to conserve the following columns: 'date', 'region', 'energy type', 'final users', 'energy consumed', 'units'
    """,

    "fuel sales": {
        [
            "period",
            "city",
            "product",
            "operator",
            "fuel type",
            "distribution channel",
            "volume",
            "units",
            "transport_type",
            "coordinates"
            "location"
        ]
    },
    "fuel consumption": {
        [
            "period",
            "city",
            "product",
            "operator",
            "fuel type",
            "final user",
            "volume",
            "units",
            "location"
        ]
    },
    "energy consumption": {
        [
            "date",
            "region",
            "energy type",
            "operator",
            "final users",
            "units",
            "location"
        ]
    }
}