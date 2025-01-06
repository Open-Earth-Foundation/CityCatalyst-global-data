import pandas as pd
import numpy as np
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # Formula
    def ef_ch4_methane_commitment(DOC, f_rec, management_level):
        """
        CH4 emission factor formula for methane commitment methodology, based on DOC, f_rec and management level.
        Source: IPCC 2006
        """

        MCF_dic = {
        'managed': 1,
        'unmanaged': 0.8,
        'uncategorized': 0.6
        }

        OX_dic = {
        'managed': 0.1,
        'unmanaged': 0,
        'uncategorized': 0
        }

        mcf = MCF_dic.get(management_level)
        ox = OX_dic.get(management_level)

        Lo = mcf*DOC*0.6*0.5*16/12

        return Lo*(1-f_rec)*(1-ox)

    # filter the df only for the treatment types that are valid for clinical waste disposal
    data = data[data['treatment_type']=='clinical waste trench']

    ## DOC = degradable organic carbon [source = IPCC 2006]
    ## units = kg C / t waste
    ## (region = world)
    data.loc[:,'DOC'] = 150 

    # assign the management level
    data.loc[:,'management_level'] = 'managed'

    # Apply the function to each row
    data.loc[:,'emissionfactor_value'] = data.apply(lambda row: ef_ch4_methane_commitment(
        DOC=row['DOC'],
        f_rec=0,  # Applying f_rec = 0 for all rows
        management_level=row['management_level']
    ), axis=1)

    # assign the emission factor units
    data['emissionfactor_units'] = 'kg/t'

    # calculate the emissions value
    data['emissions_value'] = data['emissionfactor_value']*data['total_SW']

    # assign the emissions units
    data['emissions_units'] = 'kg'

    # assign the gas name and the activity name
    data['gas_name'] = 'CH4'
    data['activity_name'] = 'clinical waste disposal'

    # assign the GPC reference number based on where the waste is treated
    data.loc[:, 'GPC_refno'] = np.where(data.loc[:,'columns_match'] == True, 'III.1.1', 'III.1.2')

    # create the metadata column to store the subcategory information
    data["metadata"] = data.apply(
        lambda row: {
            "activity_subcategory_type1": 'waste_type',
            "activity_subcategory_typename1": 'clinical waste',
            "activity_subcategory_type2": 'treatment_type',
            "activity_subcategory_typename2": row['treatment_type'],
            "activity_subcategory_type3": 'management_level',
            "activity_subcategory_typename3": row['management_level'],
            "activity_subcategory_type4": 'DOC',
            "activity_subcategory_typename4": 150,
            "activity_subcategory_type5": 'f_rec',
            "activity_subcategory_typename5": 0
        },
        axis=1,
    )

    # drop unnecessary columns
    data.drop(columns=['municipality_where_the_Unit_is', 'unit_type', 'municipality_sending', 'columns_match', 'treatment_type', 'DOC', 'management_level'], inplace=True)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'