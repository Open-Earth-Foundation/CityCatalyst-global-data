if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from pandas import DataFrame
import pandas as pd


@transformer
def transform(data: DataFrame, *args, **kwargs):

    # Filtering the df 
    required_columns = ['source_name', 'iso3_country', 'subsector', 'start_time', 'lat', 'lon', 
                    'gas', 'emissions_quantity', 'temporal_granularity', 'activity', 
                    'activity_units', 'emissions_factor', 'emissions_factor_units', 
                    'capacity', 'capacity_units', 'capacity_factor']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f'Missing required columns: {missing_columns}')
    data = data[required_columns]

    data.rename(columns={
        'source_name': 'facility_name',
        'iso3_country': 'actor_id',
        'gas': 'gas_name',
        'emissions_quantity': 'emissions_value',
        'activity': 'activity_value',
        'emissions_factor': 'emissionsfactor_value'
    }, inplace=True)

    # Extract the year from the 'start_time' column
    try:
        data['start_time'] = pd.to_datetime(data['start_time'])
    except pd.errors.ParserError as e:
        problematic_rows = data[pd.to_datetime(data['start_time'], errors='coerce').isna()]
        raise ValueError(f'Invalid datetime format in rows: {problematic_rows.index.tolist()}') from e

    data['emissions_year'] = data['start_time'].dt.year

    # Calculate annual emissions and activity values
    group_columns = [col for col in data.columns if col not in ['emissions_value', 'activity_value', 'capacity_factor', 'start_time']]
    data = (
        data.groupby(group_columns, dropna=False)
        .agg({'emissions_value': 'sum', 'activity_value': 'sum', 'capacity_factor': 'mean'})
        .reset_index()
    )

    # Convert tonnes to kilograms
    data['emissions_value'] *= 1000

    # Add emissions units
    data['emissions_units'] = "kg"

    # Add GPC reference number
    data['gpc_refno'] = "I.8.1"

    # Replace gas names
    data['gas_name'] = data['gas_name'].replace({'ch4': 'CH4', 'co2': 'CO2'})

    data['unit_denominator'] = data['activity_units'] ## BBL: barrel

    type_dic = {
        'oil-and-gas-refining': {
            'activity_name': 'type-extraction',
            'activity_subcategory_type1': 'fugitive-emissions-oil-gas-type',
            'activity_subcategory_name1': 'fugitive-emissions-oil-gas-type-all'
        }, 
        'oil-and-gas-production': {
            'activity_name': 'type-processing',
            'activity_subcategory_type1': 'fugitive-emissions-oil-gas-type',
            'activity_subcategory_name1': 'fugitive-emissions-oil-gas-type-all'
        }, 
        'oil-and-gas-transport': {
            'activity_name': 'type-distribution',
            'activity_subcategory_type1': 'fugitive-emissions-oil-gas-type',
            'activity_subcategory_name1': 'fugitive-emissions-oil-gas-type-all'
        }
    }

    # Transformations using vectorized operations this was changed to improve the performance
    for subsector, attributes in type_dic.items():
        mask = data['subsector'] == subsector
        for column_name, value in attributes.items():
            data.loc[mask, column_name] = value

    # create the activity_subcategory_type column to store the subcategory information
    data['activity_subcategory_type'] = pd.DataFrame({
        'type': data['activity_subcategory_type1'],
        'name': data['activity_subcategory_name1'],
        'source': data['facility_name']
    }).apply(lambda x: {'fugitive-emissions-oil-gas-type': x['name'], 'data-source': x['source']}, axis=1)

    data.drop(columns=['activity_subcategory_type1', 'activity_subcategory_name1'], inplace=True)

    # create the metadata column to store emission factor information
    data["metadata"] = data.apply(
        lambda row: {
            "capacity": row['capacity'],
            "capacity_units": row['capacity_units'],
            "capacity_factor": row['capacity_factor']
        },
        axis=1,
    )

    data.drop(columns=['capacity', 'capacity_units', 'capacity_factor', 'emissions_factor_units', 'subsector', 'temporal_granularity', 'facility_name'], inplace=True)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
