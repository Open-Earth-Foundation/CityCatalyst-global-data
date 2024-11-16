def clean_json_output(output: str) -> str:
    # Check if the output starts and ends with the markdown-style code block
    if output.startswith("```json") and output.endswith("```"):
        print("Output containts ```json ``` tags. Cleaning JSON output...")
        # Remove the first and last lines containing the code block tags
        output = output[
            7:-3
        ].strip()  # Remove "```json" and "```" and strip any extra spaces
    return output
