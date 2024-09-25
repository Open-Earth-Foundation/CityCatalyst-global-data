from state.agent_state import AgentState
from context.context_actval_transportation import context_actval_transportation
from context.mappings.mappings_gpc import gpc_mappings
from context.mappings.mappings_transportation import (
    fuel_mapping,
    fuel_to_gpc,
    transport_type_to_gpc,
)
from context.mappings.mappings_stationary_energy import (
    stationary_energy_scope_2_subsector_to_gpc,
)

from utils.create_prompt import create_prompt


def extraction_agent_gpc_mapping_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nEXTRACTION AGENT GPC MAPPING STATIONARY ENERGY TRANSPORTATION\n")

    task = """
Your task is to create a mapping dictionary that helps mapping activity data to gpc reference numbers for the two sectors 'Stationary Energy' sector and 'Transportation' sector from the provided dataframe 'df'.
Each activity data can be of a different subsector of the 'Stationary Energy' sector or 'Transportation' sector and therefore can have a different gpc reference number.
Each activity data only be associated with one GPC reference number. Never map multiple GPC reference numbers to the same activity data.
To identify the GPC reference number, you need to understand to entire context of the activity data. Additinal columns that provide context on the activity data help in determining the GPC reference number.
"""
    completion_steps = """
a. Load the entire dataframe 'df'. This means load all the rows and do not use df.head() to only inspect the first few rows.    
b. Identify columns that provide context for the activity data (for example what vehicle type, what building type, who it was sold to like public sector, agriculture sector, energy consumption and so on) of this activity. 
c. Then if you have identified a column that contains the relevant information about how the activity data is being used:
    1. print out the unique values of these columns
    2. make sure to include every unique value in your answer
d. Inspect the provided activity data inside the <activity_data> tags below, to understand the activity data that needs to be mapped
    - Especially pay attention to the different activity types like 'fuel consumption', 'electricity consumption' and so on as those influence the mapping. 
d. Inspect the general gpc mappings within <gpc_mappings> tags below, to understand the general GPC reference numbers and their structure.
e. Then for the identified activity data, check the gpc mappings for 'Stationay Energy' and 'Transportation' marked with <gpc_mappings_sector> tags below, to know which GPC reference numbers could be applied.
f. Then check the provided context for the sector 'Stationary Energy' and 'Transportation' marked with <context_activity_values_sector> tags below, to identify the correct GPC reference number based on the further context given in that document.
g. Make sure, to only assign one GPC reference number per activity data. Do NOT create a mapping that assigns a GPC reference number per every single row. Your task is to create a mapping based on context like usage and sector type.    
"""
    answer_format = """
- Give all your detailed reasoning inside the <reasoning> tags.
- Provide only the created mapping as JSON inside the <mapping> tags.
<answer>
    <reasoning>
    [Your detailed reasoning for creating the GPC reference number mappings. Make sure to include the reasoning for each GPC reference number you assign to the activity data]
    </reasoning>
    <mapping>
    [The mapping as JSON]
    </mapping>
</answer>
"""
    additional_information = f"""
<additional_information>
    <user_provided_context>
    This is the user provided context: {state.get("context_user_provided")}
    </user_provided_context>
    <gpc_master_document>
    You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
    </gpc_master_document>
    <activity_data>
    This is the provided activity data: {state.get("extracted_data_actval_stationary_energy_transportation")}.
    </activity_data>
    <gpc_mappings>
    The following information provides context to identify the GPC reference number for an activity value.
    This is the provided general context for Greenhouse Gas Protocol for Cities (GPC) mappings: {gpc_mappings}.
        <gpc_mappings_sector>
        The following provides context for mapping transportation activity data to Greenhouse Gas Protocol for Cities (GPC) reference numbers.
        This is the mapping of fuel names to possible GPC reference numbers: {fuel_to_gpc}.
        This is the mapping of the 'Stationary Energy' sector to possible GPC reference numbers: {stationary_energy_scope_2_subsector_to_gpc}.
        This is the mapping of the 'Transport' sector types to possible GPC reference numbers: {transport_type_to_gpc}.
        </gpc_mappings_sector>
    </gpc_mappings>
    <context_activity_values_sector>
    This is the provided context for avtivities specifically for the sector 'Transportation': {context_actval_transportation}.
    Use this information for guidance on the correct GPC reference number especially when multiple GPC reference numbers are possible for an activity value. 
    </context_activity_values_sector>
    <feedback>
        <feedback_human-in-the-loop>
        If the user has provided feedback at the end of the entire data pipeline from the human-in-the-loop agent, you find it here: {state.get("feedback_hitl")}.
        This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.
        </feedback_human-in-the-loop>
        <feedback_reasoning_agent>
        If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_gpc_mapping_stationary_energy_transportation")}.
        If feedback is available, pay special attention to this feedback and incorporate into your data extraction process.
        </feedback_reasoning_agent>
    </feedback>
</additional_information>
"""

    prompt = create_prompt(
        task, completion_steps, answer_format, additional_information
    )

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    return {
        "extracted_gpc_mapping_stationary_energy_transportation": response.get("output")
    }
