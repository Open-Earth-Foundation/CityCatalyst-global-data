from state.agent_state import AgentState
from utils.create_prompt import create_prompt

from context.context_methodologies import context_methodologies
from context.context_emission_factors import context_emission_factors


def transformation_agent_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nTRANSFORMATION AGENT STATIONARY ENERGY TRANSPORTATION\n")

    task = """
Your task is to create a transformation from activity data to emission values. 
For each identified activity data, you need to transform it into emission values bases on a specific methodology. The different methodologies for the 'Stationary Energy' sector and 'Transportation' sector are provided in the context below under <additional_information> tags.
"""
    completion_steps = """
a. Inspect the identified activity values provided in <extracted_activity_data_stationary_energy_transportation> tags. 
b. Inspect the identified gpc mappings provided in <extracted_gpc_mapping_stationary_energy_transportation> tags.    
c. Inspect the provided context for transformation methodologies for the 'Stationary Energy' sector and 'Transportation' sector provided in the <methodologies> tags below.
d. Inspect the provided dictionary of emission factors in the <emission_factors> tags below.
e. Based on the provided contet for methodologies and emission factors, calculate the emission values for the given activity data.
"""
    answer_format = """
- Give all your detailed reasoning inside the <reasoning> tags.
- Provide only the created mapping as JSON inside the <mapping> tags.
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
    This is the user provided context: {state.get("context_user_provided")}
    </user_provided_context>
    <gpc_master_document>
    You are provided with a retriever tool "Retriever" to retrieve information from the GPC Master document. Use this document every time to enrich your context.
    </gpc_master_document>
    <extracted_activity_data_stationary_energy_transportation>
    This is the provided activity data: {state.get("extracted_actval_stationary_energy_transportation")}.
    </extracted_activity_data_stationary_energy_transportation>
    <extracted_gpc_mapping_stationary_energy_transportation>
    These are the provided gpc mappings: {state.get("extracted_gpc_mapping_stationary_energy_transportation")}.
    <methodologies>
    This is the dictionary of different methodologies for the 'Stationary Energy' sector and 'Transportation' sector: {context_methodologies}
    </methodologies>
    <emission_factors>
    This is the provided dictionary of emission factors: {context_emission_factors}.
    </emission_factors>
    <feedback>
        <feedback_human-in-the-loop>
        If the user has provided feedback at the end of the entire data pipeline from the human-in-the-loop agent, you find it here: {state.get("feedback_hitl")}.
        This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.
        </feedback_human-in-the-loop>
        <feedback_reasoning_agent>
        If you have received feedback from the reasoning agent, you find it here: {state.get("feedback_extracted_gpc_mapping_stationary_energy_transportation")}.
        If feedback is available, pay special attention to this feedback and incorporate into your data extraction process.
        </feedback_reasoning_agent>
    </feedback>
</additional_information>
"""

    prompt = create_prompt(
        task, completion_steps, answer_format, additional_information
    )

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    return {"transformations_stationary_energy_transportation": response.get("output")}
