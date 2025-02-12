import pandas as pd 
import duckdb

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    # Formula
    def N_effluent(population, protein, Fnpr, F_non_con, F_ind_com):
        """
        Total annual amount of nitrogen in the wastewater effluent, kg N/yr 
        Source: IPCC 2006
        units requered:
            - population: [person]
            - protein: [kg protein / person / yr]
            - Fnpr: [kg N / kg protein]
            - F_non_con: unitless
            - F_ind_com: unitless
        """
        return population*protein*Fnpr*F_non_con*F_ind_com

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

    emissions_df = data.merge(income_groups_df, how='cross')

    # Default values
    protein = 33.58     # [kg protein / person / yr]
    Fnpr = 0.16        # [kg N / kg protein]
    F_non_con = 1.4    # for countries with garbage disposals
    F_ind_com = 1.25   # centralized systems

    # Calculate CH4 emissions
    emissions_df['N_effluent'] = emissions_df.apply(
        lambda row: N_effluent(row['total_resident_population'], protein, Fnpr, F_non_con, F_ind_com), axis=1
    )

    emissions_df['emissionfactor_value'] = 0.005
    emissions_df['emissionfactor_units'] = 'kg N2O-N / kg N'
    emissions_df['unit_denominator'] = 'kg N'

    # emissions value calculation
    emissions_df['emissions_value_tmp'] = emissions_df['N_effluent'] * (emissions_df['emissionfactor_value'] * 44/28) * emissions_df['UT_fraction']

    emissions_df = emissions_df[emissions_df['emissions_value_tmp']>0]
    
    emissions_df['activity_value'] = emissions_df['total_resident_population'] * emissions_df['UT_fraction']

    # assign the gas name and emission factor units
    emissions_df['gas_name'] = 'N2O'

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
        "treatment-name-sewer": "collection-status-type-wastewater-not-collected"
    }

    emissions_df['collection_status'] = emissions_df['treatment_type'].map(collection_status)

    # create a column to store the metadata
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

    emissions_df.drop(columns=['N_effluent', 'service_type', 'number_municipalities'], inplace=True)

    return emissions_df # data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
