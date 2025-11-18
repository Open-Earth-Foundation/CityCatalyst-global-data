import io
import pandas as pd
import duckdb
import boto3

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from os import path

from mage_ai.data_preparation.shared.secrets import get_secret_value

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
    object_key_co2 = 'files/climatetrace/version_2025/AR/CO2/buildings/*_emissions_sources_v*.csv'
    object_key_ch4 = 'files/climatetrace/version_2025/AR/CH4/buildings/*_emissions_sources_v*.csv'
    object_key_n2o = 'files/climatetrace/version_2025/AR/N2O/buildings/*_emissions_sources_v*.csv'
    

    aws_access_key_id = get_secret_value('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = get_secret_value('AWS_SECRET_ACCESS_KEY')

    conn = duckdb.connect()

    conn.execute(
        f"""
        CREATE SECRET (
            TYPE 'S3',
            KEY_ID '{aws_access_key_id}',
            SECRET '{aws_secret_access_key}',
            REGION 'us-east-1'
        );
        """
    )

    query = f"""
            SELECT *
            FROM  read_csv('s3://{bucket_name}/{object_key_co2}', union_by_name=true)
            UNION
            SELECT *
            FROM read_csv('s3://{bucket_name}/{object_key_ch4}', union_by_name=true)
            UNION
            SELECT *
            FROM read_csv('s3://{bucket_name}/{object_key_n2o}', union_by_name=true)
    """

    df = conn.execute(query).fetchdf() 
    conn.close()

    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
