# context_activity_values_transportation.py


context_activity_values_transportation = """
The following provides context for the activity values for the sector 'Transportation'.

The sector 'Transportation' contains the following 5 subsectors:

1. **On-road**
2. **Railways**
3. **Waterborne navigation**
4. **Aviation**
5. **Off-road**

Each of these subsectors has a unique set of activity values that are used to quantify the environmental impact of the sector. 
These activity values are used to calculate the environmental impact of the sector in terms of emissions, energy consumption, and other environmental indicators.

Below are examples of activity values for each subsector:

1. **On-road**:
    - Fuel sales within city boundaries
        * This can consist of gasoline, diesel, and other fuels used by vehicles within the city sold by local gas stations in retail (usually to end-users) or sold by distributors to businesses.
        * Positive examples are: 
            + Volume sold (e.g. in liters, gallons, etc.) of gasoline, diesel, CNG (compressed natural gas), and other fuels.
            + ...
        * Negative examples (not activity values) are:
            + Revenue made by selling fuels
            + ...
            
2. **Railways**:
    - Passenger-kilometers
        * This is the number of kilometers traveled by passengers on trains.
        * Examples are:
            + Number of passenger-kilometers traveled by train.
            + ...
        * Negative examples (not activity values) are:
            + Revenue made by passenger sales
            + ...
    - Freight-tonne-kilometers
        * This is the number of kilometers traveled by freight (goods) on trains.
        * Examples are:
            + Number of freight-tonne-kilometers traveled by train.
            + ...
"""

# COMMENTS
"""
If we count fuel sales by retail and distributors cant this appear double e.g. when a distributor sells to a retail station and then the retail station sells to the end user?
Can we add negative examples for each activity value? E.g. values that might appear to be activity values but are not?
Maybe revenue (like EUR or $) or something similar?
"""
