from state.agent_state import AgentState
from agents.agent_tasks import task_summary_agent


def summary_agent(state: AgentState) -> dict:
    print("\nSUMMARY AGENT\n")

    prompt = f"""
    ### Task ###
    {task_summary_agent}
        
    ### Additional information ###
    This is the user provided context: {state.get('context_user_provided')}.
    This is the path to the original data file: {state.get('file_path')}.  
    """

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)
    return {"summary": response.get("output")}
