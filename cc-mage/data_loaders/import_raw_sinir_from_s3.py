import pandas as pd
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from io import BytesIO
from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_s3_bucket(*args, **kwargs):
    """
    Load an Excel file from S3 and process it into a DataFrame.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'test-global-api'
    object_key = 'raw_data/SINIR_Brasil/Planilha_Unidades_Fluxos_RS_2022.xlsx'

    s3_client = S3.with_config(ConfigFileLoader(config_path, config_profile))

    # Retrieve the file as a binary object
    response = s3_client.client.get_object(Bucket=bucket_name, Key=object_key)
    file_content = response['Body'].read()

    # Use pandas to read the Excel file
    df = pd.read_excel(BytesIO(file_content))

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert isinstance(output, pd.DataFrame), 'The output is not a DataFrame'
    print("Data loaded successfully.")

