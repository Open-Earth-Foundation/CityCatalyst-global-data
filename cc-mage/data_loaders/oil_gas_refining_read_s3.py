from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from os import path
import pandas as pd
from io import BytesIO


@data_loader
def load_from_s3_bucket(*args, **kwargs):
    """
    Template for loading data from a S3 bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#s3
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    
    bucket_name = kwargs['bucket_name']
    route = 'raw_data/climateTRACE'

    object_keys = [
        f'{route}/oil-and-gas-production_emissions_sources_ch4.csv',
        f'{route}/oil-and-gas-production_emissions_sources_co2.csv',
        f'{route}/oil-and-gas-refining_emissions_sources_ch4.csv',
        f'{route}/oil-and-gas-refining_emissions_sources_co2.csv',
        f'{route}/oil-and-gas-transport_emissions_sources_ch4.csv',
        f'{route}/oil-and-gas-transport_emissions_sources_co2.csv'
    ]

    s3 = S3.with_config(ConfigFileLoader(config_path, config_profile))
    data_frames = []

    for object_key in object_keys:
        try:
            file_obj = s3.client.get_object(Bucket=bucket_name, Key=object_key)['Body'].read()
            data = pd.read_csv(BytesIO(file_obj))
            data_frames.append(data)
        except Exception as e:
            print(f'Error loading {object_key}: {str(e)}')
            continue

    # Concatenate all DataFrames into one
    combined_data = pd.concat(data_frames, ignore_index=True)

    # Ensure all columns have consistent types
    for col in combined_data.columns:
        if combined_data[col].dtype == 'object':
         # Convert object columns to string to handle mixed types
         combined_data[col] = combined_data[col].astype(str)

    return combined_data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
