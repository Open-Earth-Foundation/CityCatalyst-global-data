if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    # formulas
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

    # Default values
    protein = 33.58     # [kg protein / person / yr]
    Fnpr = 0.16        # [kg N / kg protein]
    F_non_con = 1.4    # for countries with garbage disposals
    F_ind_com = 1.25   # centralized systems

    # Calculate N effluent value
    data['N_effluent'] = data['total_resident_population'].apply(
        lambda P: N_effluent(P, protein, Fnpr, F_non_con, F_ind_com), axis=1
        )

    # emission factor
    data['emissionfactor_value'] = 0.005
    data['emissionfactor_units'] = 'kg N2O-N / kg N'

    # N2O emissions value calculation
    data['emissions_value_tmp'] = data['N_effluent'] * (data['emissionfactor_value'] * 44/28)

    # assign the gas name and emission factor units
    data['gas_name'] = 'N2O'

    # create a column to store the metadata
    data["metadata"] = data.apply(
        lambda row: {
            "activity_subcategory_type1": 'treatment_type',
            "activity_subcategory_typename1": 'all',
            "activity_subcategory_type2": 'N_effluent',
            "activity_subcategory_typename2": row['N_effluent'],
        },
        axis=1,
    )

    data.drop(columns=['N_effluent', 'service_type', 'number_municipalities'], inplace=True)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
