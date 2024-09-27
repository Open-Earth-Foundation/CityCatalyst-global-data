from state.agent_state import AgentState
from utils.create_prompt import create_prompt
from utils.agent_creation import create_agent_with_rag
from context.context_sector_subsector import context_sector_subsector
from utils.data_loader import load_datafile_into_df


def extraction_agent_keyval(state: AgentState) -> dict:
    print("\nEXTRACTION AGENT KEYVAL\n")

    # Get ipcc conform regions
    ipcc_regions = load_datafile_into_df("./emission_factors/emission_factors_vAI.csv")[
        "actor_name"
    ].unique()

    task = """
Your task is to extract key-value pairs from the provided dataframe 'df'.
"""

    completion_steps = f"""
a. Inspect the dataframe 'df' that you are already provided with. This means print out all the rows and do not use df.head() to only inspect the first few rows.  
b. Identify the region that the data is associated with.
    - Be specific. E.g. if only a country is mentioned, then the region is the country e.g. 'Argentina' or 'Finland' and so on. 
    - If a region (e.g. a state) is mentioned, use the specific region e.g. 'British Columbia' or 'Saskatchewan' and so on.
    - If multiple regions are mentioned (e.g. different states or countries), use 'world' as the region if the data contains multiple countries or use the country name if the data contains multiple regions inside that country. 
    This is a list of possible regions which you have to choose one single region from: {ipcc_regions}.
c. Identify the temporal resolution of the data for example if the datapoints are ordered by days, weeks, month or years.
d. Identify the associated sector according to Greenhouse Gas Protocol for Cities (GPC). Check the additional information provided below within <context_sector_subsector> tags to identify the correct sector based on the provided context.
e. Identify the accociated sub-sector according to Greenhouse Gas Protocol for Cities (GPC). Check the additional information provided below within <context_sector_subsector> tags to identify the correct sub-sector based on the provided context.
"""

    answer_format = """
- Give all your detailed reasoning inside the <reasoning> tags.
- Provide only the created JSON with extracted key-values inside the <extracted_data> tags.
<answer>
    <reasoning>
    [Your detailed reasoning for extracting the key-value pairs]
    </reasoning>
    <extracted_data_keyval>
    [The extracted data as JSON with the keys 'region', 'temporal_resolution', 'sector' and 'subsector']
    </extracted_data_keyval>
</answer>
"""

    additional_information = f"""
<additional_information>
    <file_path>
    This is the path to the original data file: {state.get('file_path')}.
    </file_path>
    <user_provided_context>
    This is the user provided context: {state.get("context_user_provided")}
    </user_provided_context>
    <gpc_master_document>
    You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
    </gpc_master_document>
    <summary>
    This is the summary of the dataset: {state.get('summary')}.
    </summary>
    <context_sector_subsector>
    This is the provided context for sectors and sub-sectors to be used: {context_sector_subsector},
    </context_sector_subsector>
    <feedback>
        <feedback_human-in-the-loop>
        If the user has provided feedback at the end of the entire data pipeline from the human-in-the-loop agent, you find it here: {state.get("feedback_hitl")}.
        This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.
        </feedback_human-in-the-loop>
        <feedback_reasoning_agent>
        If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_data_keyval")}.
        If feedback is available, pay special attention to this feedback and incorporate into your data extraction process.
        </feedback_reasoning_agent>
    </feedback>
</additional_information>
"""

    # Create the agent
    agent = create_agent_with_rag(state.get("df"), state.get("verbose"))

    # Create the prompt
    prompt = create_prompt(
        task, completion_steps, answer_format, additional_information
    )

    response = agent.invoke(prompt)

    return {"extracted_data_keyval": response.get("output")}
