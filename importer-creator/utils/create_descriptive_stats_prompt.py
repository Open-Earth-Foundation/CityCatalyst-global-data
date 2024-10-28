import pandas as pd
import json
import io


def create_descriptive_stats_prompt(df: pd.DataFrame) -> str:

    buffer = io.StringIO()
    df.info(buf=buffer)
    df_info = buffer.getvalue()

    # Get 10 sample rows of the dataframe
    df_sample_rows = df.sample(n=10).to_json(orient="records", indent=4)

    # Get the unique values per column
    df_unique_values = {
        col: df[col].unique().tolist()
        for col in df.columns
        if df[col].dtype == "object"
    }

    #     The following are 10 sample rows of the dataframe. Use it to get a more detailed understanding of the content of the dataset. This is just sample data. Do not use it to make assumptions on the entire dataset:
    # {df_sample_rows}

    prompt = f"""
The following is are the data types and null value counts for each column. Use it for understanding the general structure of the dataset:
{df_info}

The following are the unique values per column containing 'object' data types (text, strings). Use it to understand the different values per column and to make sure to always include all unique values in your answers:
{json.dumps(df_unique_values, indent=4)}
"""
    return prompt
