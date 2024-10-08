from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_coding_agent


def code_generation_agent_initial_script(
    state: AgentState,
) -> dict:
    print("\nCODE GENERATION AGENT INITIAL SCRIPT\n")

    task = """
Your task is to create a runnable python script.
Your inputs are the original dataframe 'df' and a summary with information about the dataset, potential formatting issues and suggestions on how to fix it. The summary is given in <summary> tags below.
"""

    completion_steps = """
a. Inspect the information given below in <summary> tags
b. Create a python script. This python script must contain the following:
    1. code to load the .csv file into a pandas dataframe 'df' 
        - Use a correct encoding, so that special characters are displayed correctly based on the findings in <summary> tags. 
        - When loading the datafile, define the correct seperator being used e.g. ',' or ';' and so on.
        - The path to the .csv file is provided in the additional information under <file_path> tags.
    2. a new dataframe 'df_new' that contains all the data of the original dataframe 'df' as a copy using 'df_new = df.copy(). Make all further manipulations on this new dataframe 'df_new'.
    3. normalized column names for 'df_new' where names are converted to 'lower case', strip them of any leading or trailing white spaces and replace any white spaces with underscores '_'.
    4. converted date columns to a valid datetime format based on the available data using 'pd.to_datetime'.
        - pay attention to columns that might not be clearly labeled as 'date' or 'dates' or similar and refer to the provided summary in the <summary> tags.
    5. add code to output a new .csv file 'initially_formatted.csv' containing the new dataframe 'df_new' with the changes made above. The seperator must be comma seperated ','.
    6. IMORTANT: 
        - The code must contain python comments.
        - The code must be executable and must not contain any code errors.
        - The final dataframe 'df_new' must contain all the data rows of the original dataframe 'df'.
c. Execute the code to create the new .csv file 'initially_formatted.csv'. The full path for creating the new file is '.generated/initial_script/initially_formatted.csv'.
"""

    answer_format = """
- Give all your detailed reasoning inside the <reasoning> tags.
- Provide the created python code inside the <code> tags.
    <answer>
        <reasoning>
        [Your detailed reasoning for making the changes to the dataframe]
        <code>
        [Your generated python script]
        </code>
    </answer>
"""

    additional_information = f"""
<additional_information>
        <file_path>
        This is the path to the original data file: {state.get('file_path')}.
        </file_path>
        <summary>
        This is the summary of the dataframe: {state.get("summary")}.
        </summary>
        <feedback>
            <feedback_human-in-the-loop>
            If the user has provided feedback at the end of the entire data pipeline from the human-in-the-loop agent, you find it here: {state.get("feedback_hitl")}.
            This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.
            </feedback_human-in-the-loop>
        </feedback>
    </additional_information>
"""

    prompt = create_prompt(
        task, completion_steps, answer_format, additional_information
    )

    # Create agent
    agent = create_coding_agent(state.get("df"), state.get("verbose"))

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)

    return {"code_initial_script": response.get("output")}
