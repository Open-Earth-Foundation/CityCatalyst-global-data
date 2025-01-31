if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd

@transformer
def transform(data, *args, **kwargs):

    MSW_I = {
        'gpc_refno': 'I.1.3',
        'methodology_name': 'Transmission and distribution losses',
        'methodology_description': 'This methodology quantifies greenhouse gas emissions associated with electricity lost during the transmission and distribution (T&D) of grid-supplied energy.',
        'Scope': 3
    }

    MSW_I = pd.DataFrame([MSW_I])

    return MSW_I


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
