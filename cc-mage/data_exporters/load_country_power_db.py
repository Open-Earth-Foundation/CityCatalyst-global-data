if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

from pandas import DataFrame
import sys
from mage_ai.settings.repo import get_repo_path
sys.path.insert(0, get_repo_path())
from climatetrace_country_io import export_raw_table


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    export_raw_table(df, 'ct_power')
