import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor
from langchain_experimental.agents import create_pandas_dataframe_agent
from utils.retriever_loader import load_retriever
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


# Create pandas dataframe agent without rag capabilities
def create_agent(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

    model = "gpt-4o-2024-08-06"

    # Initialize the LLM
    llm = ChatOpenAI(model=model, temperature=0)

    return create_pandas_dataframe_agent(
        llm,
        df,
        verbose=verbose,
        agent_type="tool-calling",
        prefix="""
    You are a professional data scientist who is specialized in analyzing and extracting data from complex dataframes.
        
    You have access to one main tool:
    1. A Python REPL tool for data analysis, which can be used to manipulate and query the DataFrame 'df'

    When using the Python REPL tool:
    - make sure to always import all necessary libraries at the beginning of your code. Especially always import pandas.
        <code>
        import pandas as pd
        </code>
    Use the following code to print the entire length of the dataframe:
    - Use the following code to print the entire length of the dataframe:
        <code>
        import pandas as pd
        pd.set_option('display.max_rows', None)  # Show all rows
        pd.set_option('display.max_columns', None)  # Show all columns 
        </code>
    - Do not just use df.head() to make assumptions over the content of the entire dataframe.
    """,
        allow_dangerous_code=True,
    )


# Create agent for code generation
def create_coding_agent(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

    model = "gpt-4o-2024-08-06"

    # Initialize the LLM
    llm = ChatOpenAI(model=model, temperature=0)
    # llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)

    return create_pandas_dataframe_agent(
        llm,
        df,
        verbose=verbose,
        agent_type="tool-calling",
        prefix="""
    You are a professional software engineer who is specialized in creating functional python scripts.

    You have access to one main tool:
    1. A Python REPL tool for data analysis, which can be used to manipulate and query the DataFrame 'df'

    When using the Python REPL tool:
    - make sure to always import all necessary libraries at the beginning of your code. Especially always import pandas.
        <code>
        import pandas as pd
        </code>
    Use the following code to print the entire length of the dataframe:
    - Use the following code to print the entire length of the dataframe:
        <code>
        import pandas as pd
        pd.set_option('display.max_rows', None)  # Show all rows
        pd.set_option('display.max_columns', None)  # Show all columns 
        </code>
    - Do not just use df.head() to make assumptions over the content of the entire dataframe.
    """,
        allow_dangerous_code=True,
    )


class RetrieverInput(BaseModel):
    query: str = Field(..., description="The query to send to the retriever")


# Create pandas dataframe agent with rag capabilities
def create_agent_with_rag(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

    model = "gpt-4o-2024-08-06"

    retriever = load_retriever()

    def retriever_func(query: str) -> str:
        return retriever.invoke(query)

    # Create a tool for the retriever
    retriever_tool = StructuredTool(
        name="Retriever",
        func=retriever_func,
        args_schema=RetrieverInput,
        description="""
    Use this tool to retrieve information from the GPC Master document to enrich the context regarding any tasks related to the data file. 
    Also use this tool for all analysis you are doing on the data file related to sectors, subsectors, scopes, activity data, emission values and so on.
    
    On inputs like: "What is the associated sector according to Greenhouse Gas Protocol for Cities (GPC)" you can provide relevant information about sectors and subsectors from the GPC Master document.
    On inputs like: "Your goal is to extract activity data of the Transportation sector from the provided dataframe 'df'." you can provide relevant information about this specific sector, subsectors, scopes and common activity data from the GPC Master document.
    E.g. use this tool when trying to identify the correct scope of activity data based on specific sectors.
    """,
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
    - make sure to always import all necessary libraries at the beginning of your code. Especially always import pandas.
        <code>
        import pandas as pd
        </code>
    Use the following code to print the entire length of the dataframe:
    - Use the following code to print the entire length of the dataframe:
        <code>
        import pandas as pd
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


# Create pandas dataframe agent
def create_structured_output_agent(json_schema: object, verbose: bool) -> AgentExecutor:

    model = "gpt-4o-mini"

    # Initialize the LLM
    llm = ChatOpenAI(model=model, temperature=0, verbose=verbose)
    structured_llm = llm.with_structured_output(json_schema)

    return structured_llm
