from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_coding_agent


def load_script(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        script = file.read()

    return script


def code_generation_agent_transformation_stationay_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nCODE GENERATION AGENT TRANSFORMATION STATIONARY ENERGY TRANSPORTATION\n")

    # Path to prior script in pipeline
    path = "./generated/gpc_refno_script/generated_gpc_refno_script.py"
    prior_script = load_script(path)

    task = """
Your task is to create a runnable python script.
Your inputs are the previously created python script 'generated_gpc_refno_script.py' below inside <prior_script> tags as well as the extracted transformations inside the <extracted_transformations_stationary_energy_transportation> tags.
"""

    completion_steps = """
a. Inspect the extracted transformations inside the <extracted_transformations_stationary_energy_transportation> tags.
b. Inspect the provided python script inside the <prior_script> tags.
c. Create a python script. This python script must contain the following:
    1. the original code of the prior script provided in the <prior_script> tags. You make your changes to this script.
    2. add to the new dataframe 'df_new' 1 new colum 'methodology'. Fill this column with the methodology used for that corresponding activity data bases on the extracted transformations in <extracted_transformations_stationary_energy_transportation> tags below.
    3. add to the new dataframe 'df_new' 1 new colum 'transformed_value'. 
        - Calculate the transformed value by using the identified 'methodology' together with the corresponding 'activity_value' and 'emission_factor'. For the methodology refer to <extracted_transformations_stationary_energy_transportation> tags below.
        - Add the calculated values to the 'transformed_value' column.
    4. finally replace the existing name for exporting the new .csv file from 'added_gpc_refno_data.csv' to 'transformed_data.csv'.
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
        <prior_script>
        This is the prior script provided: {prior_script}.
        <prior_script>
        <extracted_transformations_stationary_energy_transportation>
        This is the extracted transformation data: {state.get("extracted_transformations_stationary_energy_transportation")}.
        </extracted_transformations_stationary_energy_transportation> 
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

    return {
        "code_transformations_stationary_energy_transportation_script": response.get(
            "output"
        )
    }
