# context_sector_subsector.py

sub_sector_mapping = {
    "__doc__": """
    This dictionary maps Global Protocol for Community-Scale Greenhouse Gas Emission Inventories (GPC) sub-sectors to their respective GPC sectors, providing a clear overview of possible GPC sub-sectors based on GPC sector selection. 

    Instructions for the LLM:
    - The GPC sector already pre-selects the possible GPC sub-sectors.
    - GPC sub-sectors may be named differently in datasets, so focus on the descriptions to match semantically similar terms or variations in names.
    - This dictionary helps identify and map these GPC sub-sectors.
    
    Example:
    - For the "Stationary Energy" GPC sector, the GPC sub-sectors may include "Residential buildings" or "Energy industries".
    - For the "Transportation" GPC sector, the GPC sub-sectors may include "On-road" or "Aviation".

    The names provided in this dictionary are indicative and can be adjusted to match dataset terminology.
    """,
    "Stationary Energy": {
        "description": """Stationary energy sources are one of the largest contributors to a city's GHG emissions.
        These emissions come from the combustion of fuel in residential, commercial and institutional buildings, 
        and manufacturing industries and construction, as well as power plants to generate grid-supplied energy.
        This sector also includes fugitive emissions, which typically occur during extraction, transformation, 
        and transportation of primary fossil fuels.""",
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
        "description": """Transportation covers all journeys by road, rail, water and air, including inter-city and international travel. 
        GHG emissions are produced directly by the combustion of fuel or indirectly by the use of grid-supplied electricity. 
        Collecting accurate data for transportation activities, calculating emissions and allocating these emissions to cities can be a particularly challenging process. 
        To accommodate variations in data availability, existing transportation models, and inventory purposes, 
        the GPC offers additional flexibility in calculating emissions from transportation.""",
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
                This subsector also includes emissions from electricity consumption for airport operations."""
            },
            "Off-road": {
                "description": """Emissions from fuel combustion in vehicles and equipment used off-road, such as construction machinery, agricultural equipment, and recreational vehicles.
                This subsector also includes emissions from electricity consumption for off-road operations."""
            },
        },
    },
    "Waste": {
        "description": """Waste disposal and treatment produces GHG emissions through aerobic or anaerobic decomposition, or incineration. 
        GHG emissions from solid waste shall be calculated by disposal route, namely landfill, biological treatment and incineration and open burning. 
        If methane is recovered from solid waste or wastewater treatment facilities as an energy source, it shall be reported under Stationary Energy. 
        Similarly, emissions from incineration with energy recovery are reported under Stationary Energy.""",
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
        "description": """GHG emissions are produced from a wide variety of non-energy related industrial activities. 
        The main emission sources are releases from industrial processes that chemically or physically transform materials (e.g., the blast furnace in the iron and steel industry, 
        and ammonia and other chemical products manufactured from fossil fuels and used as chemical feedstock). 
        During these processes many different GHGs can be produced. 
        In addition, certain products used by industry and end-consumers, such as refrigerants, foams or aerosol cans, also contain GHGs which can be released during use and disposal.""",
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
        "description": """Emissions and removals from the Agriculture, Forestry and Other Land Use (AFOLU) sector are produced through a variety of pathways, 
        including livestock (enteric fermentation and manure management), land use and land use change (e.g., forested land being cleared for cropland or settlements), 
        and aggregate sources and non-CO2 emission sources on land (e.g., fertilizer application and rice cultivation).""",
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
