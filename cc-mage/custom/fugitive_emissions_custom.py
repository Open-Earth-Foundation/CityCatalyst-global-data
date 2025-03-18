import pandas as pd
if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):

    dic_methodologies = {
        'custom': {
            'gpc_refno': 'I.7.1',
            'methodology_name': 'custom-methodology',
            'methodology_description': 'No direct relationship to gpc methodologies.',
            'last_no': 1
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
