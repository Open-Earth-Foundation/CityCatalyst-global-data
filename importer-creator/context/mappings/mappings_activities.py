# Python dictionary to map the activity types with the GPC reference numbers and the activities names and subcategories

activity_mappings = {
    "__doc__": """
    This dictionary maps the most common activity names related to actions that generate greenhouse gas emissions and their corresponding subcategories, which include additional information to understand the activity (for example, the fuel type or the end user of the electricity).
    Each activity name has a list of the Global Protocol for Greenhouse Gas Emission Inventories (GPC) reference numbers that apply to each activity, the activity names, and the corresponding subcategories, which also include the subcategory type and name.

    Each activity name has the following keys:
    - description: Contains a brief description of the activity being referred to.
    - gpc_refno: Contains a list of possible GPC reference numbers that can apply to the activity.
    - activity_subcategories1: It contains a description of the subcategory, the type of subcategory, and a list of potential names that may apply. Within each name entry, there is an associated ID and a description that elaborates on that specific element.
    - activity_subcategories2: It contains a description of the subcategory, the type of subcategory, and a list of potential names that may apply. Within each name entry, there is an associated ID and a description that elaborates on that specific element.

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
                    "description": "It refers to the type of fuel used in the combustion process.",
                    "type": "fuel_type",
                    "name": [
                        {
                            "id": "fuel-type-anthracite",
                            "description": "it refers to anthracite coal and the different types or grades of anthracite coal",
                        },
                        {
                            "id": "fuel-type-other-bituminous-coal",
                            "description": "this term is used to distinguish non-coking bituminous coal from coking coal. It does not have the properties necessary for coking, so it is primarily used as fuel for electric power generation, heat production, and in some industrial boilers. It serves as a category that accounts for general-use bituminous coals that are not intended for specialized uses",
                        },
                        {
                            "id": "fuel-type-lignite",
                            "description": "it refers to lignite, also known as brown coal, generally used for electricity generation",
                        },
                        {
                            "id": "fuel-type-peat",
                            "description": "it refers to peat, a type of organic soil that is used as fuel. The primary uses are domestic heating, small-scale electricity generation, and soil amendment",
                        },
                        {
                            "id": "fuel-type-crude-oil",
                            "description": "it refers to crude oil, also known as petroleum, a fossil fuel that is refined into various petroleum products, and serves as a raw material in the production of plastics, chemicals, and lubricants",
                        },
                        {
                            "id": "fuel-type-gasoline",
                            "description": "it refers to gasoline, a refined product of crude oil that is used as fuel in internal combustion engines in vehicles and machinery. Also known as petrol",
                        },
                        {
                            "id": "fuel-type-other-kerosene",
                            "description": "it refers to types of kerosene that are not categorized specifically as jet fuel. The primary uses are heating, lighting, cooking, and industrial uses (non-aviation). Also known as heating kerosene",
                        },
                        {
                            "id": "fuel-type-gas-oil",
                            "description": "it refers to gas oil, a refined petroleum distillate. Used in heating systems, industrial boilers, power generation, and non-road machinery (e.g., agriculture, construction)",
                        },
                        {
                            "id": "fuel-type-diesel-oil",
                            "description": "it refers to diesel oil, a refined petroleum distillate used primarily as fuel for internal combustion engines in road vehicles, freight and passenger trains and other machinery. The primary uses are in road vehicles (cars, trucks, buses), heavy machinery (construction, agriculture), and marine engines. It is also used in some standby generators and industrial equipment.",
                        },
                        {
                            "id": "fuel-type-residual-fuel-oil",
                            "description": "it refers to residual fuel oil, a by-product of crude oil refining that is used as fuel in large boilers and industrial furnaces, it's often referred to as heavy fuel oil (HFO) or bunker fuel in marine contexts. Primarily used in marine shipping (as bunker fuel), large-scale industrial boilers, and power plants. It is also used in some heavy machinery in non-road applications.",
                        },
                        {
                            "id": "fuel-type-natural-gas",
                            "description": "it refers to natural gas, a fossil fuel that is primarily composed of methane. It is used for heating, cooking, electricity generation, and as a fuel for vehicles. It is also used as a feedstock in the production of chemicals and fertilizers",
                        },
                        {
                            "id": "fuel-type-cng",
                            "description": "it is natural gas that has been compressed to a high pressure. The primary use is fuel for vehicles, especially in public transportation and fleet vehicles",
                        },
                        {
                            "id": "fuel-type-fuel-type-natural-gas-liquids",
                            "description": "NGLs are a group of hydrocarbons that are separated from natural gas during processing. This category includes ethane, propane, butane, isobutane, and pentane. NGLs are valuable as feedstocks for the petrochemical industry, heating, cooking, blending in gasoline, and as LPG components.",
                        },
                        {
                            "id": "fuel-type-wood-wood-waste",
                            "description": "it refers to biomass fuels derived from trees, forest residues, and wood processing byproducts. The primary uses are heating, power generation, industrial fuel. Also known as Biomass Fuel",
                        },
                        {
                            "id": "fuel-type-bioethanol",
                            "description": "it refers to bioethanol, an alcohol fuel. The primary uses are transportation fuel additive and industrial uses. It known as Ethanol or Ethyl Alcohol also.",
                        },
                        {
                            "id": "fuel-type-biodiesel",
                            "description": "it refers to biodiesel, a renewable fuel. It is used as an alternative to or blended with conventional diesel fuel in vehicles and industrial engines. The primary uses are transportation, industrial engines, power generation.",
                        },
                        {
                            "id": "fuel-type-jet-gasoline",
                            "description": "it refers to jet fuel, also known as aviation gasoline or avgas, is a highly refined fuel specifically formulated for piston-engine aircraft. The primary use is as fuel for piston-engine aircraft (aviation).",
                        },
                        {
                            "id": "fuel-type-jet-kerosene",
                            "description": "Jet kerosene (jet fuel) is a highly refined kerosene-based fuel used primarily in turbine-powered aircraft (jet engines). Common types include Jet A and Jet A-1. The primary use is as fuel for turbine-engine aircraft (aviation).",
                        },
                        {
                            "id": "fuel-type-lpg",
                            "description": "it refers to liquefied petroleum gas (LPG). The primary uses are in heating, cooking, and as a fuel for vehicles. Also known as Propane-Butane Mix, Autogas.",
                        },
                        {
                            "id": "fuel-type-charcoal",
                            "description": "it refers to charcoal, a solid fuel made by heating wood in the absence of oxygen. Commonly used for cooking, heating, and in some metallurgical processes due to its high carbon content and efficient combustion.",
                        },
                        {
                            "id": "fuel-type-diesel-oil",
                            "description": "it refers to diesel oil, a refined petroleum distillate used primarily as fuel for internal combustion engines in vehicles, heavy machinery, and some industrial equipment.",
                        },
                        {
                            "id": "fuel-type-industrial-wastes",
                            "description": "it refers to industrial wastes used as fuel, which can include a range of non-hazardous by-products from manufacturing processes. Primarily used in power generation and waste-to-energy plants.",
                        },
                        {
                            "id": "fuel-type-liquefied-petroleum-gases",
                            "description": "it refers to liquefied petroleum gases (LPG), a mixture of light hydrocarbons including propane and butane, stored under pressure in liquid form. Commonly used for heating, cooking, and as vehicle fuel.",
                        },
                        {
                            "id": "fuel-type-municipal-wastes",
                            "description": "it refers to municipal wastes (non-biomass fraction), which includes non-organic waste materials such as plastics and metals, often used in waste-to-energy plants for power generation.",
                        },
                        {
                            "id": "fuel-type-naphtha",
                            "description": "it refers to naphtha, a volatile liquid hydrocarbon mixture used as a feedstock in petrochemical production, a solvent, and in gasoline blending.",
                        },
                        {
                            "id": "fuel-type-natural-charcoal",
                            "description": "it refers to natural charcoal, a form of solid biomass fuel produced by carbonizing wood in the absence of oxygen. Commonly used in cooking, heating, and certain metallurgical processes.",
                        },
                        {
                            "id": "fuel-type-other-primary-solid-biomass",
                            "description": "it refers to other primary solid biomass, including materials like crop residues, animal waste, and other organic materials used for heating, power generation, and as feedstock in biofuel production.",
                        },
                        {
                            "id": "fuel-type-propane",
                            "description": "it refers to propane, a hydrocarbon gas stored under pressure in liquid form. Widely used for heating, cooking, and as a vehicle fuel. Part of the LPG family.",
                        },
                        {
                            "id": "fuel-type-sub-bituminous-coal",
                            "description": "it refers to sub-bituminous coal, a type of coal with lower carbon content and heating value than bituminous coal. Mainly used in electricity generation and industrial heating.",
                        },
                        {
                            "id": "fuel-type-waste-oils",
                            "description": "it refers to waste oils, including used motor oils and other lubricants that can be repurposed as fuel in industrial burners or waste-to-energy applications.",
                        },
                    ],
                },
                "activity_subcategories2": {
                    "description": "It refers to the type of user that is using the fuel.",
                    "type": "user_type",
                    "name": {
                        "Residential buildings": [
                            {
                                "id": "building-type-all",
                                "description": "It refers to all residential buildings unless a specific building type is mentioned.",
                            }
                        ],
                        "Commercial and institutional buildings and facilities": [
                            {
                                "id": "type-all",
                                "description": "This category encompasses all types of commercial and institutional buildings when a specific building type is not specified. Use this category as a general identifier when the type of building is unclear or includes both commercial and institutional types.",
                            },
                            {
                                "id": "type-commercial-buildings",
                                "description": "This category specifically refers to buildings used for commercial activities. Examples include office buildings, retail stores, shopping malls, hotels, restaurants, and entertainment venues. These buildings are primarily intended for business transactions, services, and consumer interactions, and often include spaces designed for customer access and professional use.",
                            },
                            {
                                "id": "type-institutional-buildings",
                                "description": "This category specifically refers to buildings used for institutional purposes, including government, education, health care, religious, and cultural facilities. Examples include schools, hospitals, government offices, religious institutions, and museums. These buildings serve community, educational, health, or administrative functions and are usually operated by public or nonprofit organizations.",
                            },
                            {
                                "id": "type-street-lighting",
                                "description": "This category refers to street lighting infrastructure, which includes lighting installed along public streets, highways, pedestrian pathways, and public outdoor spaces. This type does not include interior building lighting or private property lighting.",
                            },
                        ],
                        "Manufacturing industries and construction": [
                            {
                                "id": "type-all",
                                "description": "This category encompasses all manufacturing industries and construction when a specific industry type is not specified. Use this general identifier when the precise type of manufacturing or construction activity is unclear or includes multiple types across this sector.",
                            },
                            {
                                "id": "type-manufacturing-industries-and-construction",
                                "description": "This refers broadly to manufacturing industries involved in the production of goods and construction activities that involve building infrastructure. Use this when referring to all manufacturing and construction sectors collectively.",
                            },
                            {
                                "id": "type-steel",
                                "description": "This category is specific to steel manufacturing industries, which involve the production of steel products from iron ore, scrap, or other raw materials.",
                            },
                            {
                                "id": "type-cement",
                                "description": "This category includes cement manufacturing industries focused on producing cement from limestone and other raw materials.",
                            },
                            {
                                "id": "type-iron",
                                "description": "This category covers industries involved in iron production, including the extraction and processing of iron ore to produce iron products.",
                            },
                            {
                                "id": "type-non-ferrous-metals",
                                "description": "This refers to the manufacturing of non-ferrous metals, including metals like aluminum, copper, and zinc.",
                            },
                            {
                                "id": "type-chemical-products",
                                "description": "This category is specific to the production of chemical products, which includes the manufacture of substances like petrochemicals, fertilizers, pharmaceuticals, and industrial gases.",
                            },
                            {
                                "id": "type-pulp-paper-and-printing",
                                "description": "This category covers industries involved in the production of pulp, paper, and printing materials.",
                            },
                            {
                                "id": "type-non-metallic-minerals",
                                "description": "This includes the production of non-metallic minerals, such as glass, ceramics, and construction materials (like clay or stone).",
                            },
                            {
                                "id": "type-transport-equipment",
                                "description": "This category refers to industries involved in the manufacturing of transportation equipment, including vehicles, aircraft, ships, and railway equipment.",
                            },
                            {
                                "id": "type-machinery",
                                "description": "This category includes the manufacturing of machinery used in various industries, from agriculture to construction. It covers industries producing heavy machinery, industrial tools, and equipment for specific applications.",
                            },
                            {
                                "id": "type-mining-and-quarrying",
                                "description": "This category encompasses activities related to mining and quarrying, including the extraction of minerals, metals, and stone from the earth.",
                            },
                            {
                                "id": "type-wood-and-wood-products",
                                "description": "This refers to industries producing wood products, including sawmills, lumber production, and the manufacture of wood-based products like furniture, plywood, and particleboard.",
                            },
                            {
                                "id": "type-construction",
                                "description": "This category includes all construction activities, covering building infrastructure, residential and commercial construction, and civil engineering projects.",
                            },
                            {
                                "id": "type-textiles-and-leather",
                                "description": "This includes industries engaged in the production of textiles, apparel, and leather goods.",
                            },
                            {
                                "id": "type-unspecified-industry",
                                "description": "This is used when the specific industry building or facility within manufacturing or construction is not specified.",
                            },
                        ],
                        "Energy industries": [
                            {
                                "id": "type-all",
                                "description": "It refers to all type of energy industries.",
                            }
                        ],
                        "Agriculture, forestry, and fishing activities": [
                            {
                                "id": "type-all",
                                "description": "It refers to all buildings where agriculture, forestry, and fishing activities ocurres. This includes farms, plantations, forests, and fishing facilities.",
                            }
                        ],
                        "Non-specified sources": [
                            {
                                "id": "type-all",
                                "description": "It refers to all non-specified sources.",
                            }
                        ],
                        "On-road": [
                            {
                                "id": "type-all",
                                "description": "This category includes all on-road vehicles, covering passenger, commercial, and other types of vehicles designed for travel on roads. Use this when the vehicle type is unspecified or encompasses multiple on-road types.",
                            },
                            {
                                "id": "vehicle-type-passenger-vehicles",
                                "description": "This category refers to passenger vehicles used primarily for transporting individuals or small groups. Examples include cars, taxis, vans, SUVs, and motorcycles. These vehicles are typically used for personal or public transportation of passengers.",
                            },
                            {
                                "id": "vehicle-type-commercial-vehicles",
                                "description": "This category includes commercial vehicles used for transporting goods or services on roads. Examples are delivery trucks, vans, lorries, and utility vehicles. These vehicles are designed to support business activities and goods movement.",
                            },
                        ],
                        "Railways": [
                            {
                                "id": "type-all",
                                "description": "This category refers to all types of railway transportation. Use this when the specific type of rail transport is not specified or includes multiple types such as passenger, freight, and high-speed trains.",
                            },
                            {
                                "id": "vehicle-type-passenger-trains",
                                "description": "This category is specific to passenger trains, which are used for transporting individuals over short or long distances. Examples include commuter trains, intercity trains, and regional trains that carry passengers between destinations.",
                            },
                            {
                                "id": "vehicle-type-freight-trains",
                                "description": "This category includes freight trains, which are designed for transporting goods rather than passengers. Examples include bulk cargo trains, container trains, and tank trains used to move raw materials, finished goods, and industrial products.",
                            },
                            {
                                "id": "vehicle-type-high-speed-trains",
                                "description": "This category refers to high-speed trains, which are specialized passenger trains operating at high speeds on dedicated tracks. Examples include trains like the TGV, Shinkansen, and other high-speed rail networks primarily used for rapid, intercity passenger travel.",
                            },
                            {
                                "id": "vehicle-type-tourist-trains",
                                "description": "This category is specific to tourist trains, which are designed to provide scenic or leisure travel experiences. Examples include heritage trains, scenic railway tours, and special trains offering sightseeing for tourists.",
                            },
                        ],
                        "Waterborne navigation": [
                            {
                                "id": "type-all",
                                "description": "This category includes all waterborne navigation vehicles used for travel or transport on water. Use this when the specific type of watercraft is not specified or when it includes multiple types like ferries, boats, and marine vessels.",
                            },
                            {
                                "id": "vehicle-type-ferries",
                                "description": "This category refers to ferries, which are boats or ships used to transport passengers and sometimes vehicles across water, often on scheduled routes. Common examples are passenger ferries, car ferries, and river ferries.",
                            },
                            {
                                "id": "vehicle-type-boats",
                                "description": "This category includes smaller boats primarily used for personal or recreational purposes. Examples are motorboats, sailboats, and fishing boats, which operate on various bodies of water for leisure, fishing, or small-scale transport.",
                            },
                            {
                                "id": "vehicle-type-marine-vessels",
                                "description": "This category encompasses larger marine vessels used for commercial and industrial purposes. Examples include cargo ships, tankers, and container ships, primarily used for long-distance transport of goods across seas and oceans.",
                            },
                        ],
                        "Aviation": [
                            {
                                "id": "type-all",
                                "description": "This category covers all aviation vehicles, encompassing both passenger and cargo aircraft. Use this category when the specific type of aircraft is not specified or includes multiple types.",
                            },
                            {
                                "id": "vehicle-type-passenger-aircraft",
                                "description": "This category refers to passenger aircraft used for transporting individuals on domestic or international flights. Examples include commercial airliners, regional jets, and private jets designed to carry passengers.",
                            },
                            {
                                "id": "vehicle-type-cargo-aircraft",
                                "description": "This category includes cargo aircraft specifically designed for transporting goods and freight rather than passengers. Examples include freighter planes, air cargo carriers, and logistics aircraft used by companies like FedEx and UPS.",
                            },
                        ],
                    },
                },
            },
            "energy_consumption": {
                "description": "It refers to the amount of energy consumed by a user or a group of users. This activity occurs in various sectors, including residential, commercial, industrial, and transportation.",
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
                    "description": "Contains the type of energy consumed.",
                    "type": "energy_type",
                    "name": [
                        {
                            "id": "energy-usage-all",
                            "description": "This category covers all types of energy usage, including electricity, heating, steam, and refrigeration. Use this when the specific type of energy usage is unspecified or includes multiple types."
                        },
                        {
                            "id": "energy-usage-electricity",
                            "description": "This category refers to electricity usage across various applications, including residential, commercial, industrial, and transportation sectors. Examples include power for lighting, appliances, industrial machinery, and electric vehicle charging stations."
                        },
                        {
                            "id": "energy-usage-electricity-chp",
                            "description": "This category covers electricity usage in systems with combined heat and power (CHP) generation, which produce electricity and capture usable heat in a single process. Commonly found in industrial facilities and large buildings for efficient on-site power and heating."
                        },
                        {
                            "id": "energy-usage-heating",
                            "description": "This category is specific to energy usage for heating purposes in stationary contexts. Examples include space heating in buildings, water heating, and heating for industrial processes."
                        },
                        {
                            "id": "energy-usage-heating-chp",
                            "description": "This category refers to heating within combined heat and power (CHP) systems, where both heat and electricity are generated simultaneously. Common applications include large buildings, district heating systems, and industrial facilities."
                        },
                        {
                            "id": "energy-usage-steam",
                            "description": "This category covers energy usage for steam production, typically in industrial processes and large commercial facilities. Examples include steam for heating, manufacturing processes, and sterilization in healthcare facilities."
                        },
                        {
                            "id": "energy-usage-steam-chp",
                            "description": "This category includes steam usage within combined heat and power (CHP) systems, where steam is produced alongside electricity. CHP systems utilizing steam are common in industrial facilities and district heating setups for energy efficiency."
                        },
                        {
                            "id": "energy-usage-refrigeration",
                            "description": "This category refers to energy used for refrigeration and cooling applications, primarily in stationary contexts. Examples include cooling systems in commercial buildings, industrial refrigeration units, and air conditioning systems."
                        },
                        {
                            "id": "energy-usage-refrigeration-chp",
                            "description": "This category covers refrigeration or cooling systems integrated with combined heat and power (CHP) systems. These setups are found in large facilities where waste heat from electricity generation is repurposed for cooling, such as in absorption chillers in commercial and industrial buildings."
                        }
                    ],
                },
                "activity_subcategories2": {
                    "description": "It refers to the type of user that is using the electricity.",
                    "type": "user_type",
                    "name": {
                        "Residential buildings": [
                            {
                                "id": "building-type-all",
                                "description": "It refers to all residential buildings unless a specific building type is mentioned.",
                            }
                        ],
                        "Commercial and institutional buildings and facilities": [
                            {
                                "id": "type-all",
                                "description": "This category encompasses all types of commercial and institutional buildings when a specific building type is not specified. Use this category as a general identifier when the type of building is unclear or includes both commercial and institutional types.",
                            },
                            {
                                "id": "type-commercial-buildings",
                                "description": "This category specifically refers to buildings used for commercial activities. Examples include office buildings, retail stores, shopping malls, hotels, restaurants, and entertainment venues. These buildings are primarily intended for business transactions, services, and consumer interactions, and often include spaces designed for customer access and professional use.",
                            },
                            {
                                "id": "type-institutional-buildings",
                                "description": "This category specifically refers to buildings used for institutional purposes, including government, education, health care, religious, and cultural facilities. Examples include schools, hospitals, government offices, religious institutions, and museums. These buildings serve community, educational, health, or administrative functions and are usually operated by public or nonprofit organizations.",
                            },
                            {
                                "id": "type-street-lighting",
                                "description": "This category refers to street lighting infrastructure, which includes lighting installed along public streets, highways, pedestrian pathways, and public outdoor spaces. This type does not include interior building lighting or private property lighting.",
                            },
                        ],
                        "Manufacturing industries and construction": [
                            {
                                "id": "type-all",
                                "description": "This category encompasses all manufacturing industries and construction when a specific industry type is not specified. Use this general identifier when the precise type of manufacturing or construction activity is unclear or includes multiple types across this sector.",
                            },
                            {
                                "id": "type-manufacturing-industries-and-construction",
                                "description": "This refers broadly to manufacturing industries involved in the production of goods and construction activities that involve building infrastructure. Use this when referring to all manufacturing and construction sectors collectively.",
                            },
                            {
                                "id": "type-steel",
                                "description": "This category is specific to steel manufacturing industries, which involve the production of steel products from iron ore, scrap, or other raw materials.",
                            },
                            {
                                "id": "type-cement",
                                "description": "This category includes cement manufacturing industries focused on producing cement from limestone and other raw materials.",
                            },
                            {
                                "id": "type-iron",
                                "description": "This category covers industries involved in iron production, including the extraction and processing of iron ore to produce iron products.",
                            },
                            {
                                "id": "type-non-ferrous-metals",
                                "description": "This refers to the manufacturing of non-ferrous metals, including metals like aluminum, copper, and zinc.",
                            },
                            {
                                "id": "type-chemical-products",
                                "description": "This category is specific to the production of chemical products, which includes the manufacture of substances like petrochemicals, fertilizers, pharmaceuticals, and industrial gases.",
                            },
                            {
                                "id": "type-pulp-paper-and-printing",
                                "description": "This category covers industries involved in the production of pulp, paper, and printing materials.",
                            },
                            {
                                "id": "type-non-metallic-minerals",
                                "description": "This includes the production of non-metallic minerals, such as glass, ceramics, and construction materials (like clay or stone).",
                            },
                            {
                                "id": "type-transport-equipment",
                                "description": "This category refers to industries involved in the manufacturing of transportation equipment, including vehicles, aircraft, ships, and railway equipment.",
                            },
                            {
                                "id": "type-machinery",
                                "description": "This category includes the manufacturing of machinery used in various industries, from agriculture to construction. It covers industries producing heavy machinery, industrial tools, and equipment for specific applications.",
                            },
                            {
                                "id": "type-mining-and-quarrying",
                                "description": "This category encompasses activities related to mining and quarrying, including the extraction of minerals, metals, and stone from the earth.",
                            },
                            {
                                "id": "type-wood-and-wood-products",
                                "description": "This refers to industries producing wood products, including sawmills, lumber production, and the manufacture of wood-based products like furniture, plywood, and particleboard.",
                            },
                            {
                                "id": "type-construction",
                                "description": "This category includes all construction activities, covering building infrastructure, residential and commercial construction, and civil engineering projects.",
                            },
                            {
                                "id": "type-textiles-and-leather",
                                "description": "This includes industries engaged in the production of textiles, apparel, and leather goods.",
                            },
                            {
                                "id": "type-unspecified-industry",
                                "description": "This is used when the specific industry building or facility within manufacturing or construction is not specified.",
                            },
                        ],
                        "Energy industries": [
                            {
                                "id": "type-all",
                                "description": "It refers to all type of energy industries.",
                            }
                        ],
                        "Agriculture, forestry, and fishing activities": [
                            {
                                "id": "type-all",
                                "description": "It refers to all buildings where agriculture, forestry, and fishing activities ocurres. This includes farms, plantations, forests, and fishing facilities.",
                            }
                        ],
                        "Non-specified sources": [
                            {
                                "id": "type-all",
                                "description": "It refers to all non-specified sources.",
                            }
                        ],
                        "On-road": [
                            {
                                "id": "type-all",
                                "description": "This category includes all on-road vehicles, covering passenger, commercial, and other types of vehicles designed for travel on roads. Use this when the vehicle type is unspecified or encompasses multiple on-road types.",
                            },
                            {
                                "id": "vehicle-type-passenger-vehicles",
                                "description": "This category refers to passenger vehicles used primarily for transporting individuals or small groups. Examples include cars, taxis, vans, SUVs, and motorcycles. These vehicles are typically used for personal or public transportation of passengers.",
                            },
                            {
                                "id": "vehicle-type-commercial-vehicles",
                                "description": "This category includes commercial vehicles used for transporting goods or services on roads. Examples are delivery trucks, vans, lorries, and utility vehicles. These vehicles are designed to support business activities and goods movement.",
                            },
                        ],
                        "Railways": [
                            {
                                "id": "type-all",
                                "description": "This category refers to all types of railway transportation. Use this when the specific type of rail transport is not specified or includes multiple types such as passenger, freight, and high-speed trains.",
                            },
                            {
                                "id": "vehicle-type-passenger-trains",
                                "description": "This category is specific to passenger trains, which are used for transporting individuals over short or long distances. Examples include commuter trains, intercity trains, and regional trains that carry passengers between destinations.",
                            },
                            {
                                "id": "vehicle-type-freight-trains",
                                "description": "This category includes freight trains, which are designed for transporting goods rather than passengers. Examples include bulk cargo trains, container trains, and tank trains used to move raw materials, finished goods, and industrial products.",
                            },
                            {
                                "id": "vehicle-type-high-speed-trains",
                                "description": "This category refers to high-speed trains, which are specialized passenger trains operating at high speeds on dedicated tracks. Examples include trains like the TGV, Shinkansen, and other high-speed rail networks primarily used for rapid, intercity passenger travel.",
                            },
                            {
                                "id": "vehicle-type-tourist-trains",
                                "description": "This category is specific to tourist trains, which are designed to provide scenic or leisure travel experiences. Examples include heritage trains, scenic railway tours, and special trains offering sightseeing for tourists.",
                            },
                        ],
                        "Waterborne navigation": [
                            {
                                "id": "type-all",
                                "description": "This category includes all waterborne navigation vehicles used for travel or transport on water. Use this when the specific type of watercraft is not specified or when it includes multiple types like ferries, boats, and marine vessels.",
                            },
                            {
                                "id": "vehicle-type-ferries",
                                "description": "This category refers to ferries, which are boats or ships used to transport passengers and sometimes vehicles across water, often on scheduled routes. Common examples are passenger ferries, car ferries, and river ferries.",
                            },
                            {
                                "id": "vehicle-type-boats",
                                "description": "This category includes smaller boats primarily used for personal or recreational purposes. Examples are motorboats, sailboats, and fishing boats, which operate on various bodies of water for leisure, fishing, or small-scale transport.",
                            },
                            {
                                "id": "vehicle-type-marine-vessels",
                                "description": "This category encompasses larger marine vessels used for commercial and industrial purposes. Examples include cargo ships, tankers, and container ships, primarily used for long-distance transport of goods across seas and oceans.",
                            },
                        ],
                        "Aviation": [
                            {
                                "id": "type-all",
                                "description": "This category covers all aviation vehicles, encompassing both passenger and cargo aircraft. Use this category when the specific type of aircraft is not specified or includes multiple types.",
                            },
                            {
                                "id": "vehicle-type-passenger-aircraft",
                                "description": "This category refers to passenger aircraft used for transporting individuals on domestic or international flights. Examples include commercial airliners, regional jets, and private jets designed to carry passengers.",
                            },
                            {
                                "id": "vehicle-type-cargo-aircraft",
                                "description": "This category includes cargo aircraft specifically designed for transporting goods and freight rather than passengers. Examples include freighter planes, air cargo carriers, and logistics aircraft used by companies like FedEx and UPS.",
                            },
                        ],
                    },
                },
            },
        },
    },
}
