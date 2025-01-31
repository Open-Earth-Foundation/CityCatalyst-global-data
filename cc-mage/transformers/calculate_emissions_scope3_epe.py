if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from pandas import DataFrame
import pandas as pd

@transformer
def transform(data: DataFrame, data_2: DataFrame, *args, **kwargs):

    data = data[['emissionfactor_id', 'emissionfactor_value', 'unit_denominator', 'datasource_name', 'active_from', 'active_to']]

    tmp = pd.merge(data_2, data, on='emissionfactor_id')

    # % of grid losses
    grid_loss = 15.77  

    #calculate EF for grid-losses
    tmp['emissionfactor_value'] *= grid_loss

    tmp['activity_value'] = pd.to_numeric(tmp['activity_value'], errors='coerce')

    # calculate emissions for grid-losses
    tmp['emissions_value'] = tmp['activity_value'] * tmp['emissionfactor_value']

    gpc_refno = {
        'I.1.2': 'I.1.3',
        'I.2.2': 'I.2.3',
        'I.3.2': 'I.3.3',
        'I.5.2': 'I.5.3'
    }
    tmp['gpc_reference_number'] = tmp['gpc_reference_number'].replace(gpc_refno)    

    return tmp


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
