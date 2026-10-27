"""Template loader — copy to cc-mage/data_loaders/load_<SOURCE>_staging.py.

Reads the cleaned release file from the S3 raw_data stage and returns a frame ready
for raw_data.<SOURCE>_staging. Keep this block small: read, light-shape, return.

Reads ONLY S3 (and Mage's own io_config via get_repo_path). No local-repo file reads —
Mage runs blocks via exec() so __file__ is undefined. Any field-rename map is either a
small inline dict (below) or, if large/changing, an S3 file loaded the same way as the data.
"""
from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from mage_ai.settings.repo import get_repo_path

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

# small, stable rename map — inline. (If this grows large, upload it to S3 and load it
# like the data, e.g. S3(...).load(bucket, "raw_data/<...>/field_map.csv").)
FIELD_MAP = {
    "<source_col>": "<modelled_col>",
}


@data_loader
def load_data(*args, **kwargs):
    source_path = kwargs["source_path"]                 # S3 key, from metadata variables
    bucket = kwargs.get("source_bucket", "test-global-api")
    config_path = path.join(get_repo_path(), "io_config.yaml")

    df = S3.with_config(ConfigFileLoader(config_path, "default")).load(bucket, source_path)
    df = df.rename(columns=FIELD_MAP)

    print(f"loaded {len(df)} rows from {source_path}")
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None and len(output) > 0, "no rows loaded"
    assert "<natural_key>" in output.columns, "natural key column missing after rename"
