if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd

@custom
def transform_custom(*args, **kwargs):

    dic_methodologies = {
        'residential': {
            'gpc_refno': 'I.1.3',
            'methodology_name': 'Transmission and distribution losses',
            'methodology_description': 'This methodology quantifies greenhouse gas emissions associated with electricity lost during the transmission and distribution (T&D) of grid-supplied energy.',
            'last_no': 3
        },
        'commercial': {
            'gpc_refno': 'I.2.3',
            'methodology_name': 'Transmission and distribution losses',
            'methodology_description': 'This methodology quantifies greenhouse gas emissions associated with electricity lost during the transmission and distribution (T&D) of grid-supplied energy.',
            'last_no': 3
        },
        'industrial': {
            'gpc_refno': 'I.3.3',
            'methodology_name': 'Transmission and distribution losses',
            'methodology_description': 'This methodology quantifies greenhouse gas emissions associated with electricity lost during the transmission and distribution (T&D) of grid-supplied energy.',
            'last_no': 3
        },
        'agriculture': {
            'gpc_refno': 'I.5.3',
            'methodology_name': 'Transmission and distribution losses',
            'methodology_description': 'This methodology quantifies greenhouse gas emissions associated with electricity lost during the transmission and distribution (T&D) of grid-supplied energy.',
            'last_no': 3
        }
    }

    # Convert dictionary to DataFrame
    data = pd.DataFrame.from_dict(dic_methodologies, orient='index').reset_index()
    data.rename(columns={'index': 'methodology_key'}, inplace=True)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
