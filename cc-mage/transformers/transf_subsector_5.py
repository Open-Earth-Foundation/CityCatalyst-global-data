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
    # Filter only relevant rows for the Off-road Vehicles category
    EF_tmp = data[data['ipcc_2006_category'] == '1.A.4.c.ii - Off-road Vehicles and Other Machinery\n'].copy()

    # Group by gas & fuel and calculate average value
    # multiple values with the same descriptions
    grouped = EF_tmp.groupby(['gas', 'fuel'], as_index=False).agg({'value': 'mean'})

    # Keep one representative row per (gas, fuel) for metadata
    metadata = EF_tmp.drop(columns=['value', 'value_min', 'value_max']).drop_duplicates(subset=['gas', 'fuel'])

    # Merge metadata and averaged value
    EF_tmp = metadata.merge(grouped, on=['gas', 'fuel'])

    # Add missing CO2 rows by copying and modifying existing ones
    # CO2 values doesn't change between subsectors
    co2_rows = data[
        (data['fuel'].isin(['Motor Gasoline', 'Diesel Oil'])) &
        (data['gas'] == 'CO2') &
        (data['Description'] == 'CO2 Emission Factor for Stationary Combustion (kg/TJ on a net calorific basis)')
    ].copy()

    co2_rows = co2_rows.drop_duplicates(subset=['gas', 'fuel'])

    # Modify fields to match Off-road category
    co2_rows['ipcc_2006_category'] = '1.A.4.c.ii - Off-road Vehicles and Other Machinery\n'
    co2_rows['Description'] = 'Default Emission Factors for Off-road Mobile Source and Machinery'

    # Concatenate the CO2 rows with the rest
    EF_tmp = pd.concat([EF_tmp, co2_rows], ignore_index=True)

    # Assign gpcrefno
    EF_tmp['gpc_reference_number'] = 'I.5.1'

    return EF_tmp


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
