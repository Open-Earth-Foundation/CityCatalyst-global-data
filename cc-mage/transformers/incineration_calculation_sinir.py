import numpy as np
import duckdb 

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
        id_vars=['municipality_code', 'IBGE_code', 'UF', 'region_name', 'municipality_where_the_Unit_is', 'year', 'unit_type', 'municipality_sending', 'sending_region_code', 'total_SW', 'actor_name', 'columns_match', 'treatment_type'], 
        value_vars=['N20', 'CH4', 'CO2'], 
        var_name='gas_name', 
        value_name='emissionfactor_value')

    # assign the emission factor units
    data['emissionfactor_units'] = 'kg/t'

    # calculate the emissions value
    data['emissions_value'] = data['emissionfactor_value']*data['total_SW']

    # assign the emissions units and the activity name
    data['emissions_units'] = 'kg'
    data['activity_name'] = 'clinical-waste-incineration'

    # assign the GPC reference number based on where the waste is incinerated
    data['GPC_refno'] = np.where(data['columns_match'] == True, 'III.3.1', 'III.3.2')

    con = duckdb.connect(database=':memory:')
    con.register('incineration_df', data)

    query = """
    SELECT *,
            CASE
                WHEN GPC_refno = 'III.3.1' THEN json_object(
                    'incineration-waste-inboundary-waste-composition', 'waste-composition-clinical-waste',
                    'incineration-waste-inboundary-technology', 'technology-continuous-incineration',
                    'incineration-waste-inboundary-boiler-type', 'boiler-type-stoker',
                    'data-source', treatment_type
                )
                WHEN GPC_refno = 'III.3.2' THEN json_object(
                    'incineration-waste-outboundary-waste-composition', 'waste-composition-clinical-waste',
                    'incineration-waste-outboundary-technology', 'technology-continuous-incineration',
                    'incineration-waste-outboundary-boiler-type', 'boiler-type-stoker',
                    'data-source', treatment_type
                ) 
            END AS activity_subcategory_type
    FROM incineration_df
    """

    # Execute the query and fetch the result into a DataFrame
    data_final = con.execute(query).fetchdf()


    data_final["default_values"] = data_final.apply(
        lambda row: {
            "fraction-of-fossil-carbon": fcf,
            "oxidation-factor": of,
            "fraction-of-carbon": cf,
            # AE: it would be good to use the same naming as the manual input formula here
            "dm": dm,
            "wf": wf
        },
        axis=1,
    )

    # drop unnecessary columns
    data_final.drop(columns=['municipality_code', 'IBGE_code', 'UF', 'region_name', 'municipality_where_the_Unit_is', 'unit_type', 'columns_match', 'treatment_type'], inplace=True)
    return data_final


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
