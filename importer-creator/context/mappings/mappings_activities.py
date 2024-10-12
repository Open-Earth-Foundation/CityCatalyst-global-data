# Python dictionary to map the activity types with the GPC reference numbers and the activities names and subcategories

activity_mappings = {
    "__doc__": """
    This dictionary maps the most common Global Protocol for Community-Scale Greenhouse Gas Emission Inventories (GPC) activity data types 'fuel_sales', 'fuel_consumption' and 'electricity_consumption' and the corresponding "activity_names" and "activity_subcategories".
    Each activity data type has a list of GPC reference numbers that apply for each activity type, and the corresponding activity names and subcategories of each activity type.

    Instructions for the LLM:
    - Names in datasets may not match these names below exactly but can be identified by the GPC reference number and options in the lists.
    - Focus on identifying semantically similar terms, synonyms, or variations in dataset names.
    - The column names in this dictionary represent common terms. If a dataset uses different terminology for a concept (e.g., 'final user' or 'distribution channed' instead of 'user_type'), map accordingly.
    - Names in the lists are indicative and can be changed according to the specific dataset.

    Examples:
    # Describe here what input would result in this output. As an example what I did in gpc mappings: 
    # - "I.1.1": Represents emissions within the sector 'Stationary Energy' and the subsector 'Residential Buildings' from fuel combustion within the city boundary (Scope 1)
    # The idea is to guide the model. E.g. this is the required output (which you have below) if you encounter this input (as an example above the goc mappings)
    - fuel_sales:{
        "gpc_reference_number": 'II.1.1',
        "activity_names": 'fuel sold',
        "activity_subcategories1": {
            "type": 'fuel_type',
            "name": 'diesel'},
        "activity_subcategories2": {
            "type": 'user_type',
            "name": 'Gas stations'}
        }
    }
    - fuel_sales:{
        "gpc_reference_number": 'I.1.2',
        "activity_names": 'electricity consumption',
        "activity_subcategories1": {
            "type": 'electricity_type',
            "name": 'grid-energy supply'},
        "activity_subcategories2": {
            "type": 'user_type',
            "name": 'residential'
        }
    }

    The names given in this dictionary are indicative and can be changed according to the specific dataset.
    """,
    "fuel_sales": {
        "description": "",  # description needed for each key
        "gpc_reference_number": {
            "description": "These are the only possible GPC reference numbers for the activity data type fuel sales",  # I added this example
            "values": ["II.1.1", "II.2.1", "II.3.1", "II.4.1", "II.5.1"],
        },
        "activity_names": ["fuel sales", "fuel sold"],
        # can the activity name be one of those? To me both are pretty much the same. Should this be an example list like 'it could be fuel sales or fuel sold'?
        # Then it would be better to habe only one value here and give this value a description like
        # "activity_names": {
        #   "type": "fuel_sales",
        #   "description": "This activity is about selling fuels.......etc.",
        # This approach (to describe it for the LLM) is always better than to list multiple similar values without any further information
        # The difference here is above to the GPC reference numbers where we list all possible values and not giving similar values as examples
        "activity_subcatogories1": {
            "description": "",  # description needed for each key
            "type": "fuel_type",
            "name": [
                "diesel",
                "petrol",
                "gasoline",
                "kerosene",
                "jet fuel",
                "biofuel",
                "ethanol",
                "biodiesel",
                "LPG",
                "CNG",
                "LNG",
                "coal",
                "fuel oil",
                "natural gas",
                "biogas",
                "wood",
                "charcoal",
                "peat",
                "waste",
                "biomass",
            ],
        },
        "activity_subcatogories2": {
            "description": "",  # description needed for each key
            "type": "user_type",
            "name": [
                "Gas stations",
                "Service stations, storage and distribution",
                "Freight transport",
                "Agriculture",
                "Public transport",
                "Vessels",
                "Aircraft",
                "Trains",
                "Railways",
                "Cars",
                "Motorcycles",
                "Buses",
                "Trucks",
                "Other",
            ],
        },
    },
    "fuel_consumption": {
        "description": "",  # description needed for each key
        "gpc_reference_number": ["I.1.1", "I.2.1", "I.3.1", "I.4.1", "I.5.1", "I.6.1"],
        "activity_names": ["fuel consumption", "fuel consumed"],
        "activity_subcatogories1": {
            "type": "fuel_type",
            "name": [
                "diesel",
                "petrol",
                "gasoline",
                "kerosene",
                "jet fuel",
                "biofuel",
                "ethanol",
                "biodiesel",
                "LPG",
                "CNG",
                "LNG",
                "coal",
                "fuel oil",
                "natural gas",
                "biogas",
                "wood",
                "charcoal",
                "peat",
                "waste",
                "biomass",
            ],
        },
        "activity_subcatogories2": {
            "type": "user_type",
            "name": [
                "all",
                "commercial",
                "residential",
                "industrial",
                "public",
                "agricultural",
                "other",
            ],
        },
    },
    "electricity_consumption": {
        "description": "",  # description needed for each key
        "gpc_reference_number": [
            "I.1.2",
            "I.2.2",
            "I.3.2",
            "I.4.2",
            "I.5.2",
            "I.6.2",
            "II.1.2",
            "II.2.2",
            "II.3.2",
            "II.4.2",
            "II.5.2",
        ],
        "activity_names": [
            "electricity consumption",
            "electricity consumed",
            "consumption",
        ],
        "activity_subcatogories1": {
            "type": "electricity_type",
            "name": [
                "electricity",
                "grip-energy supply",
                "renewable electricity",
                "non-renewable electricity",
            ],
        },
        "activity_subcatogories2": {
            "type": "user_type",
            "name": [
                "all",
                "commercial",
                "residential",
                "industrial",
                "public",
                "agricultural",
                "other",
                "transportation",
                "on-road",
                "trains",
            ],
        },
    },
}
