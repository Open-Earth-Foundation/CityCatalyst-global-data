import sys
import subprocess
import json
import pandas as pd
from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_coding_agent

# Placeholder for real import
context_activities = ""


def extract_activity_unit_agent_step_3(
    state: AgentState,
):
    print("\nEXTRACT ACTIVITY UNIT AGENT STEP 3\n")

    # Load the output files of initial script
    input_path_csv = "./generated/step_3/steps/extracted_activity_value.csv"
    input_path_script = (
        "./generated/step_3/steps/generated_script_extracted_activity_value.py"
    )

    # Load the csv file into the dataframe
    df = pd.read_csv(input_path_csv, encoding="utf-8")
    # Load the script
    with open(input_path_script, "r", encoding="utf-8") as file:
        script = file.read()

    # Define the output paths
    output_path_csv = "./generated/step_3/steps/extracted_activity_unit.csv"
    output_path_script = (
        "./generated/step_3/steps/generated_script_extracted_activity_unit.py"
    )
    output_path_markdown = (
        "./generated/step_3/steps/generated_markdown_extracted_activity_unit.md"
    )

    task = """
Your task is to extract the Greenhouse Gas protocoll for cities (GPC) 'activity unit' from the provided python pandas dataframe based on the instructions below. You will also create a runnable python script.
Your inputs are the dataframe 'df', the prior script provided below inside <prior_script> tags, the user provided context in <user_context> tags and additional context for identidying activities in <context_activities> tags. 
"""

    completion_steps = f"""
a. Inspect the csv file provided under this path: {input_path_csv}. You are provided with a pandas dataframe 'df' based on this csv file. Base your further analysis only on this dataframe. This is already an updated dataframe.
b. Inspect the user provided context in <user_context> tags.
c. Inspect the additional context for identifying the GPC activities in <context_activities> tags.
d. Inspect the provided python script under <prior_script> tags.
e. Determine the GPC 'activity unit' based on the content of the dataframe 'df', the user provided context in <user_context> tags and the additional context provided within <context_activities> tags. Each row in the dataframe 'df' should be assigned a GPC 'activity unit' based on the provided context. To do this you need to inspect the dataframe 'df' row by row and assign each row a GPC 'activity unit' based on the information provided in this row.
f. Create a python script based on the script provided within <prior_script> tags. This python script must contain the following:
    1. the original code of the prior script provided in the <prior_script> tags. You make your changes to this script. 
    2. add a column 'activity_value' to the dataframe 'df_new' with the extracted GPC 'activity_value' based on your prior analysis.
    3. finally replace the existing name for exporting the new .csv file to {output_path_csv} containing the new dataframe 'df_new' with the changes made above. The new csv file must be comma seperated ','. The file must use 'encoding="utf-8"'.
    4. IMORTANT: 
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
    <user_context>
    This is the user context provided: {state.get("user_context")}. Give this information high priority in your considerations.
    </user_context>
    <context_activities>
    This is the additional context provided for identifying the activities: {context_activities}.
    </context_activities>
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

    # Parse the agent's response
    output = parse_agent_response(response_output)

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
        try:
            result = subprocess.run([sys.executable, output_path_script], check=True)
            print("The generated script was executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing the script: {e}")
            sys.exit(1)
    else:
        print("No Python code was found in the agent's response.")
        sys.exit(1)
