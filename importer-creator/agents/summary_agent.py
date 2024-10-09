from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_agent


def summary_agent(state: AgentState) -> dict:
    print("\nSUMMARY AGENT\n")

    task = """
Your task is to provide a detailed summary of the provided DataFrame 'df'.
Include information about its structure, data types, basic statistics, and any notable patterns or insights.
"""
    completion_steps = """
a. Give a general summary about the content of the data. 
b. Then describe the format of the dataframe in detail. Give answer to the following points:
    - nuber of rows and columns
    - column names
        * what are the column names?
        * are there spaces before or after the names that could lead to issues?
        * are there any special characters in the column names that could lead to issues? If so, consider a proper encoding for reading the file into a pandas dataframe so that the special characters are read correctly.
    - which columns contain dates? The name of the column could be an indicator but check also for values inside the rows
    - data types of each column
    - any missing values
    - are there empty columns or unnecessary columns like double index columns that can be removed?
    - any other notable patterns or insights
c. Provide detailed suggestions for improvements based on your analysis.
"""
    answer_format = """
<answer>
    <summary>
    [The summary of the dataframe]
    </summary>
    <format>
    [The details to the format of the dataframe]
    </format>
    <suggestions>
    [Your suggestions for improvements]
    </suggestions>
</answer>
"""
    additional_information = f"""
<additional_information>
    <file_path>
    This is the path to the original data file: {state.get('file_path')}.
    </file_path>
    <user_provided_context>
    This is the user provided context: {state.get("context_user_provided")}
    </user_provided_context>
</additional_information>
"""

    prompt = create_prompt(
        task, completion_steps, answer_format, additional_information
    )

    agent = create_agent(state.get("df"), state.get("verbose"))

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)
    return {"summary": response.get("output")}
