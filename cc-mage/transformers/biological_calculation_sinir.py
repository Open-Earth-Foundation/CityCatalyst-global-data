import numpy as np
import duckdb 

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
        id_vars=['municipality_code', 'IBGE_code', 'UF', 'region_name', 'municipality_where_the_Unit_is', 'year', 'unit_type', 'municipality_sending', 'sending_region_code', 'total_SW', 'actor_name', 'columns_match', 'treatment_type'], 
        value_vars=['CH4', 'N2O'], 
        var_name='gas_name', 
        value_name='emissionfactor_value')

    # assign the emission factor units
    data['emissionfactor_units'] = 'kg/t'

    # calculate the emissions value
    data['emissions_value'] = data['emissionfactor_value']*data['total_SW']

    # assign the emissions units and the activity name
    data['emissions_units'] = 'kg'
    data['activity_name'] = 'mass-of-organic-waste-treated'

    # assign the GPC reference number based on where the waste is treated
    data['GPC_refno'] = np.where(data['columns_match'] == True, 'III.2.1', 'III.2.2')

    con = duckdb.connect(database=':memory:')
    con.register('composting_df', data)

    query = """
    SELECT *,
            CASE
                WHEN GPC_refno = 'III.2.1' THEN json_object(
                    'biological-treatment-inboundary-treatment-type','treatment-type-composting',
                    'biological-treatment-inboundary-waste-state','waste-state-dry-waste'
                )
                WHEN GPC_refno = 'III.2.2' THEN json_object(
                'biological-treatment-outboundary-treatment-type','treatment-type-composting',
                'biological-treatment-outboundary-waste-state','waste-state-dry-waste'
                ) 
            END AS activity_subcategory_type
    FROM composting_df
    """

    # Execute the query and fetch the result into a DataFrame
    data_final = con.execute(query).fetchdf()

    # drop unnecessary columns
    data_final.drop(columns=['municipality_code', 'IBGE_code', 'UF', 'region_name', 'municipality_where_the_Unit_is', 'unit_type', 'columns_match', 'treatment_type'], inplace=True)

    return data_final


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
