from state.agent_state import AgentState
from utils.agent_creation import create_structured_output_agent

json_schema = {
    "title": "gpc_reference_number_script",
    "description": "The updated python script containing the GPC reference numbers and reasoning for creating that script and reasoning for creating the GPC reference mappings from the data file",
    "type": "object",
    "properties": {
        "code": {
            "type": "string",
            "description": "The pure executable generated python code with GPC reference numbers added",
        },
        "reasoning": {
            "type": "string",
            "description": "The pure markdown text for the reasoning behind the GPC reference numbers mapping and for creating the python script",
        },
    },
    "required": ["code", "reasoning"],
}


def structured_output_agent_gpc_refno_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nSTRUCTURED OUTPUT AGENT GPC REFNO STATIONARY ENERGY TRANSPORTATION\n")

    prompt = f"""
    Your task is to provide structured output in JSON format. For the reasoning include both the reasoning for the GPC reference numbers mapping and reasoning for creating the python script but keep them in seperate sections divided by headers.

    <additional_information>
        <gpc_refno>
        This is the GPC reference number mapping with reasoning: {state.get("extracted_gpc_mapping_stationary_energy_transportation")}.
        </gpc_refno>
        <code_script>
        This is the python script with reasoning: {state.get("code_gpc_refno_stationary_energy_transportation_script")}.
        </code_script>
    </additional_information>
    """

    agent = create_structured_output_agent(json_schema, verbose=state.get("verbose"))

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)
    return {
        "structured_output_code_gpc_refno_stationary_energy_transportation": response
    }
