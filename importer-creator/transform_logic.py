import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor
from langchain_experimental.agents import create_pandas_dataframe_agent

from context_data import sector_sub_sector_context
from agent_tasks import (
    task_extraction_agent,
    task_reasoning_agent,
    task_code_generation_agent,
    task_code_reasoning_agent,
)

from dotenv import load_dotenv

# Load the .env file
load_dotenv()


# Define the state
class AgentState(TypedDict):
    agent: Annotated[AgentExecutor, "The pre-instantiated agent"]
    context: Annotated[str, "The context of the gpc sectors and sub-sectors"]
    user_provided_context: Annotated[str, "The user provided context"]
    pandas_df: Annotated[pd.DataFrame, "The input pandas DataFrame"]
    file_path: Annotated[str, "The file path of the original data file"]
    summary: Annotated[str, "Summary and detailed description of the file"]
    extracted_data: Annotated[dict, "Extracted specific data from the file"]
    reasoning_agent_feedback: Annotated[str, "Feedback from the reasoning agent"]
    final_output: Annotated[dict, "Final approved output"]
    reasoning_agent_iterations: Annotated[
        int, "Number of iterations by the reasoning agent"
    ]
    coding_agent: Annotated[AgentExecutor, "The pre-instantiated coding agent"]
    generated_code: Annotated[str, "Generated code"]
    code_reasoning_agent_feedback: Annotated[
        str, "Feedback from the code reasoning agent"
    ]
    code_reasoning_agent_iterations: Annotated[
        int, "Number of iterations by the code reasoning agent"
    ]
    final_code_output: Annotated[str, "Final code output"]


def load_datafile_into_df(file_path):

    # Check if the file exists and its type
    if os.path.exists(file_path):
        print(f"File found: {os.path.basename(file_path)}")
        if file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)

        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)

        else:
            print("Unsupported file type. Please provide a CSV or Excel file.")
            return None

        return df
    else:
        print(f"File not found: {os.path.basename(file_path)}")


