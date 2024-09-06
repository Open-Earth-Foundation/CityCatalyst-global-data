from langgraph.graph import StateGraph, END
from state.agent_state import AgentState

from agents.default_agent import default_agent
from agents.summary_agent import summary_agent
from agents.extraction_agent_keyval import extraction_agent_keyval
from agents.extraction_reasoning_agent import extraction_reasoning_agent
from agents.extraction_agent_structured_output import extraction_agent_structured_output
from agents.extraction_agent_actval_transportation import (
    extraction_agent_actval_transportation,
)
from agents.extraction_reasoning_agent_actval_transportation import (
    extraction_reasoning_agent_actval_transportation,
)
from agents.code_generation_agent import code_generation_agent
from agents.code_reasoning_agent import code_reasoning_agent


# Define the conditional edge
def should_extraction_continue(state: AgentState) -> str:
    if state.get("approved_extracted_data"):
        return "extraction_agent_structured_output"
        # router(state)
        # return "code_generation_agent"
    return "extraction_agent_keyval"


# Define the router conditional edge
def router(state: AgentState) -> str:
    """
    This function is used to route the extraction agent output to the appropriate agent based on the sector and sub-sector extracted.
    If no matching sector or sub-sector is extracted, the workflow ends.
    """

    structured_extracted_data = state.get("structured_extracted_data")
    sector = structured_extracted_data.get("sector")
    sub_sector = structured_extracted_data.get("sub_sector")

    print(f"structured_extracted_data: {structured_extracted_data}")
    print(f"sector: {sector}")
    print(f"sub_sector: {sub_sector}")

    match sector:
        case "Stationary Energy":
            return "extraction_agent_actval_stationary_energy"
        case "Transportation":
            return "extraction_agent_actval_transportation"
        case "Waste":
            return "extraction_agent_actval_waste"
        case _:
            print("\nNo matching sector or sub-sector found. Ending workflow.\n")
            return END


# Define the conditional edge
def should_extraction_actval_transportation_continue(state: AgentState) -> str:
    if state.get("approved_extracted_data_actval_transportation"):
        return END
    return "extraction_agent_actval_transportation"


# Define the conditional edge
def should_code_continue(state: AgentState) -> str:
    if state.get("final_code_output"):
        return "router"
    return "code_generation_agent"


# Define the graph
def create_workflow():
    workflow = StateGraph(AgentState)

    # Add nodes to the graph
    workflow.add_node("summary_agent", summary_agent)
    workflow.add_node("extraction_agent_keyval", extraction_agent_keyval)
    workflow.add_node("extraction_reasoning_agent", extraction_reasoning_agent)
    workflow.add_node(
        "extraction_agent_structured_output", extraction_agent_structured_output
    )
    workflow.add_node("extraction_agent_actval_stationary_energy", default_agent)
    workflow.add_node(
        "extraction_agent_actval_transportation", extraction_agent_actval_transportation
    )
    workflow.add_node(
        "extraction_reasoning_agent_actval_transportation",
        extraction_reasoning_agent_actval_transportation,
    )
    workflow.add_node("extraction_agent_actval_waste", default_agent)
    # workflow.add_node("code_generation_agent", code_generation_agent)
    # workflow.add_node("code_reasoning_agent", code_reasoning_agent)

    # Set the entrypoint
    workflow.set_entry_point("summary_agent")

    # Add edge to end the workflow after summary
    workflow.add_edge("summary_agent", "extraction_agent_keyval")
    workflow.add_edge("extraction_agent_keyval", "extraction_reasoning_agent")

    # Add conditional edge
    workflow.add_conditional_edges(
        "extraction_reasoning_agent",
        should_extraction_continue,
        {
            "extraction_agent_structured_output": "extraction_agent_structured_output",
            "extraction_agent_keyval": "extraction_agent_keyval",
        },
    )

    # Add conditional edge
    workflow.add_conditional_edges(
        "extraction_agent_structured_output",
        router,
        {
            "extraction_agent_actval_stationary_energy": "extraction_agent_actval_stationary_energy",
            "extraction_agent_actval_transportation": "extraction_agent_actval_transportation",
            "extraction_agent_actval_waste": "extraction_agent_actval_waste",
            END: END,
        },
    )

    workflow.add_edge(
        "extraction_agent_actval_transportation",
        "extraction_reasoning_agent_actval_transportation",
    )

    # Add conditional edge
    workflow.add_conditional_edges(
        "extraction_reasoning_agent_actval_transportation",
        should_extraction_actval_transportation_continue,
        {
            "extraction_agent_actval_transportation": "extraction_agent_actval_transportation",
            END: END,
        },
    )

    # workflow.add_edge("code_generation_agent", "code_reasoning_agent")

    # Add conditional edge
    # workflow.add_conditional_edges(
    #     "code_reasoning_agent",
    #     should_code_continue,
    #     {
    #         "code_generation_agent": "code_generation_agent",
    #         END: END,
    #     },
    # )

    return workflow.compile()
