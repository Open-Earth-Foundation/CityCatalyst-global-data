import sys
import subprocess
import json
import pandas as pd
from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_coding_agent
from utils.json_output_cleaner import clean_json_output
from utils.create_descriptive_stats_prompt import create_descriptive_stats_prompt


def setup_agent_initial_script(
    state: AgentState,
):
    """
    This agent is responsible for setting up the initial script for the data pipeline and is performing some preformatting tasks on the input data.

    Inputs:
        Original path to original csv file.
        The dataframe loaded from the original path.
        Output path for the generated files.
    """
    print("\nSETUP AGENT INITIAL SCRIPT\n")

    # Get the original path for the CSV file passed from the user
    original_path_csv = state.get("full_path")

    # Load the original CSV file into a pandas dataframe
    df_original = pd.read_csv(original_path_csv, encoding="utf-8")

    descriptive_statistics = create_descriptive_stats_prompt(df_original)

    # Define the output paths for the generated files
    output_path_csv = "./generated/initial_script/steps/1_initially.csv"
    output_path_script = "./generated/initial_script/steps/1_initially.py"
    output_path_markdown = "./generated/initial_script/steps/1_initially.md"

    task = """
Your task is to reformat a python pandas dataframe. You will do reformating based on below instructions and create a runnable python script.
Your inputs are:
- the path to the original .csv file provided by the user under <original_path> tags below.
- the original unformatted dataframe 'df_original' loaded from the original .csv file.
- the output path for the new .csv file under <output_path> tags below.
"""

    completion_steps = f"""
a. Inspect the .csv file provided under <original_path> tags below. This is the original unformatted data.
b. Inspect the provided original pandas dataframe 'df_original'.
c. Create a python script. This python script must contain the following:
    1. code to load the original .csv file provided under into a pandas dataframe 'df_original'. 
    - Use a correct encoding, so that potential special characters are displayed correctly. 
    - When loading the datafile, define the correct separator being used e.g. ',' or ';'.
    - Store the path of the orignal .csv file in a variable 'original_path'.
    - Use the following code snippet:
    ```python
    original_path = ...
    df_original = pd.read_csv(original_path, encoding=..., sep=...)
    ```
    2. a new dataframe 'df_new' that contains all the data of the original dataframe 'df_original'. Make all further manipulations on this new dataframe 'df_new'.
    - Use the following code snippet:
    ```python
    df_new = df_original.copy()
    ```
    3. normalized column names for 'df_new' where names are converted to 'lower case', strip them of any leading or trailing white spaces and replace any white spaces with underscores '_'.
    - **ATTENTION**: If after renaming the columns, 2 or more columns would end up having the same name, index them with suffixes '_a', '_b' and so on for every repeated name to make them unique. This can happen when there is e.g. the column 'EXAMPLE', 'Example' and 'example' in the original dataframe. This should result in 'example_a', 'example_b' and 'example_c' respectively in the new dataframe.
    - Use the following code snippet:
    ```python
    df_new.columns = df_new.columns.str.lower().str.strip().str.replace(' ', '_')

    cols = pd.Series(df_new.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + chr(i) for i in range(97, 97 + sum(cols == dup))]
    df_new.columns = cols
    ```
    4. normalized row entries for 'df_new' where all string entries are stripped of any leading or trailing white spaces.
    - Use the following code snippet ensuring only .map is used (not .applymap) as .applymap is deprecated since pandas version 2.1.0:
    ```python
    # pandas.DataFrame.applymap is deprecated since pandas version 2.1.0
    # The official pandas documentation recommends using .map instead of .applymap for elementwise operations on the entire dataframe
    df_new = df_new.map(lambda x: x.strip() if isinstance(x, str) else x)
    ```
    5. finally:
    - add code to output a new .csv file with the output path given below under <output_path> tags so that the new .csv file contains the new dataframe 'df_new' with the changes made above. The new .csv file must be comma separated ','. The .csv file must use 'encoding="utf-8"'.
    - store the path to the new .csv file in a variable 'output_path'.
    - Use the following code snippet:
    ```python
    output_path = ...
    df_new.to_csv(output_path, encoding='utf-8', sep=',', index=False)
    ```

    IMPORTANT: 
    - The code must contain python comments explaining the code.
    - The code must be executable and must not contain any code errors.
    - The new script must contain all the content of the initial script in addition to the added data.
    - **NEVER** replace the variable 'original_path' in the script. 
"""

    answer_format = """
Your output must be provided in JSON format. Provide all detailed reasoning in a structured and human readable way (e.g. using sub headers, bulletpoints and numbered lists) and the pure executable Python code in the following JSON format:
{
    "reasoning": "Your detailed reasoning here...",
    "code": "Your pure executable Python code here..."
}
Ensure that the output is valid JSON and does not include any additional commentary or explanation. Do not surround the JSON output with any code block markers or tags like ```json```.
"""

    additional_information = f"""
<additional_information>
<original_path>
This is the path to the original data file: {state.get("full_path")}.
</original_path>
<output_path>
The output path for the new .csv file is this: {output_path_csv}.
</output_path>
</additional_information>
"""

    prompt = create_prompt(
        task,
        completion_steps,
        answer_format,
        additional_information,
    )

    # Create agent
    agent = create_coding_agent(df_original, state.get("verbose"))

    # Invoke summary agent with custom prompt
    response = agent.invoke(descriptive_statistics + prompt)
    response_output = response.get("output")

    # Check and potentially clean the JSON output by removing ```json``` code block markers
    cleaned_response_output = clean_json_output(response_output)

    ### Code below for extracting the code from the agent's response and running it - creating the csv file ###
    # Function to parse the JSON response from the agent
    def parse_agent_response(response):
        try:
            response_dict = json.loads(response)
            reasoning = response_dict.get("reasoning", "").strip()
            code = response_dict.get("code", "").strip()
            return {"reasoning": reasoning, "code": code}
        except json.JSONDecodeError as e:
            print(f"JSON decoding failed: {e}")
            sys.exit(1)

    # Parse the agent's response
    output = parse_agent_response(cleaned_response_output)

    # Save the reasoning to a Markdown file
    if output.get("reasoning"):
        with open(output_path_markdown, "w", encoding="utf-8") as markdown_file:
            markdown_file.write(f"# Reasoning\n\n{output['reasoning']}")
    else:
        print("No reasoning was found in the agent's response.")
        sys.exit(1)

    # Save the generated code to a Python file
    if output.get("code"):

        print("Create the script...")
        with open(output_path_script, "w", encoding="utf-8") as script_file:
            script_file.write(output["code"])

        # Run the generated Python script
        print("Attempting to run the generated script...")
        try:
            result = subprocess.run([sys.executable, output_path_script], check=True)
            print("The generated script was executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the script: {e}")
            sys.exit(1)
    else:
        print("No Python code was found in the agent's response.")
        sys.exit(1)
