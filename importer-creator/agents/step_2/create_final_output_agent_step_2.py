import shutil
from state.agent_state import AgentState


def create_final_output_agent_step_2(state: AgentState):
    print("\nCREATE FINAL OUTPUT AGENT STEP 2\n")

    # Load the previously created markdown files
    input_path_markdown_extracted_actor_name = (
        "./generated/step_2/steps/generated_markdown_extracted_actor_name.md"
    )
    input_path_markdown_extracted_sector = (
        "./generated/step_2/steps/generated_markdown_extracted_sector.md"
    )
    input_path_markdown_extracted_sub_sector = (
        "./generated/step_2/steps/generated_markdown_extracted_sub_sector.md"
    )

    # Load the last created python script
    input_path_last_script = (
        "./generated/step_2/steps/generated_script_extracted_sub_sector.py"
    )

    # Load the last created csv file
    input_path_last_csv = "./generated/step_2/steps/extracted_sub_sector.csv"

    # Define output paths
    output_path_markdown = "./generated/step_2/final/generated_markdown_final_output.md"
    output_path_script = "./generated/step_2/final/generated_script_final_output.py"
    output_path_csv = "./generated/step_2/final/generated_final_output.csv"

    # Combine markdown files into one final markdown output
    with open(output_path_markdown, "w", encoding="utf-8") as outfile:
        outfile.write(f"# Report initial formatting\n\n")
        for markdown_file in [
            input_path_markdown_extracted_actor_name,
            input_path_markdown_extracted_sector,
            input_path_markdown_extracted_sub_sector,
        ]:
            with open(markdown_file, "r", encoding="utf-8") as infile:
                content = infile.read()
                outfile.write(content)
                outfile.write(f"\n\n*{infile.name}*")
                outfile.write("\n\n")  # Add some spacing between combined markdowns

    print(f"Combined markdown report saved to: {output_path_markdown}")

    # Copy the last python script and csv file to the final output directory
    shutil.copy(input_path_last_script, output_path_script)
    shutil.copy(input_path_last_csv, output_path_csv)

    print(f"Final script copied to: {output_path_script}")
    print(f"Final CSV file copied to: {output_path_csv}")