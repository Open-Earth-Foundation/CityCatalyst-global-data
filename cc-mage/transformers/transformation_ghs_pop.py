if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from pandas import DataFrame
import pandas as pd


@transformer
def transform(data: DataFrame, *args, **kwargs):

    data = data[['locode', 'population']]

    data['population'] = pd.to_numeric(data['population'], downcast='integer', errors='coerce')
    data['year'] = '2020'
    data['population_source'] = 'estimation'
    data['geographical_level'] = 'city'

    data['publisher_name'] = 'Copernicus EU'
    data['publisher_url'] = 'https://human-settlement.emergency.copernicus.eu/'
    data['datasource_name'] = 'Global Human Settlement Layer'
    data['dataset_name'] = 'GHS_POP_E2020_GLOBE_R2023A_4326_3ss_V1_0'
    data['dataset_url'] = 'https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_54009_100/V1-0/GHS_POP_E2020_GLOBE_R2023A_54009_100_V1_0.zip'


    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
