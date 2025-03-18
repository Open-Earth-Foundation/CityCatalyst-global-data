import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # Diccionary with traslations
    treatment_types_translations = {
        'Unidade de triagem (galpão ou usina)': 'sorting unit',
        'Lixão': 'open dump',
        'Aterro controlado': 'controlled landfill',
        'Unidade de compostagem (pátio ou usina)': 'composting unit',
        'Aterro sanitário': 'controlled landfill',
        'Unidade de transbordo': 'transfer unit',
        'Unid. tratamento por microondas ou autoclave': 'autoclave treatment unit',
        'Área de transb e triagem de RCC e volumosos (=ATT)': 'sorting unit',
        'Área de reciclagem de RCC (=un reciclagem entulho)': 'waste recycling area',
        'Unidade de manejo de galhadas e podas': 'pruning management unit',
        'Aterro de Resíduos da Construção Civil (=inertes)': 'construction waste landfill',
        'Vala especifica de RSS': 'clinical waste trench',
        'Outra': 'other',
        'Unidade de tratamento por incineração': 'incineration',
        'Coprocessamento': 'other',
        'Área em recuperação': 'other'
    }

    # list with the correct columns names
    col_names = ['municipality_code', 'IBGE_code', 'municipality_where_the_Unit_is', 'UF', 'region_name', 'region_code', 'id_population', 'year', 
                'unit_code', 'unit_name', 'unit_type', 'municipality_sending', 'total_SW', 'dom_plus_pub', 'clinical', 'construction', 'pruning', 'others'] 

    # assign the correct columns names
    data.columns = col_names

    # drop the first 11 rows
    data = data[11:]

    # drop unnecessary columns
    data = data.drop(columns=['id_population', 'unit_code', 'unit_name', 'dom_plus_pub', 'clinical', 'construction', 'pruning', 'others'])

    # extraction of the name of the actor, which in this case is the municipality that is sending the waste to the unit (treatment side)
    data['actor_name'] = data['municipality_sending'].str.split('/').str[0]
    data['sending_region_code'] = data['municipality_sending'].str.split('/').str[1]

    # Check if the municipality where the unit is located is the same as the actor name and if the region codes match
    data['columns_match'] = (data['municipality_where_the_Unit_is'] == data['actor_name']) & (data['UF'] == data['sending_region_code'])


    # Ensure `total_SW` column is numeric
    data['total_SW'] = pd.to_numeric(data['total_SW'], errors='coerce').fillna(0)

    # apply the translation to the treatment type
    data['treatment_type'] = data['unit_type'].map(treatment_types_translations)
    
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'