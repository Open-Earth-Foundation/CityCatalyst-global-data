"""cl-ssg/cl-ssg-projects per-project action matches (codigo_bip -> action_id, label).
Bare S3 read; the merge picks each project's best strong/goal_aligned match. Not tagged with
_source_dataset (the merge identifies this frame by its columns: codigo_bip, action_id, label).
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
    key = f"raw_data/cl_ssg/cl_ssg_projects/release/{version}/cl_ssg_projects_action_matches.csv"
    config_path = path.join(get_repo_path(), "io_config.yaml")
    return S3.with_config(ConfigFileLoader(config_path, "default")).load(bucket, key, dtype=str)
