from typing import Any
from urllib.parse import parse_qsl, urlparse

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_world_bank_projects(*args, **kwargs) -> pd.DataFrame:
    """
    Fetch World Bank projects using paginated Search API results.

    Expected kwargs:
    - source_url: base endpoint, e.g. https://search.worldbank.org/api/v2/projects
    - query_term: climate / mitigation / custom
    - rows_per_page: page size (default: 50)
    - request_timeout_seconds: per-request timeout (default: 60)
    """
    source_url = kwargs["source_url"]
    query_term = kwargs.get("query_term", "climate")
    rows_per_page = int(kwargs.get("rows_per_page", 50))
    request_timeout_seconds = int(kwargs.get("request_timeout_seconds", 60))

    all_projects = []
    offset = 0
    session = requests.Session()
    session.mount(
        "https://",
        HTTPAdapter(
            max_retries=Retry(
                total=5,
                connect=5,
                read=5,
                backoff_factor=1.2,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"],
                raise_on_status=False,
            )
        ),
    )
    session.mount(
        "http://",
        HTTPAdapter(
            max_retries=Retry(
                total=5,
                connect=5,
                read=5,
                backoff_factor=1.2,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"],
                raise_on_status=False,
            )
        ),
    )
    parsed = urlparse(source_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    base_query_params = dict(parse_qsl(parsed.query, keep_blank_values=True))

    while True:
        request_params = {
            **base_query_params,
            "format": "json",
            "rows": rows_per_page,
            "os": offset,
            "qterm": query_term,
        }
        response = session.get(
            base_url,
            params=request_params,
            timeout=request_timeout_seconds,
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        projects = data.get("projects", {})

        if not projects:
            break

        batch = list(projects.values())
        all_projects.extend(batch)

        if len(batch) < rows_per_page:
            break

        offset += rows_per_page

    df = pd.json_normalize(all_projects, sep="__")
    print(f"Fetched {len(df)} world bank projects for qterm={query_term}")
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
