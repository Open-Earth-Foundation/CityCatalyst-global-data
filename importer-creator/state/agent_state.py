from typing import TypedDict, Annotated
from langchain.agents import AgentExecutor


# Define the state
class AgentState(TypedDict):
    agent: Annotated[AgentExecutor, "The pre-instantiated agent"]
    context: Annotated[str, "The context of the gpc sectors and sub-sectors"]
    user_provided_context: Annotated[str, "The user provided context"]
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
