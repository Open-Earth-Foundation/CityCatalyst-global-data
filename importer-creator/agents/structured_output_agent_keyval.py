from state.agent_state import AgentState
from utils.agent_creation import create_structured_output_agent

json_schema = {
    "title": "extracted_data",
    "description": "The extracted key-value pairs from the data file",
    "type": "object",
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
        "sub_sector": {
            "type": "string",
            "description": "The GPC sub-sector the data file is associated with",
        },
    },
    "required": ["region", "temporal_resolution", "sector", "sub-sector"],
}


def structured_output_agent_keyval(state: AgentState) -> dict:
    print("\nSTRUCTURED OUTPUT AGENT KEYVAL\n")

    agent = create_structured_output_agent(json_schema, verbose=state.get("verbose"))

    prompt = f"""
    ### Task ###
    Your task is to provide structured output in JSON format.

    ### Additional information ###
    This is the extracted data of the previous agent: {state.get("approved_extracted_data_keyval")}.
    You find the information in the <extracted_data_keyval> tags in the output of the previous agent.
    """

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)
    return {"structured_output_keyval": response}
