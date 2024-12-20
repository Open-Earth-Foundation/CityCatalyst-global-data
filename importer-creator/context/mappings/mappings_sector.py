# context_sector_subsector.py

sector_mapping = {
    "__doc__": """
    This dictionary provides an overview of different Global Protocol for Community-Scale Greenhouse Gas Emission Inventories (GPC) sectors along with their descriptions.
    It is designed to help identify the correct sector when working with Greenhouse Gas (GHG) emission data in various domains like energy, transportation, waste, industrial processes, and agriculture.
    When deciding on the sector, consider the entire context of a given activity. Keywords like 'agriculture' do not necessarily mean that the activity belongs to the Agriculture, Forestry and Other Land Use sector,
    but could be related to fuel consumption of agricultural verhicles. 

    Instructions for the LLM:
    - Sectors may be named differently in datasets, so focus on the descriptions to match semantically similar terms or variations in names.
    - This dictionary helps identify and map these GPC sectors.

    Examples:
    - Fuel sales for agricultural vehicles belong to the Transport sector
    - Electricity consumption in office buildings belongs to the Stationary Energy sector
    - Fuel combustion in industrial facilities belongs to Stationary Energy sector
    - Raising cattle for dairy or meat production or converting forest land to cropland for agricultural purposes belongs to the Agriculture, Forestry and Other Land Use sector
    """,
    "Stationary Energy": {
        "description": """These emissions come from the combustion of fuels (e.g. propane, diesel, oil, natural gas, and others) in residential, commercial and institutional buildings and facilities and manufacturing industries and construction, 
        as well as power plants to generate grid-supplied energy. This sector also includes fugitive emissions, which typically occur during extraction, transformation, 
        and transportation of primary fossil fuels."""
    },
    "Transportation": {
        "description": """Transportation covers all journeys by road, rail, water and air, including inter-city and international travel. 
        GHG emissions are produced directly by the combustion of fuel or indirectly by the use of grid-supplied electricity.""",
    },
    "Waste": {
        "description": """The waste sector generates GHG emissions from various disposal and treatment processes, including solid waste disposal, biological treatment, incineration or open burning and wastewater. 
        Emissions from solid waste disposal arise primarily from anaerobic decomposition in landfills, which releases methane (CH4). 
        Biological treatment, such as composting or anaerobic digestion, can produce methane and carbon dioxide (CO2) depending on the process conditions. 
        Incineration and open burning of waste release CO2, methane, and nitrous oxide (N2O). 
        If methane is captured and used as an energy source from solid waste or wastewater treatment facilities, it is reported under Stationary Energy, as are emissions from incineration with energy recovery. 
        Additionally, this sector accounts for emissions from wastewater treatment processes, covering both domestic and industrial sources.""",
    },
    "Industrial Processes and Product Use": {
        "description": """GHG emissions are produced from a wide variety of non-energy related industrial activities. 
        The main emission sources are releases from industrial processes that chemically or physically transform materials (e.g., the blast furnace in the iron and steel industry, 
        and ammonia and other chemical products manufactured from fossil fuels and used as chemical feedstock). 
        During these processes many different GHGs can be produced. 
        In addition, certain products used by industry and end-consumers, such as refrigerants, foams or aerosol cans, also contain GHGs which can be released during use and disposal.""",
    },
    "Agriculture, Forestry and Other Land Use": {
        "description": """Emissions and removals from the Agriculture, Forestry and Other Land Use (AFOLU) sector are produced through a variety of pathways, 
        including livestock (enteric fermentation and manure management), land use and land use change (e.g., forested land being cleared for cropland or settlements), 
        and aggregate sources and non-CO2 emission sources on land (e.g., fertilizer application and rice cultivation).""",
    },
}
