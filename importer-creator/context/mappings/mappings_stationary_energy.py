stationary_energy_scope_2_subsector_to_gpc = {
    "__doc__": """
    This is the mapping of subsectors in the 'Stationary Energy' sector to GPC reference numbers for energy received or supplied to the grid. 
    Use this mapping to identify possible GPC reference numbers based on the subsector in the data.
    This mapping applies only for energy activity data related to energy received from the grid or supplied to the grid.
    
    E.g. if the subsector in the data is 'residential_buildings', and the activity is related to consumption of energy from the grid, the only possible GPC reference number is 'I.1.2'.
    E.g. if the subsector is 'energy_industries' and the activity is related to own use of energy from the grid for auxillary purposes, the only possible GPC reference number is 'I.4.2'. 
    E.g. if the subsector is 'energy_industries' and the activity is related to supplying energy to the grid, the only possible GPC reference number is 'I.4.2'. 
    """,
    "residential_buildings": "I.1.2",
    "commercial_and_institutional_buldings_and_facilities": "I.2.2",
    "manufacturing_industries_and_construction": "I.3.2",
    "energy_industries": {
        "energy_industries_auxillary_own_use": "I.4.2",
        "energy_industries_electricity_and_heat_production_to_the_grid": "I.4.4",
    },
}
