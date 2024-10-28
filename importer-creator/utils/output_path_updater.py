import re


def update_output_path(script, new_output_path):
    # Use regex to find and replace any assignment to output_path
    updated_script = re.sub(
        r"output_path\s*=\s*['\"].*['\"]",  # Match 'output_path = "..."' or 'output_path = '...''
        f"output_path = '{new_output_path}'",  # Replace with the new output path
        script,
    )
    return updated_script
