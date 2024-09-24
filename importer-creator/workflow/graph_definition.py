from langgraph.graph import StateGraph, END
from state.agent_state import AgentState

from agents.default_agent import default_agent
from agents.summary_agent import summary_agent

from agents.code_generation_agent_initial_script import (
    code_generation_agent_initial_script,
)
from agents.structured_output_code_agent_initial_script import (
    structured_output_code_agent_initial_script,
)
from agents.create_output_files_agent_initial_script import (
    create_output_files_agent_initial_script,
)

from agents.extraction_agent_keyval import extraction_agent_keyval
from agents.reasoning_agent_keyval import reasoning_agent_keyval
from agents.structured_output_agent_keyval import structured_output_agent_keyval


from agents.extraction_agent_actval_stationary_energy_transportation import (
    extraction_agent_actval_stationary_energy_transportation,
)

from agents.extraction_agent_gpc_mapping_stationary_energy_transportation import (
    extraction_agent_gpc_mapping_stationary_energy_transportation,
)
from agents.reasoning_agent_gpc_mapping_stationary_energy_transportation import (
    reasoning_agent_gpc_mapping_stationary_energy_transportation,
)

from agents.transformation_agent_stationary_energy_transportation import (
    transformation_agent_stationary_energy_transportation,
)

from agents.code_generation_agent_stationary_energy_transportation import (
    code_generation_agent_stationary_energy_transportation,
)

from agents.reasoning_agent_code_generation_stationary_energy_transportation import (
    reasoning_agent_code_generation_stationary_energy_transportation,
)

from agents.structured_output_agent_stationary_energy_transportation import (
    structured_output_agent_stationary_energy_transportation,
)

from agents.create_output_files_agent import create_output_files_agent

from agents.hitl_agent import hitl_agent


# Define the conditional edge
def should_extraction_continue(state: AgentState) -> str:
    if state.get("approved_extracted_data_keyval"):
        return "structured_output_agent_keyval"
    return "extraction_agent_keyval"


# Define the router conditional edge
def router(state: AgentState) -> str:
    """
    This function is used to route the extraction agent output to the appropriate agent based on the sector and sub-sector extracted.
    If no matching sector or sub-sector is extracted, the workflow ends.
    """

    structured_output_keyval = state.get("structured_output_keyval")
    sector = structured_output_keyval.get("sector")

    match sector:
        case "Stationary Energy":
            return "extraction_agent_actval_stationary_energy_transportation"
        case "Transportation":
            return "extraction_agent_actval_stationary_energy_transportation"
        case "Waste":
            return "extraction_agent_actval_waste"
        case _:
            print("\nNo matching sector or sub-sector found. Ending workflow.\n")
            return END


# Define the conditional edge
def should_extraction_gpc_mapping_stationary_energy_transportation_continue(
    state: AgentState,
) -> str:
    if state.get("approved_extracted_gpc_mapping_stationary_energy_transportation"):
        return "transformation_agent_stationary_energy_transportation"
    return "extraction_agent_gpc_mapping_stationary_energy_transportation"


def should_codegeneration_stationary_energy_transportation_continue(
    state: AgentState,
) -> str:
    if state.get("final_code_output"):
        return "structured_output_agent_stationary_energy_transportation"
    return "code_generation_agent_stationary_energy_transportation"


def has_user_provided_feedback(
    state: AgentState,
) -> str:

    feedback: str = state.get("feedback_hitl")

    if feedback == "":
        print(
            "\nNo clear command provided. Please either submit 'END' to end the workflow or provide detailed feedback.\n"
        )
        return "hitl_agent"
    elif feedback == "END":
        return END
    else:
        return "extraction_agent_actval_stationary_energy_transportation"


