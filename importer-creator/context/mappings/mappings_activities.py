# Python dictionary to map the activity types with the GPC reference numbers and the activities names and subcategories

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
    - The column names in this dictionary represent common terms. If a dataset uses different terminology for a concept (e.g., 'final user' or 'distribution channel' instead of 'user_type'), map accordingly.
    - Names in the lists are indicative and can be changed according to the specific dataset.
    """,
    "activity_names": {
        "description": "Contains the name of the actions or activities that generate greenhouse gas emissions",
        "names": {
            "fuel_combustion": {
                "description": "It refers to the process of burning fuel to produce energy, typically in the form of heat, electricity, or mechanical power. This activity occurs in various sectors, including transportation, industrial operations, power generation, and residential heating.",
                "gpc_refno": [
                    "I.1.1", "I.2.1", "I.3.1", "I.4.1", "I.5.1", "I.6.1",
                    "II.1.1", "II.2.1", "II.3.1", "II.4.1", "II.5.1"
                ],
                "activity_subcategories1": {
                    "description": "It refers to the type of fuel used in the combustion process.",
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
                        "Wood/Wood Waste", 
                        "Bioethanol", 
                        "Biodiesel", 
                        "Jet Fuel",
                        "LPG", 
                        "CNG"
                    ]
                },
                "activity_subcategories2": {
                    "description": "It refers to the type of user that is using the fuel.",
                    "type": "user_type",
                    "name": {
                        "Residential buildings": {
                            "all": {
                                "description": "It refers to all residential buildings unless a specific building type is mentioned.",
                                "id": "building-type-all"
                            }
                        },
                        "Commercial and institutional buildings and facilities": {
                            "all": {
                                "description": "It refers to all commercial and institutional buildings unless a specific building type is mentioned.",
                                "id": "type-all"
                            },
                            "Commercial buildings": {
                                "description": "Explicitly commercial buildings.",
                                "id": "type-commercial-buildings"
                            },
                            "Institutional buildings": {
                                "description": "Explicitly institutional buildings.",
                                "id": "type-institutional-buildings"
                            },
                            "Street lighting": {
                                "description": "Street lighting infrastructure.",
                                "id": "type-street-lighting"
                            }
                        },
                       "Manufacturing industries and construction": {
                            "all": {
                                "description": "It refers to all manufacturing industries and construction unless a specific building type is mentioned",
                                "id": "type-all"
                            },
                            "Manufacturing industries": {
                                "description": "It refers to manufacturing industries",
                                "id": "type-manufacturing-industries-and-construction"
                            },
                            "Steel": {
                                "description": "It refers to steel manufacturing",
                                "id": "type-steel"
                            },
                            "Cement": {
                                "description": "It refers to cement manufacturing",
                                "id": "type-cement"
                            },
                            "Iron": {
                                "description": "It refers to iron manufacturing",
                                "id": "type-iron"
                            },
                            "Non-ferrous metals": {
                                "description": "It refers to non-ferrous metals manufacturing",
                                "id": "type-non-ferrous-metals"
                            },
                            "Chemical products": {
                                "description": "It refers to chemical products manufacturing",
                                "id": "type-chemical-products"
                            },
                            "Pulp, paper, and printing": {
                                "description": "It refers to pulp, paper, and printing manufacturing",
                                "id": "type-pulp-paper-and-printing"
                            },
                            "Non-metallic minerals": {
                                "description": "It refers to non-metallic minerals manufacturing",
                                "id": "type-non-metallic-minerals"
                            },
                            "Transport equipment": {
                                "description": "It refers to transport equipment manufacturing",
                                "id": "type-transport-equipment"
                            },
                            "Machinery": {
                                "description": "It refers to machinery manufacturing",
                                "id": "type-machinery"
                            },
                            "Mining and quarrying": {
                                "description": "It refers to mining and quarrying",
                                "id": "type-mining-and-quarrying"
                            },
                            "Wood and wood products": {
                                "description": "It refers to wood and wood products manufacturing",
                                "id": "type-wood-and-wood-products"
                            },
                            "Construction": {
                                "description": "It refers to construction",
                                "id": "type-construction"
                            },
                            "Textiles and leather": {
                                "description": "It refers to textiles and leather manufacturing",
                                "id": "type-textiles-and-leather"
                            },
                            "Unspecified industry": {
                                "description": "It refers to unspecified industry",
                                "id": "type-unspecified-industry"
                            }
                        },
                        "Energy industries": {
                            "all": {
                                "description": "It refers to all energy industries unless a specific building type is mentioned",
                                "id": "type-all"
                            }
                        },
                        "Agriculture, forestry, and fishing activities": {
                            "all": {
                                "description": "It refers to all agriculture, forestry, and fishing activities unless a specific building type is mentioned",
                                "id": "type-all"
                            }
                        },
                        "Non-specified sources": {
                            "all": {
                                "description": "It refers to all non-specified sources unless a specific building type is mentioned",
                                "id": "type-all"
                            }
                        },
                        "On-road": {
                            "all": {
                                "description": "All on-road vehicles unless a specific type is mentioned.",
                                "id": "type-all"
                            },
                            "Passenger vehicles": {
                                "description": "Passenger vehicles specifically.",
                                "id": "vehicle-type-passenger-vehicles"
                            },
                            "Commercial vehicles": {
                                "description": "Commercial vehicles specifically.",
                                "id": "vehicle-type-commercial-vehicles"
                            }
                        },
                        "Railways": {
                            "all": {
                                "description": "It refers to all railways unless a specific transport type is mentioned",
                                "id": "type-all"
                            },
                            "Passenger trains": {
                                "description": "It refers to passenger trains specifically",
                                "id": "vehicle-type-passenger-trains"
                            },
                            "Freight trains": {
                                "description": "It refers to freight trains specifically",
                                "id": "vehicle-type-freight-trains"
                            },
                            "High-speed trains": {
                                "description": "It refers to high-speed trains specifically",
                                "id": "vehicle-type-high-speed-trains"
                            },
                            "Tourist trains": {
                                "description": "It refers to tourist trains specifically",
                                "id": "vehicle-type-tourist-trains"
                            }
                        },
                        "Waterborne navigation": {
                            "all": {
                                "description": "It refers to all waterborne navigation unless a specific transport type is mentioned",
                                "id": "type-all"
                            },
                            "Ferries": {
                                "description": "It refers to ferries specifically",
                                "id": "vehicle-type-ferries"
                            },
                            "Boats": {
                                "description": "It refers to boats specifically",
                                "id": "vehicle-type-boats"
                            },
                            "Marine vessels": {
                                "description": "It refers to marine vessels specifically",
                                "id": "vehicle-type-marine-vessels"
                            }
                        },
                        "Aviation": {
                            "all": {
                                "description": "All aviation unless a specific type is mentioned.",
                                "id": "type-all"
                            },
                            "Passenger aircraft": {
                                "description": "Passenger aircraft specifically.",
                                "id": "vehicle-type-passenger-aircraft"
                            },
                            "Cargo aircraft": {
                                "description": "Cargo aircraft specifically.",
                                "id": "vehicle-type-cargo-aircraft"
                            }
                        }
                    }
                }
            },
            "electricity_consumption": {
                "description": "It refers to the amount of electricity consumed by a user or a group of users. This activity occurs in various sectors, including residential, commercial, industrial, and transportation.",
                "gpc_refno": [
                    "I.1.2", "I.2.2", "I.3.2", "I.4.2", "I.5.2", "I.6.2",
                    "II.1.2", "II.2.2", "II.3.2", "II.4.2", "II.5.2"
                ],
                "activity_subcategories1": {
                    "description": "Contains the type of electricity consumed.",
                    "type": "electricity_type",
                    "name": [
                        "grid-energy supply", 
                        "renewable electricity", 
                        "non-renewable electricity"
                    ]
                },
                "activity_subcategories2": {
                    "description": "It refers to the type of user that is using the electricity.",
                    "type": "user_type",
                    "name": {
                        "Residential buildings": {
                            "all": {
                                "description": "It refers to all residential buildings unless a specific building type is mentioned.",
                                "id": "building-type-all"
                            }
                        },
                        "Commercial and institutional buildings and facilities": {
                            "all": {
                                "description": "It refers to all commercial and institutional buildings unless a specific building type is mentioned.",
                                "id": "type-all"
                            },
                            "Commercial buildings": {
                                "description": "Explicitly commercial buildings.",
                                "id": "type-commercial-buildings"
                            },
                            "Institutional buildings": {
                                "description": "Explicitly institutional buildings.",
                                "id": "type-institutional-buildings"
                            },
                            "Street lighting": {
                                "description": "Street lighting infrastructure.",
                                "id": "type-street-lighting"
                            }
                        },
                       "Manufacturing industries and construction": {
                            "all": {
                                "description": "It refers to all manufacturing industries and construction unless a specific building type is mentioned",
                                "id": "type-all"
                            },
                            "Manufacturing industries": {
                                "description": "It refers to manufacturing industries",
                                "id": "type-manufacturing-industries-and-construction"
                            },
                            "Steel": {
                                "description": "It refers to steel manufacturing",
                                "id": "type-steel"
                            },
                            "Cement": {
                                "description": "It refers to cement manufacturing",
                                "id": "type-cement"
                            },
                            "Iron": {
                                "description": "It refers to iron manufacturing",
                                "id": "type-iron"
                            },
                            "Non-ferrous metals": {
                                "description": "It refers to non-ferrous metals manufacturing",
                                "id": "type-non-ferrous-metals"
                            },
                            "Chemical products": {
                                "description": "It refers to chemical products manufacturing",
                                "id": "type-chemical-products"
                            },
                            "Pulp, paper, and printing": {
                                "description": "It refers to pulp, paper, and printing manufacturing",
                                "id": "type-pulp-paper-and-printing"
                            },
                            "Non-metallic minerals": {
                                "description": "It refers to non-metallic minerals manufacturing",
                                "id": "type-non-metallic-minerals"
                            },
                            "Transport equipment": {
                                "description": "It refers to transport equipment manufacturing",
                                "id": "type-transport-equipment"
                            },
                            "Machinery": {
                                "description": "It refers to machinery manufacturing",
                                "id": "type-machinery"
                            },
                            "Mining and quarrying": {
                                "description": "It refers to mining and quarrying",
                                "id": "type-mining-and-quarrying"
                            },
                            "Wood and wood products": {
                                "description": "It refers to wood and wood products manufacturing",
                                "id": "type-wood-and-wood-products"
                            },
                            "Construction": {
                                "description": "It refers to construction",
                                "id": "type-construction"
                            },
                            "Textiles and leather": {
                                "description": "It refers to textiles and leather manufacturing",
                                "id": "type-textiles-and-leather"
                            },
                            "Unspecified industry": {
                                "description": "It refers to unspecified industry",
                                "id": "type-unspecified-industry"
                            }
                        },
                        "Energy industries": {
                            "all": {
                                "description": "It refers to all energy industries unless a specific building type is mentioned",
                                "id": "type-all"
                            }
                        },
                        "Agriculture, forestry, and fishing activities": {
                            "all": {
                                "description": "It refers to all agriculture, forestry, and fishing activities unless a specific building type is mentioned",
                                "id": "type-all"
                            }
                        },
                        "Non-specified sources": {
                            "all": {
                                "description": "It refers to all non-specified sources unless a specific building type is mentioned",
                                "id": "type-all"
                            }
                        },
                        "On-road": {
                            "all": {
                                "description": "All on-road vehicles unless a specific type is mentioned.",
                                "id": "type-all"
                            },
                            "Passenger vehicles": {
                                "description": "Passenger vehicles specifically.",
                                "id": "vehicle-type-passenger-vehicles"
                            },
                            "Commercial vehicles": {
                                "description": "Commercial vehicles specifically.",
                                "id": "vehicle-type-commercial-vehicles"
                            }
                        },
                        "Railways": {
                            "all": {
                                "description": "It refers to all railways unless a specific transport type is mentioned",
                                "id": "type-all"
                            },
                            "Passenger trains": {
                                "description": "It refers to passenger trains specifically",
                                "id": "vehicle-type-passenger-trains"
                            },
                            "Freight trains": {
                                "description": "It refers to freight trains specifically",
                                "id": "vehicle-type-freight-trains"
                            },
                            "High-speed trains": {
                                "description": "It refers to high-speed trains specifically",
                                "id": "vehicle-type-high-speed-trains"
                            },
                            "Tourist trains": {
                                "description": "It refers to tourist trains specifically",
                                "id": "vehicle-type-tourist-trains"
                            }
                        },
                        "Waterborne navigation": {
                            "all": {
                                "description": "It refers to all waterborne navigation unless a specific transport type is mentioned",
                                "id": "type-all"
                            },
                            "Ferries": {
                                "description": "It refers to ferries specifically",
                                "id": "vehicle-type-ferries"
                            },
                            "Boats": {
                                "description": "It refers to boats specifically",
                                "id": "vehicle-type-boats"
                            },
                            "Marine vessels": {
                                "description": "It refers to marine vessels specifically",
                                "id": "vehicle-type-marine-vessels"
                            }
                        },
                        "Aviation": {
                            "all": {
                                "description": "All aviation unless a specific type is mentioned.",
                                "id": "type-all"
                            },
                            "Passenger aircraft": {
                                "description": "Passenger aircraft specifically.",
                                "id": "vehicle-type-passenger-aircraft"
                            },
                            "Cargo aircraft": {
                                "description": "Cargo aircraft specifically.",
                                "id": "vehicle-type-cargo-aircraft"
                            }
                        }
                    }
                }
            }
        }
    }
}
