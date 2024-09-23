from state.agent_state import AgentState
from context.context_actval_transportation import context_actval_transportation

from utils.create_prompt import create_prompt


def extraction_agent_actval_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nEXTRACTION AGENT ACTVAL STATIONARY ENERGY TRANSPORTATION\n")

    task = """
Your goal is to identify the activity data for the 'Stationary Energy' sector and 'Transportation' sector from the provided dataframe 'df'.
Each single row in the dataframe 'df' contains unique activity data.
Activity data consists of:
    - The activity name
    - The activity value
    - The activity unit
Identify the columns in the dataframe that represent activity data and present your detailed reasoning for this.
"""
    completion_steps = """
a. Load the entire dataframe 'df'. This means load all the rows and do not use df.head() to only inspect the first few rows.    
b. Identify columns in the dataframe that represent activity data and activity values.
c. Inspect those columns. If now activity unit is provided, infer the correct unit based on the context of the activity data using standard SI units.
"""
    answer_format = """
- Give all your detailed reasoning inside the <reasoning> tags.
- Provide only the created mapping as JSON inside the <mapping> tags.
<answer>
    <reasoning>
    [Your detailed reasoning]
    </reasoning>
    <columns>
    [The identified columns for activity data]
    </columns>
</answer>
"""
    additional_information = f"""
</additional_information>
    <file_path>
    This is the path to the original data file: {state.get('file_path')}.
    </file_path>
    <gpc_master_document>
    You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
    </gpc_master_document>
    <user_provided_context>
    This is the user provided context: {state.get("context_user_provided")}.
    </user_provided_context>
    <context_activity_values_sector>
    This is the provided context for activities specifically for the sector 'Transportation': {context_actval_transportation}.
    Use this information for finding the correct columns about activity data. 
    </context_activity_values_sector>
    <extracted_keyval_data>
    This is the extracted key-value data: {state.get("structured_output_keyval")}.
    </extracted_keyval_data>
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

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    return {"extracted_actval_stationary_energy_transportation": response.get("output")}
