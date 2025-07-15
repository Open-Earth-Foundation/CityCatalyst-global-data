from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
import pandas as pd
from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


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
    object_keys = [
        'raw_data/emission_factors/conversion_factors_volumen_to_energy.csv',
        'raw_data/emission_factors/conversion_factors_weight_to_energy.csv'
    ]
    
    # Initialize a list to hold dataframes
    dataframes = []
    
    # Load each file into a dataframe and append to the list
    for object_key in object_keys:
        # Assuming csv_data is a stream or file-like object, read it with pandas
        df = S3.with_config(ConfigFileLoader(config_path, config_profile)).load(
                            bucket_name,
                            object_key,
                        )
        df.columns = df.columns.str.strip()
        
        # Select the desired columns
        df_selected = df[['From', 'To', 'Factor', 'fuel_type']] #, 'to', 'factor', 'fuel_type']]
        
        # Append the dataframe to the list
        dataframes.append(df_selected)
    
    # Concatenate all dataframes into a single dataframe
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    return combined_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
