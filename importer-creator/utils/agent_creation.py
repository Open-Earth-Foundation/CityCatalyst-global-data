import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor
from langchain_experimental.agents import create_pandas_dataframe_agent

model = "gpt-4o"


# Create pandas dataframe agent
def create_agent(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

    # Initialize the LLM
    llm = ChatOpenAI(model=model, temperature=0)

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
    llm = ChatOpenAI(model=model, temperature=0)
    # llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)

    return create_pandas_dataframe_agent(
        llm,
        df,
        verbose=verbose,
        agent_type="tool-calling",
        # max_iterations=5, # this value can be adapted to speed up the process but potentially decrease accuracy
        allow_dangerous_code=True,
    )
