if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    # DOC generic values for EU - wet waste
    DOCi = {
        'paper': 0.4,
        'textile': 0.24,
        'food': 0.15,
        'wood': 0.43,
        'garden': 0.20,
        'nappies': 0.24,
        'rubber': 0.39,
    }

    # DOC value
    DOC = sum(DOCi.values())

    # DOCf - Fraction of DOC that is ultimately degraded
    DOCf = 0.6

    # Fraction of methane in landfill gas
    F = 0.5

    # Assuming waste is disposed in managed anaerobic landfills
    MCF = 1.0

    # frec - Fraction of methane recovered at the landfill
    frec = 0

    # OX - Oxidation factor
    OX = 0.1

    def Lo(DOC, DOCf, F, MCF):
        """
        Methane generation potential, L0
        """
        return MCF* DOC * DOCf * F * 16/12

    def CH4_emissions_MC(MSWx, Lo, frec, OX):
        """
        CH4 emissions from waste -  Methane commitment
        where:
        MSWx: waste generated (kg)
        Lo: methane generation potential (kg CH4/kg waste)
        frec: methane recovery efficiency (0-1)
        OX: oxidation factor (0-1)
        """
        return MSWx * Lo * (1-frec) * (1-OX)

    # Calculate Lo once (it's a constant)
    lo = Lo(DOC, DOCf, F, MCF)

    gdf_I = data
    gdf_I = gdf_I[gdf_I['management'] == 'Landfill']

    # Apply CH4 calculation only to Landfill rows
    gdf_I['emissions_value'] = gdf_I.apply(
        lambda row: CH4_emissions_MC(row['total_waste'], lo, frec, OX), axis=1
    )
    gdf_I['gas_name'] = 'CH4'
    gdf_I['emissions_units'] = 'kg'
    gdf_I['lo'] = lo

    gdf_I['gpc_reference_number'] = None  # Initialize column

    # scope assignation
    gdf_I.loc[gdf_I['scope'] == 1, 'gpc_reference_number'] = 'III.1.1'
    gdf_I.loc[gdf_I['scope'] == 3, 'gpc_reference_number'] = 'III.1.2'

    # methodology id assignation
    gdf_I.loc[gdf_I['scope'] == 1, 'methodology_name'] = 'methane-commitment-solid-waste-inboundary-methodology'
    gdf_I.loc[gdf_I['scope'] == 3, 'methodology_name'] = 'methane-commitment-solid-waste-outboundary-methodology'

    # activity data
    gdf_I['activity_name'] = 'solid-waste-disposal'
    gdf_I['activity_units'] = 'kg'

    return gdf_I


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
