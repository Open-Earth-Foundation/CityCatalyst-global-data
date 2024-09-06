from state.agent_state import AgentState
from agents.agent_tasks import task_extraction_agent


def extraction_agent(state: AgentState) -> dict:
    print("\nEXTRACTION AGENT\n")

    # Agent logic to extract specific data
    prompt = f"""
    ### Task ###
    {task_extraction_agent}

    ### Additional information ###
    This is the user provided context: {state.get("context_user_provided")},
    This is the provided context for sectors and sub-sectors to be used: {state.get('context_sector_subsector')},
    This is the summary of the previous agent: {state.get('summary')}.
    This is the path to the original data file: {state.get('file_path')}.

    If you have received feedback from the reasoning agent, you find it here: {state.get('reasoning_agent_feedback')}.
    If feedback is available, pay special attention to this feedback and incorporate into your data extracation process.
    """

    result = state.get("agent").invoke(prompt)

    return {"extracted_data": result.get("output")}
