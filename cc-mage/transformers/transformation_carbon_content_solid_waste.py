if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from pandas import DataFrame
import pandas as pd

@transformer
def transform(data: DataFrame, *args, **kwargs):

    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    doc_parameter_value = {
        'cc_A': 0.15,
        'cc_C': 0.4, 
        'cc_D': 0.43, 
        'cc_E': 0.2, 
        'cc_H': 0.1,
        'cc_J': 0.1,
        'cc_K': 0.1,
        'cc_B': 0.2,
        'cc_L': 0.1, 
        'cc_F': 0.15,
        'cc_G': 0.1,
        'cc_I': 0.1
    }

    doc_parameter_code = {
        'cc_A':'carbon-content-food',
        'cc_B':'carbon-content-garden',
        'cc_C':'carbon-content-paper',
        'cc_D':'carbon-content-wood',
        'cc_E':'carbon-content-textiles',
        'cc_F':'carbon-content-industrial',
        'cc_G':'carbon-content-nappies',
        'cc_H':'carbon-content-leather',
        'cc_I':'carbon-content-other',
        'cc_J':'carbon-content-plastics',
        'cc_K':'carbon-content-metal',
        'cc_L':'carbon-content-glass'
    }

    doc_i = pd.DataFrame(list(doc_parameter_value.items()), columns=['parameter_code', 'value'])
    doc_i['parameter_name'] = doc_i['parameter_code'].map(doc_parameter_code)
    doc_i['methodology_name'] = 'methane-commitment-solid-waste-inboundary-methodology'
    doc_i['gpc_refno'] = 'III.1.1'
    doc_i_2 = doc_i.copy()
    doc_i_2['methodology_name'] = 'methane-commitment-solid-waste-outboundary-methodology'
    doc_i_2['gpc_refno'] = 'III.1.2'

    doc_i_final = pd.concat([doc_i, doc_i_2], ignore_index=True)
    doc_i_final['region'] = 'world'
    doc_i_final['actor_id'] = 'world'
    doc_i_final['formula_input_units'] = 'fraction'
    doc_i_final['year'] = ''
    doc_i_final['formula_name'] = 'methane-commitment'
    doc_i_final['gas'] = 'CH4'
    doc_i_final['publisher_name'] = 'IPCC'
    doc_i_final['datasource_name'] = 'IPCC'
    doc_i_final['dataset_name'] = 'IPCC Emission Factor Database (EFDB) [2006 IPCC Guidelines]'
    doc_i_final['publisher_url'] = 'https://www.ipcc.ch/'
    doc_i_final['dataset_url'] = 'https://www.ipcc-nggip.iges.or.jp/EFDB/main.php'
    doc_i_final['reference'] = 'IPCC 2006 Guidelines for National Greenhouse Gas Inventories, Volume 5: Waste Management and Treatment, Chapter 3: Solid Waste Disposal Sites'

    doc_i_final.rename(
        columns={
            'value': 'formula_input_value'
        },
        inplace=True
    )

    # joining dfs
    waste_comp_values_final = pd.concat([data, doc_i_final], ignore_index=True)

    return waste_comp_values_final


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
