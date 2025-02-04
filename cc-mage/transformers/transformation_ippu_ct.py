if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
from pandas import DataFrame

@transformer
def transform(data: DataFrame, *args, **kwargs):
    """
    """
    # activity-subcategory diccionary
    act_subcat = {
        'chemicals': {
            'activity_name': 'chemicals-production',
            'industrial-processes-industry-type': 'industry-type-chemical-industry',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-chemical-industry',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-type-chemical-industry'
        }, 
        'other-chemicals': {
            'activity_name': 'chemicals-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-chemical-industry',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-type-chemical-industry'
        }, 
        'petrochemical-steam-cracking': {
            'activity_name': 'petrochemicals-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-chemical-industry',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-name-petrochemicals-production'
        }, 
        'other-metals': {
            'activity_name': 'other-metals-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-metal-industry',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-name-other-industries'
        },    
        'aluminum': {
            'activity_name': 'aluminium-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-metal-industry',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-name-aluminium-production'
        },
        'lime': {
            'activity_name': 'lime-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-mineral-industry',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-names-lime'
        },
        'glass': {
            'activity_name': 'glass-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-mineral-industry',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-names-glass'
        },
        'iron-and-steel': {
            'activity_name': 'iron-and-steel-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-metal-industry',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-name-iron-and-steel-production'
        }, 
        'cement': {
            'activity_name': 'cememt-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-mineral-industry',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-names-cement'
        }, 
        'textiles-leather-apparel': {
            'activity_name': 'textiles-and-leather-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-other-industries',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-name-textiles-and-leather'
        },
        'other-manufacturing': {
            'activity_name': 'other-manufacturing-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-other-industries',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-name-other-industries'
        }, 
        'pulp-and-paper': {
            'activity_name': 'pulp-and-paper-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-other-industries',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-name-pulp-and-paper'
        },
        'food-beverage-tobacco': {
            'activity_name': 'food-beverage-tobacco-production',
            'activity_subcategory_type1': 'industrial-processes-industry-type',
            'activity_subcategory_name1': 'industry-type-other-industries',
            'activity_subcategory_type2': 'industrial-processes-industry-name',
            'activity_subcategory_name2': 'industry-name-food-and-drink'
        }
    }

    # Loop through the dictionary to create columns
    # for industry, attributes in act_subcat.items():
    #     for column_name, value in attributes.items():
    #         data.loc[data['industry'] == industry, column_name] = value

    # Transformations using vectorized operations this was changed to improve the performance
    for industry, attributes in act_subcat.items():
        mask = data['industry'] == industry
        for column_name, value in attributes.items():
            data.loc[mask, column_name] = value

    # create the activity_subcategory_type column to store the subcategory information
    data["activity_subcategory_type"] = data.apply(
        lambda row: {
            row['activity_subcategory_type1'] : row['activity_subcategory_name1'],
            row['activity_subcategory_type2'] : row['activity_subcategory_name2'],
            "data-source": row['facility_name'],
            # "activity_subcategory_type1": row['activity_subcategory_type1'],
            # "activity_subcategory_typename1": row['activity_subcategory_name1'],
            # "activity_subcategory_type2": row['activity_subcategory_type2'],
            # "activity_subcategory_typename2": row['activity_subcategory_name2'],
        },
        axis=1,
    )

    data.drop(columns=['activity_subcategory_type1', 'activity_subcategory_name1', 'activity_subcategory_type2', 'activity_subcategory_name2'], inplace=True)

    # create the metadata column to store emission factor information
    data["metadata"] = data.apply(
        lambda row: {
            "capacity": row['capacity'],
            "capacity_units": row['capacity_units'],
            "capacity_factor": row['capacity_factor']
        },
        axis=1,
    )

    data.drop(columns=['capacity', 'capacity_units', 'capacity_factor'], inplace=True)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
