from state.agent_state import AgentState
from utils.agent_creation import create_agent_with_rag_and_csv_filter
from utils.create_prompt import create_prompt

from context.context_methodologies import context_methodologies

# from utils.data_loader import load_datafile_into_df
# from utils.filter_emission_factors import filter_data


def extraction_agent_transformations_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nEXTRACTION AGENT TRANSFORMATIONS STATIONARY ENERGY TRANSPORTATION\n")

    # Skip this step for now
    # return {"extracted_transformations_stationary_energy_transportation": "PASS"}

    # Filter the emission factors based on the provided filters of region
    # df = load_datafile_into_df("./emission_factors/emission_factors_vAI.csv")

    # structured_output_keyval = state.get("structured_output_code_keyval")
    # extracted_keyval_data = structured_output_keyval["extracted_data"]
    # region = extracted_keyval_data["region"]

    # # Filter the emission factors based on the provided region and drop duplicates
    # filters = {"actor_name": region}
    # filtered_emission_factors = filter_data(df, filters).drop_duplicates()

    task = """
Your task is to create a transformation from activity data to emission values. 
For each identified activity data, you need to transform it into emission values bases on a specific methodology. The different methodologies for the 'Stationary Energy' sector and 'Transportation' sector are provided in the context below under <additional_information> tags.
"""
    completion_steps = """
a. Inspect the dataframe 'df' that you are already provided with. This means print out all the rows and do not use df.head() to only inspect the first few rows.    
b. Inspect the identified activity values provided in <extracted_data_actval_stationary_energy_transportation> tags. 
c. Inspect the identified gpc mappings provided in <extracted_gpc_mapping_stationary_energy_transportation> tags.    
d. Inspect the provided context for transformation methodologies for the 'Stationary Energy' sector and 'Transportation' sector provided in the <methodologies> tags below.
e. Inspect the provided dictionary of emission factors in the <emission_factors> tags below.
f. Based on the provided context for methodologies and emission factors: 
    - decide which methodology from the <methodologies> tags below to use and which emission factor from <emission_factor> tags to apply. If you cannot find the correct emissions factor, you can use the placeholder value of 1.0.
    - your answer must include a mapping for all activity data.
    - remember that each activity data could need a different methodology and different emission factor 
"""
    answer_format = """
- Give all your detailed reasoning inside the <reasoning> tags.
- Provide the transformations that need to be applied in the <transformations> tags.
<answer>
    <reasoning>
    [Your detailed reasoning for creating the GPC reference number mappings. Make sure to include the reasoning for each GPC reference number you assign to the activity data]
    </reasoning>
    <transformations>
    [The transformed emission values]
    </transformations>
</answer>
"""
    additional_information = f"""
<additional_information>
    <file_path>
    This is the path to the original data file: {state.get('file_path')}.
    </file_path>
    <user_provided_context>
    This is the user provided context: {state.get("user_input")}. Take the region of the data for filtering from this information.
    </user_provided_context>
    <gpc_master_document>
    You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
    </gpc_master_document>
    <extracted_data_actval_stationary_energy_transportation>
    This is the provided activity data: {state.get("extracted_data_actval_stationary_energy_transportation")}.
    </extracted_data_actval_stationary_energy_transportation>
    <extracted_gpc_mapping_stationary_energy_transportation>
    These are the provided gpc mappings: {state.get("extracted_gpc_mapping_stationary_energy_transportation")}.
    </extracted_gpc_mapping_stationary_energy_transportation>
    <methodologies>
    This is the dictionary of different methodologies for the 'Stationary Energy' sector and 'Transportation' sector: {context_methodologies}
    </methodologies>
    <emission_factors>
    You are provided with a tool 'FilterData'. Use it to filter the emission factors based on filter criteria like region and gpc reference numbers and others. 
    Use this dataframe to search for the correct emission factors based on the description, GPC reference number, methodology, gas type, units and the most current year if multiple values of multiple years are given.
    </emission_factors>
    <feedback>
        <feedback_human-in-the-loop>
        If the user has provided feedback at the end of the entire data pipeline from the human-in-the-loop agent, you find it here: {state.get("feedback_hitl")}.
        This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.
        </feedback_human-in-the-loop>
    </feedback>
</additional_information>
"""
    # Create the agent
    agent = create_agent_with_rag_and_csv_filter(state.get("df"), state.get("verbose"))

    prompt = create_prompt(
        task, completion_steps, answer_format, additional_information
    )

    # Invoke summary agent with custom prompt
    # response = state.get("agent").invoke(prompt)
    response = agent.invoke(prompt)

    return {
        "extracted_transformations_stationary_energy_transportation": response.get(
            "output"
        )
    }

    # <emission_factors>
    # This is the provided dataframe containing emission factors: {filtered_emission_factors}.
    # Use this dataframe to search for the correct emission factors based on the description, GPC reference number, methodology, gas type, units and the most current year if multiple values of multiple years are given.
    # </emission_factors>