def transform(file_path, user_provided_context, verbose):
    # Transformation logic

    # Create pandas dataframe agent
    def create_agent(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

        # Initialize the LLM
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        return create_pandas_dataframe_agent(
            llm,
            df,
            verbose=verbose,
            agent_type="tool-calling",
            allow_dangerous_code=True,
        )

    # Create agent for code generation
    def create_coding_agent(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

        # Initialize the LLM
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        # llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)

        return create_pandas_dataframe_agent(
            llm,
            df,
            verbose=verbose,
            agent_type="tool-calling",
            # return_intermediate_steps=True,
            # max_iterations=5, # this value can be adapted to speed up the process but potentially decrease accuracy
            allow_dangerous_code=True,
        )

    def summary_agent(state: AgentState) -> dict:
        print("\nSUMMARY AGENT\n")

        # Provide a detailed summary of this DataFrame {state['pandas_df']}.

        prompt = f"""
        ### Task ###
        Provide a detailed summary of the provided DataFrame 'df'.
        Include information about its structure, data types, basic statistics, and any notable patterns or insights.
            
        1. First give a general summary about the content of the data.

        2. Then describe the format of the dataframe in detail. Pay special attention to the following points:
            - nuber of rows and columns
                * are the number of columns consistent throughout the rows? Or is there a mismatch?
            - column names
                * what are the column names?
                * is the same naming convention used?
                * are there spaces before or after the names that could lead to issues?
            - which columns contain dates? The name of the column could be an indicator but check also for values inside the rows
            - data types of each column
            - any missing values
            - additional potential formatting issues with the original file
                * especially if the file contains additional text information that is not part of the actual data but 
                data that is added manually on top of the actual rows e.g. meta data.
                * especially if the file contains additional text information that is not part of the actual data but
                data that is added below the actual rows e.g. footnotes.

        Give thoughts about how to solve these issues based on your analysis.
            
        ### Additional information ###
        This is the user provided context: {state['user_provided_context']}.
        This is the path to the original data file: {state['file_path']}.  
        """

        # Invoke summary agent with custom prompt
        summary = state["agent"].invoke(prompt)
        return {"summary": summary.get("output")}

    def extraction_agent(state: AgentState) -> dict:
        print("\nEXTRACTION AGENT\n")

        # print("\n", state["reasoning_agent_feedback"], "\n")

        # Agent logic to extract specific data
        prompt = f"""
        ### Task ###
        {task_extraction_agent}

        ### Additional information ###
        This is the provided context: {state['context']},
        This is the user provided context: {state['user_provided_context']},
        This is the summary of the previous agent: {state['summary']}.
        This is the path to the original data file: {state['file_path']}.

        If you have received feedback from the reasoning agent, you find it here: {state['reasoning_agent_feedback']}
        If feedback is available, pay special attention to this feedback and incorporate into your data extracation process.
        """
        # This is the orgignal dataframe 'df': {state['pandas_df']}.

        extracted_data = state["agent"].invoke(prompt)

        return {"extracted_data": extracted_data.get("output")}

    def reasoning_agent(state: AgentState) -> dict:
        print("\nREASONING AGENT\n")

        # Check if the iteration limit has been reached
        if state["reasoning_agent_iterations"] >= 5:
            print(
                "\nIteration limit reached. Automatically approving the extraction agent's output.\n"
            )
            return {"final_output": state["extracted_data"]}

        #             1. the original pandas dataframe: {state['pandas_df']},

        prompt = f"""
        ### Task ###
        {task_reasoning_agent}

        ### Additional information ###
        This is the provided context: {state['context']},
        This is the user provided context: {state['user_provided_context']},
        This is the summary of the previous agent: {state['summary']}.
        This is the path to the original data file: {state['file_path']}.
        This is the extracted data of the previous agent: {state['extracted_data']}, which only contains a json without further explanations. Only check if the values are correctly extracted.

        If you have given previous feedback to the extraction agent, you find it here: {state['reasoning_agent_feedback']}
        If you have given feedback, check the extracted data of the agent against your feedback. 
        If the extracted data aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
        """

        response = state["agent"].invoke(prompt)

        if "APPROVED" in response.get("output"):

            return {"final_output": state["extracted_data"]}
        else:
            return {
                "reasoning_agent_feedback": response.get("output"),
                "reasoning_agent_iterations": state["reasoning_agent_iterations"] + 1,
            }

    #         This is the pandas dataframe of the original data file: {state['pandas_df']}.
    # Define code generation agent
    def code_generation_agent(state: AgentState) -> dict:
        print("\nCODE GENERATION AGENT\n")

        prompt = f"""
        ### Task ###
        {task_code_generation_agent}
        
        ### Additional information ###
        This is the summary of the previous agent: {state['summary']}.
        This is the extracted data from the previous agent: {state['final_output']}.
        This is the file name of the original data file: {state['file_path']}.

        If you have received feedback from the 'code reasoning agent', you find it here: {state['code_reasoning_agent_feedback']}.
        If feedback is available, pay special attention to this feedback and incorporate into your data extracation process.
        Especially pay attention to feedback related to errors in code. 
        """

        # Invoke code agent with custom prompt
        response = state["coding_agent"].invoke(prompt)

        return {"generated_code": response.get("output")}

    def code_reasoning_agent(state: AgentState) -> dict:
        print("\nCODE REASONING AGENT\n")

        # Check if the iteration limit has been reached
        if state["code_reasoning_agent_iterations"] >= 5:
            print(
                "\nIteration limit reached. Automatically approving the last output of the code generation agent.\n"
            )
            return {"final_code_output": state["generated_code"]}

        prompt = f"""
        ### Task ###
        {task_code_reasoning_agent}

        ### Additional information ###
        This is the generated code of the previous agent: {state['generated_code']}.
        This is the file name of the original data file: {state['file_path']}.

        If you have given previous feedback to the code generation agent, you find it here: {state['code_reasoning_agent_feedback']}.
        If you have given feedback, check the generated code of the previous agent against your feedback. 
        If the generated code aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
        """
        response = state["coding_agent"].invoke(prompt)

        if "APPROVED" in response.get("output"):
            return {"final_code_output": state["generated_code"]}
        else:
            return {
                "code_reasoning_agent_feedback": response.get("output"),
                "code_reasoning_agent_iterations": state[
                    "code_reasoning_agent_iterations"
                ]
                + 1,
            }

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
        df: pd.DataFrame,
        file_path: str,
        verbose: bool = False,
    ):

        agent = create_agent(df, verbose)
        coding_agent = create_coding_agent(df, verbose)
        app = create_workflow()

        inputs = AgentState(
            agent=agent,
            context=context,
            user_provided_context=user_provided_context,
            pandas_df=df,
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

    df = load_datafile_into_df(file_path)

    state = process_dataframe(
        context=sector_sub_sector_context,
        user_provided_context=user_provided_context,
        df=df,
        file_path=file_path,
        verbose=verbose,
    )

    generated_script = state.get("final_code_output")

    return generated_script
