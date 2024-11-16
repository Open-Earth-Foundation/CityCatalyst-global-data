import pandas as pd


def filter_data(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Filter the DataFrame based on given filters.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        filters (dict): A dictionary where keys are column names and values are the values to filter by.

    Returns:
        pd.DataFrame: A filtered DataFrame.
    """
    for column, value in filters.items():
        if column in df.columns:
            df = df[df[column] == value]
        else:
            print(f"Column '{column}' not found in DataFrame.")
    return df
