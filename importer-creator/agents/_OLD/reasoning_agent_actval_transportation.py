from state.agent_state import AgentState
from context.mappings.mappings_gpc import gpc_mappings
from context.mappings.mappings_transportation import (
    fuel_mapping,
    fuel_to_gpc,
    transport_type_to_gpc,
)

# This is the mapping of fuel names to standard names that we are using in GPC (IPCC standard): {fuel_mapping}.


def reasoning_agent_actval_transportation(state: AgentState) -> dict:
    print("\nREASONING AGENT ACTIVITY VALUES TRANSPORTATION\n")

    prompt = f"""
    Your task is to check and verify the output of a previous extraction agent. 
    The output of the previous agent is this: 
    <extracted_data_actval_transportation>
    {state.get("extracted_data_actval_transportation")}.
    </extracted_data_actval_transportation>

    Follow these instructions carefully:
    1. You are already provided with a dataframe 'df' containing various data.
    2. To complete this task:
        a. Check the list of extracted activities 
        b. Load all the rows of the entire dataframe 'df' and make a row by row comparison with the extracted activities.
        b. Verify for each row the 'activity_name', 'activity_value', 'unit', 'gpc_reference_number'. Pay special attention to the correct 'gpc_reference_number'. Verify that the 'gpc_reference_number' fits to the vehicle type, scope and subsector.
    
    3. You are given additional information that is helpful in completing your task:
    <additional_information>
        <user_provided_context>
        This is the user provided context: {state.get("user_input")}
        </user_provided_context>
        <context_activity_values_transportation>
        This is the provided context for avtivities specifically for the sector 'Transportation': {state.get("context_actval_transportation")}.
        Use this information for guidance on the correct GPC reference number especially when multiple GPC reference numbers are possible for an activity value. 
        Remember that each row in the dataframe 'df' can have a different subsector and therefore a different GPC reference number.
        </context_activity_values_transportation>
        <file_path>
        This is the path to the original data file: {state.get('file_path')}.
        </file_path>
        <gpc_mappings>
        Use the following information to identify the GPC reference number for an activity value and to understand the different fuel types.
        This is the provided context for Greenhouse Gas Protocol for Cities (GPC) mappings: {gpc_mappings}.
            <gpc_mappings_transportation>
            This is the provided context for mapping transportation activities to Greenhouse Gas Protocol for Cities (GPC) reference numbers.
            This is the mapping of fuel names to possible GPC reference numbers: {fuel_to_gpc}.
            This is the mapping of transport types to possible GPC reference numbers: {transport_type_to_gpc}.
            </gpc_mappings_transportation>
        </gpc_mappings>
    </additional_information>

    If you approve, return 'APPROVED'. If not, return 'FEEDBACK: [Your feedback here]'.
"""

    # Check if the iteration limit has been reached
    if state.get("iterator_reasoning_agent_actval_transportation") >= 0:
        print(
            "\nIteration limit reached. Automatically approving the extracted activity values for 'Transportion' sector.\n"
        )
        return {
            "approved_extracted_data_actval_transportation": state.get(
                "extracted_data_actval_transportation"
            )
        }

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    # print(response.get("output"))

    if "APPROVED" in response.get("output"):
        return {
            "approved_extracted_data_actval_transportation": state.get(
                "extracted_data_actval_transportation"
            )
        }
    else:
        return {
            "feedback_extracted_data_actval_transportation": response.get("output"),
            "iterator_reasoning_agent_actval_transportation": state.get(
                "iterator_reasoning_agent_actval_transportation"
            )
            + 1,
        }
