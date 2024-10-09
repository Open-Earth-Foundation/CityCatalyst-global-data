from langgraph.graph import StateGraph, END
from state.agent_state import AgentState

from agents.default_agent import default_agent

# Import for initial script
from agents.initial_script.setup_agent_initial_script import setup_agent_initial_script
from agents.initial_script.delete_cols_agent_initial_script import (
    delete_cols_agent_initial_script,
)
from agents.initial_script.datatypes_agent_initial_script import (
    datatypes_agent_initial_script,
)
from agents.initial_script.create_final_output_agent_initial_script import (
    create_final_output_agent_initial_script,
)

# Import for step 2
from agents.step_2.extract_region_agent_step_2 import extract_region_agent_step_2
from agents.step_2.extract_sector_agent_step_2 import extract_sector_agent_step_2
from agents.step_2.extract_sub_sector_agent_step_2 import (
    extract_sub_sector_agent_step_2,
)
from agents.step_2.create_final_output_agent_step_2 import (
    create_final_output_agent_step_2,
)

# Import for step 3
from agents.step_3.extract_activity_name_agent_step_3 import (
    extract_activity_name_agent_step_3,
)
from agents.step_3.extract_activity_value_agent_step_3 import (
    extract_activity_value_agent_step_3,
)
from agents.step_3.extract_activity_unit_agent_step_3 import (
    extract_activity_unit_agent_step_3,
)

# Import for summary
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

# Import for keyval extraction
from agents.extraction_agent_keyval import extraction_agent_keyval
from agents.reasoning_agent_keyval import reasoning_agent_keyval
from agents.code_generation_agent_keyval import code_generation_agent_keyval
from agents.structured_output_agent_keyval import structured_output_agent_keyval
from agents.create_output_files_agent_keyval import create_output_files_agent_keyval

# Import for router
from agents.router_agent import router_agent

# Imports for activity values
from agents.extraction_agent_actval_stationary_energy_transportation import (
    extraction_agent_actval_stationary_energy_transportation,
)
from agents.code_generation_agent_actval_stationary_energy_transportation import (
    code_generation_agent_actval_stationay_energy_transportation,
)
from agents.structured_output_agent_actval_stationary_energy_transportation import (
    structured_output_agent_actval_stationary_energy_transportation,
)
from agents.create_output_files_agent_actval_stationary_energy_transportation import (
    create_output_files_agent_actval_stationary_energy_transportation,
)

# Imports for GPC mapping
from agents.extraction_agent_gpc_mapping_stationary_energy_transportation import (
    extraction_agent_gpc_mapping_stationary_energy_transportation,
)
from agents.reasoning_agent_gpc_mapping_stationary_energy_transportation import (
    reasoning_agent_gpc_mapping_stationary_energy_transportation,
)
from agents.code_generation_agent_gpc_mapping_stationary_energy_transportation import (
    code_generation_agent_gpc_mapping_stationay_energy_transportation,
)
from agents.structured_output_agent_gpc_refno_stationary_energy_transportation import (
    structured_output_agent_gpc_refno_stationary_energy_transportation,
)
from agents.create_output_files_agent_gpc_refno_stationary_energy_transportation import (
    create_output_files_agent_gpc_refno_stationary_energy_transportation,
)

# Imports for transformation of activity values to emissions data
from agents.extraction_agent_transformations_stationary_energy_transportation import (
    extraction_agent_transformations_stationary_energy_transportation,
)
from agents.code_generation_agent_transformation_stationary_energy_transportation import (
    code_generation_agent_transformation_stationay_energy_transportation,
)
from agents.structured_output_agent_transformation_stationary_energy_transportation import (
    structured_output_agent_transformation_stationary_energy_transportation,
)
from agents.create_output_files_agent_transformation_stationary_energy_transportation import (
    create_output_files_agent_transformation_stationary_energy_transportation,
)

from agents.hitl_agent import hitl_agent


# Define the conditional edge
def should_extraction_continue(state: AgentState) -> str:
    if state.get("approved_extracted_data_keyval"):
        return "code_generation_agent_keyval"
    return "extraction_agent_keyval"


