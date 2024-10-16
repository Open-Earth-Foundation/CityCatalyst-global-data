from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_coding_agent


def load_script(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        script = file.read()

    return script


def code_generation_agent_keyval(
    state: AgentState,
) -> dict:
    print("\nCODE GENERATION AGENT KEYVAL\n")

    # Path to initial script
    path = "./generated/initial_script/generated_initial_script.py"
    prior_script = load_script(path)

    task = """
Your task is to create a runnable python script.
Your inputs are the previously created python script 'initial_script.py' below inside <initial_script> tags as well as the extracted key-value data inside the <extracted_data_keyval> tags.
"""

    completion_steps = """
a. Inspect the extracted key-value data inside the <extracted_data_keyval> tags.
b. Inspect the provided python script inside the <initial_script> tags.
c. Create a python script. This python script must contain the following:
    1. the original code of the initial script provided in the <initial_script> tags. You make your changes to this script.
    2. a dictionary variable "extracted_keyval_data" = { ... } in the top level of the code below the imports, with the the extracted data 'region', 'temporal_resolution', 'sector' and 'subsector'. You find the data below within the <extracted_keyval_data> tags.
    3. add to the dataframe 'df_new' 4 new columns 'region', 'temporal_resolution', 'sector' and 'subsector'. Fill these columns with the extracted key value data from the <extracted_keyval_data> tags.
    4. finally replace the existing name for exporting the new .csv file from 'initially_formatted.csv' to 'added_keyval.csv'.
    5. IMORTANT: 
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
        <extracted_data_keyval>
        This is the extracted key-value data from the previous agent: {state.get("approved_extracted_data_keyval")}.
        </extracted_data_keyval>
        <prior_script>
        This is the initial script provided: {prior_script}.
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
    agent = create_coding_agent(state.get("df"), state.get("verbose"))

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)

    return {"code_keyval_script": response.get("output")}
