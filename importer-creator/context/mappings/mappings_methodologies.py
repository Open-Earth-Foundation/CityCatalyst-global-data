# context_methodologies.py

# @ Mau: Please check the mapping and
# how it is best to structure based on the information we have extracted until here like GPC number, activities and so on.
# what names do we need to use for the keys e.g. input_values and so on so thetyt align with the activities mappings?

methodologies_mapping = {
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
    - sectors: The sector to which the methodology belongs
    - scope: The scope of the methodology. This indicates for which scopes the methodology is applicable
    - gpc_refno: The GPC reference numbers associated with the methodology. 
    - input_values: The input values required for making the transformation.
    - subcategories_i_j: The subcategories for the input values. For example what fuel type (i) and building type (j) for the input values total_fuel_consumption.
    - units: The units for the input values.
    - default_value: The default emission factor value to be used for the calculation.
    - default_units: The default units for the default emission factor value which is normally used for the calculation.
    - formula: The formula to calculate the emissions from the activity data. It is encoded in LaTeX format.
    
    E.g. if the activity data is related to fuel combustion consumption for 'Stationary Energy' sector and the identified GPC reference number is 'I.2.1', the fuel type (i) and building type (j) is needed. 
    The activity value is typically in the units of TJ, kg, or m3.
    According to the formula given in the methodology, the emissions can be calculated by multiplying the activity value for the fuel type (i) and the building type (j) with the default emission_factor (i).
    This should result in emissions in 'kg'.

    E.g. if the activity data is related to energy consumption (from the grid) for 'Stationary Energy' or 'Transportation' sector and the identified GPC reference number is 'II.1.2', the building type (j) or transport type (j) is needed.
    The activity value is typically in the units of kWh.
    According to the formula given in the methodology, the emissions can be calculated by multiplying the activity value for the building type (j) or transport type (j) with the default emission_factor (i).
    This should result in emissions in 'kg'.
    """,
    "fuel_combustion_consumption": {
        "Sectors": "Stationary Energy",
        "Scope": 1,
        "gpc_refno": ["I.1.1", "I.2.1", "I.3.1", "I.4.1", "I.5.1", "I.6.1"],
        "input_values": "total_fuel_consumption",
        "subcategories_i_j": ["fuel_type (i)", "building_type (j)"],
        "units": ["TJ", "kg", "m3"],
        "default_value": "emission_factor (i)",
        "default_units": ["kg/TJ", "kg/kg", "kg/m3"],
        "formula": "\text{emissions}_\text{i,j}=\text{activity_value}_\text{i,j}*\text{emission_factor}_\text{i}",
    },
    "energy_consumption": {
        "sectors": "Stationary Energy and Transportation",
        "scope": 2,
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
        "input_values": "total_fuel_consumption",
        "subcategories_i_j": ["building_type (j)", "transport_type (j)"],
        "units": ["kWh"],
        "default_value": "emission_factor (i)",
        "dafault_units": ["kg/kW"],
        "formula": "\text{emissions}_\text{i,j}=\text{activity_value}_\text{i,j}*\text{emission_factor}_\text{i}",
    },
    "fuel_sales": {
        "sectors": "Transportation",
        "scope": 1,
        "gpc_refno": ["II.1.1", "II.2.1", "II.3.1", "II.4.1", "II.5.1"],
        "input_values": "total_fuel_sold",
        "subcategories_i_j": ["fuel_type (i)", "transport_type (j)"],
        "units": ["TJ", "kg", "m3"],
        "default_value": "emission_factor (i)",
        "default_units": ["kg/TJ", "kg/kg", "kg/m3"],
        "formula": "\text{emissions}_\text{i,j}=\text{activity_value}_\text{i,j}*\text{emission_factor}_\text{i}",
    },
    "movement_driver": {
        "sectors": "Transportation",
        "scope": 1,
        "gpc_refno": ["II.2.1"],
        "input_values": "total_movement_driver",
        "subcategories_i_j": ["transport_type (j)"],
        "units": ["pkm", "gkm"],
        "default_value": "emission_factor (j)",
        "default_units": ["kg/pkm", "kg/gkm"],
        "formula": "\text{emissions}_\text{i,j}=\text{activity_value}_\text{i,j}*\text{emission_factor}_\text{i}",
    },
}
