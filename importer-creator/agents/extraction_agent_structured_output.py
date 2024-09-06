from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from state.agent_state import AgentState
from agents.agent_tasks import task_extraction_agent_structured_output

load_dotenv()

model = "gpt-4o"

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


def extraction_agent_structured_output(state: AgentState) -> dict:
    print("\nEXTRACTION AGENT STRUCTURED OUTPUT\n")

    prompt = f"""
    ### Task ###
    {task_extraction_agent_structured_output}

    ### Additional information ###
    This is the extracted data of the previous agent: {state.get('extracted_data')}.
    """

    # Invoke summary agent with custom prompt
    result = structured_llm.invoke(prompt)
    return {"structured_extracted_data": result}
