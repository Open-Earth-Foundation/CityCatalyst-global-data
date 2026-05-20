from os import path

from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from mage_ai.settings.repo import get_repo_path

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_action_mitigation_feasibility_chain_from_s3(*args, **kwargs):
    config_path = path.join(get_repo_path(), "io_config.yaml")
    bucket_name = kwargs["bucket_name"]
    scoring_chain_key = kwargs["scoring_chain_key"]

    df = S3.with_config(ConfigFileLoader(config_path, "default")).load(
        bucket_name,
        scoring_chain_key,
    )
    print(f"Loaded {len(df)} rows from s3://{bucket_name}/{scoring_chain_key}")
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert len(output) > 0, "No rows loaded from S3"
    required_columns = {
        "action_id",
        "global_mitigation_option",
        "feasibility_dimension",
        "global_indicator",
        "global_verdict_code",
        "country_code",
        "interpretation",
    }
    missing = required_columns.difference(set(output.columns))
    assert not missing, f"Missing required columns: {sorted(missing)}"
