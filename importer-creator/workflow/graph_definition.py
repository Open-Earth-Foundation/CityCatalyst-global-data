from langgraph.graph import StateGraph, END
from state.agent_state import AgentState

# For debugging only
perform_steps = {"step_2": True, "step_3": True, "step_4": True}

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
from agents.step_2.extract_datasource_name_agent_step_2 import (
    extract_datasource_name_agent_step_2,
)
from agents.step_2.extract_actor_name_agent_step_2 import (
    extract_actor_name_agent_step_2,
)
from agents.step_2.extract_sector_agent_step_2 import extract_sector_agent_step_2
from agents.step_2.extract_sub_sector_agent_step_2 import (
    extract_sub_sector_agent_step_2,
)
from agents.step_2.create_final_output_agent_step_2 import (
    create_final_output_agent_step_2,
)
from agents.step_2.extract_scope_agent_step_2 import extract_scope_agent_step_2
from agents.step_2.extract_gpc_refno_agent_step_2 import extract_gpc_refno_agent_step_2

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
from agents.step_3.create_final_output_agent_step_3 import (
    create_final_output_agent_step_3,
)
from agents.step_3.extract_activity_subcategory_1_step_3 import (
    extract_activity_subcategory_1_step_3,
)
from agents.step_3.extract_activity_subcategory_2_step_3 import (
    extract_activity_subcategory_2_step_3,
)

# Import for step 4
from agents.step_4.extract_methodology_name_agent_step_4 import (
    extract_methodology_name_agent_step_4,
)

# Import for Human-in-the-Loop (HITL) agent
from agents.hitl_agent import hitl_agent


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

    # Add nodes for the initial script
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

    # Step 2
    if perform_steps["step_2"]:
        workflow.add_node(
            "extract_datasource_name_agent_step_2", extract_datasource_name_agent_step_2
        )
        workflow.add_node(
            "extract_actor_name_agent_step_2", extract_actor_name_agent_step_2
        )
        workflow.add_node("extract_sector_agent_step_2", extract_sector_agent_step_2)
        workflow.add_node(
            "extract_sub_sector_agent_step_2", extract_sub_sector_agent_step_2
        )
        workflow.add_node(
            "create_final_output_agent_step_2", create_final_output_agent_step_2
        )
        workflow.add_node("extract_scope_agent_step_2", extract_scope_agent_step_2)
        workflow.add_node(
            "extract_gpc_refno_agent_step_2", extract_gpc_refno_agent_step_2
        )

        # Step 2 edges
        workflow.add_edge(
            "create_final_output_agent_initial_script",
            "extract_datasource_name_agent_step_2",
        )
        workflow.add_edge(
            "extract_datasource_name_agent_step_2", "extract_actor_name_agent_step_2"
        )
        workflow.add_edge(
            "extract_actor_name_agent_step_2", "extract_sector_agent_step_2"
        )
        workflow.add_edge(
            "extract_sector_agent_step_2", "extract_sub_sector_agent_step_2"
        )
        workflow.add_edge(
            "extract_sub_sector_agent_step_2", "extract_scope_agent_step_2"
        )
        workflow.add_edge(
            "extract_scope_agent_step_2", "extract_gpc_refno_agent_step_2"
        )
        workflow.add_edge(
            "extract_gpc_refno_agent_step_2", "create_final_output_agent_step_2"
        )

        # Only add step 3 edges if perform_steps["step_3"] is True
        if perform_steps["step_3"]:
            workflow.add_edge(
                "create_final_output_agent_step_2",
                "extract_activity_name_agent_step_3",
            )
    else:
        workflow.add_edge("create_final_output_agent_initial_script", END)

    # Step 3
    if perform_steps["step_3"]:
        workflow.add_node(
            "extract_activity_name_agent_step_3", extract_activity_name_agent_step_3
        )
        workflow.add_node(
            "extract_activity_value_agent_step_3", extract_activity_value_agent_step_3
        )
        workflow.add_node(
            "extract_activity_unit_agent_step_3", extract_activity_unit_agent_step_3
        )
        workflow.add_node(
            "create_final_output_agent_step_3", create_final_output_agent_step_3
        )
        workflow.add_node(
            "extract_activity_subcategory_1_step_3",
            extract_activity_subcategory_1_step_3,
        )
        workflow.add_node(
            "extract_activity_subcategory_2_step_3",
            extract_activity_subcategory_2_step_3,
        )

        # Step 3 edges
        workflow.add_edge(
            "extract_activity_name_agent_step_3", "extract_activity_value_agent_step_3"
        )
        workflow.add_edge(
            "extract_activity_value_agent_step_3", "extract_activity_unit_agent_step_3"
        )
        workflow.add_edge(
            "extract_activity_unit_agent_step_3",
            "extract_activity_subcategory_1_step_3",
        )
        workflow.add_edge(
            "extract_activity_subcategory_1_step_3",
            "extract_activity_subcategory_2_step_3",
        )
        workflow.add_edge(
            "extract_activity_subcategory_2_step_3", "create_final_output_agent_step_3"
        )

        # Only add step 4 edges if perform_steps["step_4"] is True
        if perform_steps["step_4"]:
            workflow.add_edge(
                "create_final_output_agent_step_3",
                "extract_methodology_name_agent_step_4",
            )

    else:
        if perform_steps["step_2"]:
            workflow.add_edge("create_final_output_agent_step_2", END)
        else:
            workflow.add_edge("create_final_output_agent_initial_script", END)

    # Step 4
    if perform_steps["step_4"]:
        workflow.add_node(
            "extract_methodology_name_agent_step_4",
            extract_methodology_name_agent_step_4,
        )
        workflow.add_edge("extract_methodology_name_agent_step_4", END)

    else:
        if perform_steps["step_3"]:
            workflow.add_edge("create_final_output_agent_step_3", END)
        elif perform_steps["step_2"]:
            workflow.add_edge("create_final_output_agent_step_2", END)
        else:
            workflow.add_edge("create_final_output_agent_initial_script", END)

    # Set the entry point
    workflow.set_entry_point("setup_agent_initial_script")

    return workflow.compile()
