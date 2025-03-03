import duckdb
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
    Load data from manual input json from citycatalyst repo
    """
    con = duckdb.connect(database=':memory:')

    query = """
    SELECT *
    FROM 'https://raw.githubusercontent.com/Open-Earth-Foundation/CityCatalyst/refs/heads/develop/app/src/util/form-schema/manual-input-hierarchy.json'
    """
    df = con.execute(query).fetchdf()

    con.close()

    unpivoted_df = df.melt(var_name='gpc_reference_number', value_name='manual_input_json')

    return unpivoted_df



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
