from state.agent_state import AgentState


def hitl_agent(state: AgentState) -> dict:
    print("\nHUMAN-IN-THE-LOOP AGENT\n")

    message = """
    Please check the created files 'generated_reasoning.md' and 'generated_script.py' in the folder '/generated'.

    If you are satisfied with the generated reasoning and code, please type 'END' in all caps to finish the script. 
    Otherwise, provide feedback. Be as specific as possible. 

    1. Type 'END' to finish the script.
    2. Provide feedback to adjust the reasoning and code.
        
    Submit your response by pressing 'Enter'.
    """
    feedback_hitl = input(message)

    return {"feedback_hitl": feedback_hitl}
