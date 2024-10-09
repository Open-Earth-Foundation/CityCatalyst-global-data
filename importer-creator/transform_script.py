# transform_script.py

import json
import pandas as pd
from langchain.agents.agent import AgentExecutor
from transform_logic import transform

if __name__ == "__main__":
    import sys
    import os

    # Get the command line arguments and handling boolean values
    inputfile: str = sys.argv[1]
    context_user_provided: str = sys.argv[2]
    verbose: bool = sys.argv[3] in ["True", "true"]
    show_graph: bool = sys.argv[4] in ["True", "true"]
    hitl: bool = sys.argv[5] in ["True", "true"]

    full_path = os.path.join("./files/", inputfile)

    print("\ninputfile: ", inputfile)
    print("full_path: ", full_path)
    print("user_provided_context: ", context_user_provided)
    print("verbose: ", verbose)
    print("show_graph: ", show_graph)
    print("hitl: ", hitl)

    state = transform(full_path, context_user_provided, verbose, show_graph, hitl)

    # Custom encoder to handle non-serializable objects
    def custom_encoder(obj):
        # Convert complex object to string
        if isinstance(obj, AgentExecutor):
            return str(obj)
        # Convert pandas DataFrame to a dictionary or list
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient="records")
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )

    # Write the 'state' dictionary directly to a JSON file
    print("\n\nWRITING FINAL STATE TO JSON\n\n")
    with open("./generated/final_state.json", "w") as file:
        json.dump(state, file, indent=4, default=custom_encoder)
