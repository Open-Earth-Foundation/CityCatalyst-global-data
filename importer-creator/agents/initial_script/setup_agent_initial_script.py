import sys
import subprocess
import json
import pandas as pd
from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_coding_agent
from utils.json_output_cleaner import clean_json_output


def setup_agent_initial_script(
    state: AgentState,
):
    print("\nSETUP AGENT INITIAL SCRIPT\n")

    # Get the input path for the CSV file passed from the user
    input_path_csv = state.get("full_path")

    # Load the input CSV file into a pandas dataframe
    df = pd.read_csv(input_path_csv, encoding="utf-8")

    # Define the output paths for the generated files
    output_path_csv = "./generated/initial_script/steps/formatted_initially.csv"
    output_path_script = (
        "./generated/initial_script/steps/generated_script_initially.py"
    )
    output_path_markdown = (
        "./generated/initial_script/steps/generated_markdown_initially.md"
    )

    task = """
Your task is to reformat a python pandas dataframe. You will do reformating based on below instructions and create a runnable python script.
Your inputs are the original unformatted dataframe 'df'.
"""

    completion_steps = f"""
a. Inspect the pandas dataframe 'df'.
b. Create a python script. This python script must contain the following:
    1. code to load the original .csv file 'df = pd.read_csv' with the path provided under <file_path> tags below into a pandas dataframe 'df'. 
        - Use a correct encoding, so that special characters are displayed correctly based on the findings in <summary> tags. 
        - When loading the datafile, define the correct seperator being used e.g. ',' or ';' and so on.
        - The path to the .csv file is provided in the additional information below under <file_path> tags. Store the path in a variable 'input_path'.
    2. a new dataframe 'df_new' that contains all the data of the original dataframe 'df' as a copy using 'df_new = df.copy(). Make all further manipulations on this new dataframe 'df_new'.
    3. normalized column names for 'df_new' where names are converted to 'lower case', strip them of any leading or trailing white spaces and replace any white spaces with underscores '_'.
    4. finally:
        - add code to output a new .csv file 'df_new.to_csv' with {output_path_csv} so that the new .csv file contains the new dataframe 'df_new' with the changes made above. The new .csv file must be comma seperated ','. The .csv file must use 'encoding="utf-8"'.
        - store the path to the new .csv file in a variable 'output_path'.

    IMORTANT: 
        - The code must contain python comments.
        - The code must be executable and must not contain any code errors.
        - The new script must contain all the content of the initial script in addition to the added data.
        - **NEVER** replace the variable 'input_path' in the script. 
"""

    answer_format = """
Your output must be provided in JSON format. Provide all detailed reasoning in a structured and human readable way (e.g. using sub headers, bulletpoints and numbered lists) and the pure executable Python code in the following JSON format:
{
    "reasoning": "Your detailed reasoning here...",
    "code": "Your pure executable Python code here..."
}
Ensure that the output is valid JSON and does not include any additional commentary or explanation. Do not surround the JSON ooutput with any code block markers or tags like ```json```.
"""

    additional_information = f"""
<additional_information>
<file_path>
This is the path to the original data file: {state.get("full_path")}.
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
