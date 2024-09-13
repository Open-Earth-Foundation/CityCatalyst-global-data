from state.agent_state import AgentState
from context.mappings.mappings_gpc import gpc_mappings
from context.mappings.mappings_transportation import (
    fuel_mapping,
    fuel_to_gpc,
    transport_type_to_gpc,
)
from context.mappings.mappings_stationary_energy import (
    stationary_energy_scope_2_subsector_to_gpc,
)


def reasoning_agent_actval_stationary_energy_transportation(state: AgentState) -> dict:
    print("\nREASONING AGENT ACTIVITY VALUES STATIONARY ENERGY TRANSPORTATION\n")

    prompt = f"""
    Your task is to check and verify the output of a previous extraction agent. 
    The output of the previous agent is this: 
    <extracted_data_actval_stationary_energy_transportation>
    {state.get("extracted_data_actval_stationary_energy_transportation")}.
    </extracted_data_actval_stationary_energy_transportation>

    Follow these instructions carefully:
    1. You are already provided with a dataframe 'df' containing various data.
    2. To complete this task:
        a. Load the entire dataframe 'df'. This means load all the rows and do not use df.head() to only inspect the first few rows.
        b. Think step-by-step for each row in the dataframe 'df'. This means for each row, consider the activity data and the context like vehicle type, scope and so on. Do not assume that the different rows are related.
        c. Check the reasoning of the previous agent. This can be found within the <reasoning> tags in the output of the previous agent within <extracted_data_actval_stationary_energy_transportation> tags. 
        d. Verify the mapping that the previous agent had done. The mapping is found within the <code> tags output of the previous agent within <extracted_data_actval_stationary_energy_transportation> tags. Check if the previous agent has missed any sectors that are in the datafile, but that do not have any mapping or if there is mislabeled data.
        e. Perform test on the extracted data. The test are as follows:
            - Check if the activity values are all non-negative. If not, provide specific feedback to the previous agent stating the exact row.
            - Check if the activity values are all numeric. If not, provide specific feedback to the previous agent stating the exact row.
        e. If you approve, return 'APPROVED'. If not, return 'FEEDBACK: [Your feedback here]'.
        
    3. You are given additional information that is helpful in completing your task:
    <additional_information>
        <gpc_master_document>
        You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
        </gpc_master_document>
        <user_provided_context>
        This is the user provided context: {state.get("context_user_provided")}
        </user_provided_context>
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
        This is the provided context for avtivities specifically for the sector 'Transportation': {state.get("context_actval_transportation")}.
        Use this information for guidance on the correct GPC reference number especially when multiple GPC reference numbers are possible for an activity value. 
        Remember that each row in the dataframe 'df' can have a different subsector and scope and therefore a different GPC reference number.
        </context_activity_values_sector>
        <file_path>
        This is the path to the original data file: {state.get('file_path')}.
        </file_path>
        <feedback>
        If you have provided previous feedback, you find it here: {state.get("feedback_extracted_data_actval_stationary_energy_transportation")}. 
        If the extracted data aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
        </feedback>
    </additional_information>
"""

    # Check if the iteration limit has been reached
    if (
        state.get("iterator_reasoning_agent_actval_stationary_energy_transportation")
        >= 1
    ):
        print(
            "\nIteration limit reached. Automatically approving the extracted activity values for 'Stationary Energy' and 'Transportion' sector.\n"
        )
        return {
            "approved_extracted_data_actval_stationary_energy_transportation": state.get(
                "extracted_data_actval_stationary_energy_transportation"
            )
        }

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    # print(response.get("output"))

    if "APPROVED" in response.get("output"):
        return {
            "approved_extracted_data_actval_stationary_energy_transportation": state.get(
                "extracted_data_actval_stationary_energy_transportation"
            )
        }
    else:
        return {
            "feedback_extracted_data_actval_stationary_energy_transportation": response.get(
                "output"
            ),
            "iterator_reasoning_agent_actval_stationary_energy_transportation": state.get(
                "iterator_reasoning_agent_actval_stationary_energy_transportation"
            )
            + 1,
        }
