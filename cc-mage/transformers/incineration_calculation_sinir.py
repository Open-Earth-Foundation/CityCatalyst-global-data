import numpy as np
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # filter the df only for the treatment types that are valid for incineration
    data = data[data['treatment_type']=='incineration']

    # Emission factor for N2O from incineration
    #Source IPCC 2006
    data['N20'] = 50*1e-3 ## parameter = continuous and semi-continuous incinerators, 'ef_units' 'kg/t'

    # Source IPCC 2006
    data['CH4'] = 0.2*1e-3 ## parameter = stoke, 'ef_units' 'kg/t'

    ## for clinical waste [source = IPCC 2006]
    wf = 1
    dm = 0.9   ## type of waste = Other, inert waste
    cf = 0.6   ## carbon fraction
    fcf = 0.25 ## fossil carbon content
    of = 1     ## oxidation factor for incineration

    ef_co2_value = wf*dm*cf*fcf*of*(44/12)

    # Source IPCC 2006
    data['CO2'] = ef_co2_value*1e3  # 'ef_units' 'kg/t'

    # reformat the df
    data = data.melt(
        id_vars=['municipality_where_the_Unit_is', 'year', 'unit_type', 'municipality_sending', 'total_SW', 'actor_name', 'columns_match', 'treatment_type'], 
        value_vars=['N20', 'CH4', 'CO2'], 
        var_name='gas_name', 
        value_name='emissionfactor_value')

    # assign the emission factor units
    data['emissionfactor_units'] = 'kg/t'

    # calculate the emissions value
    data['emissions_value'] = data['emissionfactor_value']*data['total_SW']

    # assign the emissions units and the activity name
    data['emissions_units'] = 'kg'
    data['activity_name'] = 'clinical waste incineration'

    # assign the GPC reference number based on where the waste is incinerated
    data['GPC_refno'] = np.where(data['columns_match'] == True, 'III.3.1', 'III.3.2')

    # create the metadata column to store the subcategory information
    data["activity_subcategory_type"] = data.apply(
        lambda row: {
            "activity_subcategory_type1": 'waste_type',
            "activity_subcategory_typename1": 'clinical waste',
            "activity_subcategory_type2": 'treatment_type',
            "activity_subcategory_typename2": row['treatment_type'],
            "activity_subcategory_type3": 'management_level',
            "activity_subcategory_typename3": 'managed',
            "activity_subcategory_type4": 'technology_type',
            "activity_subcategory_typename4": 'continuous and semi-continuous incinerators',
            "activity_subcategory_type5": 'boiler_type',
            "activity_subcategory_typename5": 'stoke'
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
