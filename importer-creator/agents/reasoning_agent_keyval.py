from state.agent_state import AgentState
from agents.agent_tasks import task_reasoning_agent_keyval


def reasoning_agent_keyval(state: AgentState) -> dict:
    print("\nEXTRACTION REASONING AGENT\n")

    # Check if the iteration limit has been reached
    if state.get("iterator_reasoning_agent_keyval") >= 5:
        print(
            "\nIteration limit reached. Automatically approving the extraction agent's output.\n"
        )
        return {"approved_extracted_data_keyval": state.get("extracted_data_keyval")}

    prompt = f"""
    ### Task ###
    {task_reasoning_agent_keyval}

    ### Additional information ###
    This is the user provided context: {state.get('context_user_provided')},
    This is the provided context for sectors and subsectors to be used: {state.get('context_sector_subsector')},
    This is the summary of the previous agent: {state.get('summary')}.
    This is the path to the original data file: {state.get('file_path')}.
    This is the extracted data of the previous agent with explanation: {state.get("extracted_data_keyval")}.

    If you have given previous feedback to the extraction agent, you find it here: {state.get("feedback_extracted_data_keyval")}
    If you have given feedback, check the extracted data of the agent against your feedback. 
    If the extracted data aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
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
