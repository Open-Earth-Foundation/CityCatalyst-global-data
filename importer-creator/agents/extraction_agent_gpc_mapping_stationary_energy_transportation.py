from state.agent_state import AgentState
from context.mappings.mappings_gpc import gpc_mappings
from context.mappings.mappings_transportation import (
    fuel_mapping,
    fuel_to_gpc,
    transport_type_to_gpc,
)
from context.mappings.mappings_stationary_energy import (
    stationary_energy_scope_2_subsector_to_gpc,
)


def extraction_agent_gpc_mapping_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nEXTRACTION AGENT GPC MAPPING STATIONARY ENERGY TRANSPORTATION\n")

    prompt = f"""
Your goal is to create a mapping dictionary of activity data to gpc reference numbers for the two sectors 'Stationary Energy' sector and 'Transportation' sector from the provided dataframe 'df'.

Each single row in the dataframe 'df' contains unique activity data which can be of a different subsector of the 'Stationary Energy' sector or 'Transportation' sector.
Each single row in the dataframe 'df' can have a different gpc reference number.
Each row can only be associated with one GPC reference number.
To identify the GPC reference number, you need to understand to entire context of the activity data. Use the provided context below marked with <additional_information> tags.
Make sure to carefully inspect every single data row and to take all the information of that row into account when making a decision.

Follow these instructions carefully:
1. Think step-by-step for each row in the dataframe 'df'. This means for each row, consider the activity data and the context like vehicle type, scope and so on. Do not assume that the different rows are related.

2. You are already provided with the dataframe 'df' containing the activities.

3. To complete this task:
    a. Load the entire dataframe 'df'. This means load all the rows and do not use df.head() to only inspect the first few rows.    
    b. Identify columns in the dataframe that represent activity data and activity values as well as columns that give information about the sector (e.g. public, agriculture, construction, energy consumption and so on) of this activity. 
    c. Then if you have identified a column that contains the relevant information about how the activity data is being used:
        1. print out the unique values of this column
        2. make sure to include every unique value in your answer
    d. Inspect the general gpc mappings within <gpc_mappings> tags below, to understand the general GPC reference numbers and their structure.
    e. Then for the activity data, check the gpc mappings for 'Stationay Energy' and 'Transportation' marked with <gpc_mappings_sector> tags below, to know which GPC reference numbers could be applied.
    f. Then check the provided context for the sector 'Stationary Energy' and 'Transportation' marked with <context_activity_values_sector> tags below, to identify the correct GPC reference number based on the further context given in that document.
    g. Make sure, to only assign one GPC reference number to each activity data.

4. Present your answer in the following format:
    - Give all your detailed reasoning inside the <reasoning> tags.
    - Provide only the created mapping as JSON inside the <extracted_data> tags.
    <answer>
        <reasoning>
        [Your detailed reasoning for creating the GPC reference number mappings. Make sure to include the reasoning for each GPC reference number you assign to the activity data.]
        </reasoning>
        <mapping>
        [The extracted data as JSON]
        </mapping>
    </answer>
    
5. You are given additional information that is helpful in completing your task:

    <additional_information>
        <gpc_master_document>
        You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
        </gpc_master_document>
        <user_provided_context>
        This is the user provided context: {state.get("context_user_provided")}
        </user_provided_context>
        <gpc_mappings>
        The following information provides context to identify the GPC reference number for an activity value.
        This is the provided general context for Greenhouse Gas Protocol for Cities (GPC) mappings: {gpc_mappings}.
            <gpc_mappings_sector>
            The following provides context for mapping transportation activity data to Greenhouse Gas Protocol for Cities (GPC) reference numbers.
            This is the mapping of fuel names to possible GPC reference numbers: {fuel_to_gpc}.
            This is the mapping of the 'Stationary Energy' sector to possible GPC reference numbers: {stationary_energy_scope_2_subsector_to_gpc}.
            This is the mapping of the 'Transport' sector types to possible GPC reference numbers: {transport_type_to_gpc}.
            </gpc_mappings_sector>
        </gpc_mappings>
        <context_activity_values_sector>
        This is the provided context for avtivities specifically for the sector 'Transportation': {state.get("context_actval_transportation")}.
        Use this information for guidance on the correct GPC reference number especially when multiple GPC reference numbers are possible for an activity value. 
        </context_activity_values_sector>
        <extracted_keyval_data>
        This is the extracted key-value data from the previous agent: {state.get("structured_output_keyval")}.
        </extracted_keyval_data>
        <file_path>
        This is the path to the original data file: {state.get('file_path')}.
        </file_path>
        <feedback>
        If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_gpc_mapping_stationary_energy_transportation")}.
        If feedback is available, pay special attention to this feedback and incorporate into your data extraction process.
        </feedback>
    </additional_information>

Remember to base your response solely on the information provided in the dataframe and additional information. Do not make assumptions or use external knowledge.
"""

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    return {
        "extracted_gpc_mapping_stationary_energy_transportation": response.get("output")
    }


