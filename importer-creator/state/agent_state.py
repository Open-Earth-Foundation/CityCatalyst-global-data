import pandas as pd
from typing import TypedDict, Annotated
from langchain.agents import AgentExecutor


# Define the state
class AgentState(TypedDict):
    df: Annotated[pd.DataFrame, "The pandas dataframe"]
    file_path: Annotated[str, "The file path of the original data file"]
    agent: Annotated[AgentExecutor, "The pre-instantiated agent"]
    agent_code: Annotated[AgentExecutor, "The pre-instantiated coding agent"]
    context_user_provided: Annotated[str, "The user provided context"]
    summary: Annotated[str, "Summary and detailed description of the data file"]
    extracted_data_keyval: Annotated[
        str, "Extracted key-value data from the data file with explanations"
    ]
    extracted_data_actval_stationary_energy_transportation: Annotated[
        str,
        "Extracted specific activity values from the data file for the sector 'Stationary Energy' and 'Transportation' with exlanations",
    ]
    extracted_gpc_mapping_stationary_energy_transportation: Annotated[
        str,
        "Extracted gpc mapping values from the data file for the sector 'Stationary Energy' and 'Transportation' with exlanations",
    ]
    extracted_data_actval_waste: Annotated[
        str,
        "Extracted specific activity values from the data file for the sector 'Waste' with exlanations",
    ]
    transformations_stationary_energy_transportation: Annotated[
        str,
        "The transformed activity data to emissions data for the sector 'Stationary Energy' and 'Transportation' with exlanations",
    ]
    structured_output_code_initial_script: Annotated[
        dict, "Structured output for reasoning and initial code script"
    ]
    structured_output_code_keyval: Annotated[
        dict,
        "Structured output for reasoning, code and extracted key-value data from the data file",
    ]
    structured_output_code_actval_stationary_energy_transportation: Annotated[
        dict,
        "Structured output for reasoning and code for extracted activity values from the data file for the sector 'Stationary Energy' and 'Transportation",
    ]
    structured_output_code_gpc_refno_stationary_energy_transportation: Annotated[
        dict,
        "Structured output for reasoning and code for extracted GPC reference numbers from the data file for the sector 'Stationary Energy' and 'Transportation'",
    ]
    # structured_output_stationary_energy_transportation: Annotated[
    #     dict,
    #     "Structured output from the data file for sector 'Stationary Energy' and 'Transportation'",
    # ]
    structured_output_actval_waste: Annotated[
        dict,
        "Structured extracted activity values from the data file for sector 'Waste'",
    ]
    # structured_code: Annotated[dict, "Structured generated code"]
    approved_extracted_data_keyval: Annotated[
        str, "Approved extracted key-value data from the data file with explanations"
    ]
    approved_extracted_gpc_mapping_stationary_energy_transportation: Annotated[
        str,
        "Approved extracted specific activity values for sector 'Stationary Energy' and 'Transportation' with explanations",
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
    feedback_extracted_gpc_mapping_stationary_energy_transportation: Annotated[
        str,
        "Feedback from the reasoning agent for the extracted specific activity values from the data file for the sector 'Stationary Energy' and 'Transportation'",
    ]
    feedback_extracted_data_actval_waste: Annotated[
        str,
        "Feedback from the reasoning agent for the extracted specific activity values from the data file for the sector 'Waste'",
    ]
    feedback_code_generation_actval_stationary_energy_transportation: Annotated[
        str,
        "Feedback from the code reasoning agent for stationart energy and transportation",
    ]
    feedback_hitl: Annotated[str, "Feedback from the user"]
    iterator_reasoning_agent_keyval: Annotated[
        int, "Number of iterations by the reasoning agent"
    ]
    iterator_reasoning_agent_gpc_mapping_stationary_energy_transportation: Annotated[
        int,
        "Number of iterations by the reasoning agent for extracted activity values of stationary energy and transportation",
    ]
    iterator_reasoning_agent_actval_waste: Annotated[
        int,
        "Number of iterations by the reasoning agent for extracted activity values of waste",
    ]
    iterator_reasoning_agent_code_generation_actval_stationary_energy_transportation: Annotated[
        int,
        "Number of iterations by the code reasoning agent for stationary energy and transportation",
    ]
    code_initial_script: Annotated[str, "Initial code script"]
    code_keyval_script: Annotated[str, "Key-value code script"]
    code_actval_stationary_energy_transportation_script: Annotated[
        str, "Activity value code script"
    ]
    code_gpc_refno_stationary_energy_transportation_script: Annotated[
        str, "GPC reference number code script"
    ]
    generated_code: Annotated[str, "Generated code"]
    final_code_output: Annotated[str, "Final code output"]
    verbose: Annotated[bool, "Verbose mode"]
