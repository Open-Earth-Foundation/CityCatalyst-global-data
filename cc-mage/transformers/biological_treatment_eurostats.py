if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd


@transformer
def transform(data, *args, **kwargs):
    """
    notes: 
    - IPCC 2006 Waste data guidance explicitly notes that waste generation/management data are generally based on the weight of wet waste
    - treatment type: composting
    """
    def CH4_emissions_Biological(SW, EF_CH4, R):
        """
        CH4 emissions from waste -  Biological Treatment
        where:
        SW: solid waste generated (kg)
        EF_CH4: methane emission factor (kg CH4/kg waste)
        R: total ch4 recovered (kg)
        """
        return (SW * EF_CH4) - R

    def N2O_emissions_Biological(SW, EF_N2O):
        """
        N2O emissions from waste -  Biological Treatment
        where:
        SW: solid waste generated (kg)
        EF_N2O: nitrous oxide emission factor (kg N2O/kg waste)
        """
        return SW * EF_N2O

    # Default Emission factors -  Wet waste
    ef_ch4_composting = 4*10**-3   # kg CH4/kg waste
    ef_n2o_composting = 0.24*10**-3  # kg N2O/kg waste

    # assuming no methane is recovered from composting
    R = 0

    gdf_II_ch4 = data[data['management'] == 'Composting'].copy()
    gdf_II_ch4['emissions_value'] = gdf_II_ch4.apply(
        lambda row: CH4_emissions_Biological(row['total_waste'], ef_ch4_composting, R), axis=1
    )
    gdf_II_ch4['gas_name'] = 'CH4'
    gdf_II_ch4['emissions_units'] = 'kg'
    gdf_II_ch4['emissionfactor_value'] = ef_ch4_composting
    gdf_II_ch4['emissionfactor_units'] = 'kg/kg'


    gdf_II_n2o = data[data['management'] == 'Composting'].copy()
    gdf_II_n2o['emissions_value'] = gdf_II_n2o.apply(
        lambda row: N2O_emissions_Biological(row['total_waste'], ef_n2o_composting), axis=1
    )
    gdf_II_n2o['gas_name'] = 'N2O'
    gdf_II_n2o['emissions_units'] = 'kg'
    gdf_II_n2o['emissionfactor_value'] = ef_n2o_composting
    gdf_II_n2o['emissionfactor_units'] = 'kg/kg'

    # Combine into one dataframe
    gdf_II = pd.concat([gdf_II_ch4, gdf_II_n2o], ignore_index=True)

    gdf_II['gpc_reference_number'] = None  # Initialize column

    gdf_II.loc[gdf_II['scope'] == 1, 'gpc_reference_number'] = 'III.2.1'
    gdf_II.loc[gdf_II['scope'] == 3, 'gpc_reference_number'] = 'III.2.3'

    # methodology id assignation
    gdf_II.loc[gdf_II['scope'] == 1, 'methodology_name'] = 'biological-treatment-inboundary-methodology'
    gdf_II.loc[gdf_II['scope'] == 3, 'methodology_name'] = 'biological-treatment-outboundary-methodology'

    # activity data
    gdf_II['activity_name'] = 'mass-of-organic-waste-treated'
    gdf_II['activity_units'] = 'kg'

    return gdf_II

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
