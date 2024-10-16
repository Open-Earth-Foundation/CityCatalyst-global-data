import os
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
        suffix="",
        include_df_in_prompt=False,
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
        # include_df_in_prompt=False,  # test this performance
    )


# Create pandas dataframe agent
def create_structured_output_agent(json_schema: object, verbose: bool) -> AgentExecutor:

    model = "gpt-4o-mini"

    # Initialize the LLM
    llm = ChatOpenAI(model=model, temperature=0, verbose=verbose)
    structured_llm = llm.with_structured_output(json_schema)

    return structured_llm


class FilterDataInput(BaseModel):
    filters: str = Field(
        ...,
        description="Filters in the format 'column1=value1, column2=value2'. Example: 'actor_name=world, gpc_refno=I.1.1'",
    )


# Create pandas dataframe agent with RAG capabilities and the FilterData tool
# This agent is used for extraction_agent_transformations_stationary_energy_transportation.py
def create_agent_with_rag_and_csv_filter(
    df: pd.DataFrame, verbose: bool
) -> AgentExecutor:

    model = "gpt-4o-2024-08-06"

    ### Setup for the FilterData tool

    # Load the entire CSV file into a DataFrame
    file_path = "./emission_factors/emission_factors_vAI.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    # Define the filter_data_func that uses the loaded DataFrame
    def filter_data_func(filters: str) -> str:
        """Filter the DataFrame based on given filters.

        Args:
            filters (str): A string where filters are specified in the format 'column=value, column2=value2'

        Returns:
            str: A string representation of the filtered DataFrame.
        """
        # Parse filters string into a dict
        filters_dict = {}
        filters_list = filters.split(",")
        for f in filters_list:
            f = f.strip()
            if "=" in f:
                column, value = f.split("=", 1)
                column = column.strip()
                value = value.strip()
                filters_dict[column] = value

        # Apply filters to the DataFrame
        filtered_df = df.copy()
        for column, value in filters_dict.items():
            if column in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[column] == value]
            else:
                return f"Column '{column}' not found in DataFrame."

        if not filtered_df.empty:
            # Return the filtered DataFrame as a string without any row limit
            return filtered_df.to_string(index=False)
        else:
            return "No data found matching the filters."

    # Create the FilterData tool
    filter_data_tool = StructuredTool(
        name="FilterData",
        func=filter_data_func,
        args_schema=FilterDataInput,
        description="""
Use this tool to filter the DataFrame 'df' based on specific criteria.
Provide filters in the format 'column1=value1, column2=value2'.
This tool helps you retrieve emission factors without overloading the context window.
""",
    )

    ### Setup for the Retriever tool

    # Load the retriever (assumed to be defined elsewhere)
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
Also use this tool for all analysis you are doing on the data file related to sectors, subsectors, scopes, activity data, emission values, and so on.

On inputs like: "What is the associated sector according to Greenhouse Gas Protocol for Cities (GPC)" you can provide relevant information about sectors and subsectors from the GPC Master document.
On inputs like: "Your goal is to extract activity data of the Transportation sector from the provided dataframe 'df'." you can provide relevant information about this specific sector, subsectors, scopes, and common activity data from the GPC Master document.
E.g., use this tool when trying to identify the correct scope of activity data based on specific sectors.
""",
    )

    # Initialize the LLM
    llm = ChatOpenAI(model=model, temperature=0)

    # Agent instructions (prefix)
    prefix = """
You are a professional data scientist who is specialized in analyzing and extracting data from complex dataframes.

You have access to three main tools:
1. A Python REPL tool for data analysis, which can be used to manipulate and query the DataFrame 'df'
2. A Retriever tool for fetching relevant information from a Chroma database
3. A FilterData tool to filter 'df' based on specific criteria without overloading the context window.

When using the Python REPL tool:
- Make sure to always import all necessary libraries at the beginning of your code. Especially always import pandas.
    <code>
    import pandas as pd
    </code>
- Do not just use df.head() to make assumptions over the content of the entire dataframe.

When using the Retriever tool:
- Provide clear and concise search queries to get the most relevant information.
- Analyze the retrieved information in the context of the current task.

When using the FilterData tool:
- Use this tool to filter 'df' based on specific criteria.
- Provide filters in the format 'column1=value1, column2=value2'.
- This helps in avoiding overloading the context window with unnecessary data.

Combine insights from all tools to provide comprehensive answers and solutions.
"""

    return create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=verbose,
        agent_type="tool-calling",
        prefix=prefix,
        extra_tools=[retriever_tool, filter_data_tool],
        allow_dangerous_code=True,
    )
