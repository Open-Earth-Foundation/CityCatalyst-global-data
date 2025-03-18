import pandas as pd
import numpy as np
import duckdb

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
    data['activity_name'] = 'clinical-waste-disposal'

    # assign the GPC reference number based on where the waste is treated
    data.loc[:, 'GPC_refno'] = np.where(data.loc[:,'columns_match'] == True, 'III.1.1', 'III.1.2')

    mcf_name_dict = {
        'managed': 'oxidation-factor-well-managed-landfill',
        'unmanaged': 'oxidation-factor-unmanaged-landfill',
        'uncategorized': 'oxidation-factor-unmanaged-landfill'

    }

    con = duckdb.connect(database=':memory:')
    con.register('clincal_df', data)

    query = """
    SELECT *,
            json_object(
                    'data-source', treatment_type,
                     'methane-commitment-solid-waste-outboundary-oxidation-factor', 
                     case when management_level = 'managed' then 'oxidation-factor-well-managed-landfill'
                     else 'oxidation-factor-unmanaged-landfill' end
                     )
            AS activity_subcategory_type
    FROM clincal_df
    """

    # Execute the query and fetch the result into a DataFrame
    data_final = con.execute(query).fetchdf()

    data_final["default_values"] = data.apply(
        lambda row: {
            "methane-correction-factor": (lambda level: {'managed': 1, 'unmanaged': 0.8, 'uncategorized': 0.6}.get(level, 0.6))(row['management_level']),
            "methane-collected-and-removed": (lambda level: {'managed': 0.1, 'unmanaged': 0, 'uncategorized': 0}.get(level, 0))(row['management_level']),
            "DOC": 150,
            "methane-collected-and-removed": 0
        },
        axis=1,
    )

    # drop unnecessary columns
    data_final.drop(columns=['municipality_code', 'IBGE_code', 'UF', 'region_name', 'municipality_where_the_Unit_is', 'region_code', 'unit_type', 'municipality_sending', 'columns_match', 'treatment_type', 'DOC', 'management_level'], inplace=True)

    return data_final


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'