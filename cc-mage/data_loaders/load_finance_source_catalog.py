"""Read the catalog (dataset-review/catalog/index.yaml) for the finance source datasets.

The catalog is the source of truth for each source's identity, so we reference it
directly (fetched from GitHub raw) instead of carrying ~50 per-dataset pipeline
variables. Emits one row per source with the publisher/dataset/release fields +
deterministic ids, ready to register publisher_datasource + dataset_release and to
stamp the right release_id on each finance_opportunity row.
"""
import hashlib
import uuid

import pandas as pd
import requests
import yaml

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

CATALOG_INDEX_URL = (
    "https://raw.githubusercontent.com/Open-Earth-Foundation/"
    "CityCatalyst-global-data/develop/dataset-review/catalog/index.yaml"
)

# the finance pipeline's source datasets, by catalog id
SOURCE_IDS = [
    "cl-mma-fondos", "cl-minenergia-fondos", "cl-corfo-finance", "cl-subdere-fondos",
    "cl-minvu-fondos", "cl-gore-fndr", "cl-mtt-fondos", "cl-conaf-fondos",
    "cl-indap-fondos", "cl-mop-fondos",
]

# Sources whose publisher IS the funder, so funder_name may be backfilled from publisher.name
# when the extract omits it (e.g. cl-mma's FPA/FPR are MMA's own funds). Explicit, never blanket —
# add an id here only when the publishing body is also the body whose budget pays.
PUBLISHER_IS_FUNDER = {"cl-mma-fondos"}

# funder level per source (default national); GORE is regional. Local/municipal sources map here too.
FUNDER_LEVEL = {"cl-gore-fndr": "regional"}


def _md5_uuid(*parts):
    """Match Postgres MD5(CONCAT_WS('-', ...))::UUID for deterministic, cross-language ids."""
    return str(uuid.UUID(hashlib.md5("-".join(p for p in parts if p is not None).encode()).hexdigest()))


@data_loader
def load_data(*args, **kwargs):
    bucket = kwargs.get("source_bucket", "test-global-api")
    url = kwargs.get("catalog_index_url", CATALOG_INDEX_URL)
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch catalog index from {url}: {e}")
    by_id = {d["id"]: d for d in yaml.safe_load(resp.text)["datasets"]}

    rows = []
    for sid in SOURCE_IDS:
        d = by_id[sid]
        pub = d["publisher"]
        releases = d.get("releases") or [{}]
        rel = next((r for r in releases if r.get("is_latest")), releases[0])
        version = str(rel.get("version") or "v1")
        # identity (stable slugs only — no dataset_url in the hash)
        datasource_name, dataset_name = sid, d["name"]
        pk = pub["id"].replace("-", "_")
        dk = sid.replace("-", "_")
        rows.append({
            "source_dataset": f'{pub["id"]}/{sid}',                 # join key to staging
            "datasource_name": datasource_name,
            "dataset_name": dataset_name,
            "dataset_url": d.get("dataset_url") or "",
            "publisher_id": _md5_uuid(pub["name"], pub["url"]),
            "publisher_name": pub["name"],
            "publisher_url": pub["url"],
            "dataset_id": _md5_uuid(datasource_name, dataset_name),
            "release_id": _md5_uuid(datasource_name, dataset_name, version),
            "publisher_is_funder": sid in PUBLISHER_IS_FUNDER,
            "funder_level": FUNDER_LEVEL.get(sid, "national"),
            "version_label": version,
            "released_at": rel.get("released_at"),
            "retrieved_at": rel.get("retrieved_at"),
            "source_url": f"s3://{bucket}/raw_data/{pk}/{dk}/release/{version}/{dk}.csv",
        })
    df = pd.DataFrame(rows)
    print(f"finance source catalog: {len(df)} datasets from index.yaml")
    return df


@test
def test_output(output, *args) -> None:
    assert len(output) == len(SOURCE_IDS), "expected one row per finance source"
    for col in ("source_dataset", "release_id", "publisher_id", "dataset_id"):
        assert output[col].notna().all() and output[col].is_unique, f"{col} missing or not unique"
