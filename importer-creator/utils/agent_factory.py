# agent_factory.py
import pandas as pd
from utils.agent_creation import llm_with_structured_output, create_coding_agent


class AgentFactory:
    _structured_output_agent = None
    _coding_agent = None

    @staticmethod
    def get_structured_output_agent(verbose: bool):
        """
        Returns a pre-initialized structured output agent. Initializes the agent if it hasn't been created yet.
        """
        if AgentFactory._structured_output_agent is None:
            # Initialize the structured output agent only once
            print("Creating pre-instantiated structured output agent")
            AgentFactory._structured_output_agent = llm_with_structured_output(verbose)
        return AgentFactory._structured_output_agent

    @staticmethod
    def get_coding_agent(df: pd.DataFrame, verbose: bool):
        """
        Returns a pre-initialized coding agent with a pandas DataFrame. Initializes the agent if it hasn't been created yet.
        """
        if AgentFactory._coding_agent is None:
            # Initialize the coding agent only once
            print("Creating pre-instantiated coding agent")
            AgentFactory._coding_agent = create_coding_agent(df, verbose)
        return AgentFactory._coding_agent
