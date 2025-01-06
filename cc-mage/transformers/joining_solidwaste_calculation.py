import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, data_2, data_3, data_4, *args, **kwargs):

    # Creating dfs
    data = pd.DataFrame(data)
    data_2 = pd.DataFrame(data_2)
    data_3 = pd.DataFrame(data_3)
    data_4 = pd.DataFrame(data_4)

    # concatenate the dataframes
    df_final = pd.concat([data, data_2, data_3, data_4], ignore_index=True)

    # Rename the total solid waste column to activity value column
    df_final.rename(columns={'total_SW': 'activity_value'}, inplace=True)

    # Assigning year of emissions
    df_final['emissions_year'] = 2022

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
