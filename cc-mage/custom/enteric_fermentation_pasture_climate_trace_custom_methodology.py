import pandas as pd
if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):

    dic_methodologies = {
        'custom': {
            'gpc_refno': 'V.1',
            'methodology_name': 'Enteric Fermentation – Cattle Pasture Climate Trace',
            'methodology_description': 'This methodology estimates methane (CH₄) emissions from grazing cattle using gridded livestock density data and regional emission factors. It follows a combination of IPCC Tier 1 and Tier 2 approaches, adjusting default emission factors to reflect regional differences in cattle type and management.',
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

