from state.agent_state import AgentState


def create_output_files_agent_transformation_stationary_energy_transportation(
    state: AgentState,
):
    print(
        "\nCREATE OUTPUT FILES AGENT TRANSFORMATION STATIONARY ENERGY TRANSPORTATION\n"
    )

    code = state.get(
        "structured_output_code_transformation_stationary_energy_transportation"
    )["code"]
    reasoning = state.get(
        "structured_output_code_transformation_stationary_energy_transportation"
    )["reasoning"]

    with open(
        "./generated/transformation_script/generated_transformation_script.py",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(code)

    with open(
        "./generated/transformation_script/generated_transformation_reasoning.md",
        "w",
        encoding="utf-8",
    ) as file:
        file.write(reasoning)
