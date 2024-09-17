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


def extraction_agent_actval_stationary_energy_transportation(state: AgentState) -> dict:
    print("\nEXTRACTION AGENT ACTIVITY VALUES STATIONARY ENERGY TRANSPORTATION\n")

    prompt = f"""
Your goal is to extract activity data of the two sectors 'Stationary Energy' sector and 'Transportation' sector from the provided dataframe 'df'.
An activity data consists of:
    - a specific activity value
    - a unit of measurement (e.g. liters, kilometers, cubic meter, etc.)
    - a GPC reference number
Each single row in the dataframe 'df' contains unique activity data.
Each single row in the dataframe 'df' can be of a different subsector of the 'Stationary Energy' sector or 'Transportation' sector.
To identify the GPC reference number, you need to understand to entire context of the activity data. Use the provided context below marked with <additional_information> tags.
Each row can only be associated with one GPC reference number.
Make sure to carefully inspect every single data row and to take all the information of that row into account when making a decision.

Follow these instructions carefully:
1. You are already provided with the dataframe 'df' containing the activities.

2. To complete this task:
    a. Load the entire dataframe 'df'. This means load all the rows and do not use df.head() to only inspect the first few rows.
    b. Think step-by-step for each row in the dataframe 'df'. This means for each row, consider the activity data and the context like vehicle type, scope and so on. Do not assume that the different rows are related.
    c. Identify columns in the dataframe that represent activity data and activity values as well as columns that give information about the sector (e.g. public, agriculture, construction, energy consumption and so on) of this activity. 
    d. Then if you have identified a column that contains the relevant information about how the activity data is being used:
        - print out the unique values of this column
        - make sure to include every unique value in your answer
    d. Find the corresponding activity values for those rows
    e. First inspect the general gpc mappings within <gpc_mappings> tags below, to understand the general GPC reference numbers and their structure.
    f. Then for the activity data, check the gpc mappings for 'Stationay Energy' and 'Transportation' marked with <gpc_mappings_sector> tags below, to know which GPC reference numbers could be applied.
    g. Then check the provided context for the sector 'Stationary Energy' and 'Transportation' marked with <context_activity_values_sector> tags below, to identify the correct GPC reference number based on the further contecxt given in that document. Pay special attention to vehicles and keywords mentioned in this document to guide you.
    h. Create a python script. This python script must contain the following:
        1. a dictionary variable "extracted_keyval_data" = { ... } with the the extracted data 'region' and 'temporal_resolution' from the previous agent. You find the data below within the <extracted_keyval_data> tags.
        2. a dictionary that maps the activity data to the corresponding GPC reference numbers. Make sure to include a mapping for all GPC reference numbers that you have identified in the data and assigned. Include a category for 'Other' if you have identified activity data that does not fit into any of the provided categories and set the GPC reference number to 'undefined'. Make sure to include a mapping for every single sector identified.
        3. code to load the .csv file into a pandas dataframe 'df' using "encoding='utf-8'". When loading the datafile, define the correct seperator being used e.g. ',' or ';'. The path to the .csv file is provided in the additional information.
        4. a new dataframe 'df_new' that contains all the data of the original dataframe 'df' as a copy. Make further manipulations on this new dataframe 'df_new'.
        5. normalized column names to 'lower case', strip them of any leading or trailing white spaces and replace any white spaces with underscores '_'.
        6. convert any date columns to a valid datetime format based on the available data.
            - automatically infer the format from the available data. E.g. use the extracted keyvalues within <extracted_keyval_data> tags and specifically the value 'temporal_resolution' as a guiding point.
            - pay attention to columns that might not be clearly labeled as 'date' or 'dates' or similar.
        7. add to the new dataframe 'df_new' 2 new columns 'region' and 'temporal_resolution'. Fill these columns with the extracted key value data from the <extracted_keyval_data> tags.
        8. add to the new dataframe 'df_new' 3 new columns 'activity_name', 'activity_value' and 'activity_unit'. Fill these columns with the existing data extracted data from the dataframe 'df'.
        9. add to the new dataframe 'df_new' 1 new colum 'gpc_reference_number'. Fill this column with the GPC reference number you have identified for the activity data.
        10. finally add code to output a new .csv file 'formatted.csv' containing the new dataframe 'df_new' with the added columns.
        11. IMORTANT: 
            - The code must contain python comments.
            - The code must be executable and must not contain any code errors.
            - The final dataframe 'df_new' must contain all the data of the original dataframe 'df' and the added columns. If rows could not be assigned a GPC reference number, set the GPC reference number to 'undefined' according to the mapping. These rows must still be included in the final dataframe 'df_new'.

3. You are given additional information that is helpful in completing your task:

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
        If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_data_actval_stationary_energy_transportation")}.
        If feedback is available, pay special attention to this feedback and incorporate into your data extraction process.
        </feedback>
    </additional_information>

    4. Present your answer in the following format:
        - Give all your detailed reasoning inside the <reasoning> tags.
        - Provide only the python script inside the <code> tags.
        <answer>
            <reasoning>
            [Your detailed reasoning for extracting the data and mapping the GPC reference number. Make sure to include the reasoning for each GPC reference number you assign to the activity data.]
            </reasoning>
            <code>
            [Your generated python script]
            </code>
        </answer>

    Remember to base your response solely on the information provided in the dataframe and additional information. Do not make assumptions or use external knowledge.
    """

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    return {
        "extracted_data_actval_stationary_energy_transportation": response.get("output")
    }
