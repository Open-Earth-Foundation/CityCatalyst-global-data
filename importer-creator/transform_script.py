# transform_script.py

import json
from langchain.agents.agent import AgentExecutor
from transform_logic import transform

if __name__ == "__main__":
    import sys
    import os

    inputfile = sys.argv[1]
    context_user_provided = sys.argv[2]
    verbose = sys.argv[3]
    show_graph = sys.argv[4]

    full_path = os.path.join("./files/", inputfile)

    print("\ninputfile: ", inputfile)
    print("full_path: ", full_path)
    print("user_provided_context: ", context_user_provided)
    print("verbose: ", verbose)
    print("show_graph: ", show_graph)

    state = transform(full_path, context_user_provided, verbose, show_graph)

    # Custom encoder to handle non-serializable objects
    def custom_encoder(obj):
        # Convert complex object to string
        if isinstance(obj, AgentExecutor):
            return str(obj)
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )

    # Write the 'state' dictionary directly to a JSON file
    print("\n\nWRITING FINAL STATE TO JSON\n\n")
    with open("./generated/final_state.json", "w") as file:
        json.dump(state, file, indent=4, default=custom_encoder)
