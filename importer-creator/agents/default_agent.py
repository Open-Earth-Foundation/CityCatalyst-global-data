from state.agent_state import AgentState


def default_agent(state: AgentState) -> dict:
    print("\nDEFAULT AGENT\n")

    prompt = f"""
    ### Task ###
    ### Additional information ###
    """

    # Invoke summary agent with custom prompt
    summary = state.get("agent").invoke(prompt)
    return {"summary": summary.get("output")}
