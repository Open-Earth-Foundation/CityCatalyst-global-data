# Creating a Python Virtual Environment and Installing Requirements

To set up a Python virtual environment and install the dependencies specified in the `requirements.txt` file, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the project directory where the `requirements.txt` file is located.

3. Create a new virtual environment by running the following command:

   ```bash
   python -m venv .venv
   ```

   This will create a new directory named `.venv` in your project directory, which will contain the virtual environment.

4. Activate the virtual environment. The command to activate the virtual environment depends on your operating system:

   - On Windows:

     ```bash
     .venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source .venv/bin/activate
     ```

   Once activated, you should see `(venv)` or a similar indicator in your command prompt.

5. Install the required packages by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

   This will install all the packages listed in the `requirements.txt` file into your virtual environment.

# Running the script

The script can be run by the following command:

`python transform_script.py "inputfile" "Additional user info" verbose show_graph`

The parameters are:

- "inputfile": the name of the input file e.g. "input_1.csv"
- "Additional user info": Meta information about the file, e.g. information provided by the uploader of the file
- "verbose": Either 'true' or 'false'. On 'true' will output all the textout of the agents
- "show_graph": Either 'true' or 'false'. On 'true' will show the graph

# Input

Currently the script accepts .csv, .xls or .xlsx

# Output

The script will output three files:

- generated_script.py
  This is the pthon code which is doing the transformation and which can be processed for downstream tasks
- formatted.csv
  This is the formatted input file, transformed based on the `generated_script.py`
- generated_reasoning.py
  This is a markdown file with the reasoning of the model, to check the assumptions.

# Current limitations

Limitations:

- There are no steps for any preprocessing of the data before loading into a pandas dataframe. This can cause issues, if
  a) the datafile is very poorly formatted so that it cannot be meaningfully loaded into a dataframe and connections (columns vs. rows) get lost or altered which is especially true for .xls and .xlsx files
  b) e.g. a .csv file had additional data on top of the actual data rows (e.g. added meta data). Then it cannot be parsed into a pandas dataframe
- The extraction of the data currently assumes that one datafile is containing data to either stationary energy and/or transportation or waste.
