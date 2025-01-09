import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from pandas import DataFrame


@transformer
def transform(data: DataFrame, data_2: DataFrame, data_3: DataFrame, data_4: DataFrame, *args, **kwargs):

    # concatenate the dataframes
    df_final = pd.concat([data, data_2, data_3, data_4], ignore_index=True)

    # Rename the total solid waste column to activity value column
    df_final.rename(columns={'total_SW': 'activity_value', 'year': 'emissions_year'}, inplace=True)

    # Assing activity units
    df_final['activity_units'] = 't'
    df_final['actor_id'] = 'BR' #Note: actor_id here is the country id

    # Assign gpcmethod_id
    df_final.loc[df_final['GPC_refno'] == 'III.1.1', 'gpcmethod_id'] = '4e405d8c-ba58-5f50-9c0e-eeea1a682fd4'
    df_final.loc[df_final['GPC_refno'] == 'III.1.2', 'gpcmethod_id'] = 'a4326d58-731c-4c9f-197e-9384a377a47c' 
    df_final.loc[df_final['GPC_refno'] == 'III.2.1', 'gpcmethod_id'] = '3a52d2cd-bfea-25fe-401d-4942a56871ba'
    df_final.loc[df_final['GPC_refno'] == 'III.2.2', 'gpcmethod_id'] = '46112a2f-a217-be7e-fddf-fda048f2e951' 
    df_final.loc[df_final['GPC_refno'] == 'III.3.1', 'gpcmethod_id'] = '8888f986-4290-65bd-fb7d-2094c95bf9ce'
    df_final.loc[df_final['GPC_refno'] == 'III.3.2', 'gpcmethod_id'] = '00479722-d344-1d0b-243c-80760394d379'   

    # drop the rows with zero emissions
    df_final = df_final[df_final['emissions_value'] != 0]

    # drop the rows with NaN values
    df_final.dropna(subset=['emissions_value'], inplace=True)

    return df_final


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
