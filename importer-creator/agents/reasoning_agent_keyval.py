from state.agent_state import AgentState
from context.context_sector_subsector import context_sector_subsector


def reasoning_agent_keyval(state: AgentState) -> dict:
    print("\nEXTRACTION REASONING AGENT\n")

    # Check if the iteration limit has been reached
    if state.get("iterator_reasoning_agent_keyval") >= 0:
        print(
            "\nIteration limit reached. Automatically approving the extraction agent's output.\n"
        )
        return {"approved_extracted_data_keyval": state.get("extracted_data_keyval")}

    prompt = f"""
Your task is to check and verify the output of a previous extraction agent for key-value pairs from the provided dataframe 'df'. 

Follow these instructions carefully:
1. Think step-by-step

2. You are already provided with the dataframe 'df' containing the activities.

3. To complete this task:
    b. Check the reasoning of the previous agent. This can be found in the output of the previous agent within <extracted_data_keyval> tags below. 
    a. Verify the extracted key-value pairs of the previous agent. This can be found within the <extracted_data_keyval> tags in the output of the previous agent below.
    
4. Present your answer in the following format:
    If you approve, return 'APPROVED'. If not, return 'FEEDBACK: [Your feedback here]'.

5. You are given additional information that is helpful in completing your task:
    <additional_information>
        <file_path>
        This is the path to the original data file: {state.get('file_path')}.
        </file_path>
        <extracted_data_keyval>
        This is the extracted data of the previous extraction agent with explanation: {state.get("extracted_data_keyval")}.
        <extracted_data_keyval/>
        <gpc_master_document>
        You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
        </gpc_master_document>
        <user_provided_context>
        This is the user provided context: {state.get("context_user_provided")}
        </user_provided_context>
        <context_sector_subsector>
        This is the provided context for sectors and sub-sectors to be used: {context_sector_subsector},
        </context_sector_subsector>
        <summary>
        This is the summary of the dataset: {state.get('summary')}.
        </summary>
        <feedback>
        If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_data_keyval")}.
        If feedback is available, pay special attention to this feedback and incorporate into your data extraction process.
        </feedback>
    </additional_information>
"""

    response = state.get("agent").invoke(prompt)

    if "APPROVED" in response.get("output"):
        return {"approved_extracted_data_keyval": state.get("extracted_data_keyval")}
    else:
        return {
            "feedback_extracted_data_keyval": response.get("output"),
            "iterator_reasoning_agent_keyval": state.get(
                "iterator_reasoning_agent_keyval"
            )
            + 1,
        }
