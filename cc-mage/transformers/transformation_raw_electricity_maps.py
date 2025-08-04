if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
from pandas import DataFrame

@transformer
def transform(data: DataFrame, *args, **kwargs):
    """
    """
    # diccionary of GWP AR6 - 2021 - 100-year time period
    GWP_dic_100years = {
        "CO2": {"value": 1, "portion": 0.80},
        "CH4": {"value": 29.8, "portion": 0.15},
        "N2O": {"value": 273, "portion": 0.05},
    }

    gpc_mapping = {
        'I.1.2': 'energy-consumption-residential-buildings-methodology',
        'I.2.2': 'energy-consumption-commercial-buildings-methodology', 
        'I.3.2': 'energy-consumption-manufacturing-and-construction-methodology', 
        'I.4.2': 'energy-consumption-energy-industries-methodology', 
        'I.5.2': 'energy-consumption-agriculture-forestry-fishing-activities-methodology', 
        'I.6.2': 'energy-consumption-non-specific-sources-methodology', 
        'II.1.2': 'electricity-consumption-on-road-transport-methodology', 
        'II.2.2': 'electricity-consumption-railways-methodology', 
        'II.3.2': 'electricity-consumption-waterborne-navigation-methodology', 
        'II.4.2': 'electricity-consumption-aviation-methodology', 
        'II.5.2': 'electricity-consumption-off-road-transport-methodology', 
    }

    # standarization of zone ids
    data['Zone id'].replace({'CL-SEN':'CL', 'ES-CE': 'ES', 'FR-COR': 'FR', 'US-SW-PNM': 'US'}, inplace=True)

    # Extract the year from the 'start_time' column
    data['Datetime (UTC)'] = pd.to_datetime(data['Datetime (UTC)'])
    data['year'] = data['Datetime (UTC)'].dt.year

    # rename columns
    data.rename(columns={
        'Country': 'region', 
        'Zone id': 'actor_id',
        'Carbon intensity gCO₂eq/kWh (direct)': 'emissions_per_activity',
        'Data estimation method': 'reference',
        'Data source': 'datasource_name'}, 
        inplace=True)

    # units conversion from gCO₂eq/kWh to kgCO₂eq/kWh
    data['emissions_per_activity'] *= 1e-3

    # filter needed columns
    data = data[['region', 'actor_id', 'emissions_per_activity', 'reference', 'year', 'datasource_name']]

    # applying portions of contribution of each gas and calculating emission values
    new_rows = []
    for index, row in data.iterrows():
        total_co2e = row["emissions_per_activity"]

        for gas in GWP_dic_100years.keys():
            new_row = row.copy()
            new_row["gas"] = gas
            new_row["emissions_per_activity"] = (
                GWP_dic_100years[gas]["portion"] * total_co2e
            ) / GWP_dic_100years[gas]["value"]
            new_rows.append(new_row)

    data = pd.DataFrame(new_rows)

    # assign gpc_reference_number and methodology_name
    data = pd.concat([
        data.assign(gpc_reference_number=gpc, methodology_name=methodology)
        for gpc, methodology in gpc_mapping.items()
    ], ignore_index=True)

    # adding extra columns
    data['units'] = 'kg/kWh'
    data['activity_name'] = 'activity-energy-consumption'
    data['activity_units'] = 'kWh'
    data['publisher_name'] = 'Electricity Maps'
    data['publisher_url'] = 'https://portal.electricitymaps.com/dashboard'
    data['dataset_name'] = 'Carbon intensity'
    data['dataset_url'] = 'https://portal.electricitymaps.com/datasets/'

    # assigning generic datasource_name for empty values
    data['datasource_name'].fillna('Electricity Maps', inplace=True)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