# Your goal is to extract activity data of the two sectors 'Stationary Energy' sector and 'Transportation' sector from the provided dataframe 'df'.
# An activity data consists of:
#     - a specific activity value
#     - a unit of measurement (e.g. liters, kilometers, cubic meter, etc.)
#     - a GPC reference number
# Each single row in the dataframe 'df' contains unique activity data.
# Each single row in the dataframe 'df' can be of a different subsector of the 'Stationary Energy' sector or 'Transportation' sector.
# To identify the GPC reference number, you need to understand to entire context of the activity data. Use the provided context below marked with <additional_information> tags.
# Each row can only be associated with one GPC reference number.
# Make sure to carefully inspect every single data row and to take all the information of that row into account when making a decision.

# Follow these instructions carefully:
# 1. Think step-by-step for each row in the dataframe 'df'. This means for each row, consider the activity data and the context like vehicle type, scope and so on. Do not assume that the different rows are related.
# 2. You are already provided with the dataframe 'df' containing the activities.

# 3. To complete this task:
#     a. Load the entire dataframe 'df'. This means load all the rows and do not use df.head() to only inspect the first few rows.    c. Identify columns in the dataframe that represent activity data and activity values as well as columns that give information about the sector (e.g. public, agriculture, construction, energy consumption and so on) of this activity.
#     b. Then if you have identified a column that contains the relevant information about how the activity data is being used:
#         1. print out the unique values of this column
#         2. make sure to include every unique value in your answer
#     c. Find the corresponding activity values for those rows
#     d. First inspect the general gpc mappings within <gpc_mappings> tags below, to understand the general GPC reference numbers and their structure.
#     e. Then for the activity data, check the gpc mappings for 'Stationay Energy' and 'Transportation' marked with <gpc_mappings_sector> tags below, to know which GPC reference numbers could be applied.
#     f. Then check the provided context for the sector 'Stationary Energy' and 'Transportation' marked with <context_activity_values_sector> tags below, to identify the correct GPC reference number based on the further contecxt given in that document. Pay special attention to vehicles and keywords mentioned in this document to guide you.

# 4. You are given additional information that is helpful in completing your task:

#     <additional_information>
#         <gpc_master_document>
#         You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
#         </gpc_master_document>
#         <user_provided_context>
#         This is the user provided context: {state.get("context_user_provided")}
#         </user_provided_context>
#         <gpc_mappings>
#         The following information provides context to identify the GPC reference number for an activity value.
#         This is the provided general context for Greenhouse Gas Protocol for Cities (GPC) mappings: {gpc_mappings}.
#             <gpc_mappings_sector>
#             The following provides context for mapping transportation activity data to Greenhouse Gas Protocol for Cities (GPC) reference numbers.
#             This is the mapping of fuel names to possible GPC reference numbers: {fuel_to_gpc}.
#             This is the mapping of the 'Stationary Energy' sector to possible GPC reference numbers: {stationary_energy_scope_2_subsector_to_gpc}.
#             This is the mapping of the 'Transport' sector types to possible GPC reference numbers: {transport_type_to_gpc}.
#             </gpc_mappings_sector>
#         </gpc_mappings>
#         <context_activity_values_sector>
#         This is the provided context for avtivities specifically for the sector 'Transportation': {state.get("context_actval_transportation")}.
#         Use this information for guidance on the correct GPC reference number especially when multiple GPC reference numbers are possible for an activity value.
#         </context_activity_values_sector>
#         <extracted_keyval_data>
#         This is the extracted key-value data from the previous agent: {state.get("structured_output_keyval")}.
#         </extracted_keyval_data>
#         <file_path>
#         This is the path to the original data file: {state.get('file_path')}.
#         </file_path>
#         <feedback>
#         If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_data_actval_stationary_energy_transportation")}.
#         If feedback is available, pay special attention to this feedback and incorporate into your data extraction process.
#         </feedback>
#     </additional_information>

# 5. Present your answer in the following format:
#     - Give all your detailed reasoning inside the <reasoning> tags.
#     - Provide only extracted data as JSON inside the <extracted_data> tags.
#     <answer>
#         <reasoning>
#         [Your detailed reasoning for extracting the data and mapping the GPC reference number. Make sure to include the reasoning for each GPC reference number you assign to the activity data.]
#         </reasoning>
#         <extracted_data>
#         [The extracted data as JSON]
#         </extracted_data>
#     </answer>

#     Remember to base your response solely on the information provided in the dataframe and additional information. Do not make assumptions or use external knowledge.
# """
