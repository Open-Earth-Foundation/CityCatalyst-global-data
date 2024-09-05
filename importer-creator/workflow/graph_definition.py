from langgraph.graph import StateGraph, END
from state.agent_state import AgentState

from agents.summary_agent import summary_agent
from agents.extraction_agent import extraction_agent
from agents.reasoning_agent import reasoning_agent
from agents.code_generation_agent import code_generation_agent
from agents.code_reasoning_agent import code_reasoning_agent


# Define the conditional edge
def should_extraction_continue(state: AgentState) -> str:
    if state.get("final_output"):
        return "code_generation_agent"
    return "extraction_agent"


# Define the conditional edge
def should_code_continue(state: AgentState) -> str:
    if state.get("final_code_output"):
        return END
    return "code_generation_agent"


# Define the graph
def create_workflow():
    workflow = StateGraph(AgentState)

    # Add nodes to the graph
    workflow.add_node("summary_agent", summary_agent)
    workflow.add_node("extraction_agent", extraction_agent)
    workflow.add_node("reasoning_agent", reasoning_agent)
    workflow.add_node("code_generation_agent", code_generation_agent)
    workflow.add_node("code_reasoning_agent", code_reasoning_agent)

    # Set the entrypoint
    workflow.set_entry_point("summary_agent")

    # Add edge to end the workflow after summary
    workflow.add_edge("summary_agent", "extraction_agent")
    workflow.add_edge("extraction_agent", "reasoning_agent")

    # Add conditional edge
    workflow.add_conditional_edges(
        "reasoning_agent",
        should_extraction_continue,
        {
            "extraction_agent": "extraction_agent",
            "code_generation_agent": "code_generation_agent",
        },
    )

    workflow.add_edge("code_generation_agent", "code_reasoning_agent")

    # Add conditional edge
    workflow.add_conditional_edges(
        "code_reasoning_agent",
        should_code_continue,
        {
            "code_generation_agent": "code_generation_agent",
            END: END,
        },
    )

    return workflow.compile()
