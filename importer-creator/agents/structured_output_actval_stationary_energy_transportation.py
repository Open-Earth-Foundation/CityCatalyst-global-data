from langchain_openai import ChatOpenAI
from state.agent_state import AgentState
from dotenv import load_dotenv

load_dotenv()

model = "gpt-4o-mini"

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

# Initialize the LLM
llm = ChatOpenAI(model=model, temperature=0)
structured_llm = llm.with_structured_output(json_schema)


def structured_output_actval_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nSTRUCTURED OUTPUT ACTVAL STATIONARY ENERGY TRANSPORTATION\n")

    prompt = f"""
    Your task is to provide structured output in JSON format based on the output of a previous agent.

    1. Output the text within <code> tags inside the "code" key of the JSON object as executable python code. Only include the final code output without any xml tags.
    2. Output the text within <reasoning> tags inside the "reasoning" key of the JSON object as markdown text. Only include the final markdown text output without any xml tags.

    <additional_information>
        <output_previous_agent>
        This is the output of the previous agent: {state.get("approved_extracted_data_actval_stationary_energy_transportation")}.
        </output_previous_agent>
    </additional_information>
    """

    # Invoke summary agent with custom prompt
    response = structured_llm.invoke(prompt)
    return {"structured_output_stationary_energy_transportation": response}
