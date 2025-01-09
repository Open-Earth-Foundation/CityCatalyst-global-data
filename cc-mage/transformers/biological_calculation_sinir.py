import numpy as np
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # filter the df only for the treatment types that are valid for biological treatment
    data = data[data['treatment_type'].isin(['composting unit', 'pruning management unit'])]

    # Source IPCC, ef units = kg ch4 / t of waste, composting - dry waste
    data['CH4'] = 10
    data['N2O'] = 0.6

    # reformat the df
    data = data.melt(
        id_vars=['municipality_where_the_Unit_is', 'year', 'unit_type', 'municipality_sending', 'total_SW', 'actor_name', 'columns_match', 'treatment_type'], 
        value_vars=['CH4', 'N2O'], 
        var_name='gas_name', 
        value_name='emissionfactor_value')

    # assign the emission factor units
    data['emissionfactor_units'] = 'kg/t'

    # calculate the emissions value
    data['emissions_value'] = data['emissionfactor_value']*data['total_SW']

    # assign the emissions units and the activity name
    data['emissions_units'] = 'kg'
    data['activity_name'] = 'composting of organic waste'

    # assign the GPC reference number based on where the waste is treated
    data['GPC_refno'] = np.where(data['columns_match'] == True, 'III.2.1', 'III.2.2')

    # create the metadata column to store the subcategory information
    data["activity_subcategory_type"] = data.apply(
        lambda row: {
            "activity_subcategory_type1": 'waste_type',
            "activity_subcategory_typename1": 'organic waste',
            "activity_subcategory_type2": 'treatment_type',
            "activity_subcategory_typename2": row['treatment_type'],
            "activity_subcategory_type3": 'management_level',
            "activity_subcategory_typename3": 'managed',
            "activity_subcategory_type4": 'waste_state',
            "activity_subcategory_typename4": 'dry waste'
        },
        axis=1,
    )

    # drop unnecessary columns
    data.drop(columns=['municipality_where_the_Unit_is', 'unit_type', 'municipality_sending', 'columns_match', 'treatment_type'], inplace=True)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
