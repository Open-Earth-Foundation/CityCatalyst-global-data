# context_actval_transportation.py

# - Fuel sales within city boundaries (GPC reference number: II.1.1, Scope: 1)
#     * This can consist of gasoline, diesel, and other fuels used by vehicles for example sold by local gas stations (usually to end-users) or sold by distributors to businesses.
#     * Keywords: on-road, transportation, freight, sold to public, etc.
#     * Vehicles: including electric and fuelpowered cars, taxis, buses, etc.

context_actval_transportation = """
The following provides context for the activities for the sector 'Transportation'.
Each of these subsectors has a unique set of activities and keywords that can help identifying the correct GPC referecnce number. 
Different subsectors can share activities like fuel sales. Therefore it is important to also consider the vehicle type like taxi or agricultural tractor to identify the correct GPC reference number.    

Below are examples of activities for each of the 5 subsector:

a. On-road (GPC reference number: II.1)
    * This can consist of gasoline, diesel, and other fuels used by vehicles for example sold by local gas stations (usually to end-users) or sold by distributors to businesses.
    * Vehicles that are typically included here are: electric and fuelpowered cars, taxis, buses, etc. used on public roads.
    * Keywords: on-road, transportation, freight, sold to public, etc.

b. Railways (GPC reference number: II.2):
    * Vehicles that are typically included here are: trams, urban railway subway systems, regional (inter-city) commuter rail transport, national rail system, and international rail systems, etc.

c. Waterborne navigation (GPC reference number: II.3):
    * Vehicles that are typically included here are: sightseeing ferries, domestic inter-city vehicles, or international water-borne vehicles

d. Aviation (GPC reference number: II.4):
    * Vehicles that are typically included here are: helicopters, domestic inter-city flights, and international flights, etc.

e. Off-road (GPC reference number: II.5):
    * This can consist of gasoline, diesel, and other fuels used by **off-road** vehicles for example used for construction, agriculture, or other off-road activities.
    * Vehicles that are typically included here are: airport ground support equipment, agricultural tractors, chain saws, forklifts, snowmobiles, etc. used off-road.
    * Keywords: off-road, construction, agriculture, farming, etc.
"""
