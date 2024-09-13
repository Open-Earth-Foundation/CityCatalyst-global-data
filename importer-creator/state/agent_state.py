from typing import TypedDict, Annotated
from langchain.agents import AgentExecutor


# Define the state
class AgentState(TypedDict):
    file_path: Annotated[str, "The file path of the original data file"]
    agent: Annotated[AgentExecutor, "The pre-instantiated agent"]
    agent_code: Annotated[AgentExecutor, "The pre-instantiated coding agent"]
    context_user_provided: Annotated[str, "The user provided context"]
    context_sector_subsector: Annotated[
        str, "The context of the gpc sectors and subsectors"
    ]
    context_actval_stationary_energy: Annotated[
        str, "The context of the activity values for the sector 'Stationary Energy'"
    ]
    context_actval_transportation: Annotated[
        str, "The context of the activity values for the sector 'Transportation'"
    ]
    context_actval_waste: Annotated[
        str, "The context of the activity values for the sector 'Waste'"
    ]
    summary: Annotated[str, "Summary and detailed description of the data file"]
    extracted_data_keyval: Annotated[
        str, "Extracted key-value data from the data file with explanations"
    ]
    extracted_data_actval_stationary_energy: Annotated[
        str,
        "Extracted specific activity values from the data file for the sector 'Stationary Energy' with exlanations",
    ]
    extracted_data_actval_transportation: Annotated[
        str,
        "Extracted specific activity values from the data file for the sector 'Transportation' with exlanations",
    ]
    extracted_data_actval_waste: Annotated[
        str,
        "Extracted specific activity values from the data file for the sector 'Waste' with exlanations",
    ]
    structured_data_keyval: Annotated[
        dict, "Structured extracted key-value data from the data file"
    ]
    structured_data_actval_stationary_energy: Annotated[
        dict,
        "Structured extracted activity values from the data file for sector 'Stationary Energy'",
    ]
    structured_data_actval_transportation: Annotated[
        dict,
        "Structured extracted activity values from the data file for sector 'Transportation'",
    ]
    structured_data_actval_waste: Annotated[
        dict,
        "Structured extracted activity values from the data file for sector 'Waste'",
    ]
    structured_code: Annotated[dict, "Structured generated code"]
    approved_extracted_data_keyval: Annotated[
        str, "Approved extracted key-value data from the data file with explanations"
    ]
    approved_extracted_data_actval_stationary_energy: Annotated[
        str,
        "Approved extracted specific activity values for sector 'Stationary Energy' with explanations",
    ]
    approved_extracted_data_actval_transportation: Annotated[
        str,
        "Approved extracted specific activity values for sector 'Transportation' with explanations",
    ]
    approved_extracted_data_actval_waste: Annotated[
        str,
        "Approved extracted specific activity values for sector 'Waste' with explanations",
    ]
    approved_generated_code: Annotated[
        str,
        "Approved generated code from the code reasoning agent with explanations",
    ]
    feedback_extracted_data_keyval: Annotated[
        str, "Feedback from the key-value reasoning agent"
    ]
    feedback_extracted_data_actval_stationary_energy_transportation: Annotated[
        str,
        "Feedback from the reasoning agent for the extracted specific activity values from the data file for the sector 'Stationary Energy' and 'Transportation'",
    ]
    feedback_extracted_data_actval_stationary_energy: Annotated[
        str,
        "Feedback from the reasoning agent for the extracted specific activity values from the data file for the sector 'Stationary Energy'",
    ]
    feedback_extracted_data_actval_transportation: Annotated[
        str,
        "Feedback from the reasoning agent for the extracted specific activity values from the data file for the sector 'Transportation'",
    ]
    feedback_extracted_data_actval_waste: Annotated[
        str,
        "Feedback from the reasoning agent for the extracted specific activity values from the data file for the sector 'Waste'",
    ]
    feedback_code_generation: Annotated[str, "Feedback from the code reasoning agent"]
    iterator_reasoning_agent_keyval: Annotated[
        int, "Number of iterations by the reasoning agent"
    ]
    iterator_reasoning_agent_actval_stationary_energy: Annotated[
        int,
        "Number of iterations by the reasoning agent for extracted activity values of stationary energy",
    ]
    iterator_reasoning_agent_actval_transportation: Annotated[
        int,
        "Number of iterations by the reasoning agent for extracted activity values of transportation",
    ]
    iterator_reasoning_agent_actval_waste: Annotated[
        int,
        "Number of iterations by the reasoning agent for extracted activity values of waste",
    ]
    iterator_reasoning_agent_code: Annotated[
        int, "Number of iterations by the code reasoning agent"
    ]
    generated_code: Annotated[str, "Generated code"]
    final_code_output: Annotated[str, "Final code output"]
