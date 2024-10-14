import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, data_2, *args, **kwargs):
    """
    """

    #filtering data emissions in a city level
    data_emissions = data[data['datasource_name'].isin(['Climate TRACE Fall_2023', 'Google EIE', 'SEEG'])]

    #filtering benchmark dataset only for emissions and lower and upper bounds House
    benchmark_emissions = data_2[
        (data_2['Variable_name'] == 'emissions') & 
        (data_2['statistic_name'].isin(['lower_bound', 'upper_bound']))
    ]

    # Pivot the filtered benchmark data to have lower and upper bounds in separate columns
    benchmark_emissions_pivot = benchmark_emissions.pivot_table(
        index='gpc_refno', 
        columns='statistic_name', 
        values='statistic_value'  
    ).reset_index()

    # Merge the benchmark bounds back to the emissions data
    merged_data = pd.merge(
        data_emissions,
        benchmark_emissions_pivot,
        left_on='gpc_reference_number',   
        right_on='gpc_refno',             
        how='left'                        
    )

    # Define a function to validate emissions
    def validate_emission(emission, lower, upper):
        if pd.isnull(lower) or pd.isnull(upper):
            return 'No Benchmark Data'
        elif emission < lower:
            return 'Below Benchmark'
        elif emission > upper:
            return 'Above Benchmark'
        else:
            return 'Within Benchmark'

    # Apply the validation function to each row
    merged_data['Validation'] = merged_data.apply(
        lambda row: validate_emission(row['emissions_value'], row['lower_bound'], row['upper_bound']),
        axis=1
    )

    return merged_data[merged_data['Validation']=='Within Benchmark']

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'