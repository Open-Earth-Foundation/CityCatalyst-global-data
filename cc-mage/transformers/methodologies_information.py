if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from pandas import DataFrame

@transformer
def transform(data, *args, **kwargs):

    # To fill the columns
    dic_methodologies = {
        'MSW_I': {
            'gpc_refno': 'III.1.1',
            'methodology_name': 'methane-commitment-solid-waste-inboundary-methodology',
            'methodology_description': '',
            'scope': 1
        },
        'MSW_O': {
            'gpc_refno': 'III.1.2',
            'methodology_name': 'methane-commitment-solid-waste-outboundary-methodology',
            'methodology_description': '',
            'scope': 3
        },
        'BIO_I': {
            'gpc_refno': 'III.2.1',
            'methodology_name': 'biological-treatment-inboundary-methodology',
            'methodology_description': '',
            'scope': 1
        },
        'BIO_O': {
            'gpc_refno': 'III.2.2',
            'methodology_name': 'biological-treatment-outboundary-methodology',
            'methodology_description': '',
            'scope': 3
        },
        'INC_I': {
            'gpc_refno': 'III.3.1',
            'methodology_name': 'incineration-waste-inboundary-methodology',
            'methodology_description': '',
            'scope': 1
        },
        'INC_O': {
            'gpc_refno': 'III.3.2',
            'methodology_name': '',
            'methodology_description': 'incineration-waste-outboundary-methodology',
            'scope': 3
        },
        'WW_I': {
            'gpc_refno': 'III.4.1',
            'methodology_name': 'wastewater-inside-methodology',
            'methodology_description': '',
            'scope': 1
        },
        'WW_O': {
            'gpc_refno': 'III.4.2',
            'methodology_name': 'wastewater-outside-methodology',
            'methodology_description': '',
            'scope': 3
        }
    }

    data = pd.DataFrame(dic_methodologies)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
