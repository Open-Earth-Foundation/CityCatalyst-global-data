from state.agent_state import AgentState


def hitl_agent_initial_script(state: AgentState) -> dict:
    print("\nHUMAN-IN-THE-LOOP AGENT INITIAL SCRIPT\n")

    # Check if the HITL flag is set for manual HITL feedback
    if state.get("hitl") == True:
        print("The HITL flag is set to True")

        message = """
        Please check the created files in the folder './generated/initial_script/final'.

        You may check the resulting csv file in the file `final_output.csv`
        You may check the changes and assumption of the model made in the file `final_output.md`

        If everything looks good, just press 'Enter' to proceed with the script.

        You may make changes directly to the file `final_output.py`. 
        After completing your changes just press 'Enter'.
        The script will automatically proceed with the updated file.
        """
        input(message)

    else:
        print("The HITL flag is set to False")
