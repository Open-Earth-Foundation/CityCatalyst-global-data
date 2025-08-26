import io
import pandas as pd
import duckdb
import boto3

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from os import path

from mage_ai.data_preparation.shared.secrets import get_secret_value


@data_loader
def load_from_s3_bucket(*args, **kwargs):
    bucket_name = kwargs['bucket_name']
    object_key = 'files/climatetrace/version_2025/climatetrace_transport_onroad_source_emissions.parquet'

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
        FROM read_parquet('s3://{bucket_name}/{object_key}', hive_partitioning=true)
        WHERE iso3_country = 'CAN'
        ;
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
