import sys
import re
import subprocess
import pandas as pd
from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_coding_agent


def setup_agent_initial_script(
    state: AgentState,
) -> dict:
    print("\nSETUP AGENT INITIAL SCRIPT\n")

    # Get the input path for the CSV file passed from the user
    input_path_csv = state.get("file_path")

    # Load the input CSV file into a pandas dataframe
    df = pd.read_csv(input_path_csv)

    # Define the output paths for the generated files
    output_path_csv = "./generated/initial_script/formatted_initially.csv"
    output_path_script = "./generated/initial_script/generated_script_initially.py"

    # Function to load the Python script content
    def load_script(script_path):
        with open(script_path, "r") as file:
            script_content = file.read()
        return script_content

    task = """
Your task is to reformat a python pandas dataframe. You will do reformating based on below instructions and create a runnable python script.
Your inputs are the original unformatted dataframe 'df'.
"""

    completion_steps = f"""
a. Inspect the pandas dataframe 'df'.
b. Create a python script. This python script must contain the following:
    1. code to load the .csv file into a pandas dataframe 'df' 
        - Use a correct encoding, so that special characters are displayed correctly based on the findings in <summary> tags. 
        - When loading the datafile, define the correct seperator being used e.g. ',' or ';' and so on.
        - The path to the .csv file is provided in the additional information below under <file_path> tags.
    2. a new dataframe 'df_new' that contains all the data of the original dataframe 'df' as a copy using 'df_new = df.copy(). Make all further manipulations on this new dataframe 'df_new'.
    3. normalized column names for 'df_new' where names are converted to 'lower case', strip them of any leading or trailing white spaces and replace any white spaces with underscores '_'.
    4. add code to output a new .csv file {output_path_csv} containing the new dataframe 'df_new' with the changes made above. The new csv file must be comma seperated ','.
    6. IMORTANT: 
        - The code must contain python comments.
        - The code must be executable and must not contain any code errors.
        - The final dataframe 'df_new' must contain all the data rows of the original dataframe 'df'.
"""

    answer_format = """
- Give all your detailed reasoning inside the <reasoning> tags.
- Provide the created python code inside the <code> tags.
    <answer>
        <reasoning>
            [Your detailed reasoning for making the changes to the dataframe]
        </reasoning>
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
    agent = create_coding_agent(df, state.get("verbose"))

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)
    response_output = response.get("output")

    ### Code below for extracting the code from the agent's response and running it - creating the csv file ###
    # Function to extract the code from the agent's response
    def extract_code_from_response(response_output):
        code_match = re.search(r"<code>([\s\S]*?)</code>", response_output)
        if code_match:
            return code_match.group(1).strip()
        return None

    # Extract the Python code
    generated_code = extract_code_from_response(response_output)

    if generated_code:
        # Save the generated code to a Python file
        with open(output_path_script, "w") as script_file:
            script_file.write(generated_code)

        # Run the generated Python script
        try:
            result = subprocess.run([sys.executable, output_path_script], check=True)
            print("The generated script was executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the script: {e}")
    else:
        print("No Python code was found in the agent's response.")

    return {"code_initial_script": response_output}
