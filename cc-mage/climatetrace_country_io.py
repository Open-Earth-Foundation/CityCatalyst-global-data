"""Shared helpers for Climate TRACE country-package loaders."""
from io import BytesIO
from os import path
from tempfile import gettempdir

import boto3
import pandas as pd
from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError
from mage_ai.io.config import ConfigFileLoader
from mage_ai.settings.repo import get_repo_path

RAW_COLUMNS = [
    'iso3_country',
    'sector',
    'subsector',
    'start_time',
    'gas',
    'lat',
    'lon',
    'emissions_quantity',
    'source_name',
    'activity',
    'activity_units',
    'emissions_factor',
    'emissions_factor_units',
]

CITY_MAPPING_FILE = 'ct_to_city_mapping.csv'
COMBINED_GASES = (
    ('CO2', 'co2'),
    ('CH4', 'ch4'),
    ('N2O', 'n2o'),
)
DEFAULT_FILE_VERSION = '5_10_0'


def empty_emissions_frame() -> pd.DataFrame:
    return pd.DataFrame(columns=RAW_COLUMNS)


def _canonical_sector(sector: str) -> str:
    return (sector or '').strip().lower().replace('_', '-').replace(' ', '-')


def _country_code(kwargs: dict) -> str:
    return str(kwargs.get('country_code') or 'PHL').strip().upper()


def _file_version(kwargs: dict) -> str:
    raw = kwargs.get('ct_file_version')
    if raw is None or raw == '':
        return DEFAULT_FILE_VERSION
    # YAML 5_10_0 is parsed as int 5100; Mage also stores it that way.
    if raw in (5100, '5100', 5_10_0):
        return DEFAULT_FILE_VERSION
    version = str(raw).strip().lstrip('vV')
    if version == '5100':
        return DEFAULT_FILE_VERSION
    return version or DEFAULT_FILE_VERSION


def _clean_secret(value):
    if value is None:
        return None
    text = str(value).strip().strip('"').strip("'")
    if not text or text.startswith('{{') or 'mage_secret_var' in text:
        return None
    return text


def _aws_keys(kwargs: dict):
    key_id = _clean_secret(kwargs.get('aws_access_key_id'))
    secret = _clean_secret(kwargs.get('aws_secret_access_key'))
    if not key_id or not secret:
        from mage_ai.data_preparation.shared.secrets import get_secret_value

        key_id = key_id or _clean_secret(get_secret_value('AWS_ACCESS_KEY_ID'))
        secret = secret or _clean_secret(get_secret_value('AWS_SECRET_ACCESS_KEY'))
    if not key_id or not secret:
        raise RuntimeError(
            'Missing Mage secrets AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY.'
        )
    print(f'AWS access key id length={len(key_id)} prefix={key_id[:4]}')
    return key_id, secret


def _combined_object_key(country_code: str, gas_dir: str, gas_file: str, version: str) -> str:
    return (
        f'files/climatetrace/version_2025/country/{country_code}/'
        f'{gas_dir}/emissions_{gas_file}_v{version}.csv'
    )


def _select_raw_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return empty_emissions_frame()
    work = df.copy()
    for col in RAW_COLUMNS:
        if col not in work.columns:
            work[col] = pd.NA
    out = work[RAW_COLUMNS].copy()
    out['start_time'] = pd.to_datetime(out['start_time'], errors='coerce')
    return out


def _cache_path(bucket_name: str, country_code: str, version: str) -> str:
    return path.join(
        gettempdir(),
        f'ct_country_{bucket_name}_{country_code}_{version}.pkl',
    )


def _read_s3_csv(bucket_name: str, object_key: str, kwargs: dict) -> pd.DataFrame:
    """Signed GetObject on an exact key. DuckDB httpfs GETs are often unsigned 403s."""
    key_id, secret = _aws_keys(kwargs)
    client = boto3.client(
        's3',
        aws_access_key_id=key_id,
        aws_secret_access_key=secret,
        region_name='us-east-1',
        config=BotoConfig(signature_version='s3v4'),
    )
    try:
        body = client.get_object(Bucket=bucket_name, Key=object_key)['Body'].read()
    except ClientError as exc:
        error = exc.response.get('Error') or {}
        raise RuntimeError(
            f"{object_key}: AWS {error.get('Code')} {error.get('Message')}"
        ) from exc
    return pd.read_csv(BytesIO(body))


