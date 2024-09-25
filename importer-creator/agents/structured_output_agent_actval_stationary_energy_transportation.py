from state.agent_state import AgentState
from utils.agent_creation import create_structured_output_agent

json_schema = {
    "title": "activity_data_script",
    "description": "The updated python script containing the activity data and reasoning for creating that script and extracting the activity data from the data file",
    "type": "object",
    "properties": {
        "code": {
            "type": "string",
            "description": "The pure executable generated python code with extracted activity data added",
        },
        "reasoning": {
            "type": "string",
            "description": "The pure markdown text for the reasoning behind extracting the activity data and for creating the python script",
        },
    },
    "required": ["code", "reasoning"],
}


def structured_output_agent_actval_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nSTRUCTURED OUTPUT AGENT ACTVAL STATIONARY ENERGY TRANSPORTATION\n")

    prompt = f"""
    Your task is to provide structured output in JSON format. For the reasoning include both the reasoning for extracting the key-value data and for creating the python script but keep them in seperate sections divided by headers.

    <additional_information>
        <extracted_data>
        This is the extracted key-value data from the previous agent with reasoning: {state.get("approved_extracted_data_keyval")}.
        </extracted_data>
        <prior_script>
        This is the prior python script with reasoning: {state.get("code_actval_stationary_energy_transportation_script")}.
        </prior_script>
    </additional_information>
    """

    agent = create_structured_output_agent(json_schema, verbose=state.get("verbose"))

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)
    return {"structured_output_code_actval_stationary_energy_transportation": response}
