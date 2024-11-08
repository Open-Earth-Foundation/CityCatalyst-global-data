import re


def update_file_paths(script, original_path, new_output_path):
    # Update original_path using regex
    updated_script_input_path = re.sub(
        r"original_path\s*=\s*['\"].*['\"]",  # Match 'original_path = "..."' or 'original_path = '...''
        f"original_path = '{original_path}'",  # Replace with the passed original_path variable
        script,
    )

    # Use regex to find and replace any assignment to output_path
    updated_script_output_path = re.sub(
        r"output_path\s*=\s*['\"].*['\"]",  # Match 'output_path = "..."' or 'output_path = '...''
        f"output_path = '{new_output_path}'",  # Replace with the new output path
        updated_script_input_path,
    )
    return updated_script_output_path