def load_country_all_emissions(kwargs: dict) -> pd.DataFrame:
    """Read the combined per-gas country CSVs from S3 using exact object keys."""
    bucket_name = kwargs['bucket_name']
    country_code = _country_code(kwargs)
    version = _file_version(kwargs)
    cache_file = _cache_path(bucket_name, country_code, version)
    if path.exists(cache_file):
        cached = pd.read_pickle(cache_file)
        if cached is not None and not cached.empty:
            return cached

    frames = []
    errors = []
    print(
        f'CT exact-key GetObject country={country_code} version={version} '
        f'(combined files, not per-sector folders)'
    )
    for gas_dir, gas_file in COMBINED_GASES:
        object_key = _combined_object_key(country_code, gas_dir, gas_file, version)
        print(f'GET s3://{bucket_name}/{object_key}')
        try:
            frames.append(_read_s3_csv(bucket_name, object_key, kwargs))
            print(f'Loaded s3://{bucket_name}/{object_key}')
        except Exception as exc:
            errors.append(f'{object_key}: {exc}')
            print(f'Failed s3://{bucket_name}/{object_key}: {exc}')

    if not frames:
        raise RuntimeError(
            'Could not read Climate TRACE country files from S3. '
            'Use exact object keys (GetObject); glob listing is not allowed. '
            + ' | '.join(errors)
        )

    df = _select_raw_columns(pd.concat(frames, ignore_index=True))
    if not df.empty:
        df.to_pickle(cache_file)
    return df


def load_country_sector_emissions(sector: str, kwargs: dict) -> pd.DataFrame:
    """
    Read Climate TRACE v2025 country source CSVs for one sector from S3.

    Layout:
      s3://{bucket}/files/climatetrace/version_2025/country/{ISO3}/{GAS}/emissions_{gas}_v{version}.csv
    """
    canon_sector = _canonical_sector(sector)
    combined = load_country_all_emissions(kwargs)
    if combined is None or combined.empty:
        return empty_emissions_frame()

    sector_match = combined['sector'].map(_canonical_sector) == canon_sector
    filtered = combined.loc[sector_match].copy()
    return filtered if not filtered.empty else empty_emissions_frame()


def export_raw_table(df: pd.DataFrame, table_name: str) -> None:
    from mage_ai.io.postgres import Postgres

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    with Postgres.with_config(ConfigFileLoader(config_path, 'default')) as loader:
        loader.export(
            df,
            'raw_data',
            table_name,
            index=False,
            if_exists='replace',
        )


def load_ct_gpc_mapping(filename: str, kwargs: dict) -> pd.DataFrame:
    """Load a CT→GPC mapping from the repo, falling back to S3."""
    local_path = path.join(
        get_repo_path(),
        'datasets',
        'climatetrace',
        'mappings',
        filename,
    )
    if path.exists(local_path):
        return pd.read_csv(local_path)

    bucket_name = kwargs['bucket_name']
    object_key = f'files/climatetrace/version_2025/mappings/{filename}'
    return _read_s3_csv(bucket_name, object_key, kwargs)


def load_ct_sector_mapping(sector: str, kwargs: dict) -> pd.DataFrame:
    """Load mapped GPC rows for one CT sector from ct_to_city_mapping.csv."""
    df = load_ct_gpc_mapping(CITY_MAPPING_FILE, kwargs)
    if df is None or df.empty:
        return pd.DataFrame()

    canon_sector = _canonical_sector(sector)
    work = df.copy()
    work['sector'] = work['sector'].astype(str).map(_canonical_sector)
    work['subsector'] = work['subsector'].astype(str).str.strip()
    if 'mapping' in work.columns:
        work = work[work['mapping'].astype(str).str.strip().str.upper() == 'Y']
    work = work[work['sector'] == canon_sector]
    if 'gpc_reference_number' in work.columns:
        work['gpc_reference_number'] = (
            work['gpc_reference_number'].astype(str).str.strip()
        )
        work = work[~work['gpc_reference_number'].str.lower().isin(['', 'nan'])]
    return work.drop(columns=['mapping'], errors='ignore')
