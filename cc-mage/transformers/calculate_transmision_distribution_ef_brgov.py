if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from pandas import DataFrame

@transformer
def transform(data: DataFrame, *args, **kwargs):

    # source: World Bank (WDI)
    grid_loss = 15.77  # % of grid losses

    # Applying % of grid losses
    data['emissionfactor_value'] *= grid_loss

    # Change datasource
    data['datasource_name'] = 'World Bank' ## TBC with Amanda

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
