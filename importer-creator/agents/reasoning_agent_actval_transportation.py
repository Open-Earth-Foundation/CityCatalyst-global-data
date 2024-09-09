from state.agent_state import AgentState


def reasoning_agent_actval_transportation(state: AgentState) -> dict:
    print("\nREASONING AGENT ACTIVITY VALUES TRANSPORTATION\n")

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

    prompt = f"""
    ### Task ###
    

    ### Additional information ###
    This is the user provided context: {state.get("context_user_provided")},
    This is the provided context for avtivity values specifically for the sector 'Transportation': {state.get('context_activity_values_transportation')},
    This is the summary of the previous agent: {state.get('summary')}.
    This is the path to the original data file: {state.get('file_path')}.
    This is the extracted activity data for sector 'Transportation' of the previous agent with explanation: {state.get("extracted_data_actval_transportation")}.
    
    If you have given previous feedback to the extraction agent for activity values for sector 'Transportation', you find it here: {state.get("feedback_extracted_data_actval_transportation")}
    If you have given feedback, check the extracted data of the agent against your feedback. 
    If the extracted data aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
    """

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
