from state.agent_state import AgentState
from agents.agent_tasks import task_code_reasoning_agent


def code_reasoning_agent(state: AgentState) -> dict:
    print("\nCODE REASONING AGENT\n")

    # Check if the iteration limit has been reached
    if state.get("code_reasoning_agent_iterations") >= 5:
        print(
            "\nIteration limit reached. Automatically approving the last output of the code generation agent.\n"
        )
        return {"final_code_output": state.get("generated_code")}

    prompt = f"""
    ### Task ###
    {task_code_reasoning_agent}

    ### Additional information ###
    This is the generated code of the previous agent: {state.get('generated_code')}.
    This is the file name of the original data file: {state.get('file_path')}.

    If you have given previous feedback to the code generation agent, you find it here: {state.get('code_reasoning_agent_feedback')}.
    If you have given feedback, check the generated code of the previous agent against your feedback. 
    If the generated code aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
    """
    response = state.get("coding_agent").invoke(prompt)

    if "APPROVED" in response.get("output"):
        return {"final_code_output": state.get("generated_code")}
    else:
        return {
            "code_reasoning_agent_feedback": response.get("output"),
            "code_reasoning_agent_iterations": state.get(
                "code_reasoning_agent_iterations"
            )
            + 1,
        }
