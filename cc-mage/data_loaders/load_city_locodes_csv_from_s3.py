from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from mage_ai.settings.repo import get_repo_path

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader

STRING_COLUMNS = ("comuna_code", "country_code", "region_code", "region_name", "comuna_name", "locode")


@data_loader
def load_city_locodes_csv_from_s3(*args, **kwargs):
    config_path = path.join(get_repo_path(), "io_config.yaml")
    bucket_name = kwargs.get("bucket_name") or kwargs.get("source_bucket", "test-global-api")
    object_key = kwargs.get(
        "city_locodes_key",
        "raw_data/cl-ssg/cl-ssg-policy-documents/releases/v1/local_codes.csv",
    ).strip("/")

    df = S3.with_config(ConfigFileLoader(config_path, "default")).load(
        bucket_name,
        object_key,
    )
    for col in STRING_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype("string").fillna("")
    print(f"Loaded {len(df)} rows from s3://{bucket_name}/{object_key}")
    return df
