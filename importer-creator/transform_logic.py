from state.agent_state import AgentState
from workflow.graph_definition import create_workflow
from utils.graph_renderer import render_graph
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


# Function to run the workflow and process the dataframe
def process_datafile(
    full_path: str,
    datasource_name: str,
    user_input: str,
    verbose: bool,
    show_graph: bool,
    hitl: bool,
):

    # Create the workflow and render the graph
    app = create_workflow()
    if show_graph:
        render_graph(app)

    inputs = {
        "full_path": full_path,
        "datasource_name": datasource_name,
        "user_input": user_input,
        "feedback_hitl": "",
        "verbose": verbose,
        "hitl": hitl,
    }

    result = app.invoke(inputs)
    return result


# Main function to call
def transform(
    full_path: str,
    datasource_name: str,
    user_input: str,
    verbose: bool,
    show_graph: bool,
    hitl: bool,
):

    state = process_datafile(
        full_path=full_path,
        datasource_name=datasource_name,
        user_input=user_input,
        verbose=verbose,
        show_graph=show_graph,
        hitl=hitl,
    )

    return state
