# Python dictionary to map scopes to their corresponding activities

# fuel sales are fuel combustion

scope_mappings = {
    "__doc__": """
    This dictionary maps the GPC scope numbers from Global Protocol for Community-Scale Greenhouse Gas Emission Inventories (GPC) to their corresponding activities.

    Instructions for the LLM:
    - Combustion or consumption of fuels like diesel, methane, propane, oil, liquified petroleum gas, etc. is always considered to be scope 1 emissions. Fuel sales are also considered to be scope 1 emissions.
    - Grid-supplied energy and energy consumed like electricity, heat, cold and steam is always considered to be scope 2 emissions

    Examples:
    - Combustion of fuels for cars is assigned to scope 1
    - Data about fuel sales like selling of oils for usage in products are assigned to scope 1
    - Grid-supplied energy like electricity for office buildings is assigned to scope 2
    """,
    "1": {
        "description": "Scope 1 emissions are direct emissions from sources located within the city boundary.",
        "examples": [
            "Combustion of fuels",
            "Consumption of fuels",
            "Fuggitive emissions",
            "Inboundary trips",
            "Trips within the city boundary",
            "Waste disposed within the city",
            "Waste treated biologically within the city",
            "Waste treated within the city",
            "Fuel sales",
            "Fuel distribution",
        ],
    },
    "2": {
        "description": "Scope 2 emissions are indirect emissions resulting from the consumption of grid-supplied electricity, heat, steam, and/or cooling within the city boundary.",
        "examples": [
            "Grid-supplied energy like electricity, heat, cold and steam",
            "Grid energy consumed",
            "Energy consumption",
        ],
    },
    "3": {
        "description": "Scope 3 emissions are all other indirect emissions that occur outside the city boundary as a result of activities taking place within the city.",
        "examples": [
            "Transmission and distribution losses from purchased electricity",
            "Transmission and distribution losses from grid-supplied energy",
            "Transboundary journeys",
            "Waste disposed outside the city",
            "Waste treated biologically outside the city",
            "Waste treated outside the city",
        ],
    },
}
