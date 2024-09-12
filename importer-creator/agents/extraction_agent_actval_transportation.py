from state.agent_state import AgentState

# from agents.agent_tasks import task_extraction_agent_actval_transportation
from context.mappings.mappings_gpc import gpc_mappings
from context.mappings.mappings_transportation import (
    fuel_mapping,
    fuel_to_gpc,
    transport_type_to_gpc,
)

# a. contains the new dataframe 'df_new' that contains all the data of the original dataframe 'df'
# b. in each row the corresponding GPC reference number has been added as a new column for each individual activity value. Each row can only be associated with one GPC reference number.
# c. the correct GPC naming convention has been used where applicable and available
# d. the activity value has been added.

# <summary>
# This is the summary of the previous agent: {state.get('summary')}.
# </summary>

# Output a list of python dictionaries. Each dictionary inside the corresponds to a row in the dataframe 'df'. Each dictionary should contain the following key-value pairs:
#    {[{
#     "rownumber": "value",
#     "gpc_sector": "value",
#     "gpc_reference_number": "value",
#     "activity_name": "value",
#     "activity_value": "value"
#    },
#    {...}]}

# Once you extracted the data, create a python script. This script must contain:
#     a. a dictionary that maps the activities to the corresponding GPC reference numbers
#     b. the new dataframe 'df_new' that contains all the data of the original dataframe 'df'
#     c. in each row the corresponding GPC reference number as a new column for each individual activity value. Each row can only be associated with one GPC reference number.
#     d. the correct GPC naming convention has been used where applicable and available
#     e. the activity value has been added as a new column
#     f. the unit of the activity value has been added as a new column
# Do not use sample data for this task but only use the entire provided dataframe 'df'.
# <code>
# [Your generated python script]
# </code>
# This is the mapping of fuel names to standard names that we are using in GPC (IPCC standard): {fuel_mapping}.


def extraction_agent_actval_transportation(state: AgentState) -> dict:
    print("\nEXTRACTION AGENT ACTIVITY VALUES TRANSPORTATION\n")

    prompt = f"""
Your goal is to extract activity data of the 'Transportation' sector from the provided dataframe 'df'.
An activity data consists of:
    - a specific activity value
    - a unit of measurement (e.g. liters, kilometers, cubic meter, etc.)
    - a GPC reference number
Each single row in the dataframe 'df' contains unique activity data.
Each single row in the dataframe 'df' can be of a different subsector of the 'Transportation' sector.
To identify the GPC reference number, you need to understand to entire context of the activity data. Use the provided context below marked with <additional_information> tags.
Each row can only be associated with one GPC reference number.
Make sure to carefully inspect every single data row and to take all the information of that row into account when making a decision.

Follow these instructions carefully:
1. You are already provided with the dataframe 'df' containing the activities.

2. To complete this task:
    a. Think step-by-step for each row in the dataframe 'df'. This means for each row, consider the activity data and the context like vehicle type, scope and so on. Do not assume that the different rows are related.
    b. Identify columns in the dataframe that represent activity data and activity values as well as columns that give information about the sector (e.g. public, agriculture, construction, and so on) of this activity. 
    c. Find the corresponding activity values for those rows
    d. First inspect the general gpc mappings within <gpc_mappings> tags below, to understand the general GPC reference numbers and their structure.
    d. Then for the activity data, check the gpc mappings for transportation marked with <gpc_mappings_transportation> tags below, to know which GPC reference numbers could be applied.
    e. Then check the provided context for the sector 'Transportation' marked with <context_activity_values_transportation> tags below, to identify the correct GPC reference number based on the further contecxt given in that document. Pay special attention to vehicles and keywords mentioned in this document to guide you.
    f. Add the relevant GPC reference number based on the provided context. 
   
4. Present your findings in the following format:
   <answer>
    <reasoning>
    [Your reasoning for extracting the data and mapping the GPC reference number]
    </reasoning>
    <list>
    [List with entries of extracted data corresponding the dataframe 'df'. Each entry should contain the following key-value pairs: 'rownumber', 'activity_name', 'activity_value', 'unit', 'gpc_reference_number'. The list must contain an entry for each row in the dataframe 'df'.]
    </list>
   </answer> 

5. You are given additional information that is helpful in completing your task:

    <additional_information>
        <user_provided_context>
        This is the user provided context: {state.get("context_user_provided")}
        </user_provided_context>
        <context_activity_values_transportation>
        This is the provided context for avtivities specifically for the sector 'Transportation': {state.get("context_actval_transportation")}.
        Use this information for guidance on the correct GPC reference number especially when multiple GPC reference numbers are possible for an activity value. 
        Remember that each row in the dataframe 'df' can have a different subsector and therefore a different GPC reference number.
        </context_activity_values_transportation>
        <file_path>
        This is the path to the original data file: {state.get('file_path')}.
        </file_path>
        <gpc_mappings>
        Use the following information to identify the GPC reference number for an activity value and to understand the different fuel types.
        This is the provided context for Greenhouse Gas Protocol for Cities (GPC) mappings: {gpc_mappings}.
            <gpc_mappings_transportation>
            This is the provided context for mapping transportation activities to Greenhouse Gas Protocol for Cities (GPC) reference numbers.
            This is the mapping of fuel names to possible GPC reference numbers: {fuel_to_gpc}.
            This is the mapping of transport types to possible GPC reference numbers: {transport_type_to_gpc}.
            </gpc_mappings_transportation>
        </gpc_mappings>
        <feedback>
        If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_data_actval_transportation")}.
        If feedback is available, pay special attention to this feedback and incorporate into your data extraction process.
        If the extracted data aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
        </feedback>
    </additional_information>

Remember to base your response solely on the information provided in the dataframe and additional information. Do not make assumptions or use external knowledge.
"""

    # If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_data_actval_transportation")}.
    # If feedback is available, pay special attention to this feedback and incorporate into your data extracation process.

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    print(response.get("output"))

    return {"extracted_data_actval_transportation": response.get("output")}
