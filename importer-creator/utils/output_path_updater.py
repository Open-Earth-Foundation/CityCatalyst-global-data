def update_output_path(script, new_output_path):
    # Find and replace the output path in the script
    return script.replace(
        "output_path = './generated/initial_script/steps/1_initially.csv'",
        f"output_path = '{new_output_path}'",
    )
