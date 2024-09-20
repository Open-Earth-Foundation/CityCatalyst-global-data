from state.agent_state import AgentState


def create_output_files_agent(state: AgentState):
    print("\nCREATE OUTPUT FILES AGENT\n")

    code = state.get("structured_output_stationary_energy_transportation")["code"]
    reasoning = state.get("structured_output_stationary_energy_transportation")[
        "reasoning"
    ]

    with open("./generated/generated_script.py", "w") as file:
        file.write(code)

    with open("./generated/generated_reasoning.md", "w") as file:
        file.write(reasoning)
