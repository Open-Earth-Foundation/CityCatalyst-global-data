"""INDAP fund->action mapping: read the raw CSV from S3 exactly as it is.

No transformation here — shaping (deriving source_opportunity_id, filtering) happens in the
next block, transformers/transform_finance_opportunity_action.py.
"""
from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from mage_ai.settings.repo import get_repo_path

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data(*args, **kwargs):
    bucket = kwargs.get("source_bucket", "test-global-api")
    version = kwargs.get("source_release_version", "v1")
    key = f"raw_data/cl_indap/cl_indap_fondos/release/{version}/cl_indap_fondos_to_actions.csv"
    config_path = path.join(get_repo_path(), "io_config.yaml")
    return S3.with_config(ConfigFileLoader(config_path, "default")).load(bucket, key)
