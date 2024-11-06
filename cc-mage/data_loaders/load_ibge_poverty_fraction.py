import numpy as np
from sklearn.preprocessing import MinMaxScaler
import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def process_ibge_data(url, indicator_name):
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
    
    # Handle outliers
    lower_limit = df_series['variable_value'].quantile(0.05)
    upper_limit = df_series['variable_value'].quantile(0.95)

    df_series['variable_value'] = np.where(df_series['variable_value'] >= upper_limit,
                                           upper_limit,
                                           np.where(df_series['variable_value'] <= lower_limit,
                                                    lower_limit,
                                                    df_series['variable_value']))
    
    # Custom min-max scaling to avoid 0 and 1
    min_value = df_series['variable_value'].min()
    max_value = df_series['variable_value'].max()
    scaled_min = 0.01
    scaled_max = 0.99

    df_series['value_scaled'] = df_series['variable_value'].apply(
        lambda x: (
            (x - min_value) / (max_value - min_value) * (scaled_max - scaled_min) + scaled_min
        ) if pd.notnull(x) else None
    )
    df_series['series_year'] = series_year
    df_series['indicator_name'] = indicator_name

    return df_series

@data_loader
def load_data_from_api(data, *args, **kwargs):
    """
    Loading data from API for IBGE and other sources
    """
    all_data = []

    # Process IBGE data
    ibge_data = data[data['datasoure'] == 'IBGE']
    for _, row in ibge_data.iterrows():
        df = process_ibge_data(row['url'], row['indicator_name'])
        df['datasoure'] = 'IBGE'
        all_data.append(df)

    # Combine all dataframes
    final_df = pd.concat(all_data, ignore_index=True)

    return final_df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert isinstance(output, pd.DataFrame), 'The output is not a DataFrame'
    assert len(output) > 0, 'The dataframe is empty'
