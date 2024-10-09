import shutil
from state.agent_state import AgentState


def create_final_output_agent_initial_script(state: AgentState):
    print("\nCREATE FINAL OUTPUT AGENT INITIAL SCRIPT\n")

    # Load the previously created markdown files
    input_path_markdown_initially = (
        "./generated/initial_script/steps/generated_markdown_initially.md"
    )
    input_path_markdown_deleted_columns = (
        "./generated/initial_script/steps/generated_markdown_deleted_columns.md"
    )
    input_path_markdown_datatypes = (
        "./generated/initial_script/steps/generated_markdown_datatypes.md"
    )

    # Load the last created python script
    input_path_last_script = (
        "./generated/initial_script/steps/generated_script_datatypes.py"
    )

    # Load the last created csv file
    input_path_last_csv = "./generated/initial_script/steps/formatted_datatypes.csv"

    # Define output paths
    output_path_markdown = (
        "./generated/initial_script/final/generated_markdown_final_output.md"
    )
    output_path_script = (
        "./generated/initial_script/final/generated_script_final_output.py"
    )
    output_path_csv = "./generated/initial_script/final/generated_final_output.csv"

    # Combine markdown files into one final markdown output
    with open(output_path_markdown, "w") as outfile:
        outfile.write(f"# Report initial formatting\n\n")
        for markdown_file in [
            input_path_markdown_initially,
            input_path_markdown_deleted_columns,
            input_path_markdown_datatypes,
        ]:
            with open(markdown_file, "r") as infile:
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
