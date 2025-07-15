if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import re
import statistics
import math
from pandas import DataFrame

@transformer
def transform(data: DataFrame, *args, **kwargs):
    """
    """

    # change gas name to gas formula
    def gas_name_to_formula(value, replace_dict=None):
        '''replace gas name with formula'''
        if replace_dict is None:
            replace_dict = {
                'CARBON DIOXIDE\n': 'CO2',
                'METHANE\n': 'CH4',
                'NITROUS OXIDE\n': 'N2O',
                'Sulphur Hexafluoride\n': 'SF6',
                'CARBON MONOXIDE\n': 'CO',
                'Nitrogen Trifluoride\n': 'NF3',
                'AMMONIA\n': 'NH3',
            }
        else:
            replace_dict = {key.upper(): value for key, value in replace_dict.items()}

        new_value = replace_dict.get(value.upper(), None)

        if new_value:
            return new_value

        return value

    # separete min, max and calculate the average value
    def separate_min_max_median(val):
        """Extract value, takes median if range is given."""
        if isinstance(val, float):
            return {"value": val, "value_min": None, "value_max": None}

        # Normalize spaces and remove extra characters
        value = re.sub(r"\s+", "", val.strip())

        # Patterns
        range_pattern = r"(?P<min>[\d.]+)-(?P<max>[\d.]+)"  # Standard range
        plus_minus_pattern = r"(?P<base>[\d.]+)\+/-\s*(?P<delta>[\d.]+)"  # ± notation
        single_pattern = r"^([\d.]+)(?:\(.*\))?$"  # Single number with optional text

        # Matching
        if match := re.search(range_pattern, value):
            min_val = float(match.group("min"))
            max_val = float(match.group("max"))
            median = statistics.median([min_val, max_val])
            return {"value": median, "value_min": min_val, "value_max": max_val}

        elif match := re.search(plus_minus_pattern, value):
            base = float(match.group("base"))
            delta = float(match.group("delta"))
            min_val = base - delta
            max_val = base + delta
            return {"value": base, "value_min": min_val, "value_max": max_val}

        elif match := re.match(single_pattern, value):
            return {
                "value": float(match.group(1)),
                "value_min": None,
                "value_max": None,
            }

        # Fallback if no pattern matched
        return {"value": None, "value_min": None, "value_max": None}

    # drop extra columns
    # tecnologies, parameters, region, abatement/control technologies, other properties aren't needed because we're selecting default EFs
    df = data.drop(
        columns=[
            "IPCC 1996 Source/Sink Category",
            "Fuel 1996",
            "Type of parameter",
            "IPCC Worksheet",
            "Source of data",
            "Data provider",
            "Technologies / Practices",
            "Parameters / Conditions",
            "Region / Regional Conditions",
            "Abatement / Control Technologies",
            "Other properties"
        ]
    )

    # clean up the df
    output_list = []

    for _, row in df.iterrows():
        # get min, max, and median value
        value = row.pop("Value")
        value_dic = separate_min_max_median(value)

        # rename rows and convert to dictionary
        row_dic = row.rename(
            {
                "Unit": "units",
                "IPCC 2006 Source/Sink Category": "ipcc_2006_category",
                "Gas": "gas",
                "Fuel 2006": "fuel",
                "Equation": "equation",
                "Technical Reference": "reference"
            }
        ).to_dict()

        # merge dictionaries
        dic_tmp = {**row_dic, **value_dic}

        # convert nan to None
        output_dic = {
            key: None if (isinstance(value, float)) and math.isnan(value) else value
            for key, value in dic_tmp.items()
        }

        # replace name of gas with chemical formula
        output_dic["gas"] = gas_name_to_formula(output_dic["gas"])

        # append to list
        output_list.append(output_dic)
        
    df = pd.DataFrame(output_list)

    # delete rows with NaN values
    df = df[~df['value'].isna()]

    # filter only for the interested gases
    gas = ["CO2", "CH4", "N2O"]
    df = df[df["gas"].isin(gas)]

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'