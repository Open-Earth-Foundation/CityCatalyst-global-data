if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd
from pandas import DataFrame

@transformer
def transform(data: DataFrame, *args, **kwargs):

    # Filtering the df 
    data = data[['source_name', 'iso3_country', 'subsector', 'start_time', 'lat', 'lon', 'gas', 'emissions_quantity', 'temporal_granularity', 'activity', 
    'activity_units', 'emissions_factor', 'emissions_factor_units', 'capacity', 'capacity_units', 'capacity_factor']]

    data.rename(columns={
        'source_name': 'facility_name',
        'iso3_country': 'actor_id',
        'subsector': 'industry',
        'gas': 'gas_name',
        'emissions_quantity': 'emissions_value',
        'activity': 'activity_value',
        'emissions_factor': 'emissionsfactor_value'
    }, inplace=True)

    # Extract the year from the 'start_time' column
    data['start_time'] = pd.to_datetime(data['start_time'])
    data['emissions_year'] = data['start_time'].dt.year

    # Calculate annual emissions and activity values
    group_columns = [col for col in data.columns if col not in ['emissions_value', 'activity_value', 'capacity_factor']]
    data = (
        data.groupby(group_columns)
        .agg({'emissions_value': 'sum', 'activity_value': 'sum', 'capacity_factor': 'mean'})
        .reset_index()
    )

    # Convert tonnes to kilograms
    data['emissions_value'] *= 1000

    # Add emissions units
    data['emissions_units'] = "kg"

    # Add GPC reference number
    data['gpc_refno'] = "IV.1"

    # unit denominator
    data['unit_denominator'] = "t"

    # Replace gas names
    data['gas_name'] = data['gas_name'].replace({'co2': 'CO2'})

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
