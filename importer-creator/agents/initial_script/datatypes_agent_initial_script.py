import sys
import subprocess
import json
import pandas as pd
from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_coding_agent


def datatypes_agent_initial_script(state: AgentState):
    print("\nFIX DATATYPES AGENT INITIAL SCRIPT\n")

    # Load the previously created formatted csv file into a pandas dataframe
    input_path_csv = "./generated/initial_script/steps/formatted_deleted_columns.csv"
    input_path_script = (
        "./generated/initial_script/steps/generated_script_deleted_columns.py"
    )

    # Load the csv file into the dataframe
    df = pd.read_csv(input_path_csv, encoding="utf-8")
    # Load the script
    with open(input_path_script, "r", encoding="utf-8") as file:
        script = file.read()

    output_path_csv = "./generated/initial_script/steps/formatted_datatypes.csv"
    output_path_script = (
        "./generated/initial_script/steps/generated_script_datatypes.py"
    )
    output_path_markdown = (
        "./generated/initial_script/steps/generated_markdown_datatypes.md"
    )

    task = """
Your task is to inspect and correect the datatypes of columns of the provided DataFrame 'df'. You will also create a runnable python script.
Your inputs are the dataframe 'df' and the prior script provided below inside <prior_script> tags.
"""
    completion_steps = f"""
a. Inspect the csv file provided under this path: {input_path_csv}. You are provided with a pandas dataframe 'df' based on this csv file. Base your further analysis only on this dataframe. This is already an updated dataframe.
b. Inspect the datatypes of each column in the dataframe 'df' and output a list of suggested corrections. 
c. Inspect the columns in the dataframe 'df' that contain dates and temporal data. Check if those columns have the correct datatype for dates.
d. Inspect the provided python script under <prior_script> tags.
d. Create a python script based on the script provided within <prior_script> tags. This python script must contain the following:
    1. the original code of the prior script provided in the <prior_script> tags. You make your changes to this script.
    2. corrected datatypes for the columns in the dataframe 'df_new' based on your prior analysis.
    3. converted date columns to a valid datetime format based on the available data using 'pd.to_datetime' and based on your prior analysis.
        - pay attention to columns that might not be clearly labeled as 'date' or 'dates' or similar but that still contain dates and temporal data.
    4. finally replace the existing name for exporting the new .csv file to {output_path_csv} containing the new dataframe 'df_new' with the changes made above. The new csv file must be comma seperated ','. The file must use 'encoding="utf-8"'.
    5. IMORTANT: 
        - The code must contain python comments.
        - The code must be executable and must not contain any code errors.
        - The new script must contain all the content of the initial script in addition to the added data.
"""
    answer_format = """
Your output must be provided in JSON format. Provide all detailed reasoning and the pure executable Python code in the following JSON format:
{
    "reasoning": "Your detailed reasoning here...",
    "code": "Your pure executable Python code here..."
}
Ensure that the output is valid JSON and does not include any additional commentary or explanation. Do not surround the JSON ooutput with any code block markers or tags like ```json```.
"""
    additional_information = f"""
<additional_information>
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

    agent = create_coding_agent(df, state.get("verbose"))

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)
    response_output = response.get("output")

    ### Code below for extracting the code from the agent's response and running it - creating the csv file ###
    # Function to parse the JSON response from the agent
    def parse_agent_response(response_output):
        try:
            response_dict = json.loads(response_output)
            reasoning = response_dict.get("reasoning", "").strip()
            code = response_dict.get("code", "").strip()
            return {"reasoning": reasoning, "code": code}
        except json.JSONDecodeError as e:
            print(f"JSON decoding failed: {e}")
            sys.exit(1)
            # return {"reasoning": response_output.strip(), "code": None}

    # Parse the agent's response
    output = parse_agent_response(response_output)

    # Save the reasoning to a Markdown file
    if output.get("reasoning"):
        with open(output_path_markdown, "w", encoding="utf-8") as markdown_file:
            markdown_file.write(f"# Reasoning\n\n{output['reasoning']}")
    else:
        print("No reasoning was found in the agent's response.")
        sys.exit(1)

    if output.get("code"):
        # Save the generated code to a Python file
        with open(output_path_script, "w", encoding="utf-8") as script_file:
            script_file.write(output["code"])

        # Run the generated Python script
        try:
            result = subprocess.run([sys.executable, output_path_script], check=True)
            print("The generated script was executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the script: {e}")
            sys.exit(1)
    else:
        print("No Python code was found in the agent's response.")
        sys.exit(1)

    # return {"summary": response.get("output")}
