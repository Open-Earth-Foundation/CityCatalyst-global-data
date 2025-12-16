from pandas import json_normalize
import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(data, *args, **kwargs):
    """
    Load emissions data from API for all city IDs in the input dataframe.
    """
    gases = ['co2', 'ch4', 'n2o']
    dfs = []
    year = kwargs['year']

    city_records = data[['ct_cityid', 'locode']].drop_duplicates()

    for _, row in city_records.iterrows():
        city_id = row['ct_cityid']
        locode = row['locode']

        for gas in gases:
            url = f'https://api.climatetrace.org/v7/sources/emissions?year={year}&gas={gas}&cityId={cityId}'
            api_data = requests.get(url).json()
            df = json_normalize(api_data).explode('subsectors.timeseries').reset_index(drop=True)
            df = pd.concat(
                [
                    df.drop(columns=['subsectors.timeseries']),
                    json_normalize(df['subsectors.timeseries']).add_prefix('timeseries_')
                ],
                axis=1
            )
            df = df[
                [
                    'location.name',
                    'location.cityId',
                    'timeseries_year',
                    'timeseries_month',
                    'timeseries_sector',
                    'timeseries_subsector',
                    'timeseries_gas',
                    'timeseries_emissionsQuantity'
                ]
            ]
            df.columns = [
                'city_name',
                'city_id',
                'year',
                'month',
                'sector',
                'subsector',
                'gas',
                'emissions_quantity'
            ]
            df['locode'] = locode
            df = df.groupby(
                ['city_name', 'city_id', 'locode', 'year', 'sector', 'subsector', 'gas'],
                as_index=False
            )['emissions_quantity'].sum()
            dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
