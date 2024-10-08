import sys
import re
import subprocess
import pandas as pd
from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_coding_agent


def delete_cols_agent_initial_script(
    state: AgentState,
) -> dict:
    print("\nDELETE COLUMNS AGENT INITIAL SCRIPT\n")

    # Load the previously created formatted csv file into a pandas dataframe
    input_path_csv = "./generated/initial_script/formatted_initially.csv"
    input_path_script = "./generated/initial_script/generated_script_initially.py"

    # Load the dataframe and the script
    df = pd.read_csv(input_path_csv)
    with open(input_path_script, "r") as file:
        script = file.read()

    # Define the output paths
    output_path_csv = "./generated/initial_script/formatted_deleted_columns.csv"
    output_path_script = (
        "./generated/initial_script/generated_script_deleted_columns.py"
    )

    # Create the prompt
    task = """
Your task is to inspect the dataframe 'df' and to delete all unnecessary columns based on the provided information below. You will also create a runnable python script.
Your inputs are the dataframe 'df' and information about which columns are necessary and cannot be deleted (positive list). Also you are provided with user provided context about the datafile. You find this information below under <additional_information> tags.
"""

    completion_steps = f"""
a. Inspect the pandas dataframe 'df'.
b. Inspect the positive list of columns that cannot be deleted provided under <positive_list> tags.
c. Based on the positive list and the provided dataframe 'df', output a list of columns that are not necessary and can be deleted.
d. Inspect the provided python script under <prior_script> tags.
e. Create a python script based on the script provided within <prior_script> tags. This python script must contain the following:
    1. the original code of the prior script provided in the <prior_script> tags. You make your changes to this script. 
    2. delete all columns from the dataframe 'df_new' that are not necessary based on your analysis of the positive list provided under <positive_list> tags. If you are in doubt about a certain column, do not delete it.
    3. finally replace the existing name for exporting the new .csv file to {output_path_csv} containing the new dataframe 'df_new' with the changes made above. The new csv file must be comma seperated ','. 
    4. IMORTANT: 
        - The code must contain python comments.
        - The code must be executable and must not contain any code errors.
        - The new script must contain all the content of the initial script in addition to the added data.
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
    <user_context>
        This is the user provided context about the datafile: {state.get("user_context")}.
    </user_context>
    <positive_list>
        This is the positive list of columns with descriptions. Use this to define which columns are not necessary and can be deleted: {state.get("positive_list")}.
    </positive_list>
    <prior_script>
        This is the prior script provided: {script}.
    </prior_script>
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

    return {"code_initial_script": response.get("output")}
