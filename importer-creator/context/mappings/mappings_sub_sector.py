# context_sector_subsector.py

sub_sector_mapping = {
    "__doc__": """
    This dictionary maps Global Protocol for Community-Scale Greenhouse Gas Emission Inventories (GPC) sub-sectors to their respective GPC sectors, providing a clear overview of possible GPC sub-sectors based on GPC sector selection. 
    
    Instructions for the LLM:
    - The selected GPC sector already pre-selects the possible GPC sub-sectors.
    - GPC sub-sectors may be named differently in datasets, so focus on the descriptions to match semantically similar terms or variations in names.
    - This dictionary helps identify and map these GPC sub-sectors.
    
    Example 1: The current row was assigned the GPC sector "Stationary Energy". The GPC sub-sectors may only include one of "Residential buildings", "Commercial and institutional buildings and facilities", "Manufacturing industries and construction", "Energy industries", "Agriculture, forestry, and fishing activities", "Non-specified sources", "Fugitive emissions from mining, processing, storage, and transportation of coal" or "Fugitive emissions from oil and natural gas systems". The data contains the channel 'residential' which indicates usage for residential buildings. Based on this dictionary, this maps to the sub-sector "Residential buildings".
    Example 2: The current row was assigned the GPC sector "Transportation". The GPC sub-sectors may only include on of "On-road", "Railways", "Waterborne navigation", "Aviation" or "Off-road". The data inside the row contains contextual data related to 'agriculture' which indicates usage for agricultural vehicles. Based on this dictionary, this maps to the sub-sector "Off-road".
    Example 3: The current row was assigned the GPC sector "Transportation". The GPC sub-sectors may only include on of "On-road", "Railways", "Waterborne navigation", "Aviation" or "Off-road". The data inside the row contains contextual data related to 'ship fuels' which indicates usage for ships. Based on this dictionary, this maps to the sub-sector "Waterborne navigation".
    Example 4: The current row was assigned the GPC sector "Transportation". The GPC sub-sectors may only include on of "On-road", "Railways", "Waterborne navigation", "Aviation" or "Off-road". The data inside the row contains contextual data related to 'Jet fuel' which indicates usage for airplanes. Based on this dictionary, this maps to the sub-sector "Aviation".
    """,
    "Stationary Energy": {
        "subsectors": {
            "Residential buildings": {
                "description": """Emissions from the combustion of fuels used in residential buildings, such as natural gas, heating oil, and other fuels for heating, cooking, and other household activities. 
                Also, includes emissions from electricity consumption in residential buildings."""
            },
            "Commercial and institutional buildings and facilities": {
                "description": """Emissions from fuel combustion in commercial and institutional buildings and facilities, such as schools, hospitals, and office buildings, used for space heating, cooling, and power generation.
                Also, includes emissions from electricity consumption in commercial and institutional buildings."""
            },
            "Manufacturing industries and construction": {
                "description": """Emissions from fuel combustion in manufacturing industries and construction activities, including the use of furnaces, boilers, and machinery for production processes.
                Also, includes emissions from electricity consumption in manufacturing industries and construction activities."""
            },
            "Energy industries": {
                "description": """Emissions from energy generation facilities within the city boundary, including power plants that supply electricity and heat to the grid. It covers activities like electricity generation, petroleum refining, and the manufacture of solid fuels.
                Also, includes emissions from electricity consumption in energy industries."""
            },
            "Agriculture, forestry, and fishing activities": {
                "description": """Emissions from fuel combustion for energy use in agriculture, forestry, and fishing activities, such as the use of machinery for crop production, forest management, and fisheries.
                Also, includes emissions from electricity consumption in agriculture, forestry, and fishing activities."""
            },
            "Non-specified sources": {
                "description": """Emissions from fuel combustion and electricity consumption that cannot be attributed to a specific source within the stationary energy sector.
                This category is used when the source of emissions is not known or cannot be specified."""
            },
            "Fugitive emissions from mining, processing, storage, and transportation of coal": {
                "description": """Fugitive emissions released during the extraction, processing, storage, and transportation of solid fuels like coal. These emissions include methane released from mining operations."""
            },
            "Fugitive emissions from oil and natural gas systems": {
                "description": """Fugitive emissions released during the production, processing, storage, and distribution of oil and natural gas. This includes venting, flaring, and leaks from equipment and pipelines."""
            },
        },
    },
    "Transportation": {
        "subsectors": {
            "On-road": {
                "description": """Emissions from fuel combustion in on-road vehicles, including cars, trucks, buses, and motorcycles used for personal and commercial travel within the city boundary. 
                This subsector also includes emissions from electricity consumption for electric vehicles."""
            },
            "Railways": {
                "description": """Emissions from fuel combustion in trains, including both passenger and freight rail services, 
                as well as emissions from electricity consumption for electric rail systems and activities related with railways operations."""
            },
            "Waterborne navigation": {
                "description": """Emissions from fuel combustion in ships, ferries, and other vessels navigating within inland and coastal waters, including emissions from port activities.
                This subsector also includes emissions from electricity consumption (grid-supplied electricity) related to waterborne operations ."""
            },
            "Aviation": {
                "description": """Emissions from fuel combustion in aircraft, including domestic flights and flights departing from airports that serve the city, even if the airport is located outside the city boundary.
                This subsector also includes emissions from electricity consumption for airport operations. Typical keywords are 'Jet fuel', 'Kerosene' or 'Aircraft' but can also include semantically similar words. 
                All activities related to airplanes, air travel and aviation operations should be assigned to this subsector."""
            },
            "Off-road": {
                "description": """Emissions from fuel combustion in vehicles and equipment used off-road, such as construction machinery, agricultural equipment, and recreational vehicles.
                This subsector also includes emissions from electricity consumption for off-road operations."""
            },
        },
    },
    "Waste": {
        "subsectors": {
            "Disposal of solid waste": {
                "description": """Emissions from the decomposition of organic waste in landfills, where methane is released as waste breaks down anaerobically. 
                Includes emissions from managed and unmanaged landfill sites."""
            },
            "Biological treatment of waste": {
                "description": """Emissions from the aerobic or anaerobic decomposition of organic waste in composting facilities or anaerobic digestion systems, which produce methane, carbon dioxide, and other gases."""
            },
            "Incineration and open burning of waste": {
                "description": """Emissions from the combustion of waste materials in incineration plants or through open burning, producing carbon dioxide, methane, and nitrous oxide as waste is burned."""
            },
            "Wastewater treatment and discharge": {
                "description": """Emissions from the treatment of domestic and industrial wastewater, including methane and nitrous oxide produced during the treatment process and from sludge management."""
            },
        },
    },
    "Industrial Processes and Product Use": {
        "subsectors": {
            "Industrial processes": {
                "description": """Emissions from industrial activities that chemically or physically transform materials, such as the production of cement, iron and steel, chemicals, and other products. 
                This subsector includes direct emissions from industrial processes and indirect emissions from electricity consumption."""
            },
            "Product use": {
                "description": """Focuses on emissions that arise from the use of products containing GHGs within the city boundary. 
                These include substances like refrigerants, aerosol propellants, and fire suppression agents that release GHGs during their usage, maintenance, or disposal. 
                This subsector captures the non-energy emissions that result from the physical or chemical properties of these products."""
            },
        },
    },
    "Agriculture, Forestry and Other Land Use": {
        "subsectors": {
            "Livestock": {
                "description": """Emissions from enteric fermentation in ruminants and manure management systems, which release methane as part of the digestive process and decomposition of organic material."""
            },
            "Land use": {
                "description": """Emissions and removals from changes in land use, such as deforestation, afforestation, and conversion of land to different uses, impacting carbon stocks and soil carbon levels."""
            },
            "Aggregate sources": {
                "description": """Emissions from non-CO2 sources such as fertilizer application, burning of agricultural residues, and rice cultivation, which release nitrous oxide and methane."""
            },
        },
    },
}
