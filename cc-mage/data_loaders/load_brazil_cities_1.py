import io
import pandas as pd
import duckdb
import boto3
from sqlalchemy import create_engine

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
    Load data from a S3 bucket.
    Specify your configuration settings in 'io_config.yaml'.
    """

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'test-global-api'
    object_key = 'files/local/brazil/br_city_boundary.parquet'

    df = S3.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    ) 

    return df

    # bucket_name = kwargs['bucket_name']
    # object_key = kwargs['object_key']

    # aws_access_key_id = get_secret_value('AWS_ACCESS_KEY_ID')
    # aws_secret_access_key = get_secret_value('AWS_SECRET_ACCESS_KEY')

    # conn = duckdb.connect()

    # conn.execute(
    #     f"""
    #     CREATE SECRET (
    #         TYPE 'S3',
    #         KEY_ID '{aws_access_key_id}',
    #         SECRET '{aws_secret_access_key}',
    #         REGION 'us-east-1'
    #     );
    #     """
    # )

    # query = f"""
    #     SELECT  primary_name,
    #             REPLACE(region, 'BR-', '') as region,
    #             osm_id,
    #             geometry,
    #             rnk 
    #     FROM 's3://{bucket_name}/{object_key}'
    #     WHERE  rnk =1
    #     ;
    # """

    # df = conn.execute(query).fetchdf() 
    # conn.close()

    # return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
