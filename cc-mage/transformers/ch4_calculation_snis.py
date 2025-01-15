if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

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

    def CH4_emissions(income_group_dic, EF_dic, df, TOW_column, S, R):
        """
        Calculate the formula for each row in a DataFrame where TOW is a column.

        Formula:
        (summatory(i,j)(Ui * Ti,j * EFj)) * (TOW - S) - R

        Parameters:
        income_group_dic (dict): Nested dictionary containing U*T values as percentages.
        EF_dic (dict): Dictionary of EF_j values for each treatment type.
        df (pd.DataFrame): DataFrame containing TOW values.
        TOW_column (str): Name of the column in the DataFrame for TOW values.
        S (float): Scalar value S.
        R (float): Scalar value R.

        Returns:
        pd.Series: A Series with the calculated results for each row.
        """
        total_sum = 0

        # Calculate the summation part of the formula
        for data in income_group_dic.values():
            for treatment_type, UT_percent in data['U*T'].items():
                UT_fraction = UT_percent / 100  # Convert percentage to fraction
                EF_j = EF_dic.get(treatment_type, 0)  # Get EF value for treatment type
                total_sum += UT_fraction * EF_j

        df['emissionfactor_value'] = total_sum

        # Apply the formula for each row
        results = (df['emissionfactor_value'] * (df[TOW_column] - S)) - R
        return results

    income_group_dic = {
        'high': {
            'U*T': {
                'None': 0,
                'Sewer': 20,
                'Septic tank': 0,
                'Latrine': 5,
                'Other': 0
            }
        },
        'low': {
            'U*T': {
                'None': 11.8,
                'Sewer': 23.6,
                'Septic tank': 0,
                'Latrine': 23.6,
                'Other': 0
            }
        },
        'rural': {
            'U*T': {
                'None': 7,
                'Sewer': 2,
                'Septic tank': 0,
                'Latrine': 7,
                'Other': 0
            }
        }
    }

    EF_dic = {
        'None': 0.057,
        'Sewer': 0.0756,
        'Septic tank': 0,
        'Latrine': 0.15,
        'Other': 0
    }

    # Calculate TOW
    bod = 18.25
    i = 1.25
    data['TOW'] = data['total_resident_population'].apply(lambda P: TOW(P, bod, i))

    # Calculate CH4 emissions applying the function
    S = 0  
    R = 0
    TOW_column = 'TOW'

    # Calculate the results for each row in the DataFrame
    data['emissions_value_tmp'] = CH4_emissions(income_group_dic, EF_dic, data, TOW_column, S, R)

    # create a column to store the metadata
    data["activity_subcategory_type"] = data.apply(
        lambda row: {
            "activity_subcategory_type1": 'treatment_type',
            "activity_subcategory_typename1": 'all',
            "activity_subcategory_type2": 'TOW',
            "activity_subcategory_typename2": row['TOW']
        },
        axis=1,
    )

    # Deleting extra columns
    data.drop(columns=['TOW', 'service_type', 'number_municipalities'], inplace=True)

    # Assigning gas 
    data['gas_name'] = 'CH4'

    # Assigning emission factor units
    data['emissionfactor_units'] = 'kg / kg BOD'
    data['unit_denominator'] = 'kg BOD'

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'