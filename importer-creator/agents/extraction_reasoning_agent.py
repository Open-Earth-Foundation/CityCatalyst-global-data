from state.agent_state import AgentState
from agents.agent_tasks import task_reasoning_agent


def extraction_reasoning_agent(state: AgentState) -> dict:
    print("\nEXTRACTION REASONING AGENT\n")

    # Check if the iteration limit has been reached
    if state.get("extraction_reasoning_agent_iterations") >= 5:
        print(
            "\nIteration limit reached. Automatically approving the extraction agent's output.\n"
        )
        return {"approved_extracted_data": state.get("extracted_data")}

    prompt = f"""
    ### Task ###
    {task_reasoning_agent}

    ### Additional information ###
    This is the user provided context: {state.get('context_user_provided')},
    This is the provided context for sectors and subsectors to be used: {state.get('context_sector_subsector')},
    This is the summary of the previous agent: {state.get('summary')}.
    This is the path to the original data file: {state.get('file_path')}.
    This is the extracted data of the previous agent with explanation: {state.get('extracted_data')}.

    If you have given previous feedback to the extraction agent, you find it here: {state.get('extraction_reasoning_agent_feedback')}
    If you have given feedback, check the extracted data of the agent against your feedback. 
    If the extracted data aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
    """

    response = state.get("agent").invoke(prompt)

    if "APPROVED" in response.get("output"):
        return {"approved_extracted_data": state.get("extracted_data")}
    else:
        return {
            "extraction_reasoning_agent_feedback": response.get("output"),
            "extraction_reasoning_agent_iterations": state.get(
                "extraction_reasoning_agent_iterations"
            )
            + 1,
        }
