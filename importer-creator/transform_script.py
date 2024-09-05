# transform_script.py

from transform_logic import transform

if __name__ == "__main__":
    import sys
    import os

    inputfile = sys.argv[1]
    user_provided_context = sys.argv[2]
    verbose = sys.argv[3]
    show_graph = sys.argv[4]

    full_path = os.path.join("./files/", inputfile)

    print("inputfile: ", inputfile)
    print("full_path: ", full_path)
    print("user_provided_context: ", user_provided_context)
    print("verbose: ", verbose)
    print("show_graph: ", show_graph)

    generated_script = transform(full_path, user_provided_context, verbose, show_graph)

    # Write the generated script to a file
    with open("generated_script.py", "w") as file:
        file.write(generated_script)
