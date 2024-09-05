import pandas as pd
from langgraph.graph import StateGraph, END

from state.agent_state import AgentState
from utils.agent_creation import create_agent, create_coding_agent
from agents.summary_agent import summary_agent
from agents.extraction_agent import extraction_agent
from agents.reasoning_agent import reasoning_agent
from agents.code_generation_agent import code_generation_agent
from agents.code_reasoning_agent import code_reasoning_agent
from utils.data_loader import load_datafile_into_df

from context.context_data import sector_sub_sector_context

from dotenv import load_dotenv

# Load the .env file
load_dotenv()


# Transformation logic
def transform(file_path, user_provided_context, verbose):

    # Define the conditional edge
    def should_extraction_continue(state: AgentState) -> str:
        if state.get("final_output"):
            return "code_generatoin_agent"
        return "extraction_agent"

    # Define the conditional edge
    def should_code_continue(state: AgentState) -> str:
        if state.get("final_code_output"):
            return "end"
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
                "code_generatoin_agent": "code_generation_agent",
            },
        )

        workflow.add_edge("code_generation_agent", "code_reasoning_agent")

        # Add conditional edge
        workflow.add_conditional_edges(
            "code_reasoning_agent",
            should_code_continue,
            {
                "code_generation_agent": "code_generation_agent",
                "end": END,
            },
        )

        return workflow.compile()

    # Function to run the workflow
    def process_dataframe(
        context: str,
        user_provided_context: str,
        file_path: str,
        verbose: bool = False,
    ):

        df = load_datafile_into_df(file_path)

        # Create the agents
        agent = create_agent(df, verbose)
        coding_agent = create_coding_agent(df, verbose)

        # Create the workflow
        app = create_workflow()

        inputs = AgentState(
            agent=agent,
            context=context,
            user_provided_context=user_provided_context,
            file_path=file_path,
            summary="",
            extracted_data={},
            reasoning_agent_feedback="",
            final_output={},
            reasoning_agent_iterations=0,
            coding_agent=coding_agent,
            generated_code="",
            code_reasoning_agent_feedback="",
            code_reasoning_agent_iterations=0,
            final_code_output="",
        )

        print(app.get_graph().draw_ascii())

        result = app.invoke(inputs)
        return result

    state = process_dataframe(
        context=sector_sub_sector_context,
        user_provided_context=user_provided_context,
        file_path=file_path,
        verbose=verbose,
    )

    generated_script = state.get("final_code_output")

    return generated_script
