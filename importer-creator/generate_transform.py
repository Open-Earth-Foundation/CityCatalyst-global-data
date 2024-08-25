# Description: Generate a transformer script

template = """
# %s

from transform_logic import transform

if __name__ == "__main__":
    import sys

    transform(sys.argv[1], sys.argv[2])
"""


def generate_transformer(inputfile, scriptfile):
    with open(scriptfile, "w") as f:
        f.write(template % scriptfile)


if __name__ == "__main__":
    import sys

    generate_transformer(sys.argv[1], sys.argv[2])
