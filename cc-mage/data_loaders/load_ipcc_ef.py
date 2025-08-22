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
    object_key = 'files/ipcc/EFDB_2006_IPCC_guidelines.csv'

    df = S3.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )

    target_names = [
    "ef_id",
    "ipcc_1996_sector",
    "ipcc_2006_sector",
    "gas_name",
    "fuel_1996",
    "fuel_2006",
    "type_parameter",
    "description",
    "technology",
    "conditions",
    "region",
    "abatement",
    "properties",
    "ef_value",
    "unit",
    "equation",
    "ipcc_worksheet",
    "technical_reference",
    "data_source",
    "data_provider"
    ]

    df.columns = target_names

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
