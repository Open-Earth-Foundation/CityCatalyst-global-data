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
    Load data from a S3 bucket.
    Specify your configuration settings in 'io_config.yaml'.
    """

    bucket_name = kwargs['bucket_name']
    object_key_ipcc = 'files/ipcc/EFDB_output.xlsx'

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
        INSTALL spatial;
        LOAD spatial;
        
        SELECT  "EF ID" AS ef_id,
                REPLACE(REGEXP_REPLACE("IPCC 1996 Source/Sink Category", '\n', '|'), CHR(10), '|') AS ipcc_sector_multi,
                REPLACE(REGEXP_REPLACE("Gas", '\n', '|'), CHR(10), '|') AS gas_multi,
                "Fuel 1996" AS fuel_1996,
                "Fuel 2006" AS fuel_2006,
                "Type of parameter" AS type_parameter,
                Description,
                "Technologies / Practices" AS technologies_paractises,
                "Parameters / Conditions" AS parameters_conditions,
                "Region / Regional Conditions" AS region,
                "Abatement / Control Technologies" AS control_paractises,
                "Other properties" AS properties,
                Value AS emissionsfactor_value,
                Unit AS emissionsfactor_units,
                Equation AS ipcc_equation,
                "IPCC Worksheet" AS ipcc_worksheet,
                "Technical Reference" AS technical_reference,
                "Source of data" AS dataset_name,
                "Data provider" AS data_source
        FROM st_read('s3://{bucket_name}/{object_key_ipcc}')
        WHERE "IPCC 2006 Source/Sink Category" LIKE '1.A.3%'
        ;
    """
    
    df = conn.execute(query).fetchdf() 
    conn.close()

    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
