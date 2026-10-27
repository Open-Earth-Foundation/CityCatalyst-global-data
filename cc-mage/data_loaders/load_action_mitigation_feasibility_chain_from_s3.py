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
def test_output(output, *args, **kwargs) -> None:
    assert output is not None, "The output is undefined"
    assert len(output) > 0, "No rows loaded from S3"
    required_columns = {
        "action_id",
        "global_mitigation_option",
        "action_mapping_strength",
        "option_family",
        "feasibility_dimension",
        "global_indicator",
        "global_verdict_code",
        "global_verdict_description",
        "city_indicator",
        "country_code",
        "city_indicator_direction",
        "city_family_scope",
        "interpretation",
    }
    missing = required_columns.difference(set(output.columns))
    assert not missing, f"Missing required columns: {sorted(missing)}"

    required_values = {
        "action_id",
        "global_mitigation_option",
        "feasibility_dimension",
        "global_indicator",
        "global_verdict_code",
        "country_code",
        "interpretation",
    }
    null_counts = output[list(required_values)].isna().sum()
    null_columns = null_counts[null_counts > 0].to_dict()
    assert not null_columns, f"Null values in required columns: {null_columns}"

    natural_key = [
        "country_code",
        "action_id",
        "global_mitigation_option",
        "feasibility_dimension",
        "global_indicator",
        "city_indicator",
    ]
    duplicate_count = int(output.duplicated(natural_key, keep=False).sum())
    assert duplicate_count == 0, (
        f"Duplicate scoring-chain natural keys: {duplicate_count} rows"
    )

    active_bridges = output[
        output["city_indicator_direction"].isin(["positive", "negative"])
    ]
    channel_counts = active_bridges.groupby(
        ["action_id", "country_code", "city_indicator"]
    )["global_indicator"].nunique()
    violations = channel_counts[channel_counts > 1]
    assert violations.empty, (
        "A city indicator reaches an action through multiple global indicators: "
        f"{violations.to_dict()}"
    )

    expected_row_count = kwargs.get("expected_row_count")
    if expected_row_count is not None:
        assert len(output) == int(expected_row_count), (
            f"Expected {expected_row_count} rows, got {len(output)}"
        )

    expected_action_count = kwargs.get("expected_action_count")
    if expected_action_count is not None:
        action_count = int(output["action_id"].nunique())
        assert action_count == int(expected_action_count), (
            f"Expected {expected_action_count} actions, got {action_count}"
        )

    expected_active_bridge_count = kwargs.get("expected_active_bridge_count")
    if expected_active_bridge_count is not None:
        assert len(active_bridges) == int(expected_active_bridge_count), (
            f"Expected {expected_active_bridge_count} active bridge rows, "
            f"got {len(active_bridges)}"
        )

    expected_source_release_label = kwargs.get("source_release_label")
    if "release_id" in output.columns and expected_source_release_label:
        source_release_labels = set(output["release_id"].dropna().astype(str).unique())
        assert source_release_labels == {str(expected_source_release_label)}, (
            f"Expected source release {expected_source_release_label}, got "
            f"{sorted(source_release_labels)}"
        )
