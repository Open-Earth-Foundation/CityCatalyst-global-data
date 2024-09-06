from state.agent_state import AgentState
from utils.agent_creation import create_agent, create_coding_agent
from utils.data_loader import load_datafile_into_df
from workflow.graph_definition import create_workflow

from context.context_sector_subsector import context_sector_subsector
from context.context_activity_values_transportation import (
    context_activity_values_transportation,
)

from utils.graph_renderer import render_graph

from dotenv import load_dotenv

# Load the .env file
load_dotenv()


# Function to run the workflow and process the dataframe
def process_datafile(
    context_user_provided: str,
    file_path: str,
    verbose: bool,
    show_graph: bool,
):

    # Load the datafile into a dataframe
    df = load_datafile_into_df(file_path)

    # Create the agents
    agent = create_agent(df, verbose)
    coding_agent = create_coding_agent(df, verbose)

    # Create the workflow and render the graph
    app = create_workflow()
    if show_graph:
        render_graph(app)

    inputs = AgentState(
        agent=agent,
        coding_agent=coding_agent,
        context_user_provided=context_user_provided,
        context_sector_subsector=context_sector_subsector,
        context_activity_values_transportation=context_activity_values_transportation,
        file_path=file_path,
        summary="",
        extracted_data="",
        structured_extracted_data={},
        reasoning_agent_feedback="",
        final_output={},
        reasoning_agent_iterations=0,
        extracted_data_actval_transportation="",
        structured_extracted_data_actval_transportation={},
        generated_code="",
        code_reasoning_agent_feedback="",
        code_reasoning_agent_iterations=0,
        final_code_output="",
    )

    result = app.invoke(inputs)
    return result


# Main function to call
def transform(file_path, context_user_provided, verbose, show_graph):

    state = process_datafile(
        context_user_provided=context_user_provided,
        file_path=file_path,
        verbose=verbose,
        show_graph=show_graph,
    )

    generated_script = state.get("final_code_output")

    return generated_script
