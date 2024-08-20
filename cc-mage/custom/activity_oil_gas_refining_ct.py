import pandas as pd

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def transform_custom(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    ## Activity_Subcategory 
    act = args[0]

    # Drop duplicate rows
    act = act.drop_duplicates(subset=['source_id', 'source_type'], ignore_index=True)

    # Create a json column with the extra information
    # easier to convert to json in database rather than python.
    #act.loc[:, 'activity_subcategory_type'] = act.apply(lambda row: f"facility_type:{row['source_type']}, facility_name:{row['source_name']}", axis=1)

    # Note: this info isn't in the data, it's from the methodology
    # Assign activity units
    act.loc[:, 'activity_units'] = 'bpd'   # units: barrels per day

    # Select the columns of interest
    act = act[['source_id','activity_name', 'activity_units', 'source_type', 'source_name', 'gpc_refno']]

    return act

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'