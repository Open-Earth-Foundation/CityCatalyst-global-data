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
            'methodology_name': 'Enteric Fermentation – Cattle Operations Climate Trace',
            'methodology_description': 'This methodology estimates methane (CH₄) emissions from confined cattle (e.g., feedlots and dairies) using a facility-level approach. It is based on IPCC Tier 2 methods, incorporating region-specific emission factors and cattle diet data to improve accuracy over default Tier 1 approaches.',
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