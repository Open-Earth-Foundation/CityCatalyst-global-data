##---------------------------------------------------------
## Mapping Diccionaries
##---------------------------------------------------------
# mapping fuel names from the source to IPCC
fuel_mapping = {
    "Motor Gasoline/Petrol": "Gasoline",
    "On-Road Diesel Fuel": "Diesel",
    "Liquefied Petroleum Gases (LPG)": "Liquefied Petroleum Gas (LPG)",
    "Kerosene - Type Jet Fuel": "Kerosene",
    "Motor Gasoline": "Gasoline",
    "Diesel Fuel": "Diesel",
    "Residual Fuel Oil2": "Residual Fuel Oil",
    "Ethanol (100%)": "Ethanol",
    "Biodiesel (100%)": "Biodiesel",
    "E85 Ethanol/Gasoline*": "E85 Ethanol",
    "B20 Biodiesel/Diesel*": "B20 Biodiesel",
    "Aviation spirit (Aviation Gasoline)": "Aviation Gasoline",
    "Aviation turbine fuel (Jet Fuel)": "Jet Fuel",
    "Diesel (100% mineral diesel)": "Diesel",
    "Fuel oil (Residual Fuel Oil)": "Residual Fuel Oil",
    "Petrol (100% mineral petrol) (Motor Gasoline)": "Gasoline",
    "Processed fuel oils - residual oil": "Residual Fuel Oil",
    "Natural gas (100% mineral blend)": "Natural Gas",
    "Bioethanol3": "Bioethanol",
    "Biodiesel ME3": "Biodiesel",
    "Jet Fuel": "Jet Kerosene",
    "LPG": "Liquefied Petroleum Gas (LPG)",
}

# mapping fuel names to gpc_refno
fuel_to_gpc = {
    "__doc__": """
    This is the mapping of fuel names to possible GPC reference numbers. Use this mapping to identify all possible GPC reference numbers based on the fuel names in the data. 
    You will need to combine this mapping with other information to identify a single correct GPC reference number.

    E.g. if the fuel name in the data is 'Motor Gasoline/Petrol', the possible GPC reference numbers are ['II.1.1', 'II.2.1', 'II.3.1', 'II.5.1'].
    E.g. if the fuel name in the data is 'Jet Kerosene', the only possible GPC reference numbers are ['II.4.1'].

    This gives you a guide on a possible pre-assignment of GPC reference numbers based on the fuel names in the data. In cases where multiple GPC reference numbers are possible for a fuel name, use further provided context to identify the correct GPC reference number.
   
    Note: The names are exmaple names and can vary in the data. The names could also be in a different language depending on the data file. Use your best judgement to find semantically similar names in the data.
    """,
    "Jet Kerosene": ["II.4.1"],
    "Aviation Gasoline": ["II.4.1"],
    "Motor Gasoline/Petrol": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "On-Road Diesel Fuel": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "Residual Fuel Oil": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "Liquefied Petroleum Gases (LPG)": [
        "II.1.1",
        "II.2.1",
        "II.3.1",
        "II.4.1",
        "II.5.1",
    ],
    "Compressed Natural Gas (CNG)": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "Kerosene - Type Jet Fuel": ["II.4.1"],
    "Motor Gasoline": ["II.1.1", "II.2.1", "II.3.1", "II.4.1", "II.5.1"],
    "Diesel Fuel": ["II.1.1", "II.2.1", "II.3.1", "II.4.1", "II.5.1"],
    "Residual Fuel Oil2": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "Liquefied Natural Gas (LNG)": ["II.1.1", "II.2.1", "II.3.1", "II.4.1", "II.5.1"],
    "E85 Ethanol/Gasoline*": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "B20 Biodiesel/Diesel*": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "Aviation spirit (Aviation Gasoline)": ["II.4.1"],
    "Aviation turbine fuel (Jet Fuel)": ["II.4.1"],
    "Diesel (100% mineral diesel)": ["II.1.1", "II.2.1", "II.3.1", "II.4.1", "II.5.1"],
    "Fuel oil (Residual Fuel Oil)": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "Petrol (100% mineral petrol) (Motor Gasoline)": [
        "II.1.1",
        "II.2.1",
        "II.3.1",
        "II.4.1",
        "II.5.1",
    ],
    "Processed fuel oils - residual oil": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "Natural gas (100% mineral blend)": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "Ethanol (100%)": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "Biodiesel (100%)": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "Bioethanol3": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    "Biodiesel ME3": ["II.1.1", "II.2.1", "II.3.1", "II.5.1"],
    # Check with Mau
    "Off-Road Diesel Fuel": ["II.5.1"],
}

