if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # filter by the intereted columns
    data = data[['municipality_name', 'service_type', 'GE12b', 'GE005', 'ES005', 'ES006', 'ES014', 'ES015']]
    
    #rename columns
    column_names = ['municipality_name', 'service_type', 'total_resident_population','number_municipalities', 'collected', 'treated', 'imported', 'exported']
    data.columns = column_names

    # Select only the rows related to the sewer system information and one mucipality atended by the service
    data = data[~df_f['service_type'].isin(['Água']) & (df_f['number_municipalities'] == 1)]

    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'