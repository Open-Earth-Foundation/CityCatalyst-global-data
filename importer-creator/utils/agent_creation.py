import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor
from langchain_experimental.agents import create_pandas_dataframe_agent


# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.retriever_loader import load_retriever
from langchain.agents import Tool

model = "gpt-4o-2024-08-06"


# Create pandas dataframe agent
def create_agent(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

    # Initialize the LLM
    llm = ChatOpenAI(model=model, temperature=0)

    return create_pandas_dataframe_agent(
        llm,
        df,
        verbose=verbose,
        agent_type="tool-calling",
        prefix="""
    You are a professional data scientist who is specialized in analyzing and extracting data from complex dataframes.
        
    Use the following code to print the entire length of the dataframe:
    <code>
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.max_columns', None)  # Show all columns 
    </code>
    Do not just use df.head() to make assumptions over the content of the entire dataframe.
    """,
        allow_dangerous_code=True,
    )


# Create agent for code generation
def create_coding_agent(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

    # Initialize the LLM
    llm = ChatOpenAI(model=model, temperature=0)
    # llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)

    return create_pandas_dataframe_agent(
        llm,
        df,
        verbose=verbose,
        agent_type="tool-calling",
        # max_iterations=5, # this value can be adapted to speed up the process but potentially decrease accuracy
        prefix="""
        You are a professional software engineer who is specialized in creating functional python scripts.

        Use the following code to print the entire length of the dataframe:
        <code>
        pd.set_option('display.max_rows', None)  # Show all rows
        pd.set_option('display.max_columns', None)  # Show all columns 
        </code>
        Do not just use df.head() to make assumptions over the content of the entire dataframe.
        """,
        allow_dangerous_code=True,
    )


# Create pandas dataframe agent with rag capabilities
def create_agent_with_rag(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

    retriever = load_retriever()

    # Create a tool for the retriever
    retriever_tool = Tool(
        name="Retriever",
        func=lambda x: retriever.invoke(str(x)),
        description="Use this tool to retrieve information from the GPC Master document to enrich the context regarding any tasks related to the dataframe 'df'.",
    )

    # Initialize the LLM
    llm = ChatOpenAI(model=model, temperature=0)

    return create_pandas_dataframe_agent(
        llm,
        df,
        verbose=verbose,
        agent_type="tool-calling",
        prefix="""
    You are a professional data scientist who is specialized in analyzing and extracting data from complex dataframes.

    You have access to two main tools:
    1. A Python REPL tool for data analysis, which can be used to manipulate and query the DataFrame 'df'
    2. A Retriever tool for fetching relevant information from a Chroma database

    When using the Python REPL tool:
    Use the following code to print the entire length of the dataframe:
    - Use the following code to print the entire length of the dataframe:
        <code>
        pd.set_option('display.max_rows', None)  # Show all rows
        pd.set_option('display.max_columns', None)  # Show all columns 
        </code>
    - Do not just use df.head() to make assumptions over the content of the entire dataframe.

    When using the Retriever tool:
    - Provide clear and concise search queries to get the most relevant information.
    - Analyze the retrieved information in the context of the current task.

    Combine insights from both tools to provide comprehensive answers and solutions.
    """,
        extra_tools=[retriever_tool],
        allow_dangerous_code=True,
    )
