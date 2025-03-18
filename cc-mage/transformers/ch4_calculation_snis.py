import pandas as pd 

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # def CH4_emissions(income_group_dic, EF_dic, df, TOW_column, S, R):
    #     """
    #     Calculate the formula for each row in a DataFrame where TOW is a column.

    #     Formula:
    #     (summatory(i,j)(Ui * Ti,j * EFj)) * (TOW - S) - R

    #     Parameters:
    #     income_group_dic (dict): Nested dictionary containing U*T values as percentages.
    #     EF_dic (dict): Dictionary of EF_j values for each treatment type.
    #     df (pd.DataFrame): DataFrame containing TOW values.
    #     TOW_column (str): Name of the column in the DataFrame for TOW values.
    #     S (float): Scalar value S.
    #     R (float): Scalar value R.

    #     Returns:
    #     pd.Series: A Series with the calculated results for each row.
    #     """
    #     total_sum = 0

    #     # Calculate the summation part of the formula
    #     for data in income_group_dic.values():
    #         for treatment_type, UT_percent in data['U*T'].items():
    #             UT_fraction = UT_percent / 100  # Convert percentage to fraction
    #             EF_j = EF_dic.get(treatment_type, 0)  # Get EF value for treatment type
    #             total_sum += UT_fraction * EF_j

    #     df['emissionfactor_value'] = total_sum

    #     # Apply the formula for each row
    #     results = (df['emissionfactor_value'] * (df[TOW_column] - S)) - R
    #     return results

    # Constants
    bod = 18.25
    i = 1.25
    S = 0  
    R = 0
    TOW_column = 'TOW'

    # Functions
    def TOW(P, BOD, I):
        """
        Units required:
        - P: cap
        - BOD: kg BOD / cap / yr
        - I: unitless

        example: TOW(520600, 18.25, 1.25)
        """
        return P*BOD*I

    data[TOW_column] = data['total_resident_population'].apply(lambda P: TOW(P, bod, i))

    # Create DataFrame for income groups and their U*T values
    income_groups_data = {
        'income-group-type-urban-high-income': {
            'treatment-name-none': 0,
            'treatment-name-sewer': 20,
            'treatment-name-septic-system': 0,
            'treatment-name-latrine': 5,
            'treatment-name-other': 0
        },
        'income-group-type-urban-low-income': {
            'treatment-name-none': 11.8,
            'treatment-name-sewer': 23.6,
            'treatment-name-septic-system': 0,
            'treatment-name-latrine': 23.6,
            'treatment-name-other': 0
        },
        'income-group-type-rural': {
            'treatment-name-none': 7,
            'treatment-name-sewer': 2,
            'treatment-name-septic-system': 0,
            'treatment-name-latrine': 7,
            'treatment-name-other': 0
        }
    }


    EF_dic = {
        'treatment-name-none': 0.057,
        'treatment-name-sewer': 0.0756,
        'treatment-name-septic-system': 0,
        'treatment-name-latrine': 0.15,
        'treatment-name-other': 0
    }

    # Create a DataFrame from the income groups
    income_groups = []
    for income_group, treatments in income_groups_data.items():
        for treatment_type, UT_percent in treatments.items():
            income_groups.append({
                'income_group': income_group,
                'treatment_type': treatment_type,
                'UT_fraction': UT_percent / 100,  # Convert percentage to fraction
            })
    income_groups_df = pd.DataFrame(income_groups)

    ef_df = pd.DataFrame(list(EF_dic.items()), columns=['treatment_type', 'EF'])
    merged_df = income_groups_df.merge(ef_df, on='treatment_type', how='left')

    emissions_df = data.merge(merged_df, how='cross')

    emissions_df['emissions_value_tmp'] = (
        emissions_df['UT_fraction'] * emissions_df['EF'] * (emissions_df[TOW_column] - S) - R
    )

    emissions_df = emissions_df[emissions_df['emissions_value_tmp']>0]

    emissions_df['activity_value'] = emissions_df['total_resident_population'] * emissions_df['UT_fraction']

    # Add treatment status column based on conditions
    treated_status = {
        "treatment-name-septic-system": "treatment-status-type-wastewater-treated",
        "treatment-name-latrine": "treatment-status-type-wastewater-treated",
        "treatment-name-other": "treatment-status-type-wastewater-treated",
        "treatment-name-none": "treatment-status-type-wastewater-untreated",
        "treatment-name-sewer": "treatment-status-type-wastewater-untreated"
    }

    emissions_df['treatment_status'] = emissions_df['treatment_type'].map(treated_status)

    collection_status = {
        "treatment-name-septic-system": "collection-status-type-wastewater-collected",
        "treatment-name-latrine": "collection-status-type-wastewater-collected",
        "treatment-name-other": "collection-status-type-wastewater-collected",
        "treatment-name-none": "collection-status-type-wastewater-not-collected",
        "treatment-name-sewer": "collection-status-type-wastewater-collected"
    }

    emissions_df['collection_status'] = emissions_df['treatment_type'].map(collection_status)

    #create a column to store the metadata
    # emissions_df["activity_subcategory_type"] = emissions_df.apply(
    #     lambda row: {
    #         "wastewater-inside-domestic-calculator-income-group": row['income_group'],
    #         "wastewater-inside-domestic-calculator-treatment-name": row['treatment_type'],
    #         "wastewater-inside-domestic-calculator-treatment-status": row['treatment_status'],
    #         "wastewater-inside-domestic-calculator-collection-status": row['collection_status'],
    #         #"total-organic-sludge-removed": S,
    #         #"activity_subcategory_typename2": row['TOW']
    #     },
    #     axis=1,
    # )

    # Deleting extra columns
    emissions_df.drop(columns=['TOW', 'service_type', 'number_municipalities'], inplace=True)

    # Assigning gas 
    emissions_df['gas_name'] = 'CH4'

    # Assigning emission factor units
    emissions_df['emissionfactor_units'] = 'kg / kg BOD'
    emissions_df['unit_denominator'] = 'kg BOD'

    return emissions_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'