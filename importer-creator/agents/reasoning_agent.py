from state.agent_state import AgentState
from agents.agent_tasks import task_reasoning_agent


def reasoning_agent(state: AgentState) -> dict:
    print("\nREASONING AGENT\n")

    # Check if the iteration limit has been reached
    if state["reasoning_agent_iterations"] >= 5:
        print(
            "\nIteration limit reached. Automatically approving the extraction agent's output.\n"
        )
        return {"final_output": state["extracted_data"]}

    #             1. the original pandas dataframe: {state['pandas_df']},

    prompt = f"""
    ### Task ###
    {task_reasoning_agent}

    ### Additional information ###
    This is the user provided context: {state['user_provided_context']},
    This is the provided context for sectors and sub-sectors to be used: {state['context']},
    This is the summary of the previous agent: {state['summary']}.
    This is the path to the original data file: {state['file_path']}.
    This is the extracted data of the previous agent: {state['extracted_data']}, which only contains a json without further explanations. Only check if the values are correctly extracted.

    If you have given previous feedback to the extraction agent, you find it here: {state['reasoning_agent_feedback']}
    If you have given feedback, check the extracted data of the agent against your feedback. 
    If the extracted data aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
    """

    response = state["agent"].invoke(prompt)

    if "APPROVED" in response.get("output"):
        return {"final_output": state["extracted_data"]}
    else:
        return {
            "reasoning_agent_feedback": response.get("output"),
            "reasoning_agent_iterations": state["reasoning_agent_iterations"] + 1,
        }
