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

    # filtering df to only include default EFs for stationary combustion
    EF_df = data[data['Description'].isin([
        'CO2 Emission Factor for Stationary Combustion (kg/TJ on a net calorific basis)',
        'CH4 Emission Factor for Stationary Combustion (kg/TJ on a net calorific basis)',
        'N2O Emission Factor for Stationary Combustion (kg/TJ on a net calorific basis)'
    ])]

    category_to_gpc_refno = {
        '1.A.1 - Energy Industries\n': 'I.4.1',
        '1.A.2 - Manufacturing Industries and Construction\n': 'I.3.1',
        '1.A.4.a - Commercial/Institutional\n': 'I.2.1',
        '1.A.4.b - Residential\n1.A.4.c.i - Stationary\n': 'I.1.1'
    }

    # replace IPCC 2006 categories with GPC ref no
    EF_df['gpc_reference_number'] = EF_df['ipcc_2006_category'].replace(category_to_gpc_refno)

    # check if each fuel has all required gases
    required_gases = {'CO2', 'CH4', 'N2O'}

    #missing_gases_df = (
    #    EF_df.groupby(['gpc_reference_number', 'fuel'])['gas']
    #    .apply(set) 
    #    .reset_index()
    #)
    #print(missing_gases_df)

    # Adding firewood EFs
    wood_rows = EF_df[EF_df['fuel'] == 'Wood/Wood Waste'].copy()
    wood_rows['fuel'] = 'firewood'
    EF_df = pd.concat([EF_df, wood_rows], ignore_index=True)

    # EFs for subsector 6
    #I'm duplicating the same EFs from I.1.1
    non_specific = EF_df[EF_df['gpc_reference_number'] == 'I.1.1'].copy()
    non_specific['gpc_reference_number'] = 'I.6.1'

    tmp_final = pd.concat([EF_df, non_specific], ignore_index=True)

    return tmp_final


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
