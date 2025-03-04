import pandas as pd 
import duckdb
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
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
    object_key = 'files/c40/C40_GPC_Database.csv'

    df = S3.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )

    con = duckdb.connect(database=':memory:')
    con.register('c40_rawdata', df)

    query = """
    WITH data_raw AS (
    SELECT City,Country,Region,Boundary,Year_calendar, Population,Area,GDP, "I.1.1"::varchar as "I.1.1","I.1.2"::varchar as "I.1.2","I.1.3","I.2.1","I.2.2"::varchar as "I.2.2","I.2.3","I.3.1","I.3.2","I.3.3","I.4.1","I.4.2","I.4.3","I.4.4","I.5.1","I.5.2","I.5.3","I.6.1","I.6.2","I.6.3","I.7.1","I.8.1","II.1.1"::varchar as "II.1.1","II.1.2","II.1.3","II.2.1","II.2.2","II.2.3","II.3.1","II.3.2","II.3.3","II.4.1","II.4.2","II.4.3","II.5.1","II.5.2","II.5.3","III.1.1","III.1.2","III.1.3","III.2.1","III.2.2","III.2.3","III.3.1","III.3.2","III.3.3","III.4.1","III.4.2","III.4.3","IV.1","IV.2","V.1","V.2","V.3","VI.1"
    FROM c40_rawdata
    ),
    flattened_data AS (
    SELECT
        city,
        country,
        region,
        boundary,
        year_calendar as emissions_year,
        population,
        area,
        GDP,
        gpc_reference_number,
        emissions as emissions_value,
        'tonnes' as emissions_units,
        'co2eq' as gas_name
    FROM
        data_raw
    UNPIVOT (
        emissions FOR gpc_reference_number IN (
            "I.1.1", "I.1.2", "I.1.3", "I.2.1", "I.2.2", "I.2.3", "I.3.1", "I.3.2", "I.3.3", "I.4.1", "I.4.2", "I.4.3", "I.4.4", "I.5.1", "I.5.2", "I.5.3", "I.6.1", "I.6.2", "I.6.3", "I.7.1", "I.8.1",
            "II.1.1", "II.1.2", "II.1.3", "II.2.1", "II.2.2", "II.2.3", "II.3.1", "II.3.2", "II.3.3", "II.4.1", "II.4.2", "II.4.3", "II.5.1", "II.5.2", "II.5.3",
            "III.1.1", "III.1.2", "III.1.3", "III.2.1", "III.2.2", "III.2.3", "III.3.1", "III.3.2", "III.3.3", "III.4.1", "III.4.2", "III.4.3",
            "IV.1", "IV.2",
            "V.1", "V.2", "V.3",
            "VI.1"
        )
    )
    )
    SELECT 	city,country,region,boundary,emissions_year,--population,area,GDP,
            gpc_reference_number,
            emissions_value::numeric*1000 as emissions_value,
            'kg'emissions_units,
            gas_name
    FROM flattened_data
    WHERE boundary NOT IN ('Province / District / State', 'County', 'Whole area of the TMG jurisdiction including island area', 'Multnomah County', 'Comprehensive Land Use Plan (CLUP)')
    AND trim(emissions_value) NOT IN ('NO', 'NE', 'IE (II.1.1)', 'IE (I.1.1)', 'IE', 'C')
    """

    data_final = con.execute(query).fetchdf()

    return data_final


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