# mapping transport types to gpc_refno
transport_type_to_gpc = {
    "__doc__": """
    This is the mapping of transportation types to possible GPC reference numbers. Use this mapping to identify all possible GPC reference numbers based on the transportation types in the data.
    
    E.g. if the transport type in the data is 'Rail', the only possible GPC reference number is ['II.2.1'].
    E.g. if the transport type in the data is 'Agriculture Equipment', the only possible GPC reference number is ['II.5.1'].
    E.g. if the transport type in the data is 'Medium-Duty Truck', the possible GPC reference numbers are ['II.1.1', 'II.5.1'].

    This gives you a guide on a possible pre-assignment of GPC reference numbers based on the transport types in the data. In cases where multiple GPC reference numbers are possible for a transport type, use further provided context to identify the correct GPC reference number.
    
    Note: The names are exmaple names and can vary in the data. The names could also be in a different language depending on the data file. Use your best judgement to find semantically similar names in the data.
    """,
    "Rail": ["II.2.1"],
    "Agriculture Equipment": ["II.5.1"],
    "Forestry Equipment": ["II.5.1"],
    "Industry Equipment": ["II.5.1"],
    "Household Equipment": ["II.5.1"],
    "Ship and Boat": ["II.3.1"],
    "Locomotives": ["II.2.1"],
    "Aircraft": ["II.4.1"],
    "Agricultural Equipment1": ["II.5.1"],
    "Construction Equipment2": ["II.5.1"],
    "Lawn and Garden Equipment": ["II.5.1"],
    "Airport Equipment": ["II.5.1"],
    "Industrial/Commercial Equipment": ["II.5.1"],
    "Logging Equipment": ["II.5.1"],
    "Railroad Equipment": ["II.5.1"],
    "Recreational Equipment": ["II.5.1"],
    "Freight flights": ["II.4.1"],
    "Vans": ["II.1.1"],
    "HGV - Rigid": ["II.1.1", "II.5.1"],
    "HGV - Articulated": ["II.1.1"],
    "HGV - Type Unknown": ["II.1.1"],
    "Sea tanker": ["II.3.1"],
    "Cargo ship": ["II.3.1"],
    "Medium-Duty Truck": ["II.1.1", "II.5.1"],
    "Heavy-Duty Truck": ["II.1.1", "II.5.1"],
    "Waterborne Craft": ["II.3.1"],
    "Medium-Duty Truck": ["II.1.1", "II.5.1"],
    "Heavy-Duty Truck": ["II.1.1", "II.5.1"],
    "Passenger Car6": ["II.1.1"],
    "Light-Duty Truck7": ["II.1.1", "II.5.1"],
    "Air Travel - Short Haul": ["II.4.1"],
    "Air - Medium Haul": ["II.4.1"],
    "Air - Long Haul": ["II.4.1"],
    "Intercity Rail": ["II.2.1"],
    "Intercity Rail ": ["II.2.1"],
    "Commuter Rail": ["II.2.1"],
    "Transit Rail": ["II.2.1"],
    "Bus": ["II.1.1", "II.5.1"],
    "Medium-Duty Truck5": ["II.1.1", "II.5.1"],
    "Heavy-Duty Truck5": ["II.1.1", "II.5.1"],
    "Waterborne Craft": ["II.3.1"],
    "Aircraft": ["II.4.1"],
    "Passenger Car8": ["II.1.1"],
    "Light-Duty Truck9": ["II.1.1", "II.5.1"],
    "Motorcycle": ["II.1.1"],
    "Air - Domestic1,2": ["II.4.1"],
    "Air - Short Haul1, up to 3700km distance": ["II.4.1"],
    "Air - Long Haul1, over 3700km distance": ["II.4.1"],
    "Air - International1": ["II.4.1"],
    "Taxi": ["II.1.1"],
    "Average Ferry": ["II.3.1"],
    # Confirm with Mau
    "Public Transport Bus": ["II.1.1"],
    "Public Transport Rail": ["II.2.2"],
}
