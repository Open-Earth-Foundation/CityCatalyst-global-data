from state.agent_state import AgentState
from context.context_sector_subsector import context_sector_subsector


def extraction_agent_keyval(state: AgentState) -> dict:
    print("\nEXTRACTION AGENT KEYVAL\n")

    # Agent logic to extract specific data
    prompt = f"""
Your task is to extract key-value pairs from the provided dataframe 'df'.

Follow these instructions carefully:
1. Think step-by-step

2. You are already provided with the dataframe 'df' containing the activities.

3. To complete this task:
    a. Identify the region that the data is associated with.
        - Be specific. E.g. if only a country is mentioned, then the region is the country. 
        - If a city or a region (e.g. a state) is mentioned, use the specific city or region. 
        - If multiple regions are mentioned (e.g. different cities, states or countries), use the most specific region that captures all mentioned regions. E.g. 'global' for multiple countries of different continents or 'Europe' for multiple regions in europe or 'Argentina' for multiple regions or cities in Argentina and so on.
        Name the biggest region that captures all mentioned regions in the data file and that is most specific at the same time.
    b. Identify the temporal resolution of the data for example if the datapoints are ordered by days, weeks, month or years.
    c. Identify the associated sector according to Greenhouse Gas Protocol for Cities (GPC). Check the additional information provided below within <context_sector_subsector> tags to identify the correct sector based on the provided context.
    d. Identify the accociated sub-sector according to Greenhouse Gas Protocol for Cities (GPC). Check the additional information provided below within <context_sector_subsector> tags to identify the correct sub-sector based on the provided context.

4. Present your answer in the following format:
    - Give all your detailed reasoning inside the <reasoning> tags.
    - Provide only the created JSON with extracted key-values inside the <extracted_data> tags.
    <answer>
        <reasoning>
        [Your detailed reasoning for extracting the key-value pairs]
        </reasoning>
        <extracted_data_keyval>
        [The extracted data as JSON]
        </extracted_data_keyval>
    </answer>

5. You are given additional information that is helpful in completing your task:
    <additional_information>
        <gpc_master_document>
        You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
        </gpc_master_document>
        <user_provided_context>
        This is the user provided context: {state.get("context_user_provided")}
        </user_provided_context>
        <context_sector_subsector>
        This is the provided context for sectors and sub-sectors to be used: {context_sector_subsector},
        </context_sector_subsector>
        <summary>
        This is the summary of the dataset: {state.get('summary')}.
        </summary>
        <file_path>
        This is the path to the original data file: {state.get('file_path')}.
        </file_path>
        <feedback>
        If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_data_keyval")}.
        If feedback is available, pay special attention to this feedback and incorporate into your data extraction process.
        </feedback>
    </additional_information>
"""

    response = state.get("agent").invoke(prompt)

    return {"extracted_data_keyval": response.get("output")}
