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
        "Consumption of fuels"
    ],
    "2": [
        "Grid-supplied energy like electricity, heat, cold and steam",
        "Energy consumption"
    ],
    "3": [
        "Transmission and distribution losses from purchased electricity",
        "Transmission and distribution losses from grid-supplied energy",
        "Transboundary journeys",
        "waste disposed outside the city",
        "waste treated biologically outside the city"
    ],
}
