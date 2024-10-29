import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Loading data from API for IBGE
    """
    aggregate_id = 4714
    variable_id = 93
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{aggregate_id}/periodos/2015-2023/variaveis/{variable_id}?localidades=N6"
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)
    expanded_resultados = pd.json_normalize(df['resultados'].explode())
    expanded_series = pd.json_normalize(expanded_resultados['series'].explode())
    expanded_series[['id', 'variable', 'units']] = df[['id', 'variavel', 'unidade']].iloc[0]

    return expanded_series


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
