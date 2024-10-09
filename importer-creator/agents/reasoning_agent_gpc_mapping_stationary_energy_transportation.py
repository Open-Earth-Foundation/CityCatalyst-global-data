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

# e. Perform test on the extracted data. The test are as follows:
#     - Check if the activity values are all non-negative. If not, provide specific feedback to the previous agent stating the exact row.
#     - Check if the activity values are all numeric. If not, provide specific feedback to the previous agent stating the exact row.


def reasoning_agent_gpc_mapping_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nREASONING AGENT GPC MAPPING STATIONARY ENERGY TRANSPORTATION\n")

    prompt = f"""
Your task is to check and verify the output of a previous extraction agent inside the <extracted_gpc_mapping_stationary_energy_transportation> tags below. 

Follow these instructions carefully:
1. Think step-by-step for each row in the dataframe 'df'. This means for each row, consider the activity data and the context like vehicle type, scope and so on. Do not assume that the different rows are related.

2. Consider the human-in-the-loop feedback provided in the <feedback_human-in-the-loop> tags below if available. This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.

3. You are already provided with a dataframe 'df' containing various data.

4. To complete this task:
    a. Load the entire dataframe 'df'. This means load all the rows and do not use df.head() to only inspect the first few rows.
    b. Check the reasoning of the previous agent. This can be found within the <reasoning> tags in the output of the previous agent within <extracted_gpc_mapping_stationary_energy_transportation> tags. 
    c. Verify the mapping that the previous agent had done. The mapping is found within the <mapping> tags output of the previous agent. Check if the previous agent has missed any values that are in the datafile but that do not have any mapping or if there is mislabeled data. For this, check the all unique values in that identified column of the datafile.
    d. Make sure that each activity was only mapped to one GPC reference number. If not, provide feedback to the previous agent.
    
5. Present your answer in the following format:
    If you approve, return 'APPROVED'. If not, return 'FEEDBACK: [Your feedback here]'.
    
6. You are given additional information that is helpful in completing your task:
    <additional_information>
        <file_path>
        This is the path to the original data file: {state.get('file_path')}.
        </file_path>
        <user_provided_context>
        This is the user provided context: {state.get("context_user_provided")}
        </user_provided_context>
        <extracted_gpc_mapping_stationary_energy_transportation>
        The output of the previous agent is this: {state.get("extracted_gpc_mapping_stationary_energy_transportation")}.
        </extracted_gpc_mapping_stationary_energy_transportation>
        <gpc_master_document>
        You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
        </gpc_master_document>
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
        Remember that each row in the dataframe 'df' can have a different subsector and scope and therefore a different GPC reference number.
        </context_activity_values_sector>
        <feedback>
            <feedback_human-in-the-loop>
            If the user has provided feedback at the end of the entire data pipeline from the human-in-the-loop agent, you find it here: {state.get("feedback_hitl")}.
            This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.
            </feedback_human-in-the-loop>
            <feedback_reasoning_agent>
            If you have provided previous feedback, you find it here: {state.get("feedback_extracted_gpc_mapping_stationary_energy_transportation")}. 
            If the extracted data aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
            </feedback_reasoning_agent>
        </feedback>
    </additional_information>
"""

    # Check if the iteration limit has been reached
    if (
        state.get(
            "iterator_reasoning_agent_gpc_mapping_stationary_energy_transportation"
        )
        >= 0
    ):
        print(
            "\nIteration limit reached. Automatically approving the extracted gpc mappings for 'Stationary Energy' and 'Transportion' sector.\n"
        )
        return {
            "approved_extracted_gpc_mapping_stationary_energy_transportation": state.get(
                "extracted_gpc_mapping_stationary_energy_transportation"
            )
        }

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    if "APPROVED" in response.get("output"):
        return {
            "approved_extracted_gpc_mapping_stationary_energy_transportation": state.get(
                "extracted_gpc_mapping_stationary_energy_transportation"
            )
        }
    else:
        return {
            "feedback_extracteds_gpc_mapping_stationary_energy_transportation": response.get(
                "output"
            ),
            "iterator_reasoning_agent_gpc_mapping_stationary_energy_transportation": state.get(
                "iterator_reasoning_agent_gpc_mapping_stationary_energy_transportation"
            )
            + 1,
        }
