from state.agent_state import AgentState
from agents.agent_tasks import task_extraction_agent


def extraction_agent(state: AgentState) -> dict:
    print("\nEXTRACTION AGENT\n")

    # Agent logic to extract specific data
    prompt = f"""
    ### Task ###
    {task_extraction_agent}

    ### Additional information ###
    This is the user provided context: {state['user_provided_context']},
    This is the provided context for sectors and sub-sectors to be used: {state['context']},
    This is the summary of the previous agent: {state['summary']}.
    This is the path to the original data file: {state['file_path']}.

    If you have received feedback from the reasoning agent, you find it here: {state['reasoning_agent_feedback']}
    If feedback is available, pay special attention to this feedback and incorporate into your data extracation process.
    """

    extracted_data = state["agent"].invoke(prompt)

    return {"extracted_data": extracted_data.get("output")}
