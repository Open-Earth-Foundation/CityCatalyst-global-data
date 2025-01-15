import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from pandas import DataFrame


@transformer
def transform(data: DataFrame, data_2: DataFrame, *args, **kwargs):

    # final df
    df_final = pd.concat([data, data_2], ignore_index=True)

    # calculate the fraction of each scope
    df_final['fraction_scope1'] = (df_final['collected']-df_final['exported']-df_final['imported'])/df_final['collected']
    df_final['fraction_scope3'] = df_final['exported']/df_final['collected']

    # calculate the emissions for each scope
    df_final['III.4.1'] = df_final['emissions_value_tmp']*df_final['fraction_scope1']
    df_final['III.4.2'] = df_final['emissions_value_tmp']*df_final['fraction_scope3']


    # reformating the DataFrame
    df_final = df_final.melt(
        id_vars=['municipality_name', 'total_resident_population', 'emissionfactor_value', 'gas_name', 'emissionfactor_units', 
                'activity_subcategory_type', 'unit_denominator'], 
        value_vars=['III.4.1', 'III.4.2'], 
        var_name='GPC_refno', 
        value_name='emissions_value')

    # Assign gpcmethod_id
    df_final.loc[df_final['GPC_refno'] == 'III.4.1', 'gpcmethod_id'] = 'd08015c1-e605-233c-3244-38eabeb14e49'
    df_final.loc[df_final['GPC_refno'] == 'III.4.2', 'gpcmethod_id'] = '73872423-5961-c665-90b0-efcae15606a5'

    # emissions units
    df_final['emissions_units'] = 'kg'

    # drop the rows with zero emissions
    df_final = df_final[df_final['emissions_value'] != 0]

    # drop the rows with NaN values
    df_final.dropna(subset=['emissions_value'], inplace=True)

    # rename the population column by income group as the activity value
    df_final.rename(columns={'total_resident_population': 'activity_value', 'municipality_name': 'actor_name'}, inplace=True)

    # assign the activity units
    df_final['activity_units'] = 'person'
    df_final['activity_name'] = 'source-type-domestic-wastewater'
    df_final['emissions_year'] = 2022

    return df_final


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'