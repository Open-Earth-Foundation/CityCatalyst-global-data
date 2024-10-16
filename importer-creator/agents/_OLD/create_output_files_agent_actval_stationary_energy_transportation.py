from state.agent_state import AgentState


def create_output_files_agent_actval_stationary_energy_transportation(
    state: AgentState,
):
    print("\nCREATE OUTPUT FILES AGENT ACTVAL STATIONARY ENERGY TRANSPORTATION\n")

    code = state.get("structured_output_code_actval_stationary_energy_transportation")[
        "code"
    ]
    reasoning = state.get(
        "structured_output_code_actval_stationary_energy_transportation"
    )["reasoning"]

    with open(
        "./generated/actval_script/generated_actval_script.py", "w", encoding="utf-8"
    ) as file:
        file.write(code)

    with open(
        "./generated/actval_script/generated_actval_reasoning.md",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(reasoning)
