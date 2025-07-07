import pandas as pd
from typing import TypedDict, Annotated, Optional


# Define the state with required fields for initialization
class AgentState(TypedDict, total=False):
    df: Annotated[pd.DataFrame, "The pandas dataframe"]  # Added by agents
    full_path: Annotated[str, "The file path of the original data file"]
    datasource_name: Annotated[str, "The datasource name"]
    user_input: Annotated[str, "The user provided context"]
    feedback_hitl: Annotated[str, "Feedback from the user"]
    verbose: Annotated[bool, "Verbose mode"]
    hitl: Annotated[bool, "Human-in-the-loop flag"]
    run_dir: Annotated[str, "The run directory for this execution"]
