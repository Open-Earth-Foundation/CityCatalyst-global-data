import shutil
from state.agent_state import AgentState
from utils.file_paths_updater import update_file_paths
from utils.path_helper import get_run_path, ensure_path_exists


def create_final_output_agent_step_3(state: AgentState):
    print("\nCREATE FINAL OUTPUT AGENT STEP 3\n")

    # Load the previously created markdown files
    input_path_markdown_extracted_activity_name = get_run_path(state, "step_3/steps/1_activity_name.md")
    input_path_markdown_extracted_sector = get_run_path(state, "step_3/steps/2_activity_value.md")
    input_path_markdown_extracted_sub_sector = get_run_path(state, "step_3/steps/3_activity_unit.md")
    input_path_markdown_extracted_activity_subcategory_1 = get_run_path(state, "step_3/steps/4_activity_subcategory_1.md")
    input_path_markdown_extracted_activity_subcategory_2 = get_run_path(state, "step_3/steps/5_activity_subcategory_2.md")
    
    # Load the last created python script
    input_path_last_script = get_run_path(state, "step_3/steps/5_activity_subcategory_2.py")

    # Load the last created csv file
    input_path_last_csv = get_run_path(state, "step_3/steps/5_activity_subcategory_2.csv")

    # Define output paths
    output_path_markdown = get_run_path(state, "step_3/final/final_output.md")
    output_path_script = get_run_path(state, "step_3/final/final_output.py")
    output_path_csv = get_run_path(state, "step_3/final/final_output.csv")
    
    # Ensure output directories exist
    ensure_path_exists(output_path_markdown)
    ensure_path_exists(output_path_script)
    ensure_path_exists(output_path_csv)

    # Combine markdown files into one final markdown output
    with open(output_path_markdown, "w", encoding="utf-8") as outfile:
        outfile.write(f"# Report step 3\n\n")
        for markdown_file in [
            input_path_markdown_extracted_activity_name,
            input_path_markdown_extracted_sector,
            input_path_markdown_extracted_sub_sector,
            input_path_markdown_extracted_activity_subcategory_1,
            input_path_markdown_extracted_activity_subcategory_2,
        ]:
            with open(markdown_file, "r", encoding="utf-8") as infile:
                content = infile.read()
                outfile.write(content)
                outfile.write(f"\n\n*{infile.name}*")
                outfile.write("\n\n")  # Add some spacing between combined markdowns

    print(f"Combined markdown report saved to: {output_path_markdown}")

    # Update the output path in the last python script

    # Read the content of the last python script
    with open(input_path_last_script, "r", encoding="utf-8") as infile:
        script_content = infile.read()

    # Update the file paths in the script content
    updated_script_content = update_file_paths(
        script_content,
        original_path=state.get("full_path"),
        new_output_path=output_path_csv,
    )

    # Write the updated script to the output path
    with open(output_path_script, "w", encoding="utf-8") as outfile:
        outfile.write(updated_script_content)

    print(f"Final script updated and saved to: {output_path_script}")

    # Copy the last python script and csv file to the final output directory
    shutil.copy(input_path_last_csv, output_path_csv)
    print(f"Final CSV file copied to: {output_path_csv}")

    return state
