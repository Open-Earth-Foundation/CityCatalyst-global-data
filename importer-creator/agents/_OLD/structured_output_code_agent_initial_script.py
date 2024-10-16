from state.agent_state import AgentState
from utils.agent_creation import create_structured_output_agent

json_schema = {
    "title": "initial_script",
    "description": "The initial script and reasoning for creating it from the data file",
    "type": "object",
    "properties": {
        "code": {
            "type": "string",
            "description": "The pure executable generated python code for the initial python script",
        },
        "reasoning": {
            "type": "string",
            "description": "The pure markdown text for the reasoning behind creating the initial python script",
        },
    },
    "required": ["code", "reasoning"],
}


def structured_output_code_agent_initial_script(state: AgentState) -> dict:
    print("\nSTRUCTURED OUTPUT CODE AGENT INITIAL SCRIPT\n")

    prompt = f"""
    Your task is to provide structured output in JSON format. 
    For the reasoning include both the key points of the summary and the reasoning for creating the python script but keep them in seperate sections divided by headers.

    <additional_information>
        <summary>
        This is the summary of the dataset: {state.get('summary')}.
        </summary>
        <code_initial_script>
        This is the initial python script with reasoning: {state.get("code_initial_script")}.
        </code_initial_script>
    </additional_information>
    """

    # Create structured output agent
    agent = create_structured_output_agent(json_schema, verbose=state.get("verbose"))

    # Invoke summary agent with custom prompt
    response = agent.invoke(prompt)
    return {"structured_output_code_initial_script": response}
