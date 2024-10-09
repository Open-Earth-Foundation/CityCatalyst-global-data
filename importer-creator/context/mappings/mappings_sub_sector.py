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
    "stationary_energy": {
        "description": "GPC sub-sectors associated with stationary energy sources.",
        "sub_sectors": {
            "Residential buildings": "",
            "Commercial and institutional buildings and facilities": "",
            "Manufacturing industries and construction": "",
            "Energy industries": "",
            "Energy generation supplied to the grid": "",
            "Agriculture, forestry, and fishing activities": "",
            "Non-specified sources": "",
            "Fugitive emissions from mining, processing, storage, and transportation of coal": "",
            "Fugitive emissions from oil and natural gas systems": "",
        },
    },
    "transportation": {
        "description": "GPC sub-sectors associated with different modes of transportation, each contributing to GHG emissions through fuel combustion or electricity use.",
        "sub_sectors": {
            "On-road": "",
            "Railways": "",
            "Waterborne navigation": "",
            "Aviation": "",
            "Off-road": "",
        },
    },
    "waste": {
        "description": "GPC sub-sectors associated with waste management and treatment processes that generate GHG emissions, differentiated by waste origin and disposal methods.",
        "sub_sectors": {
            "Disposal of solid waste generated in the city": "",
            "Disposal of solid waste generated outside the city": "",
            "Biological treatment of waste generated in the city": "",
            "Biological treatment of waste generated outside the city": "",
            "Incineration and open burning of waste generated in the city": "",
            "Incineration and open burning of waste generated outside the city": "",
            "Wastewater generated in the city": "",
            "Wastewater generated outside the city": "",
        },
    },
    "industrial_process_and_product_use": {
        "description": "",
        "sub_sectors": {},
    },
    "agriculture_forestry_and_land_use": {
        "description": "",
        "sub_sectors": {},
    },
}
