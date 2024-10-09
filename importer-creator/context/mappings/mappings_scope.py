# Python dictionary to map scopes to their corresponding activities

scope_mappings = {
    "__doc__": """
    This dictionary maps the scopes numbers from GPC (Global Protocol for Community-Scale Greenhouse Gas Emission Inventories) to their corresponding activities.

    Examples:
    - Combustion or consumption of fuels is always considered to be scope 1 emissions
    - Grid-supplied energy like electricity, heat, cold and steam is always considered to be scope 2 emissions
    """,
    
    "1": [
        "Combustion of fuels",
        "Consumption of fuels",
        "Fuggitive emissions",
        "Inboundary trips",
        "Trips within the city boundary",
        "Waste disposed within the city",
        "Waste treated biologically within the city",
        "Waste treated within the city",
    ],
    "2": [
        "Grid-supplied energy like electricity, heat, cold and steam",
        "Grid energy consumed",
        "Energy consumption"
    ],
    "3": [
        "Transmission and distribution losses from purchased electricity",
        "Transmission and distribution losses from grid-supplied energy",
        "Transboundary journeys",
        "Waste disposed outside the city",
        "Waste treated biologically outside the city",
        "Waste treated outside the city"
    ],
}
