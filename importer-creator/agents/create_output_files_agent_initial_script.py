from state.agent_state import AgentState


def create_output_files_agent_initial_script(state: AgentState):
    print("\nCREATE OUTPUT FILES AGENT INITIAL SCRIPT\n")

    code = state.get("structured_output_code_initial_script")["code"]
    reasoning = state.get("structured_output_code_initial_script")["reasoning"]

    with open(
        "./generated/initial_script/generated_initial_script.py", "w", encoding="utf-8"
    ) as file:
        file.write(code)

    with open(
        "./generated/initial_script/generated_initial_reasoning.md",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(reasoning)
