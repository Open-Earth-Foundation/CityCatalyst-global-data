from state.agent_state import AgentState
from agents.agent_tasks import task_extraction_agent_actval_transportation


def extraction_agent_actval_transportation(state: AgentState) -> dict:
    print("\nEXTRACTION AGENT ACTIVITY VALUES TRANSPORTATION\n")

    prompt = f"""
    <task_description>
    {task_extraction_agent_actval_transportation}
    </task_description>

    <additional_information>
    <user_provided_context>
    This is the user provided context: {state.get("context_user_provided")}
    </user_provided_context>
    <context_activity_values_transportation>
    This is the provided context for avtivity values specifically for the sector 'Transportation': {state.get("context_actval_transportation")},
    </context_activity_values_transportation>
    <summary>
    This is the summary of the previous agent: {state.get('summary')}.
    </summary>
    <file_path>
    This is the path to the original data file: {state.get('file_path')}.
    </file_path>
    </additional_information>
    """

    # If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_data_actval_transportation")}.
    # If feedback is available, pay special attention to this feedback and incorporate into your data extracation process.

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    print(response.get("output"))

    return {"extracted_data_actval_transportation": response.get("output")}
