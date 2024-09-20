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


def extraction_agent_actval_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nEXTRACTION AGENT ACTVAL STATIONARY ENERGY TRANSPORTATION\n")

    goal = "Extract relevant GPC reference numbers for each activity in the dataframe."
    step_4 = "Present as a JSON object with keys: activity, GPC_reference_number."
    step_5 = "Context about the city and transportation details."
    step_6 = """<gpc_master_document>
                You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
                </gpc_master_document>
                <user_provided_context>
                This is the user provided context: 
                </user_provided_context>
                <gpc_mappings>
                The following information provides context to identify the GPC reference number for an activity value.
                This is the provided general context for Greenhouse Gas Protocol for Cities (GPC) mappings: .
                    <gpc_mappings_sector>
                    The following provides context for mapping transportation activity data to Greenhouse Gas Protocol for Cities (GPC) reference numbers.
                    This is the mapping of fuel names to possible GPC reference numbers: .
                    This is the mapping of the 'Stationary Energy' sector to possible GPC reference numbers: .
                    This is the mapping of the 'Transport' sector types to possible GPC reference numbers: .
                    </gpc_mappings_sector>
                </gpc_mappings>
                <context_activity_values_sector>
                This is the provided context for activities specifically for the sector 'Transportation':.
                Use this information for guidance on the correct GPC reference number especially when multiple GPC reference numbers are possible for an activity value. 
                </context_activity_values_sector>
                <extracted_keyval_data>
                This is the extracted key-value data from the previous agent:.
                </extracted_keyval_data>
                <file_path>
                This is the path to the original data file: .
                </file_path>
                <feedback>
                    <feedback_human-in-the-loop>
                    If the user has provided feedback at the end of the entire data pipeline from the human-in-the-loop agent, you find it here: .
                    This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.
                    </feedback_human-in-the-loop>
                    <feedback_reasoning_agent>
                    If you have received feedback from the reasoning agent, you find it here:.
                    If feedback is available, pay special attention to this feedback and incorporate it into your data extraction process.
                    </feedback_reasoning_agent>
                </feedback>
    """

    prompt = create_prompt(goal, step_4, step_5, step_6)

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    return {"extracted_actval_stationary_energy_transportation": response.get("output")}
