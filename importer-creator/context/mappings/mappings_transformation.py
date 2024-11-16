transformation_mapping = {
    "__doc__": """
    This is the dictionary of different methodologies for the 'Stationary Energy' sector and 'Transportation' sector.
    It is used to provide context for choosing the correct methodology and for making transformations from activity data to emission values.

    The dictionary contains the following:
    4 methodologies as follows:
    1. fuel_combustion_consumption
    2. energy_consumption
    3. fuel_sales
    4. movement_driver

    Each methodology contains the following:
    - activity_value: A description of the input values required for making the transformation.
    - activity_units: The units for the activity value.
    - emission_factor_value: A description of the emission factor value to be used for the calculation.
    - emission_factor_units: The units for the emission factor value.
    - formula: The formula to calculate the emissions from the activity data.

    For examples:
    - if the methodology is "fuel_combustion_consumption" and the activity value is 1000 TJ with an emission factor of 100 kg/TJ, the emissions will be calculated as:
    Emissions = 1000 TJ * 100 kg/TJ = 100,000 kg.
    - if the methodology is "energy_consumption" and the activity value is 1000 kWh with an emission factor of 0.5 kg/kWh, the emissions will be calculated as:
    Emissions = 1000 kWh * 0.5 kg/kWh = 500 kg.
    """,
    "fuel_combustion_consumption": {
        "activity_value": "Fuel consumption (e.g., mass or volume of fuel used)",
        "units": ["TJ", "kg", "m3"],
        "emission_factor_value": "Emission factor associated with the fuel type",
        "emission_factor_units": ["kg/TJ", "kg/kg", "kg/m3"],
        "formula": "activity_value * emission_factor_value"
    },
    "energy_consumption": {
        "activity_value": "Energy consumption in kilowatt-hours",
        "units": ["kWh"],
        "emission_factor_value": "Emission factor per unit of electricity consumed",
        "emission_factor_units": ["kg/kWh"],
        "formula": "activity_value * emission_factor_value"
    },
    "fuel_sales": {
        "activity_value": "Total fuel sales data",
        "units": ["TJ", "kg", "m3"],
        "emission_factor_value": "Emission factor for the specific fuel type",
        "emission_factor_units": ["kg/TJ", "kg/kg", "kg/m3"],
        "formula": "activity_value * emission_factor_value"
    },
    "movement_driver": {
        "activity_value": "Transport activity data (e.g., passenger-kilometers or goods-kilometers)",
        "units": ["pkm", "gkm"],
        "emission_factor_value": "Emission factor for the specific vehicle type",
        "emission_factor_units": ["kg/pkm", "kg/gkm"],
        "formula": "activity_value * emission_factor_value"
    },
}
