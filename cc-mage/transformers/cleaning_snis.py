if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    #column_names = ['municipality_name', 'service_type', 'total_resident_population','number_municipalities', 'collected', 'treated', 'imported', 'exported']
    #data.columns = column_names

    # Select only the rows related to the sewer system information and one mucipality atended by the service
    data = data[~data['service_type'].isin(['Água']) & (data['number_municipalities'] == 1)]

    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'