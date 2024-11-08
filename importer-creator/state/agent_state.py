import pandas as pd
from typing import TypedDict, Annotated


# Define the state
class AgentState(TypedDict):
    df: Annotated[pd.DataFrame, "The pandas dataframe"]
    full_path: Annotated[str, "The file path of the original data file"]
    datasource_name: Annotated[str, "The datasource name"]
    user_input: Annotated[str, "The user provided context"]
    feedback_hitl: Annotated[str, "Feedback from the user"]
    verbose: Annotated[bool, "Verbose mode"]
    hitl: Annotated[bool, "Human-in-the-loop flag"]
