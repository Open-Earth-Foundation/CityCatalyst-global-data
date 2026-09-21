"""Shared helpers for Climate TRACE country-package loaders."""
from os import environ, path
from tempfile import gettempdir

import pandas as pd
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
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


def empty_emissions_frame() -> pd.DataFrame:
    return pd.DataFrame(columns=RAW_COLUMNS)


def _canonical_sector(sector: str) -> str:
    return (sector or '').strip().lower().replace('_', '-').replace(' ', '-')


def _country_code(kwargs: dict) -> str:
    return str(kwargs.get('country_code') or 'PHL').strip().upper()


def _aws_keys():
    try:
        from mage_ai.data_preparation.shared.secrets import get_secret_value

        key_id = get_secret_value('AWS_ACCESS_KEY_ID')
        secret = get_secret_value('AWS_SECRET_ACCESS_KEY')
        if key_id and secret:
            return key_id, secret
    except Exception:
        pass
    return environ.get('AWS_ACCESS_KEY_ID'), environ.get('AWS_SECRET_ACCESS_KEY')


def _configure_duckdb_s3(conn) -> None:
    conn.execute('INSTALL httpfs; LOAD httpfs;')
    key_id, secret = _aws_keys()
    if key_id and secret:
        conn.execute(
            f"""
            CREATE SECRET (
                TYPE 'S3',
                KEY_ID '{key_id}',
                SECRET '{secret}',
                REGION 'us-east-1'
            );
            """
        )
        return
    conn.execute(
        """
        CREATE SECRET (
            TYPE 'S3',
            PROVIDER CREDENTIAL_CHAIN,
            REGION 'us-east-1'
        );
        """
    )


def _read_csv_glob(conn, bucket_name: str, object_key: str) -> pd.DataFrame:
    query = (
        f"SELECT * FROM read_csv('s3://{bucket_name}/{object_key}', "
        "union_by_name=true)"
    )
    return conn.execute(query).fetchdf()


def _select_raw_columns(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return empty_emissions_frame()
    missing = [col for col in RAW_COLUMNS if col not in df.columns]
    if missing:
        for col in missing:
            df[col] = pd.NA
    out = df[RAW_COLUMNS].copy()
    out['start_time'] = pd.to_datetime(out['start_time'], errors='coerce')
    return out


def _combined_object_keys(country_code: str):
    return [
        f'files/climatetrace/version_2025/country/{country_code}/{gas_dir}/'
        f'emissions_{gas_file}_v*.csv'
        for gas_dir, gas_file in COMBINED_GASES
    ]


def _legacy_object_keys(country_code: str, sector: str):
    folder = sector.replace('-', '_')
    return [
        f'files/climatetrace/version_2025/{country_code}/{gas}/{folder}/'
        f'*_emissions_sources_v*.csv'
        for gas, _ in COMBINED_GASES
    ]


def _cache_path(bucket_name: str, country_code: str) -> str:
    return path.join(
        gettempdir(),
        f'ct_country_{bucket_name}_{country_code}.pkl',
    )


def load_country_all_emissions(kwargs: dict) -> pd.DataFrame:
    """Read the combined per-gas country CSVs from S3."""
    import duckdb

    bucket_name = kwargs['bucket_name']
    country_code = _country_code(kwargs)
    cache_file = _cache_path(bucket_name, country_code)
    if path.exists(cache_file):
        cached = pd.read_pickle(cache_file)
        if cached is not None and not cached.empty:
            return cached

    conn = duckdb.connect()
    frames = []
    try:
        _configure_duckdb_s3(conn)
        for object_key in _combined_object_keys(country_code):
            try:
                frames.append(_read_csv_glob(conn, bucket_name, object_key))
            except Exception as exc:
                print(
                    f'Skipping combined {object_key} for country={country_code}: {exc}'
                )
        df = pd.concat(frames, ignore_index=True) if frames else empty_emissions_frame()
    finally:
        conn.close()

    df = _select_raw_columns(df)
    if not df.empty:
        df.to_pickle(cache_file)
    return df


def load_country_sector_emissions(sector: str, kwargs: dict) -> pd.DataFrame:
    """
    Read Climate TRACE v2025 country source CSVs for one sector from S3.

    Preferred layout (combined all-sector files per gas):
      s3://{bucket}/files/climatetrace/version_2025/country/{ISO3}/{GAS}/emissions_{gas}_v*.csv

    Fallback (legacy per-sector folders):
      s3://{bucket}/files/climatetrace/version_2025/{CC}/{GAS}/{sector}/*_emissions_sources_v*.csv
    """
    import duckdb

    bucket_name = kwargs['bucket_name']
    country_code = _country_code(kwargs)
    canon_sector = _canonical_sector(sector)

    combined = load_country_all_emissions(kwargs)
    if combined is not None and not combined.empty:
        sector_match = combined['sector'].map(_canonical_sector) == canon_sector
        filtered = combined.loc[sector_match].copy()
        if not filtered.empty:
            return filtered

    conn = duckdb.connect()
    frames = []
    try:
        _configure_duckdb_s3(conn)
        for object_key in _legacy_object_keys(country_code, sector):
            try:
                frames.append(_read_csv_glob(conn, bucket_name, object_key))
            except Exception as exc:
                print(
                    f'Skipping {object_key} for sector={sector} '
                    f'country={country_code}: {exc}'
                )
        df = pd.concat(frames, ignore_index=True) if frames else empty_emissions_frame()
    finally:
        conn.close()

    df = _select_raw_columns(df)
    if df.empty:
        return empty_emissions_frame()
    sector_match = df['sector'].map(_canonical_sector) == canon_sector
    filtered = df.loc[sector_match].copy()
    return filtered if not filtered.empty else df


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

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    bucket_name = kwargs['bucket_name']
    object_key = f'files/climatetrace/version_2025/mappings/{filename}'
    return S3.with_config(ConfigFileLoader(config_path, 'default')).load(
        bucket_name,
        object_key,
    )


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
