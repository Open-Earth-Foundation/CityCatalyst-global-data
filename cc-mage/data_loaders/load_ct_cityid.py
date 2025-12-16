from pandas import json_normalize
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
    Template for loading data from API
    """
    country_code3 = kwargs['country_code3']
    url = f'https://api.climatetrace.org/v7/cities?name=&country={country_code3}'
    data = requests.get(url).json()
    df = json_normalize(data)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
