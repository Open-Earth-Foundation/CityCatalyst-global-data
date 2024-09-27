from state.agent_state import AgentState


def hitl_agent(state: AgentState) -> dict:
    print("\nHUMAN-IN-THE-LOOP AGENT\n")

    message = """
    Please check the created files in the folder './generated'.

    If you are satisfied with the generated reasoning and code, please type 'NO FEEDBACK' in all caps to proceed with the script. 
    Otherwise, provide feedback. Be as specific as possible. The current step will be repeated with your feedback in mind.

    1. Type 'NO FEEDBACK' to proceed.
    2. Provide feedback to adjust the reasoning and code.
        
    Submit your response by pressing 'Enter'.
    """
    feedback_hitl = input(message)

    if feedback_hitl == "NO FEEDBACK":
        return {"feedback_hitl": "NO FEEDBACK"}

    # Update the state with the feedback
    return {"feedback_hitl": feedback_hitl}
