if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd


@transformer
def transform(data, *args, **kwargs):

    # Non-biogenic CO2 emissions from the incineration of waste
    def CO2_emissions_Incineration(m, waste_composition, dm, CF, FCF, OX):
        """
        Non-biogenic CO2 emissions from the incineration of waste
        
        Parameters:
        m: mass of waste incinerated (kg)
        waste_composition: dict with waste fractions (%) by type
        dm: dict with dry matter content by type
        CF: dict with carbon fraction by type
        FCF: dict with fossil carbon fraction by type
        OX: oxidation factor (as percentage, e.g., 100 = 1.0)
        
        Note: If a key is not found, uses 'other' as fallback
        Note: sum of waste_composition should be 100
        """
        
        total = 0
        for waste_type, WF_percent in waste_composition.items():
            
            # Get values, fallback to 'other' if key not found
            WF = WF_percent / 100  # Convert percentage to fraction
            dm_val = dm.get(waste_type, dm.get('other', 0))
            CF_val = CF.get(waste_type, CF.get('other', 0))
            FCF_val = FCF.get(waste_type, FCF.get('other', 0))
            OF_val = OX / 100  # Convert percentage to fraction
            
            contribution = WF * dm_val * CF_val * FCF_val * OF_val
            total += contribution
        
        return m * total * (44/12)

    def other_emissions_Incineration(m, EF):
        """
        CH4 or N2O emissions from waste -  Incineration
        where:
        m: mass of waste incinerated (kg)
        EF: CH4 or N2O emission factor (kg CH4/kg waste) / (kg N2O/kg waste)
        """
        return m * EF

    # Germany -> western region EU
    waste_composition = {
        'food': 30.1, 
        'paper': 21.8, 
        'wood': 7.5,
        'textile': 4.7,
        'rubber': 1.4,
        'plastic': 6.2,
        'metal': 3.6,
        'glass': 10.0,
        'other': 14.6
        }

    dm = {
        'paper': 0.90,
        'textile': 0.80,
        'food': 0.40,
        'wood': 0.85,
        'garden': 0.40,
        'nappies': 0.40,
        'rubber': 0.84,
        'plastic': 1,
        'metal': 1,
        'glass': 1,
        'other': 0.90
        }

    CF = {
        'paper': 0.46,
        'textile': 0.50,
        'food': 0.38,
        'wood': 0.50,
        'garden': 0.49,
        'nappies': 0.70,
        'rubber': 0.67,
        'plastic': 0.75,
        'other': 0.03
        }

    FCF = {
        'paper': 0.1,
        'textile': 0.20,
        'garden': 0,
        'nappies': 0.10,
        'rubber': 0.20,
        'plastic': 1,
        'other': 1
    }

    OX = 100

    # Continuos incineration by default for EU
    # original value from IPCC 2006 
    # # ch4 = 0.2 units: kg/Gg waste wet weight
    # # n2o = 50 units: g/tonnes waste wet weight
    ef_ch4_incineration = 0.2*10**-6	# units: kg/kg waste wet weight
    ef_n2o_incineration = 50	        # units: kg/kg waste wet weight

    gdf_III_co2 = data[data['management'] == 'Incineration'].copy()
    gdf_III_co2['emissions_value'] = gdf_III_co2.apply(
        lambda row: CO2_emissions_Incineration(row['total_waste'], waste_composition, dm, CF, FCF, OX), axis=1
    )
    gdf_III_co2['gas_name'] = 'CO2'
    gdf_III_co2['emissions_units'] = 'kg'

    gdf_III_ch4 = data[data['management'] == 'Incineration'].copy()
    gdf_III_ch4['emissions_value'] = gdf_III_ch4.apply(
        lambda row: other_emissions_Incineration(row['total_waste'], ef_ch4_incineration), axis=1
    )
    gdf_III_ch4['gas_name'] = 'CH4'
    gdf_III_ch4['emissions_units'] = 'kg'
    gdf_III_ch4['emissionfactor_value'] = ef_ch4_incineration

    gdf_III_n2o = data[data['management'] == 'Incineration'].copy()
    gdf_III_n2o['emissions_value'] = gdf_III_n2o.apply(
        lambda row: other_emissions_Incineration(row['total_waste'], ef_ch4_incineration), axis=1
    )
    gdf_III_n2o['gas_name'] = 'N2O'
    gdf_III_n2o['emissions_units'] = 'kg'
    gdf_III_n2o['emissionfactor_value'] = ef_n2o_incineration

    # Combine into one dataframe
    gdf_III = pd.concat([gdf_III_co2, gdf_III_ch4, gdf_III_n2o], ignore_index=True)

    gdf_III['gpc_reference_number'] = None  # Initialize column

    gdf_III.loc[gdf_III['scope'] == 1, 'gpc_reference_number'] = 'III.3.1'
    gdf_III.loc[gdf_III['scope'] == 3, 'gpc_reference_number'] = 'III.3.3'

    # methodology id assignation
    gdf_III.loc[gdf_III['scope'] == 1, 'methodology_name'] = 'incineration-waste-inboundary-methodology'
    gdf_III.loc[gdf_III['scope'] == 3, 'methodology_name'] = 'incineration-waste-outboundary-methodology'

    # activity data
    gdf_III['activity_name'] = 'total-mass-of-waste-incinerated-or-burned'
    gdf_III['activity_units'] = 'kg'

    return gdf_III


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
