from state.agent_state import AgentState


def code_generation_agent_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nCODE GENERATION AGENT STATIONARY ENERGY TRANSPORTATION\n")

    prompt = f"""
Your goal is to create a runnable python script. 
Your inputs are the dataframe 'df' and extracted data provided in the <additional_information> tags below.

Follow these instructions carefully:
1. Think step-by-step for each each of your tasks

2. Consider the human-in-the-loop feedback provided in the <feedback_human-in-the-loop> tags below if available. This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.

3. You are already provided with the dataframe 'df' containing the activities.

4. To complete this task:
    a. Load the entire dataframe 'df'. This means load all the rows and do not use df.head() to only inspect the first few rows.
    b. Create a python script. This python script must contain the following:
        1. a dictionary variable "extracted_keyval_data" = { ... } with the the extracted data 'region' and 'temporal_resolution' from the previous agent. You find the data below within the <extracted_keyval_data> tags.
        2. a dictionary that maps the activity data to the corresponding GPC reference numbers. You find the data below within the <extracted_gpc_mapping_stationary_energy_transportation> tags.
        3. code to load the .csv file into a pandas dataframe 'df' using "encoding='utf-8'". When loading the datafile, define the correct seperator being used e.g. ',' or ';'. The path to the .csv file is provided in the additional information.
        4. a new dataframe 'df_new' that contains all the data of the original dataframe 'df' as a copy. Make further manipulations on this new dataframe 'df_new'.
        5. normalized column names to 'lower case', strip them of any leading or trailing white spaces and replace any white spaces with underscores '_'.
        6. convert any date columns to a valid datetime format based on the available data.
            - automatically infer the format from the available data. E.g. use the extracted keyvalues within <extracted_keyval_data> tags and specifically the value 'temporal_resolution' as a guiding point.
            - pay attention to columns that might not be clearly labeled as 'date' or 'dates' or similar.
        7. add to the new dataframe 'df_new' 2 new columns 'region' and 'temporal_resolution'. Fill these columns with the extracted key value data from the <extracted_keyval_data> tags.
        8. add to the new dataframe 'df_new' 3 new columns 'activity_name', 'activity_value' and 'activity_unit'. Fill these columns with the existing data extracted data from the dataframe 'df'.
        9. add to the new dataframe 'df_new' 1 new colum 'gpc_reference_number'. Fill this column with the GPC reference number of the mappings between <extracted_gpc_mapping_stationary_energy_transportation> tags below.
        10. finally add code to output a new .csv file 'formatted.csv' containing the new dataframe 'df_new' with the added columns.
        11. IMORTANT: 
            - The code must contain python comments.
            - The code must be executable and must not contain any code errors.
            - The final dataframe 'df_new' must contain all the data of the original dataframe 'df' and the added columns. If rows could not be assigned a GPC reference number, set the GPC reference number to 'undefined' according to the mapping. These rows must still be included in the final dataframe 'df_new'.

5. Present your answer in the following format:
    - Provide only the python script inside the <code> tags.
    <answer>
        <code>
        [Your generated python script]
        </code>
    </answer>

6. You are given additional information that is helpful in completing your task:

    <additional_information>
        <file_path>
        This is the path to the original data file: {state.get('file_path')}.
        </file_path>
        <extracted_keyval_data>
        This is the extracted key-value data from the previous agent: {state.get("structured_output_keyval")}.
        </extracted_keyval_data>
        <extracted_gpc_mapping_stationary_energy_transportation>
        This is the extracted gpc mapping data from the previous agent: {state.get("approved_extracted_gpc_mapping_stationary_energy_transportation")}.
        </extracted_gpc_mapping_stationary_energy_transportation> 
        <feedback>
            <feedback_human-in-the-loop>
            If the user has provided feedback at the end of the entire data pipeline from the human-in-the-loop agent, you find it here: {state.get("feedback_hitl")}.
            This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.
            </feedback_human-in-the-loop>
            <feedback_reasoning_agent>
            If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_code_generation_actval_stationary_energy_transportation")}.
            If feedback is available, pay special attention to this feedback and incorporate into your data extraction process.
            </feedback_reasoning_agent>
        </feedback>
    </additional_information>
"""

    # Invoke summary agent with custom prompt
    response = state.get("agent_code").invoke(prompt)

    return {"generated_code": response.get("output")}
