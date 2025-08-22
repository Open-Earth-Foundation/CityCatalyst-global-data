if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
from pandas import DataFrame

@transformer
def transform(data: DataFrame, *args, **kwargs):

    # Filtering the df 
    data = data[['source_name', 'subsector', 'start_time', 'lat', 'lon', 'gas', 'emissions_quantity', 'temporal_granularity', 'activity', 'activity_units', 'emissions_factor', 'emissions_factor_units', 
                            'capacity', 'capacity_units', 'capacity_factor']]

    data = data.rename(columns={
        'gas': 'gas_name',
        'emissions_quantity': 'emissions_value',
        'activity': 'activity_value',
        'emissions_factor': 'emissionfactor_value',
        'emissions_factor_units': 'units'
    })

    # Standardize gas name and convert time
    data['gas_name'] = data['gas_name'].str.upper()
    data['start_time'] = pd.to_datetime(data['start_time'])
    data['emissions_year'] = data['start_time'].dt.year

    # Choose grouping columns explicitly
    group_columns = [
        'source_name', 'lat', 'lon', 'gas_name', 'activity_units', 'capacity_units', 'emissions_year', 'units'
    ]

    data = (
        data.groupby(group_columns, dropna=False)
        .agg({
            'emissions_value': 'sum',
            'activity_value': 'sum',
            'capacity': 'mean',
            'capacity_factor': 'mean',
            'emissionfactor_value': 'mean',
        })
        .reset_index()
    )

    # Convert tonnes to kilograms
    data['emissions_value'] *= 1000

    # Add emissions units
    data['emissions_units'] = "kg"

    # Change EF units
    data['emissionfactor_value'] *= 1000
    data['units'] = 'kg/animal head(s)'

    # Add GPC reference number
    data['gpc_refno'] = "V.1"

    # Add activity details
    data['activity_name'] = "total-livestock"
    data['livestock-species'] = "species-cattle"
    data['livestock-activity-type'] = "type-manure-management"
    data['livestock-subactivity-type'] = "type-manure-management-operation"
    data['methodology_name'] = 'type-manure-management-operation-cattle-CT'
    data['methodology_description'] = 'This methodology estimates methane (CH₄) and nitrous oxide (N₂O) emissions from manure storage and treatment systems at confined cattle facilities. It follows IPCC Tier 2 methods, using country-specific manure management system distributions, climate data, and facility-level cattle counts to refine emissions estimates.'
    data['publisher_name'] = 'ClimateTRACE'
    data['publisher_url'] = 'https://climatetrace.org/'
    data['datasource_name'] = 'ClimateTRACEv2024'
    data['dataset_name'] = 'Manure Management Cattle Operation v4.3.1'
    data['dataset_url'] = 'https://downloads.climatetrace.org/v4.3.1/sector_packages/ch4/agriculture.zip'

    # Replace gas names
    data['gas_name'] = data['gas_name'].replace({'n2o': 'N2O','ch4': 'CH4'})

    # Only complete years
    data = data[data['emissions_year'] < 2025]

    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'