import duckdb
from mage_ai.data_preparation.shared.secrets import get_secret_value

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_s3(*args, **kwargs):
    """
    Load MapBiomas Chile LULC city attributes from S3 CSV and join with the
    OCHA COD-AB parquet to resolve locode from comuna code.

    CSV schema (INE-shaped raw_data export):
        region, comuna, region_nombre, comuna_nombre,
        attribute_type, attribute_value, attribute_units, attribute_category

    OCHA AB parquet schema:
        comuna_code, country_code, region_code, region_name,
        comuna_name, locode, locode_name, geometry (WKB)

    Output staging schema:
        locode, region_nombre, attribute_type, attribute_value,
        attribute_units, attribute_category
    """
    bucket_name = kwargs["bucket_name"]
    lulc_key = kwargs["lulc_key"]
    ocha_ab_key = kwargs["ocha_ab_key"]

    aws_access_key_id = get_secret_value("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_secret_value("AWS_SECRET_ACCESS_KEY")

    conn = duckdb.connect()
    conn.execute("INSTALL spatial;")
    conn.execute("LOAD spatial;")
    conn.execute(
        f"""
        CREATE SECRET (
            TYPE 'S3',
            KEY_ID '{aws_access_key_id}',
            SECRET '{aws_secret_access_key}',
            REGION 'us-east-1'
        );
    """
    )

    query = f"""
        SELECT
            ab.locode,
            c.region_nombre,
            c.attribute_type,
            ROUND(c.attribute_value::DOUBLE, 1)::VARCHAR AS attribute_value,
            c.attribute_units,
            c.attribute_category
        FROM read_csv_auto('s3://{bucket_name}/{lulc_key}') AS c
        INNER JOIN (
            SELECT DISTINCT
                comuna_code::VARCHAR AS comuna_code,
                locode
            FROM read_parquet('s3://{bucket_name}/{ocha_ab_key}')
            WHERE locode IS NOT NULL
        ) AS ab
            ON c.comuna::VARCHAR = REPLACE(ab.comuna_code, 'CL', '')::int
    """

    df = conn.execute(query).fetchdf()
    conn.close()
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
    assert len(output) > 0, "No rows returned"
    assert output["locode"].notna().all(), "Null locodes found after join"
    assert output["locode"].str.startswith("CL").all(), "Non-CL locodes found"
    assert output["attribute_type"].notna().all(), "Null attribute_type found"
