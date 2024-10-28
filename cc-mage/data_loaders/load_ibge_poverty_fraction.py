from sklearn.preprocessing import MinMaxScaler
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
    agg_id = '3563' #  5938, 3563, 4714, 5457
    variable_id = '2010' #  516, 2010, 614, 216
    url = f"https://servicodados.ibge.gov.br/api/v3/agregados/{agg_id}/periodos/-1/variaveis/{variable_id}?localidades=N6"
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data)
    expanded_resultados = pd.json_normalize(df['resultados'].explode())
    df_expanded = df.drop(columns=['resultados']).join(expanded_resultados)
    df_series = pd.json_normalize(df_expanded.explode('series')['series'])
    series_year = df_series.columns[4]
    df_series.columns = ['location_id', 'location_level', 'location_level_name', 'location', 'variable_value']
    df_series[['id', 'variable', 'units']] = df_expanded[['id', 'variavel', 'unidade']].iloc[0]
    df_series['variable_value'] = pd.to_numeric(df_series['variable_value'], errors='coerce')
    scaler = MinMaxScaler()
    df_series['value_scaled'] = scaler.fit_transform(df_series[['variable_value']])
    df_series['series_year'] =  series_year

    return df_series


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
