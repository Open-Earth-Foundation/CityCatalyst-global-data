import sys
import subprocess
import json
import pandas as pd
from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_coding_agent
from context.mappings.mappings_sector import sector_mapping
from utils.json_output_cleaner import clean_json_output


def extract_sector_agent_step_2(
    state: AgentState,
):
    print("\nEXTRACT SECTOR AGENT STEP 2\n")

    # Load the output files of initial script
    input_path_csv = "./generated/step_2/steps/extracted_region.csv"
    input_path_script = "./generated/step_2/steps/generated_script_extracted_region.py"

    # Load the csv file into the dataframe
    df = pd.read_csv(input_path_csv, encoding="utf-8")
    # Load the script
    with open(input_path_script, "r", encoding="utf-8") as file:
        script = file.read()

    # Define the output paths
    output_path_csv = "./generated/step_2/steps/extracted_sector.csv"
    output_path_script = "./generated/step_2/steps/generated_script_extracted_sector.py"
    output_path_markdown = (
        "./generated/step_2/steps/generated_markdown_extracted_sector.md"
    )

    task = """
Your task is to extract the Global Protocol for Community-Scale Greenhouse Gas Emission Inventories (GPC) sector from the provided python pandas dataframe based on instructions below. You will also create a runnable python script.
Your inputs are the dataframe 'df', the prior script provided below inside <prior_script> tags, the user provided context in <user_context> tags and additional context for identidying the GPC sector in <context_sector> tags.
"""

    completion_steps = f"""
a. Inspect the csv file provided under this path: {input_path_csv}. You are provided with a pandas dataframe 'df' based on this csv file. Base your further analysis only on this dataframe. This is already an updated dataframe based on the python script under <prior_script> tags.
    - NEVER load the csv file provided in the script under <prior_script> tags from the line 'df = pd.read_csv'. You will work with the updated dataframe 'df' provided under this path: {input_path_csv}.
b. Inspect the user provided context in <user_context> tags.
c. Inspect the additional context for identifying the GPC sector in <context_sector> tags.
d. Inspect the provided python script under <prior_script> tags.
e. Determine the GPC sector based on the content of the dataframe 'df', the user provided context in <user_context> tags and the additional context provided within <context_sector> tags. Each row in the dataframe 'df' should be assigned a GPC sector based on the provided context. To do this you need to work row by row and assign each row a GPC sector based on the information provided in this row.
f. Create a python script based on the script provided within <prior_script> tags. This python script must contain the following:
    1. the original code of the prior script provided in the <prior_script> tags. You make your changes to this script. 
    2. a mapping dictionary for the GPC sector based on your prior analysis. 
    3. add a column 'sector_name' to the dataframe 'df_new' which applies a GPC sector to each row of the 'df' based on the created mapping dictionary.
    4. finally:
    - replace the output path for exporting the new .csv file 'df_new.to_csv' with {output_path_csv} so that the new .csv file contains the new dataframe 'df_new' with the changes made above. The new .csv file must be comma seperated ','. The .csv file must use 'encoding="utf-8"'.
    - NEVER replace the input path for loading the original .csv file 'df = pd.read_csv'.
    5. IMORTANT: 
    - The code must contain python comments.
    - The code must be executable and must not contain any code errors.
    - The new script must contain all the content of the initial script in addition to the added data.
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
<user_context>
This is the user context provided: {state.get("context_user_provided")}. Give this information high priority in your considerations.
</user_context>
<context_sector>
This is the additional context provided for identifying the sector: {json.dumps(sector_mapping, indent=4)}
</context_sector>
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
