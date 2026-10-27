"""cl-ocha-ab comuna -> city locode lookup (for finance_project.actor_id).
Bare S3 read of the admin-boundaries release, projected to the join columns (geometry is
large and unused here). Not tagged _source_dataset; the merge identifies it by its columns
(comuna_code, locode) and uses it only to resolve actor_id, never as a modelled source.
"""
from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from mage_ai.settings.repo import get_repo_path

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader

LOOKUP_COLS = ["comuna_code", "comuna_name", "region_name", "locode"]


@data_loader
def load_data(*args, **kwargs):
    bucket = kwargs.get("source_bucket", "test-global-api")
    version = kwargs.get("locode_release_version", "2021")
    key = f"raw_data/ocha_rolac/cl_ocha_ab/release/{version}/cl_ocha_ab.parquet"
    config_path = path.join(get_repo_path(), "io_config.yaml")
    return S3.with_config(ConfigFileLoader(config_path, "default")).load(bucket, key, columns=LOOKUP_COLS)
