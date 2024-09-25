from state.agent_state import AgentState
from utils.agent_creation import create_structured_output_agent

json_schema = {
    "title": "transformation_script",
    "description": "The updated python script containing the transformed activity values and reasoning for creating that script and reasoning for creating the transformations from the data file",
    "type": "object",
    "properties": {
        "code": {
            "type": "string",
            "description": "The pure executable generated python code with transformation values added",
        },
        "reasoning": {
            "type": "string",
            "description": "The pure markdown text for the reasoning behind the transformations and for creating the python script",
        },
    },
    "required": ["code", "reasoning"],
}


def structured_output_agent_transformation_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nSTRUCTURED OUTPUT AGENT TRANSFORMATION STATIONARY ENERGY TRANSPORTATION\n")

    prompt = f"""
    Your task is to provide structured output in JSON format. For the reasoning include both the reasoning for the transformations of the activity values and reasoning for creating the python script but keep them in seperate sections divided by headers.

    <additional_information>
        <transformations>
        These are the transformations with reasoning: {state.get("extracted_transformations_stationary_energy_transportation")}.
        </transformations>
        <code_script>
        This is the python script with reasoning: {state.get("code_transformations_stationary_energy_transportation_script")}.
        </code_script>
    </additional_information>
    """

    agent = create_structured_output_agent(json_schema, verbose=state.get("verbose"))

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)
    return {
        "structured_output_code_transformation_stationary_energy_transportation": response
    }
