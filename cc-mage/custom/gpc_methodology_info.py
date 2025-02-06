if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd  

@custom
def transform_custom(*args, **kwargs):
    """
    Transform function to create a DataFrame from a dictionary.
    """
    dic_methodologies = {
        'MSW_I': {
            'gpc_refno': 'III.1.1',
            'methodology_name': 'methane-commitment-solid-waste-inboundary-methodology',
            'methodology_description': 'It estimates the total methane emissions generated from waste disposal sites based on the total organic content of waste deposited and its potential to produce methane over time. It assumes that all biodegradable waste deposited in a landfill will eventually generate methane, regardless of the timeframe.',
            'Scope': 1
        },
        'MSW_O': {
            'gpc_refno': 'III.1.2',
            'methodology_name': 'methane-commitment-solid-waste-outboundary-methodology',
            'methodology_description': 'It estimates the total methane emissions generated from waste disposal sites based on the total organic content of waste deposited and its potential to produce methane over time. It assumes that all biodegradable waste deposited in a landfill will eventually generate methane, regardless of the timeframe.',
            'Scope': 3
        },
        'BIO_I': {
            'gpc_refno': 'III.2.1',
            'methodology_name': 'biological-treatment-inboundary-methodology',
            'methodology_description': 'It estimates emissions from the aerobic or anaerobic decomposition of organic waste during processes such as composting and anaerobic digestion. Emissions primarily include methane (CH₄) and nitrous oxide (N₂O), depending on the treatment conditions and waste composition.',
            'Scope': 1
        },
        'BIO_O': {
            'gpc_refno': 'III.2.2',
            'methodology_name': 'biological-treatment-outboundary-methodology',
            'methodology_description': 'It estimates emissions from the aerobic or anaerobic decomposition of organic waste during processes such as composting and anaerobic digestion. Emissions primarily include methane (CH₄) and nitrous oxide (N₂O), depending on the treatment conditions and waste composition.',
            'Scope': 3
        },
        'INC_I': {
            'gpc_refno': 'III.3.1',
            'methodology_name': 'incineration-waste-inboundary-methodology',
            'methodology_description': 'It estimates emissions from the combustion of waste materials in controlled facilities or through open burning. Emissions primarily include carbon dioxide (CO₂), methane (CH₄), and nitrous oxide (N₂O), depending on the composition of the waste and combustion efficiency.',
            'Scope': 1
        },
        'INC_O': {
            'gpc_refno': 'III.3.2',
            'methodology_name': 'incineration-waste-outboundary-methodology',
            'methodology_description': 'It estimates emissions from the combustion of waste materials in controlled facilities or through open burning. Emissions primarily include carbon dioxide (CO₂), methane (CH₄), and nitrous oxide (N₂O), depending on the composition of the waste and combustion efficiency.',
            'Scope': 3
        },
        'WW_I': {
            'gpc_refno': 'III.4.1',
            'methodology_name': 'wastewater-inside-methodology',
            'methodology_description': 'It estimates emissions from the treatment and discharge of domestic and industrial wastewater. Emissions primarily include methane (CH₄) from anaerobic decomposition and nitrous oxide (N₂O) from nitrogen compounds during treatment processes.',
            'Scope': 1
        },
        'WW_O': {
            'gpc_refno': 'III.4.2',
            'methodology_name': 'wastewater-outside-methodology',
            'methodology_description': 'It estimates emissions from the treatment and discharge of domestic and industrial wastewater. Emissions primarily include methane (CH₄) from anaerobic decomposition and nitrous oxide (N₂O) from nitrogen compounds during treatment processes.',
            'Scope': 3
        },
    
    }

    # Convert dictionary to DataFrame
    data = pd.DataFrame.from_dict(dic_methodologies, orient='index').reset_index()
    data.rename(columns={'index': 'methodology_key'}, inplace=True)

    return data

@test
def test_output(output, *args) -> None:
    """
    Test the output of the custom transform function.
    """
    assert output is not None, 'The output is undefined'
    assert not output.empty, 'The output DataFrame is empty'
    assert 'gpc_refno' in output.columns, 'Missing column: gpc_refno'
    assert 'methodology_name' in output.columns, 'Missing column: methodology_name'