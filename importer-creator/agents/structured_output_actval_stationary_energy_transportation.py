from state.agent_state import AgentState
from utils.agent_creation import create_structured_output_agent

json_schema = {
    "title": "structured_output_actval_stationary_energy_transportation",
    "description": "The structured output for the extracted activity data from the data file (code and reasoning)",
    "type": "object",
    "properties": {
        "code": {
            "type": "string",
            "description": "The pure executable generated python code for extracting the data from the data file",
        },
        "reasoning": {
            "type": "string",
            "description": "The pure markdown text for the reasoning behind the extracted avtivity values and generated code",
        },
    },
    "required": ["code", "reasoning"],
}


def structured_output_actval_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nSTRUCTURED OUTPUT ACTVAL STATIONARY ENERGY TRANSPORTATION\n")

    agent = create_structured_output_agent(json_schema, verbose=state.get("verbose"))

    prompt = f"""
    Your task is to provide structured output in JSON format based on the output of a previous agent.

    1. Output the text within <code> tags as executable python code within <final_code_output> tags below. Only include the final code output without any xml tags.
    2. Output the text within <reasoning> tags as markdown text. Combine all the reasonings between <reasoning> tags into a final markdown text. Do not create a summary but create a detailed collections of the individual reasonings. Only include the final markdown text output without any xml tags.

    <additional_information>
        <final_code_output>
        This is the final code output: {state.get("final_code_output")}.
        </final_code_output>
        <reasoning>
            <reasoning_gpc_mappings>
            This is the reasoning for the created gpc mappings: {state.get("approved_extracted_gpc_mapping_stationary_energy_transportation")}.
            </reasoning_gpc_mappings>
            <reasoning_activity_values>
            This is the reasoning for extracting the activity values: EMPTY
            </reasoning_activity_values>
            <reasoning_emission_value_conversion>
            This is the reasoning for the emission value conversions: EMPTY
            </reasoning_emission_value_conversion>
        </reasoning>
    </additional_information>
    """

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)
    return {"structured_output_stationary_energy_transportation": response}
