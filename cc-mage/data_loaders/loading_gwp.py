import pandas as pd
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader, test

@data_loader
def load_data_from_db(*args, **kwargs):
    """
    Load data from a specific table in a PostgreSQL database.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    # SQL query 
    query = """
    SELECT * FROM modelled.global_warming_potential;
    """

    # Initialize the Postgres connection and run the query
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        df = loader.load(query)

    # Return the resulting dataframe
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert isinstance(output, pd.DataFrame), 'The output is not a DataFrame'