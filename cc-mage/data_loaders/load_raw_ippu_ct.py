from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from os import path
import pandas as pd
from io import BytesIO

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_s3_bucket(*args, **kwargs):
    """
    Load multiple CSV files from an S3 bucket, clean and ensure consistent data types.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = kwargs['bucket_name']
    route = 'raw_data/climateTRACE'
    object_keys = [
        f'{route}/aluminum_emissions_sources.csv',
        f'{route}/cement_emissions_sources.csv',
        f'{route}/chemicals_emissions_sources.csv',
        f'{route}/food-beverage-tobacco_emissions_sources.csv',
        f'{route}/glass_emissions_sources.csv',
        f'{route}/iron-and-steel_emissions_sources.csv',
        f'{route}/lime_emissions_sources.csv',
        f'{route}/other-chemicals_emissions_sources.csv',
        f'{route}/other-manufacturing_emissions_sources.csv',
        f'{route}/other-metals_emissions_sources.csv',
        f'{route}/petrochemical-steam-cracking_emissions_sources.csv',
        f'{route}/pulp-and-paper_emissions_sources.csv',
        f'{route}/textiles-leather-apparel_emissions_sources.csv'
    ]

    s3 = S3.with_config(ConfigFileLoader(config_path, config_profile))
    data_frames = []

    for object_key in object_keys:
        file_obj = s3.client.get_object(Bucket=bucket_name, Key=object_key)['Body'].read()
        data = pd.read_csv(BytesIO(file_obj))
        data_frames.append(data)

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
