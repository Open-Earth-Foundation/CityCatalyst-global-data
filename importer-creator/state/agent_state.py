from typing import TypedDict, Annotated
from langchain.agents import AgentExecutor


# Define the state
class AgentState(TypedDict):
    agent: Annotated[AgentExecutor, "The pre-instantiated agent"]
    coding_agent: Annotated[AgentExecutor, "The pre-instantiated coding agent"]
    context_user_provided: Annotated[str, "The user provided context"]
    context_sector_subsector: Annotated[
        str, "The context of the gpc sectors and sub-sectors"
    ]
    context_activity_values_transportation: Annotated[
        str, "The context of the activity values for the sector 'Transportation'"
    ]
    file_path: Annotated[str, "The file path of the original data file"]
    summary: Annotated[str, "Summary and detailed description of the data file"]
    extracted_data: Annotated[
        str, "Extracted specific data from the data file with explanations"
    ]
    structured_extracted_data: Annotated[
        dict, "Structured extracted specific data from the data file"
    ]
    reasoning_agent_feedback: Annotated[str, "Feedback from the reasoning agent"]
    final_output: Annotated[dict, "Final approved output"]
    reasoning_agent_iterations: Annotated[
        int, "Number of iterations by the reasoning agent"
    ]
    extracted_data_actval_transportation: Annotated[
        str,
        "Extracted specific activity values from the data file for the sector 'Transportation' with exlanations",
    ]
    structured_extracted_data_actval_transportation: Annotated[
        dict,
        "Structured extracted specific activity values from the data file for the sector 'Transportation'",
    ]
    generated_code: Annotated[str, "Generated code"]
    code_reasoning_agent_feedback: Annotated[
        str, "Feedback from the code reasoning agent"
    ]
    code_reasoning_agent_iterations: Annotated[
        int, "Number of iterations by the code reasoning agent"
    ]
    final_code_output: Annotated[str, "Final code output"]
