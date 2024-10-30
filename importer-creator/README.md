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

The script is using Python 3.12.4.

```bash
pip install -r requirements.txt
```

This will install all the packages listed in the `requirements.txt` file into your virtual environment.

# Running the script

The parameters are:

flags:
--input-file
--datasource-name
--user-input
--verbose
--show-graph
--hitl

The script can be run by the following command:

`python transform_script.py --input-file FILENAME --datasource-name DATASOURCE --user-input CONTEXT --verbose --show-graph --hitl`

--input-file is required. The script will be looking for the file name inside /files folder
--datasource-name and --user-input are recommended to pass in as much information about the dataset as available
--verbose will enable LLM output to the console for debugging. However debugging via LangSmith is recommended
--show-graph will show the agent pipeline at the beginning of the script
--hitl will enable intermediate human-in-the-loop input

Example:

`python transform_script.py --input-file UAE_fuel_sales.csv --datasource-name "Ministry of Energy & Infrastructure (MEAI)" --user-input "A dataset about oil and gas sales for different regions in the United Arab Emirates (UAE) for the years 2015 to 2020 provided by the Ministry of Energy & Infrastructure (MEAI)" --show-graph`

# Input

Currently the script accepts clean .csv files with one data entry per row

# Output

The script will output three files after each step:

- python script
  This is the pthon code which is doing the transformation and which can be processed for downstream tasks
- csv file
  This is the formatted input file after the step, transformed based on the python script
- markdown file
  This is a markdown file with the reasoning of the model, to check the assumptions.
