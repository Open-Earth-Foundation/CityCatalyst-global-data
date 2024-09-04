# generated_script.py

from transform_logic import transform

if __name__ == "__main__":
    import sys

    inputfile = sys.argv[1]
    user_provided_context = sys.argv[2]
    verbose = sys.argv[3]

    print("inputfile: ", inputfile)
    print("user_provided_context: ", user_provided_context)
    print("verbose: ", verbose)

    generated_script = transform(inputfile, user_provided_context, verbose)

    # Write the generated script to a file
    with open("generated_script.py", "w") as file:
        file.write(generated_script)