# Define the router conditional edge
def router(state: AgentState) -> str:
    """
    This function is used to route the extraction agent output to the appropriate agent based on the sector and sub-sector extracted.
    If no matching sector or sub-sector is extracted, the workflow ends.
    """

    structured_output_code_keyval = state.get("structured_output_code_keyval")[
        "extracted_data"
    ]
    sector = structured_output_code_keyval.get("sector")

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
        return "code_generation_agent_gpc_mapping_stationay_energy_transportation"
    return "extraction_agent_gpc_mapping_stationary_energy_transportation"


def should_codegeneration_stationary_energy_transportation_continue(
    state: AgentState,
) -> str:
    if state.get("final_code_output"):
        return "structured_output_agent_stationary_energy_transportation"
    return "code_generation_agent_stationary_energy_transportation"


def has_user_provided_feedback(
    state: AgentState,
    return_node: str,
    next_node: str,
) -> str:

    feedback: str = state.get("feedback_hitl")

    if feedback == "NO FEEDBACK":
        return next_node
    else:
        return return_node


# Define the graph
def create_workflow():
    workflow = StateGraph(AgentState)

    # Add nodes to the graph

    # Initial script
    workflow.add_node("summary_agent", summary_agent)
    workflow.add_node("setup_agent_initial_script", setup_agent_initial_script)
    workflow.add_node(
        "delete_cols_agent_initial_script", delete_cols_agent_initial_script
    )
    workflow.add_node("datatypes_agent_initial_script", datatypes_agent_initial_script)
    workflow.add_node(
        "create_final_output_agent_initial_script",
        create_final_output_agent_initial_script,
    )

    workflow.add_edge("setup_agent_initial_script", "delete_cols_agent_initial_script")
    workflow.add_edge(
        "delete_cols_agent_initial_script", "datatypes_agent_initial_script"
    )
    workflow.add_edge(
        "datatypes_agent_initial_script", "create_final_output_agent_initial_script"
    )
    workflow.add_edge(
        "create_final_output_agent_initial_script", "extract_region_agent_step_2"
    )

    # Step 2
    workflow.add_node("extract_region_agent_step_2", extract_region_agent_step_2)
    workflow.add_node("extract_sector_agent_step_2", extract_sector_agent_step_2)
    workflow.add_node(
        "extract_sub_sector_agent_step_2", extract_sub_sector_agent_step_2
    )
    workflow.add_node(
        "create_final_output_agent_step_2", create_final_output_agent_step_2
    )

    workflow.add_edge("extract_region_agent_step_2", "extract_sector_agent_step_2")
    workflow.add_edge("extract_sector_agent_step_2", "extract_sub_sector_agent_step_2")
    workflow.add_edge(
        "extract_sub_sector_agent_step_2", "create_final_output_agent_step_2"
    )
    workflow.add_edge(
        "create_final_output_agent_step_2", "extract_activity_name_agent_step_3"
    )

    # Step 3
    workflow.add_node(
        "extract_activity_name_agent_step_3", extract_activity_name_agent_step_3
    )
    workflow.add_node(
        "extract_activity_value_agent_step_3", extract_activity_value_agent_step_3
    )
    workflow.add_node(
        "extract_activity_unit_agent_step_3", extract_activity_unit_agent_step_3
    )

    workflow.add_edge(
        "extract_activity_name_agent_step_3", "extract_activity_value_agent_step_3"
    )
    workflow.add_edge(
        "extract_activity_value_agent_step_3", "extract_activity_unit_agent_step_3"
    )
    workflow.add_edge("extract_activity_unit_agent_step_3", END)

    ### Below old flow
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
    workflow.add_node("hitl_agent_1", hitl_agent)

    # Keyval extraction
    workflow.add_node("extraction_agent_keyval", extraction_agent_keyval)
    workflow.add_node("reasoning_agent_keyval", reasoning_agent_keyval)
    workflow.add_node("code_generation_agent_keyval", code_generation_agent_keyval)
    workflow.add_node("structured_output_agent_keyval", structured_output_agent_keyval)
    workflow.add_node(
        "create_output_files_agent_keyval", create_output_files_agent_keyval
    )
    workflow.add_node("hitl_agent_2", hitl_agent)

    # Router
    workflow.add_node("router_agent", router_agent)

    # Activity values extraction
    workflow.add_node(
        "extraction_agent_actval_stationary_energy_transportation",
        extraction_agent_actval_stationary_energy_transportation,
    )
    workflow.add_node(
        "code_generation_agent_actval_stationay_energy_transportation",
        code_generation_agent_actval_stationay_energy_transportation,
    )
    workflow.add_node(
        "structured_output_agent_actval_stationary_energy_transportation",
        structured_output_agent_actval_stationary_energy_transportation,
    )
    workflow.add_node(
        "create_output_files_agent_actval_stationary_energy_transportation",
        create_output_files_agent_actval_stationary_energy_transportation,
    )
    workflow.add_node("hitl_agent_3", hitl_agent)

    # GPC mapping extraction
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
        "code_generation_agent_gpc_mapping_stationay_energy_transportation",
        code_generation_agent_gpc_mapping_stationay_energy_transportation,
    )
    workflow.add_node(
        "structured_output_agent_gpc_refno_stationary_energy_transportation",
        structured_output_agent_gpc_refno_stationary_energy_transportation,
    )
    workflow.add_node(
        "create_output_files_agent_gpc_refno_stationary_energy_transportation",
        create_output_files_agent_gpc_refno_stationary_energy_transportation,
    )
    workflow.add_node("hitl_agent_4", hitl_agent)

    # Transformation of activity values to emissions data
    workflow.add_node(
        "extraction_agent_transformations_stationary_energy_transportation",
        extraction_agent_transformations_stationary_energy_transportation,
    )
    workflow.add_node(
        "code_generation_agent_transformation_stationay_energy_transportation",
        code_generation_agent_transformation_stationay_energy_transportation,
    )
    workflow.add_node(
        "structured_output_agent_transformation_stationary_energy_transportation",
        structured_output_agent_transformation_stationary_energy_transportation,
    )
    workflow.add_node(
        "create_output_files_agent_transformation_stationary_energy_transportation",
        create_output_files_agent_transformation_stationary_energy_transportation,
    )
    workflow.add_node("hitl_agent_5", hitl_agent)

    # Set the entrypoint
    # workflow.set_entry_point("summary_agent")
    workflow.set_entry_point("setup_agent_initial_script")

    # Add edge to end the workflow after summary
    workflow.add_edge("summary_agent", "code_generation_agent_initial_script")

    workflow.add_edge(
        "code_generation_agent_initial_script",
        "structured_output_code_agent_initial_script",
    )

    # # Parallel execution 1
    workflow.add_edge(
        "structured_output_code_agent_initial_script",
        "create_output_files_agent_initial_script",
    )
    # Parallel execution 2
    workflow.add_edge(
        "structured_output_code_agent_initial_script",
        "hitl_agent_1",
    )

    # Add conditional edge
    workflow.add_conditional_edges(
        "hitl_agent_1",
        lambda state: has_user_provided_feedback(
            state,
            return_node="summary_agent",
            next_node="extraction_agent_keyval",
        ),
        {
            "summary_agent": "summary_agent",
            "extraction_agent_keyval": "extraction_agent_keyval",
        },
    )

    workflow.add_edge("extraction_agent_keyval", "reasoning_agent_keyval")

    # Add conditional edge
    workflow.add_conditional_edges(
        "reasoning_agent_keyval",
        should_extraction_continue,
        {
            "code_generation_agent_keyval": "code_generation_agent_keyval",
            "extraction_agent_keyval": "extraction_agent_keyval",
        },
    )

    workflow.add_edge("code_generation_agent_keyval", "structured_output_agent_keyval")
    workflow.add_edge(
        "structured_output_agent_keyval", "create_output_files_agent_keyval"
    )

    workflow.add_edge("structured_output_agent_keyval", "hitl_agent_2")

    # Add conditional edge
    workflow.add_conditional_edges(
        "hitl_agent_2",
        lambda state: has_user_provided_feedback(
            state,
            return_node="extraction_agent_keyval",
            next_node="router_agent",
        ),
        {
            "extraction_agent_keyval": "extraction_agent_keyval",
            "router_agent": "router_agent",
        },
    )

    # Add conditional edge
    workflow.add_conditional_edges(
        "router_agent",
        router,
        {
            "extraction_agent_actval_stationary_energy_transportation": "extraction_agent_actval_stationary_energy_transportation",
            "extraction_agent_actval_waste": "extraction_agent_actval_waste",
            END: END,
        },
    )

    workflow.add_edge(
        "extraction_agent_actval_stationary_energy_transportation",
        "code_generation_agent_actval_stationay_energy_transportation",
    )

    workflow.add_edge(
        "code_generation_agent_actval_stationay_energy_transportation",
        "structured_output_agent_actval_stationary_energy_transportation",
    )
    # Parallel execution 1
    workflow.add_edge(
        "structured_output_agent_actval_stationary_energy_transportation",
        "create_output_files_agent_actval_stationary_energy_transportation",
    )
    # Parallel execution 2
    workflow.add_edge(
        "structured_output_agent_actval_stationary_energy_transportation",
        "hitl_agent_3",
    )

    # Add conditional edge
    workflow.add_conditional_edges(
        "hitl_agent_3",
        lambda state: has_user_provided_feedback(
            state,
            return_node="extraction_agent_actval_stationary_energy_transportation",
            next_node="extraction_agent_gpc_mapping_stationary_energy_transportation",
        ),
        {
            "extraction_agent_actval_stationary_energy_transportation": "extraction_agent_actval_stationary_energy_transportation",
            "extraction_agent_gpc_mapping_stationary_energy_transportation": "extraction_agent_gpc_mapping_stationary_energy_transportation",
        },
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
            "code_generation_agent_gpc_mapping_stationay_energy_transportation": "code_generation_agent_gpc_mapping_stationay_energy_transportation",
        },
    )

    workflow.add_edge(
        "code_generation_agent_gpc_mapping_stationay_energy_transportation",
        "structured_output_agent_gpc_refno_stationary_energy_transportation",
    )
    # Parallel execution 1
    workflow.add_edge(
        "structured_output_agent_gpc_refno_stationary_energy_transportation",
        "create_output_files_agent_gpc_refno_stationary_energy_transportation",
    )
    # Parallel execution 2
    workflow.add_edge(
        "structured_output_agent_gpc_refno_stationary_energy_transportation",
        "hitl_agent_4",
    )

    # Add conditional edge
    workflow.add_conditional_edges(
        "hitl_agent_4",
        lambda state: has_user_provided_feedback(
            state,
            return_node="extraction_agent_gpc_mapping_stationary_energy_transportation",
            next_node="extraction_agent_transformations_stationary_energy_transportation",
        ),
        {
            "extraction_agent_gpc_mapping_stationary_energy_transportation": "extraction_agent_gpc_mapping_stationary_energy_transportation",
            "extraction_agent_transformations_stationary_energy_transportation": "extraction_agent_transformations_stationary_energy_transportation",
        },
    )

    workflow.add_edge(
        "extraction_agent_transformations_stationary_energy_transportation",
        "code_generation_agent_transformation_stationay_energy_transportation",  # "code_generation_agent_stationary_energy_transportation",
    )
    workflow.add_edge(
        "code_generation_agent_transformation_stationay_energy_transportation",
        "structured_output_agent_transformation_stationary_energy_transportation",
    )
    # Parallel execution 1
    workflow.add_edge(
        "structured_output_agent_transformation_stationary_energy_transportation",
        "create_output_files_agent_transformation_stationary_energy_transportation",
    )
    # Parallel execution 2
    workflow.add_edge(
        "structured_output_agent_transformation_stationary_energy_transportation",
        "hitl_agent_5",
    )

    # Add conditional edge
    workflow.add_conditional_edges(
        "hitl_agent_5",
        lambda state: has_user_provided_feedback(
            state,
            return_node="extraction_agent_transformations_stationary_energy_transportation",
            next_node=END,
        ),
        {
            "extraction_agent_transformations_stationary_energy_transportation": "extraction_agent_transformations_stationary_energy_transportation",
            END: END,
        },
    )

    return workflow.compile()
