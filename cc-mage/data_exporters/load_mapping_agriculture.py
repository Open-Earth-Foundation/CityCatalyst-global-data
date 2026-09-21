if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

from pandas import DataFrame
from climatetrace_country_io import export_raw_table


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    export_raw_table(df, 'ct_agriculture_mapping')