# Define the graph
def create_workflow():
    workflow = StateGraph(AgentState)

    # Add nodes to the graph
    workflow.add_node("summary_agent", summary_agent)

    workflow.add_node(
        "code_generation_agent_initial_script", code_generation_agent_initial_script
    )
    workflow.add_node(
        "structured_output_code_agent_initial_script",
        structured_output_code_agent_initial_script,
    )
    workflow.add_node(
        "create_output_files_agent_initial_script",
        create_output_files_agent_initial_script,
    )

    workflow.add_node("extraction_agent_keyval", extraction_agent_keyval)
    workflow.add_node("reasoning_agent_keyval", reasoning_agent_keyval)
    workflow.add_node("structured_output_agent_keyval", structured_output_agent_keyval)
    workflow.add_node(
        "extraction_agent_actval_stationary_energy_transportation",
        extraction_agent_actval_stationary_energy_transportation,
    )
    workflow.add_node(
        "extraction_agent_gpc_mapping_stationary_energy_transportation",
        extraction_agent_gpc_mapping_stationary_energy_transportation,
    )
    workflow.add_node("extraction_agent_actval_waste", default_agent)
    workflow.add_node(
        "reasoning_agent_gpc_mapping_stationary_energy_transportation",
        reasoning_agent_gpc_mapping_stationary_energy_transportation,
    )
    workflow.add_node(
        "transformation_agent_stationary_energy_transportation",
        transformation_agent_stationary_energy_transportation,
    )
    workflow.add_node(
        "code_generation_agent_stationary_energy_transportation",
        code_generation_agent_stationary_energy_transportation,
    )
    workflow.add_node(
        "reasoning_agent_code_generation_stationary_energy_transportation",
        reasoning_agent_code_generation_stationary_energy_transportation,
    )
    workflow.add_node(
        "structured_output_agent_stationary_energy_transportation",
        structured_output_agent_stationary_energy_transportation,
    )

    workflow.add_node("hitl_agent", hitl_agent)

    workflow.add_node("create_output_files_agent", create_output_files_agent)

    # Set the entrypoint
    workflow.set_entry_point("summary_agent")

    # Add edge to end the workflow after summary
    workflow.add_edge("summary_agent", "code_generation_agent_initial_script")

    workflow.add_edge(
        "code_generation_agent_initial_script",
        "structured_output_code_agent_initial_script",
    )

    workflow.add_edge(
        "structured_output_code_agent_initial_script",
        "create_output_files_agent_initial_script",
    )

    workflow.add_edge(
        "create_output_files_agent_initial_script", "extraction_agent_keyval"
    )

    workflow.add_edge("extraction_agent_keyval", "reasoning_agent_keyval")

    # Add conditional edge
    workflow.add_conditional_edges(
        "reasoning_agent_keyval",
        should_extraction_continue,
        {
            "structured_output_agent_keyval": "structured_output_agent_keyval",
            "extraction_agent_keyval": "extraction_agent_keyval",
        },
    )

    # Add conditional edge
    workflow.add_conditional_edges(
        "structured_output_agent_keyval",
        router,
        {
            "extraction_agent_actval_stationary_energy_transportation": "extraction_agent_actval_stationary_energy_transportation",
            "extraction_agent_actval_waste": "extraction_agent_actval_waste",
            END: END,
        },
    )

    workflow.add_edge(
        "extraction_agent_actval_stationary_energy_transportation",
        "extraction_agent_gpc_mapping_stationary_energy_transportation",
    )

    workflow.add_edge(
        "extraction_agent_gpc_mapping_stationary_energy_transportation",
        "reasoning_agent_gpc_mapping_stationary_energy_transportation",
    )

    # Add conditional edge
    workflow.add_conditional_edges(
        "reasoning_agent_gpc_mapping_stationary_energy_transportation",
        should_extraction_gpc_mapping_stationary_energy_transportation_continue,
        {
            "extraction_agent_gpc_mapping_stationary_energy_transportation": "extraction_agent_gpc_mapping_stationary_energy_transportation",
            "transformation_agent_stationary_energy_transportation": "transformation_agent_stationary_energy_transportation",
        },
    )

    workflow.add_edge(
        "transformation_agent_stationary_energy_transportation",
        END,  # "code_generation_agent_stationary_energy_transportation",
    )

    workflow.add_edge(
        "code_generation_agent_stationary_energy_transportation",
        "reasoning_agent_code_generation_stationary_energy_transportation",
    )

    # Add conditional edge
    workflow.add_conditional_edges(
        "reasoning_agent_code_generation_stationary_energy_transportation",
        should_codegeneration_stationary_energy_transportation_continue,
        {
            "code_generation_agent_stationary_energy_transportation": "code_generation_agent_stationary_energy_transportation",
            "structured_output_agent_stationary_energy_transportation": "structured_output_agent_stationary_energy_transportation",
        },
    )

    workflow.add_edge(
        "structured_output_agent_stationary_energy_transportation",
        "create_output_files_agent",
    )

    workflow.add_edge("create_output_files_agent", "hitl_agent")

    # Add conditional edge
    workflow.add_conditional_edges(
        "hitl_agent",
        has_user_provided_feedback,
        {
            "hitl_agent": "hitl_agent",
            "extraction_agent_actval_stationary_energy_transportation": "extraction_agent_actval_stationary_energy_transportation",
            END: END,
        },
    )

    return workflow.compile()
