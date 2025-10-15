import pandas as pd
import yaml
import requests
import re
import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = "https://raw.githubusercontent.com/Open-Earth-Foundation/CityCatalyst-global-data/refs/heads/develop/cc-mage/datasets/datasource_seeder.yaml"
    response = requests.get(url)
    data = yaml.safe_load(response.text)
    df = pd.DataFrame(data)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

    patterns = [
        r"^https://ccglobal\.openearth\.dev/api/v1/source/[a-zA-Z0-9_ ]+/city/:locode/:year/:gpcReferenceNumber$",  # Pattern for v1
        r"^https://ccglobal\.openearth\.dev/api/v0/[a-zA-Z0-9_/ ]+/city/:locode/:year/:gpcReferenceNumber$",  # Pattern for v0
        r"^https://ccglobal\.openearth\.dev/api/v1/source/[a-zA-Z0-9_ ]+/country/:country/:year/:gpcReferenceNumber$",  # Pattern for country
        r"^https://ccglobal\.openearth\.dev/api/v0/[a-zA-Z0-9_/ ]+/country/:country/:year/:gpcReferenceNumber$",  # Pattern for country
        r"^https://ccglobal\.openearth\.dev/api/v1/source/[a-zA-Z0-9_ ]+/region/:region/:year/:gpcReferenceNumber$",  # Pattern for region
        r"^https://ccglobal\.openearth\.dev/api/v0/[a-zA-Z0-9_/ ]+/region/:region/:year/:gpcReferenceNumber$",   # Pattern for region
        r"^https://ccglobal\.openearth\.dev/api/v0/ghgi/notation_key/NO/source/[a-zA-Z0-9_ ]+/city/:actor_id/:gpc_reference_number$"  # Pattern for GHGI notation key
    ]

    # Check for valid endpoints against all patterns
    def matches_any_pattern(endpoint):
        return any(re.match(pattern, endpoint) for pattern in patterns)

    invalid_endpoints = output['api_endpoint'][~output['api_endpoint'].apply(matches_any_pattern)]

    assert invalid_endpoints.empty, f'Invalid endpoints found: {invalid_endpoints.count(), invalid_endpoints.tolist()}'