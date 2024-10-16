from state.agent_state import AgentState


def create_output_files_agent_gpc_refno_stationary_energy_transportation(
    state: AgentState,
):
    print("\nCREATE OUTPUT FILES AGENT GPC REFNO STATIONARY ENERGY TRANSPORTATION\n")

    code = state.get(
        "structured_output_code_gpc_refno_stationary_energy_transportation"
    )["code"]
    reasoning = state.get(
        "structured_output_code_gpc_refno_stationary_energy_transportation"
    )["reasoning"]

    with open(
        "./generated/gpc_refno_script/generated_gpc_refno_script.py",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(code)

    with open(
        "./generated/gpc_refno_script/generated_gpc_refno_reasoning.md",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(reasoning)
