import pandas as pd
import yaml
import requests
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
    url = "https://raw.githubusercontent.com/Open-Earth-Foundation/CityCatalyst-global-data/refs/heads/develop/cc-mage/datasets/datasource_seeder.yaml"
    response = requests.get(url)
    data = yaml.safe_load(response.text)
    df = pd.DataFrame(data)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
