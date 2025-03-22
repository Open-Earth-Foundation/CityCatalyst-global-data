if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import fiona
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np


@transformer
def transform(data, *args, **kwargs):

    # List available layers
    layers = fiona.listlayers(gpkg_path)
    layers = layers[:-1]

    filtered_dfs = []

    # Read each layer and filter by 'COUNTRY' = 'BRAZIL'
    for layer in layers:
        try:
            gdf = gpd.read_file(gpkg_path, layer=layer)
            if 'COUNTRY' in gdf.columns:  # Check if the column exists
                gdf_filtered = gdf[gdf['COUNTRY'] == 'BRAZIL'].copy()
                gdf_filtered['SOURCE_LAYER'] = layer
                filtered_dfs.append(gdf_filtered)
        except Exception as e:
            print(f"Error reading layer {layer}: {e}")

    final_gdf = gpd.GeoDataFrame(pd.concat(filtered_dfs, ignore_index=True))

    final_gdf = final_gdf[['CATEGORY', 'COUNTRY', 'STATE_PROV', 'FAC_NAME', 'FAC_STATUS', 'LATITUDE', 'LONGITUDE']]

    final_gdf.columns = ['type', 'country', 'region', 'facility_name', 'status', 'lat', 'lon']

    final_gdf.loc[:, 'gpc_reference_number'] = 'I.8.1'
    


    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
