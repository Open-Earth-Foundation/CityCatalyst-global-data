from state.agent_state import AgentState


def create_output_files_agent_keyval(state: AgentState):
    print("\nCREATE OUTPUT FILES AGENT KEYVAL\n")

    code = state.get("structured_output_code_keyval")["code"]
    reasoning = state.get("structured_output_code_keyval")["reasoning"]

    with open(
        "./generated/keyval_script/generated_keyval_script.py", "w", encoding="utf-8"
    ) as file:
        file.write(code)

    with open(
        "./generated/keyval_script/generated_keyval_reasoning.md",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(reasoning)
