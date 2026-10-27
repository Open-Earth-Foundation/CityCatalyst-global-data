import hashlib
import json
import time
from os import path
from typing import Any

import pandas as pd
import requests
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from mage_ai.settings.repo import get_repo_path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def _requests_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=1.2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def _fetch_world_bank_project_ids(country_code: str | None = None) -> list[dict[str, str | None]]:
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    country_filter = ""
    if country_code:
        safe_country_code = country_code.replace("'", "").strip().upper()
        country_filter = f"AND UPPER(country_code) = '{safe_country_code}'"
    query = f"""
    SELECT source_project_id::TEXT, country_code::TEXT
    FROM modelled.project_portfolio
    WHERE source_name = 'world_bank'
      AND source_project_id IS NOT NULL
      {country_filter}
    """
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        result = loader.load(query)
    rows = (
        result[["source_project_id", "country_code"]]
        .dropna(subset=["source_project_id"])
        .drop_duplicates(subset=["source_project_id"])
        .to_dict("records")
    )
    return rows


def _document_id(doc_id: str, doc: dict[str, Any]) -> str:
    for key in ("guid", "id", "docid"):
        value = doc.get(key)
        if value:
            return str(value)
    if doc_id and doc_id != "facets":
        return str(doc_id)
    digest_input = json.dumps(doc, sort_keys=True).encode("utf-8")
    return hashlib.md5(digest_input).hexdigest()


@data_loader
def load_world_bank_project_documents(*args, **kwargs) -> pd.DataFrame:
    """
    Fetch World Bank document metadata for project IDs in modelled.project_portfolio.

    Expected kwargs:
    - rows_per_page: page size for WDS endpoint (default: 200)
    - request_timeout_seconds: per-request timeout (default: 60)
    - sleep_seconds: delay between requests (default: 0.2)
    - source_name: source filter from project_portfolio (default: world_bank)
    - country_code: optional country code filter (e.g. BR, CL)
    """
    rows_per_page = int(kwargs.get("rows_per_page", 200))
    request_timeout_seconds = int(kwargs.get("request_timeout_seconds", 60))
    sleep_seconds = float(kwargs.get("sleep_seconds", 0.2))
    source_name = kwargs.get("source_name", "world_bank")
    country_code = kwargs.get("country_code")
    object_key_prefix = kwargs.get(
        "object_key_prefix",
        "files/world_bank/world_bank_projects/documents",
    ).strip("/")

    if source_name != "world_bank":
        raise ValueError("This loader currently supports source_name='world_bank' only.")

    project_rows = _fetch_world_bank_project_ids(country_code=country_code)
    session = _requests_session()
    base_url = "https://search.worldbank.org/api/v3/wds"
    results: list[dict[str, Any]] = []

    for project_row in project_rows:
        project_id = str(project_row["source_project_id"])
        project_country_code = project_row.get("country_code")
        params = {
            "format": "json",
            "rows": rows_per_page,
            "os": 0,
            "fl": "docdt,docty,lang,display_title,pdfurl,url,guid",
            "qterm": project_id,
        }

        try:
            response = session.get(
                base_url,
                params=params,
                timeout=request_timeout_seconds,
            )
            response.raise_for_status()
            payload: dict[str, Any] = response.json()
            documents = payload.get("documents", {})
        except Exception as exc:
            print(f"Failed to fetch documents for {project_id}: {exc}")
            time.sleep(sleep_seconds)
            continue

        for doc_id, doc in documents.items():
            if doc_id == "facets" or not isinstance(doc, dict):
                continue

            pdf_url = doc.get("pdfurl")
            if not pdf_url:
                continue

            document_id = _document_id(str(doc_id), doc)
            object_key = f"{object_key_prefix}/{project_id}/{document_id}.pdf"
            results.append(
                {
                    "source_name": source_name,
                    "project_id": project_id,
                    "country_code": project_country_code,
                    "document_id": document_id,
                    "document_type": doc.get("docty"),
                    "document_title": doc.get("display_title"),
                    "document_date": doc.get("docdt"),
                    "language_code": doc.get("lang"),
                    "pdf_url": pdf_url,
                    "source_document_url": doc.get("url"),
                    "s3_bucket": "test-global-api",
                    "s3_object_key": object_key,
                    "s3_uri": f"s3://test-global-api/{object_key}",
                    "document_payload": json.dumps(doc, ensure_ascii=True),
                }
            )

        time.sleep(sleep_seconds)

    df = pd.DataFrame(results)
    print(
        f"Fetched {len(df)} world bank documents across "
        f"{df['project_id'].nunique() if not df.empty else 0} projects."
    )
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
