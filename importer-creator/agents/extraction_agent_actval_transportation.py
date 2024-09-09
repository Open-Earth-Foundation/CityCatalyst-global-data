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


def extraction_agent_actval_transportation(state: AgentState) -> dict:
    print("\nEXTRACTION AGENT ACTIVITY VALUES TRANSPORTATION\n")

    prompt = f"""
Your goal is to find the activity values for the 'Transportation' sector within the provided dataframe 'df'.
Once you found the activity values, map a GPC reference number to each activity value based on the provided context below.
Different rows can correspond to different GPC reference numbers based on the acitivities they represent but each row can only be associated with one GPC reference number.
Follow these instructions carefully:

1. You are already provided with a dataframe 'df' containing various data. The dataframe will be presented in the following format:

2. To complete this task:
   a. Look for a column in the dataframe that represents sectors or categories. If no column is clearly labeled, you may need to infer the required data based on the format of the dataframe.
   b. Find the corresponding activity values for those row(s) and add the relevant GPC reference number based on the provided context.

3. Refer to the additional additional information in <additional_information> tags, especially the <context_activity_values_transportation> tags and <gpc_mappings> tags.

4. Present your findings in the following format:
   <answer>
   Output a list of python dictionaries. Each dictionary inside the corresponds to a row in the dataframe 'df'. Each dictionary should contain the following key-value pairs:
   {[{
    "rownumber": "value",
    "gpc_sector": "value",
    "gpc_reference_number": "value",
    "activity_name": "value",
    "activity_value": "value"  
   },
   {...}]}
   </answer>

5. You are given additional information that is helpful in completing your task:

    <additional_information>
        <user_provided_context>
        This is the user provided context: {state.get("context_user_provided")}
        </user_provided_context>
        <context_activity_values_transportation>
        This is the provided context for avtivity values specifically for the sector 'Transportation': {state.get("context_actval_transportation")},
        </context_activity_values_transportation>
        <file_path>
        This is the path to the original data file: {state.get('file_path')}.
        </file_path>
        <gpc_mappings>
        This is the provided context for Greenhouse Gas Protocol for Cities (GPC) mappings: {gpc_mappings}.
        This is the mapping of fuel names to standard names that we are using in GPC (IPCC standard): {fuel_mapping}.
        Use this information to identify the GPC reference number for an activity value and to understand the different fuel types.
            <gpc_mappings_transportation>
            This is the provided context for mapping transportation activities to Greenhouse Gas Protocol for Cities (GPC) reference numbers.
            This is the mapping of fuel names to GPC reference numbers: {fuel_to_gpc}.
            This is the mapping of transport types to GPC reference numbers: {transport_type_to_gpc}.
            </gpc_mappings_transportation>
        </gpc_mappings>
    </additional_information>

Remember to base your response solely on the information provided in the dataframe and additional information. Do not make assumptions or use external knowledge.
"""

    # If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_data_actval_transportation")}.
    # If feedback is available, pay special attention to this feedback and incorporate into your data extracation process.

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    print(response.get("output"))

    return {"extracted_data_actval_transportation": response.get("output")}
