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
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = kwargs['bucket_name']
    object_key = 'raw_data/euro_stast/Municipal_waste_statistics_20250210.xlsx'

    s3 = S3.with_config(ConfigFileLoader(config_path, config_profile))

    file_obj = s3.client.get_object(
        Bucket=bucket_name,
        Key=object_key
    )['Body'].read()

    # Read both sheets
    dfs = pd.read_excel(
        BytesIO(file_obj),
        sheet_name=['Table 1', 'Table 2'],
        engine='openpyxl'
    )

    # dfs is a dict: {'Table 1': df1, 'Table 2': df2}
    return dfs