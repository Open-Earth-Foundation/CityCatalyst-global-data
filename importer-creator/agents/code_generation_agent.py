from state.agent_state import AgentState
from agents.agent_tasks import task_code_generation_agent


def code_generation_agent(state: AgentState) -> dict:
    print("\nCODE GENERATION AGENT\n")

    prompt = f"""
    ### Task ###
    {task_code_generation_agent}
    
    ### Additional information ###
    This is the summary of the previous agent: {state.get('summary')}.
    This is the extracted data from the previous agent: {state.get('final_output')}.
    This is the file name of the original data file: {state.get('file_path')}.

    If you have received feedback from the 'code reasoning agent', you find it here: {state.get('code_reasoning_agent_feedback')}.
    If feedback is available, pay special attention to this feedback and incorporate into your data extracation process.
    Especially pay attention to feedback related to errors in code. 
    """

    # Invoke code agent with custom prompt
    response = state.get("coding_agent").invoke(prompt)

    return {"generated_code": response.get("output")}
