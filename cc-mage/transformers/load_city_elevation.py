import requests

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def get_elevation(latitude, longitude):
    """Fetch elevation data from an external API."""
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={latitude},{longitude}"
    response = requests.get(url)
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]['elevation']
    else:
        return None


@transformer
def transform(data, *args, **kwargs):
    """
    Transform input data to add elevation based on lat and lon.

    Args:
        data: DataFrame containing lat and lon columns.

    Returns:
        DataFrame with added elevation column.
    """
    # Check if 'lat' and 'lon' columns exist in the DataFrame
    if 'lat' in data.columns and 'lon' in data.columns:
        # Create a list to store elevation data
        elevations = []

        # Iterate through the rows of the DataFrame
        for index, row in data.iterrows():
            lat = row['lat']
            lon = row['lon']
            elevation = get_elevation(lat, lon)
            elevations.append(elevation)

        # Add the elevations to the DataFrame
        data['elevation'] = elevations
    
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'