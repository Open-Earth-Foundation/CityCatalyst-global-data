from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from state.agent_state import AgentState
from agents.agent_tasks import task_structured_output_agent_keyval

load_dotenv()

model = "gpt-4o-mini"

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

# Initialize the LLM
llm = ChatOpenAI(model=model, temperature=0)
structured_llm = llm.with_structured_output(json_schema)


def structured_output_agent_keyval(state: AgentState) -> dict:
    print("\nSTRUCTURED OUTPUT AGENT KEYVAL\n")

    prompt = f"""
    ### Task ###
    {task_structured_output_agent_keyval}

    ### Additional information ###
    This is the extracted data of the previous agent: {state.get("approved_extracted_data_keyval")}.
    """

    # Invoke summary agent with custom prompt
    response = structured_llm.invoke(prompt)
    return {"structured_output_keyval": response}
