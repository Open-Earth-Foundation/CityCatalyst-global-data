if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from pandas import DataFrame
import pandas as pd

@transformer
def transform(data: DataFrame, data_2: DataFrame, *args, **kwargs):

    dic_waste_comp = {
        'food waste': 'waste-composition-food', 
        'paper and cardboard': 'waste-composition-paper', 
        'wood': 'waste-composition-wood', 
        'textiles': 'waste-composition-textiles', 
        'rubber and leather': 'waste-composition-leather',
        'plastics': 'waste-composition-plastics',
        'metal': 'waste-composition-metal',
        'glass (and pottery and china)': 'waste-composition-glass',
        'other': 'waste-composition-other'
    }

    dic_parameter_code = {
        'waste-composition-food': 'WCF_A',
        'waste-composition-garden': 'WCF_B',
        'waste-composition-paper': 'WCF_C', 
        'waste-composition-wood': 'WCF_D', 
        'waste-composition-textiles': 'WCF_E', 
        'waste-composition-industrial': 'WCF_F',
        'waste-composition-nappies': 'WCF_G',
        'waste-composition-leather': 'WCF_H',
        'waste-composition-other': 'WCF_I',
        'waste-composition-plastics': 'WCF_J',
        'waste-composition-metal': 'WCF_K',
        'waste-composition-glass': 'WCF_L'
    }

    #rename df
    ipcc_regions = data_2

    # drop extra columns
    # tecnologies, parameters, region, abatement/control technologies, other properties aren't needed because we're selecting default EFs
    df = data.drop(
        columns=[
            "IPCC 1996 Source/Sink Category",
            "Type of parameter",
            "IPCC Worksheet",
            "Source of data",
            "Data provider",
            "Parameters / Conditions",
            "Abatement / Control Technologies",
            "Other properties",
            "Technologies / Practices"
        ]
    )

    df = df[(df['Description'].str.contains("MSW composition data by percent", na=False)) & (df['IPCC 2006 Source/Sink Category'] == '4.A - Solid Waste Disposal')]  

    df = df.rename(
        columns={
            "Unit": "units",
            "IPCC 2006 Source/Sink Category": "ipcc_2006_category",
            "Gas": "gas",
            "Equation": "equation",
            "Technical Reference": "reference",
            "Region / Regional Conditions": "region"
            }
        )

    # replace name of gas with chemical formula
    df['gas'] = 'CH4'

    # Extracting the composition data
    df['pairs'] = df['Value'].str.split(', ')
    df = df.explode('pairs')
    df = df[df['pairs'].notna() & df['pairs'].str.contains(' = ')]
    df[['type', 'value']] = df['pairs'].str.split(' = ', expand=True)

    # Convert to numeric
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    # Delete extra columns
    df.drop(columns=["pairs"], inplace=True)

    # Normalize the values within each region
    sum_per_ef_id = df.groupby('EF ID')['value'].transform('sum')
    df['value'] = (df['value'] / sum_per_ef_id) * 100

    df['value'] = df['value'].round(0)

    df['parameter_name'] = df['type'].map(dic_waste_comp)

    df['parameter_code'] = df['parameter_name'].map(dic_parameter_code)

    df = df.merge(
        ipcc_regions[['country_name', 'country_code', 'preference']],
        left_on='region',
        right_on='country_name',
        how='left'
    )

    df.dropna(subset=['country_code'], inplace=True)

    # Drop duplicates by keeping the row with the lowest preference
    df = df.sort_values('preference').drop_duplicates(
        subset=['parameter_code', 'country_code'], keep='first'
    )

    df.drop(
        columns=[
            'EF ID',
            'ipcc_2006_category',
            'Description',
            'region',
            'Value',
            'equation',
            'type',
            'country_name',
            'preference',
            'units'
        ],
        inplace=True
    )

    df.rename(columns={'country_code': 'actor_id'}, inplace=True)

    # Filling missing values from IPCC
    # Set of all required parameter_codes
    required_codes = set(dic_parameter_code.values())

    new_rows = []

    for actor in df['actor_id'].unique():
        actor_df = df[df['actor_id'] == actor]
        base_row = actor_df.iloc[0]  # use first row as template for metadata
        existing_codes = set(actor_df['parameter_code'].dropna())
        missing_codes = required_codes - existing_codes

        for code in missing_codes:
            # Find the corresponding parameter_name from the dictionary
            parameter_name = next(k for k, v in dic_parameter_code.items() if v == code)
            
            new_row = base_row.copy()
            new_row['parameter_code'] = code
            new_row['parameter_name'] = parameter_name
            new_row['value'] = 0
            new_row['reference'] = 'filled missing value'
            new_rows.append(new_row)

    df_missing = pd.DataFrame(new_rows)

    df = pd.concat([df, df_missing], ignore_index=True)

    df = df.sort_values(by=['actor_id', 'parameter_code']).reset_index(drop=True)

    df['methodology_name'] = 'methane-commitment-solid-waste-inboundary-methodology'
    df['gpc_refno'] = 'III.1.1'
    df_2 = df.copy()
    df_2['methodology_name'] = 'methane-commitment-solid-waste-outboundary-methodology'
    df_2['gpc_refno'] = 'III.1.2'

    df_final = pd.concat([df, df_2], ignore_index=True)

    df_final['formula_input_units'] = 'percent'
    df_final['year'] = ''
    df_final['formula_name'] = 'methane-commitment'
    df_final['publisher_name'] = 'IPCC'
    df_final['datasource_name'] = 'IPCC'
    df_final['dataset_name'] = 'IPCC Emission Factor Database (EFDB) [2006 IPCC Guidelines]'
    df_final['publisher_url'] = 'https://www.ipcc.ch/'
    df_final['dataset_url'] = 'https://www.ipcc-nggip.iges.or.jp/EFDB/main.php'

    df_final.rename(
        columns={
            'value': 'formula_input_value'
        },
        inplace=True
    )

    return df_final

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
