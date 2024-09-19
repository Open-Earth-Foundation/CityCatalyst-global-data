from state.agent_state import AgentState


def summary_agent(state: AgentState) -> dict:
    print("\nSUMMARY AGENT\n")

    prompt = f"""
Your task is to provide a detailed summary of the provided DataFrame 'df'.
Include information about its structure, data types, basic statistics, and any notable patterns or insights.
    
1. First give a general summary about the content of the data.

2. Then describe the format of the dataframe in detail. Pay special attention to the following points:
    - nuber of rows and columns
        * are the number of columns consistent throughout the rows? Or is there a mismatch?
    - column names
        * what are the column names?
        * is the same naming convention used?
        * are there spaces before or after the names that could lead to issues?
    - which columns contain dates? The name of the column could be an indicator but check also for values inside the rows
    - data types of each column
    - any missing values
    - additional potential formatting issues with the original file
        * especially if the file contains additional text information that is not part of the actual data but 
        data that is added manually on top of the actual rows e.g. meta data.
        * especially if the file contains additional text information that is not part of the actual data but
        data that is added below the actual rows e.g. footnotes.

Give thoughts about how to solve these issues based on your analysis.
        
### Additional information ###
<additional_information>
    <user_provided_context>
    This is the user provided context: {state.get('context_user_provided')}.
    </user_provided_context>
    <file_path>
    This is the path to the original data file: {state.get('file_path')}.
    </file_path>
</additional_information>
"""

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)
    return {"summary": response.get("output")}
