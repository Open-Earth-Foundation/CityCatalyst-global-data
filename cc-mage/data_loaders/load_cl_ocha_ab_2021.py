import duckdb
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_s3(*args, **kwargs):
    """
    Load Chile admin boundaries (OCHA COD-AB 2021) from S3 GeoParquet.

    Schema: comuna_code, country_code, region_code, region_name,
            comuna_name, locode, locode_name, geometry (WKB)

    Uses read_parquet() instead of st_read() so DuckDB can apply
    column pruning and byte-range reads — only fetches needed columns.
    Only rows where locode IS NOT NULL are returned.
    """
    bucket_name = kwargs['bucket_name']
    ocha_ab_key = kwargs['ocha_ab_key']

    aws_access_key_id = get_secret_value('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = get_secret_value('AWS_SECRET_ACCESS_KEY')

    conn = duckdb.connect()

    conn.execute("INSTALL spatial;")
    conn.execute("LOAD spatial;")

    conn.execute(f"""
        CREATE SECRET (
            TYPE 'S3',
            KEY_ID '{aws_access_key_id}',
            SECRET '{aws_secret_access_key}',
            REGION 'us-east-1'
        );
    """)

    query = f"""
        SELECT
            locode,
            comuna_name                                         AS city_name,
            'municipality'                                      AS city_type,
            country_code,
            region_code,
            NULL::VARCHAR                                       AS osm_id,
            ST_AsText(ST_GeomFromWKB(geometry))                 AS wkt_geom,
            ST_Y(ST_Centroid(ST_GeomFromWKB(geometry)))         AS lat,
            ST_X(ST_Centroid(ST_GeomFromWKB(geometry)))         AS lon,
            ST_YMax(ST_GeomFromWKB(geometry))                   AS bbox_north,
            ST_YMin(ST_GeomFromWKB(geometry))                   AS bbox_south,
            ST_XMax(ST_GeomFromWKB(geometry))                   AS bbox_east,
            ST_XMin(ST_GeomFromWKB(geometry))                   AS bbox_west
        FROM read_parquet('s3://{bucket_name}/{ocha_ab_key}')
        WHERE locode IS NOT NULL
    """

    df = conn.execute(query).fetchdf()
    conn.close()

    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert len(output) > 0, 'No rows returned'
    assert output['locode'].notna().all(), 'Null locodes found — filter not applied'
    assert output['locode'].str.startswith('CL').all(), 'Non-CL locodes found'
