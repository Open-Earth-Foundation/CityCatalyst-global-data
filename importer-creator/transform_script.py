# transform_script.py

import json
from transform_logic import transform

if __name__ == "__main__":
    import sys
    import os

    inputfile = sys.argv[1]
    context_user_provided = sys.argv[2]
    verbose = sys.argv[3]
    show_graph = sys.argv[4]

    full_path = os.path.join("./files/", inputfile)

    print("inputfile: ", inputfile)
    print("full_path: ", full_path)
    print("user_provided_context: ", context_user_provided)
    print("verbose: ", verbose)
    print("show_graph: ", show_graph)

    state = transform(full_path, context_user_provided, verbose, show_graph)
    # print("\n\n\nGET FINAL OUTPUT\n\n\n")

    # code = final_output.get("code")
    # reasoning = final_output.get("reasoning")

    # Create a script and reasoning file
    print("\nWRITE FINAL STATE TO FILE\n")
    with open("./generated/final_state.txt", "w") as file:
        json.dump(state, file, indent=4)

    # print("\nCREATE MARKDOWN FILE\n")
    # with open("./generated/generated_reasoning.md", "w") as file:
    #     file.write(reasoning)

    # generated_script = transform(full_path, context_user_provided, verbose, show_graph)
    # # Write the generated script to a file
    # with open("generated_script.py", "w") as file:
    #     file.write(generated_script)
