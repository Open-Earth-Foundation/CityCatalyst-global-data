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
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        # Check if 'resultados' exists in the data
        if 'resultados' not in data:
            raise KeyError("'resultados' key not found in the response data")

        df = pd.json_normalize(data)
        expanded_resultados = pd.json_normalize(df['resultados'].explode())
        df_expanded = df.drop(columns=['resultados']).join(expanded_resultados)
        df_series = pd.json_normalize(df_expanded.explode('series')['series'])
        series_year = df_series.columns[4]
        df_series.columns = ['location_id', 'location_level', 'location_level_name', 'location', 'variable_value']
        df_series[['id', 'variable', 'units']] = df_expanded[['id', 'variavel', 'unidade']].iloc[0]
        df_series['series_year'] = series_year
        df_series['indicator_name'] = indicator_name

        return df_series

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")  # Log HTTP errors
    except KeyError as e:
        print(f"Key error: {e}")  # Log if 'resultados' is not found
    except Exception as e:
        print(f"An error occurred: {e}")  # Log other unexpected errors

    return pd.DataFrame()  # Return an empty DataFrame on error

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
        if not df.empty:  # Only append if df is not empty
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