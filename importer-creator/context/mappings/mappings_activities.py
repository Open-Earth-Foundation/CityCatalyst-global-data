# Python dictionary to map the activity types with the GPC reference numbers and the activities names and subcategories

# transportatin
# subcategory type 2 is specific vehicel type like car, taxi, whatever. If not found its generally on-road
# commercial buildings: always general commercial buildings unless specific building type is mentioned like street lighting or istitutional building

activity_mappings = {
    "__doc__": """
    This dictionary maps the most common activity names related to actions that generate greenhouse gas emissions and their corresponding subcategories, which include additional information to understand the activity (for example, the fuel type or the end user of the electricity).
    Each activity name has a list of the Global Protocol for Greenhouse Gas Emission Inventories (GPC) reference numbers that apply to each activity, the activity names, and the corresponding subcategories, which also include the subcategory type and name.

    Each activity name has the following keys:
    - description: Contains a brief description of the activity being referred to.
    - gpc_refno: Contains a list of possible GPC reference numbers that can apply to the activity.
    - activity_subcategories1: Contains the subcategories related to the activity. It includes the type and the name of the subcategory.
    - activity_subcategories2: Contains the subcategories related to the activity. It includes the type and the name of the subcategory.

    Instructions for the LLM:
    - Names in datasets may not match these names below exactly but can be identified by the GPC reference number and options in the lists.
    - Focus on identifying semantically similar terms, synonyms, or variations in dataset names.
    - The column names in this dictionary represent common terms. If a dataset uses different terminology for a concept (e.g., 'final user' or 'distribution channed' instead of 'user_type'), map accordingly.
    - Names in the lists are indicative and can be changed according to the specific dataset.

    Examples:
    - If the dataset contains data from diesel sales with a GPC reference number "I.1.1" in the transportation sector, the activity name would be 'fuel combustion' and the subcategories would be "fuel type": "diesel".
    - If the dataset contains data from electricity consumption in residential buildings, the activity name would be 'electricity consumption' and the subcategories would be "electricity type": "grid-energy supply" and "user type": "residential buildings".
    - If the dataset contains data from consumption of natural gases in industrial facilities, the activity name would be 'fuel combustion' and the subcategories would be "fuel type": "natural gas" and "user type": "industrial facilities".

    The names given in this dictionary are indicative and can be changed according to the specific dataset.
    """,
    "activity_names": {
        "description": "Contains the name of the actions or activities that generate greenhouse gas emissions",
        "names": {
            "fuel_combustion": {
                "description": "It refers to the process of burning fuel to produce energy, typically in the form of heat, electricity, or mechanical power. This activity occurs in various sectors, including transportation, industrial operations, power generation, and residential heating.",
                "gpc_refno": [
                    "I.1.1",
                    "I.2.1",
                    "I.3.1",
                    "I.4.1",
                    "I.5.1",
                    "I.6.1",
                    "II.1.1",
                    "II.2.1",
                    "II.3.1",
                    "II.4.1",
                    "II.5.1",
                ],
                "activity_subcategories1": {
                    "description": "It refers of the type of fuel used in the combustion process",
                    "type": "fuel_type",
                    "name": [
                        "Anthracite",
                        "Other Bituminous Coal",
                        "Lignite",
                        "Peat",
                        "Crude Oil",
                        "Motor Gasoline",
                        "Other Kerosene",
                        "Gas Oil",
                        "Diesel Oil",
                        "Residual Fuel Oil",
                        "Natural Gas",
                        "Other Primary Solid Biomass",
                        "Wood/Wood Waste",
                        "Charcoal",
                        "Sub-Bituminous Coal",
                        "Refinery Gas",
                        "Coking Coal",
                        "Liquefied Petroleum Gases",
                        "Coke Oven Coke and Lignite Coke",
                        "Industrial Wastes",
                        "Waste Oils",
                        "Naphtha",
                        "Municipal Wastes (non-biomass fraction)",
                        "Aviation Gasoline",
                        "Jet Fuel",
                        "Jet Kerosene",
                        "Compressed Natural Gas (CNG)",
                        "Kerosene",
                        "E85 Ethanol",
                        "B20 Biodiesel",
                        "Ethanol",
                        "Biodiesel",
                        "Bioethanol",
                        "Diesel",
                        "Liquefied Petroleum Gas (LPG)",
                        "Petrol",
                        "CNG",
                        "LPG",
                    ],
                },
                "activity_subcategories2": {
                    "description": "It refers to the type of user that is using the fuel. This can be a residential building, commercial building, industrial facility, or any transportation sector.",
                    "type": "user_type",
                    # This mapping will not work properly as the different names are too similar e.g. Trains and Railways. How are they different?
                    "name": [
                        "Residential buildings",
                        "Commercial buildings",
                        "Intuitional buildings",
                        "Street lighting",
                        "Industrial facilities",
                        "Public facilities",
                        "Agricultural facilities",
                        "Manufacturing facilities",
                        "Power plants",
                        "Energy Industry",
                        "Transportation",
                        "Machinery",
                        "Freight transport",
                        "Public transport",
                        "Trains",
                        "Railways",
                        "Cars",
                        "Motorcycles",
                        "Buses",
                        "Trucks",
                        "Off-road vehicles",
                        "Fishing mobile combustion",
                        "Emergency vehicles",
                        "Service vehicles",
                        "Gas stations",
                        "Service stations, storage and distribution",
                        "Vessels",
                        "Aircraft",
                    ],
                },
            },
            "electricity_consumption": {
                "description": "It refers to the amount of electricity consumed by a user or a group of users. This activity occurs in various sectors, including residential, commercial, industrial, and transportation.",
                "gpc_refno": [
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
                "activity_subcategories1": {
                    "description": "Contains the type of electricity consumed",
                    "type": "electricity_type",
                    "name": [
                        "grid-energy supply",
                        "renewable electricity",
                        "non-renewable electricity",
                    ],
                },
                "activity_subcategories2": {
                    "description": "It refers to the type of user that is using the electricity. This can be a residential building, commercial building, industrial facility, or any transportation sector.",
                    "type": "user_type",
                    # This mapping will not work properly as the different names are too similar e.g. Trains and Railways. How are they different?
                    "name": [
                        "Residential buildings",
                        "Commercial buildings",
                        "Intuitional buildings",
                        "Street lighting",
                        "Industrial facilities",
                        "Public facilities",
                        "Agricultural facilities",
                        "Manufacturing facilities",
                        "Power plants",
                        "Energy Industry",
                        "Transportation",
                        "Machinery",
                        "Freight transport",
                        "Public transport",
                        "Trains",
                        "Railways",
                        "Cars",
                        "Buses",
                        "Trucks",
                        "Off-road vehicles",
                        "Fishing mobile combustion",
                        "Emergency vehicles",
                        "Service vehicles",
                    ],
                },
            },
        },
    },
}
