import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, data_2, *args, **kwargs):
    """
    """
    ## Transformation to CO2e
    gwp = data[['gas_name', 'ar5']]
    emissions = data_2[['datasource_name', 'actor_id', 'gpc_reference_number', 'emissions_value', 'emissions_year', 'gas_name']]
    
    # apply GWP 
    tmp = pd.merge(emissions, gwp, on='gas_name', how='left')
    tmp['emissions_value'] *= tmp['ar5']

    # calculate CO2e emissions
    tmp = tmp.groupby(['datasource_name', 'actor_id', 'gpc_reference_number', 'emissions_year']).agg({
        'emissions_value': 'sum'
    }).reset_index()

    return tmp


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'