"""gcf/gcf-projects (GCF Chile slice): bare S3 read, tag, hand to merge."""
from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from mage_ai.settings.repo import get_repo_path

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader

SOURCE = "gcf/gcf-projects"


@data_loader
def load_data(*args, **kwargs):
    bucket = kwargs.get("source_bucket", "test-global-api")
    version = kwargs.get("source_release_version", "v1")
    key = f"raw_data/gcf/gcf_projects/release/{version}/gcf_projects.csv"
    config_path = path.join(get_repo_path(), "io_config.yaml")
    df = S3.with_config(ConfigFileLoader(config_path, "default")).load(bucket, key, dtype=str)
    df["_source_dataset"] = SOURCE
    return df
