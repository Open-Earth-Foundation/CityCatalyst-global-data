# context_methodologies.py
methodologies_mapping = {
    "__doc__": """
    This is the dictionary of different methodologies for the 'Stationary Energy' sector and 'Transportation' sector.
    It is used to provide context for choosing the correct methodology based on the GPC (Global Protocol for Community-Scale Greenhouse Gas Emission Inventories) reference number and the activity units.

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
    - units: The units for the input values.
    - activity_name: The name of the activity to which the methodology is applicable.
    
    Examples:
    - if the activity name is "fuel_combustion", the gpc_refno is 'II.1.1' and the units are 'TJ', 'kg', or 'm3', the methodology to be used is 'fuel_combustion_consumption'.
    - if the activity name is "electricity_consumption", the gpc_refno is 'II.1.2' and the units are 'kWh', the methodology to be used is 'energy_consumption'.
    - if the activity name is "fuel_combustion", the gpc_refno is 'I.1.1' and the units are 'TJ', 'kg', or 'm3', the methodology to be used is 'fuel_sales'.
    - if the activity name is "vehicle_kilometers_traveled", the gpc_refno is 'II.2.1' and the units are 'pkm' or 'gkm', the methodology to be used is 'movement_driver'.
    """,
    "fuel_combustion_consumption": {
        "Sectors": "Stationary Energy",
        "Scope": 1,
        "gpc_refno": ["I.1.1", "I.2.1", "I.3.1", "I.4.1", "I.5.1", "I.6.1"],
        "activity_name": "fuel_combustion",
        "units": ["TJ", "kg", "m3"]
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
        "activity_name": "electricity_consumption",
        "units": ["kWh"]
    },
    "fuel_sales": {
        "sectors": "Transportation",
        "scope": 1,
        "gpc_refno": ["II.1.1", "II.2.1", "II.3.1", "II.4.1", "II.5.1"],
        "activity_name": "fuel_combustion",
        "units": ["TJ", "kg", "m3"]
    },
    "movement_driver": {
        "sectors": "Transportation",
        "scope": 1,
        "gpc_refno": ["II.2.1"],
        "activity_name": "vehicle_kilometers_traveled",
        "units": ["pkm", "gkm"]
    }
}
