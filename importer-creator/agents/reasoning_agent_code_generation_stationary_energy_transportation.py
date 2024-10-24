from state.agent_state import AgentState


def reasoning_agent_code_generation_stationary_energy_transportation(
    state: AgentState,
) -> dict:
    print("\nREASONING AGENT CODE GENERATION STATIONARY ENERGY TRANSPORTATION\n")

    prompt = f"""
Your task is to check and verify python script, that was created by the previous code generation agent found within <generated_code> tags. 
    
<generated_code>
This is the generated code: {state.get("generated_code")}.
</generated_code>

Follow these instructions carefully:
1. Think step-by-step

2. Consider the human-in-the-loop feedback provided in the <feedback_human-in-the-loop> tags below if available. This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.

3. To complete this task:
    a. Load the created python script of the previous agent.
    c. Check if the dictionary mappings were done correctly. You find the mappings of the previous agents within <extracted_keyval_data> tags and <extracted_gpc_mapping_stationary_energy_transportation> tags. 
    e. Run the code and make sure that the code runs without any errors. If you encounter any errors, provide feedback to the previous agent.
    d. Provide feedback regarding possible code improvements if any. 

4. Present your answer in the following format:
    If you approve, return 'APPROVED'. If not, return 'FEEDBACK: [Your feedback here]'.
    
5. You are given additional information that is helpful in completing your task:
<additional_information>
    <file_path>
    This is the path to the original data file: {state.get('file_path')}.
    </file_path>
    <extracted_keyval_data>
    This is the extracted key-value data from the previous agent: {state.get("structured_output_keyval")}.
    </extracted_keyval_data>
    <extracted_gpc_mapping_stationary_energy_transportation>
    This is the extracted activity data from the previous agent: {state.get("approved_extracted_gpc_mapping_stationary_energy_transportation")}.
    </extracted_gpc_mapping_stationary_energy_transportation>
    <feedback>
        <feedback_human-in-the-loop>
        If the user has provided feedback at the end of the entire data pipeline from the human-in-the-loop agent, you find it here: {state.get("feedback_hitl")}.
        This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.
        </feedback_human-in-the-loop>
        <feedback_reasoning_agent>
        If you have provided previous feedback, you find it here: {state.get("feedback_code_generation_actval_stationary_energy_transportation")}. 
        If the extracted data aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
        <feedback_reasoning_agent>
    </feedback>
</additional_information>
"""

    # Check if the iteration limit has been reached
    if (
        state.get(
            "iterator_reasoning_agent_code_generation_actval_stationary_energy_transportation"
        )
        >= 0
    ):
        print(
            "\nIteration limit reached. Automatically approving the generated code for 'Stationary Energy' and 'Transportion' sector.\n"
        )
        return {"final_code_output": state.get("generated_code")}

    # Invoke summary agent with custom prompt
    response = state.get("agent").invoke(prompt)

    if "APPROVED" in response.get("output"):
        return {"final_code_output": state.get("generated_code")}
    else:
        return {
            "feedback_code_generation_actval_stationary_energy_transportation": response.get(
                "output"
            ),
            "iterator_reasoning_agent_code_generation_actval_stationary_energy_transportation": state.get(
                "iterator_reasoning_agent_code_generation_actval_stationary_energy_transportation"
            )
            + 1,
        }
