# from utils.agent_creation import (
#     create_coding_agent,
#     create_agent_with_rag,
# )
from utils.data_loader import load_datafile_into_df

# from workflow.graph_definition import create_workflow
from utils.graph_renderer import render_graph
from dotenv import load_dotenv

from state.agent_state import AgentState
from langgraph.graph import StateGraph, END
from state.agent_state import AgentState

from agents.extraction_agent_transformations_stationary_energy_transportation import (
    extraction_agent_transformations_stationary_energy_transportation,
)

# Load the .env file
load_dotenv()


# Function to run the workflow and process the dataframe
def process_datafile(
    context_user_provided: str,
    file_path: str,
    verbose: bool,
    show_graph: bool,
    hitl: bool,
):

    # Load the datafile into a dataframe
    df = load_datafile_into_df(file_path)

    # Create the agents
    # agent = create_agent_with_rag(df, verbose)
    # agent_code = create_coding_agent(df, verbose)

    # Create the workflow and render the graph
    # app = create_workflow()

    # Define the graph
    worklflow = StateGraph(AgentState)

    worklflow.add_node(
        "extraction_agent_transformations_stationary_energy_transportation",
        extraction_agent_transformations_stationary_energy_transportation,
    )
    worklflow.add_edge(
        "extraction_agent_transformations_stationary_energy_transportation", END
    )
    worklflow.set_entry_point(
        "extraction_agent_transformations_stationary_energy_transportation"
    )
    app = worklflow.compile()

    if show_graph:
        render_graph(app)

    inputs = AgentState(
        ### dataframe
        df=df,
        ### file path
        file_path=file_path,
        ### agents
        # agent=agent,
        # agent_code=agent_code,
        ### contexts
        context_user_provided=context_user_provided,
        ### summary
        summary="",
        ### extracted data (output from extraction agents)
        extracted_data_keyval="",
        extracted_data_actval_stationary_energy_transportation="",
        extracted_gpc_mapping_stationary_energy_transportation="""
        The GPC mapping for the 'Stationary Energy' and 'Transportation' sectors is as follows:
        I.1.1
        I.2.2
        II.1.1
        """,
        extracted_data_actval_waste="",
        extracted_transformations_stationary_energy_transportation="",
        ### structured output data (output from structured output agents)
        # structured_output_code_initial_script={},
        # structured_output_code_keyval={},
        # structured_output_code_actval_stationary_energy_transportation={},
        # structured_output_code_gpc_refno_stationary_energy_transportation={},
        # structured_output_code_transformation_stationary_energy_transportation={},
        # structured_output_actval_waste={},
        ### approved data (output from reasoning agent)
        # approved_extracted_data_keyval="",
        # approved_extracted_gpc_mapping_stationary_energy_transportation="",
        # approved_extracted_data_actval_waste="",
        # approved_generated_code="",
        ### feedback (output from reasoning agent)
        # feedback_extracted_data_keyval="",
        # feedback_extracted_gpc_mapping_stationary_energy_transportation="",
        # feedback_extracted_data_actval_waste="",
        # feedback_code_generation_actval_stationary_energy_transportation="",
        feedback_hitl="The dataset is about data in Argentina",
        ### iterators (for reasoning agents)
        # iterator_reasoning_agent_keyval=0,
        # iterator_reasoning_agent_gpc_mapping_stationary_energy_transportation=0,
        # iterator_reasoning_agent_actval_waste=0,
        # iterator_reasoning_agent_code_generation_actval_stationary_energy_transportation=0,
        ### generated code (output from code generation agent)
        # code_initial_script="",
        # code_keyval_script="",
        # code_actval_stationary_energy_transportation_script="",
        # code_gpc_refno_stationary_energy_transportation_script="",
        # code_transformations_stationary_energy_transportation_script="",
        ### verbose
        verbose=verbose,
        ### hitl
        hitl=hitl,
    )

    result = app.invoke(inputs)
    return result


# Main function to call
def transform(file_path, context_user_provided, verbose, show_graph, hitl):

    state = process_datafile(
        context_user_provided=context_user_provided,
        file_path=file_path,
        verbose=verbose,
        show_graph=show_graph,
        hitl=hitl,
    )

    return state


if __name__ == "__main__":
    transform(
        file_path="./files/raw_enargas_gas_consumption_AR.csv",
        context_user_provided="""
        This is a dataset about gas consumptions in the region (actor_name) of Argentina for the gpc sectors 'Stationary Energy' and 'Transportation'
        """,
        verbose=True,
        show_graph=True,
        hitl=False,
    )
