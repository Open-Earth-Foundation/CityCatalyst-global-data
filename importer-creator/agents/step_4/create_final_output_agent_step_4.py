import shutil
from state.agent_state import AgentState


def create_final_output_agent_step_4(state: AgentState):
    print("\nCREATE FINAL OUTPUT AGENT STEP 4\n")

    # Load the previously created markdown files
    input_path_markdown_extracted_methodology_name = (
        "./generated/step_4/steps/generated_markdown_extracted_methodology_name.md"
    )
    # input_path_markdown_extracted_sector = (
    #     "./generated/step_4/steps/generated_markdown_extracted_....md"
    # )
    # input_path_markdown_extracted_sub_sector = (
    #     "./generated/step_4steps/generated_markdown_extracted_....md"
    # )

    # Load the last created python script
    input_path_last_script = (
        "./generated/step_4/steps/generated_script_extracted_....py"
    )

    # Load the last created csv file
    input_path_last_csv = "./generated/step_4/steps/extracted_....csv"

    # Define output paths
    output_path_markdown = "./generated/step_4/final/generated_markdown_final_output.md"
    output_path_script = "./generated/step_4/final/generated_script_final_output.py"
    output_path_csv = "./generated/step_4/final/generated_final_output.csv"

    # Combine markdown files into one final markdown output
    with open(output_path_markdown, "w", encoding="utf-8") as outfile:
        outfile.write(f"# Report step 3\n\n")
        for markdown_file in [
            input_path_markdown_extracted_methodology_name,
            # input_path_markdown_extracted_sector,
            # input_path_markdown_extracted_sub_sector,
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
