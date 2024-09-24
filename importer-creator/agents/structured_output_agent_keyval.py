from state.agent_state import AgentState
from utils.agent_creation import create_structured_output_agent

json_schema = {
    "title": "key-value_script",
    "description": "The updated python script containing the key-value data, reasoning, and extracted key-value data from the data file",
    "type": "object",
    "properties": {
        "code": {
            "type": "string",
            "description": "The pure executable generated python code with extracted key-value data added",
        },
        "reasoning": {
            "type": "string",
            "description": "The pure markdown text for the reasoning behind extracting the key-value data and for creating the python script",
        },
        "extracted_data": {
            "type": "object",
            "description": "The extracted key-value pairs from the data file",
            "properties": {
                "region": {
                    "type": "string",
                    "description": "The region that the data file is associated with",
                },
                "temporal_resolution": {
                    "type": "string",
                    "description": "The temporal resolution of the data points (e.g., days, months, years)",
                },
                "sector": {
                    "type": "string",
                    "description": "The GPC sector the data file is associated with",
                },
                "subsector": {
                    "type": "string",
                    "description": "The GPC sub-sector the data file is associated with",
                },
            },
            "required": ["region", "temporal_resolution", "sector", "subsector"],
        },
    },
    "required": ["code", "reasoning", "extracted_data"],
}


def structured_output_agent_keyval(state: AgentState) -> dict:
    print("\nSTRUCTURED OUTPUT AGENT KEYVAL\n")

    prompt = f"""
    Your task is to provide structured output in JSON format. For the reasoning include both the reasoning for extracting the key-value data and for creating the python script but keep them in seperate sections divided by headers.

    <additional_information>
        <extracted_data>
        This is the extracted key-value data from the previous agent with reasoning: {state.get("approved_extracted_data_keyval")}.
        </extracted_data>
        <code_initial_script>
        This is the initial python script with reasoning: {state.get("code_keyval_script")}.
        </code_initial_script>
    </additional_information>
    """

    agent = create_structured_output_agent(json_schema, verbose=state.get("verbose"))

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)
    return {"structured_output_code_keyval": response}
