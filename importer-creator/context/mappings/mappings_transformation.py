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
    - gpc_refno: The GPC reference numbers associated with the methodology. ## for Minh: not sure about this, but we need gpc_refno to filter the Emission Factors
    - activity_value: The input values required for making the transformation.
    - activity_subcategorytype1: The subcategory type for the input value. For example what fuel_type
    - activity_subcategorytypename1: The subcategory name for the subcategory type. For example "Diesel"
    - activity_units: The units for the activity value.
    - emission_factor_value: The default emission factor value to be used for the calculation.
    - emission_factor_units: The default units for the default emission factor value which is normally used for the calculation.
    - formula: The formula to calculate the emissions from the activity data.
    
    E.g. if the methodology name is "fuel_combustion_consumption" for the identified GPC reference number 'I.1.1', the activity_subcategorytypename1 is needed.
    The activity value is typically in the units of TJ, kg, or m3.
    According to the formula given in the methodology, the emissions can be calculated by multiplying the activity value for the activity_subcategorytypename1 with the emission_factor_value, with the same units as the activity_units in the denominador.
    Which means that if the activity_units are in TJ, the emission_factor_units should be in kg/TJ.
    This should result in emissions in 'kg'.
    E.g. if the activity value is 1000 TJ and the emission factor value is 100 kg/TJ, the emissions will be 1000 TJ * 100 kg/TJ = 100,000 kg. ## For Minh: is this a good example for the model?
    """,
    "fuel_combustion_consumption": {
        "gpc_refno": ["I.1.1", "I.2.1", "I.3.1", "I.4.1", "I.5.1", "I.6.1"],
        "activity_value": "", #(??)
        "activity_subcategorytype1": "fuel_type",
        "activity_subcategorytypename1": "", #(??)
        "units": ["TJ", "kg", "m3"],
        "emission_factor_value": "", #(??)
        "emission_factor_units": ["kg/TJ", "kg/kg", "kg/m3"],
        "formula": "activity_value"*"emission_factor_value"
    },
    "energy_consumption": {
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
        "activity_value": "", #(??)
        "activity_subcategorytype1": "", #(??)
        "activity_subcategorytypename1": "", #(??)
        "units": ["kWh"],
        "emission_factor_value": "", #(??)
        "emission_factor_units": ["kg/kWh"],
        "formula": "activity_value"*"emission_factor_value"
    },
    "fuel_sales": {
        "gpc_refno": ["II.1.1", "II.2.1", "II.3.1", "II.4.1", "II.5.1"],
        "activity_value": "", #(??)
        "activity_subcategorytype1": "fuel_type",
        "activity_subcategorytypename1": "", #(??)
        "units": ["TJ", "kg", "m3"],
        "emission_factor_value": "", #(??)
        "emission_factor_units": ["kg/TJ", "kg/kg", "kg/m3"],
        "formula": "activity_value"*"emission_factor_value"
    },
    "movement_driver": {
        "gpc_refno": ["II.2.1"],
        "activity_value": "", #(??)
        "activity_subcategorytype1": "vehicle_type",
        "activity_subcategorytypename1": "", #(??)
        "units": ["pkm", "gkm"],
        "emission_factor_value": "", #(??)
        "emission_factor_units": ["kg/pkm", "kg/gkm"],
        "formula": "activity_value"*"emission_factor_value"
    },
}