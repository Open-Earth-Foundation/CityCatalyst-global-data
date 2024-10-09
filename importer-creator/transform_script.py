# transform_script.py
import sys
import os
import argparse
import json
import pandas as pd
from langchain.agents.agent import AgentExecutor
from transform_logic import transform

if __name__ == "__main__":

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Transform script with optional flags."
    )

    # Required arguments
    parser.add_argument("inputfile", type=str, help="Input file name")
    parser.add_argument(
        "context_user_provided", type=str, help="Context provided by the user"
    )

    # Optional flags
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")
    parser.add_argument("--show-graph", action="store_true", help="Show graph option")
    parser.add_argument("--hitl", action="store_true", help="Enable human-in-the-loop")

    # Parse arguments
    args = parser.parse_args()

    # Resolve file path
    full_path = os.path.join("./files/", args.inputfile)

    print("\ninputfile: ", args.inputfile)
    print("full_path: ", full_path)
    print("user_provided_context: ", args.context_user_provided)
    print("verbose: ", args.verbose)
    print("show_graph: ", args.show_graph)
    print("hitl: ", args.hitl)

    state = transform(
        full_path, args.context_user_provided, args.verbose, args.show_graph, args.hitl
    )

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
