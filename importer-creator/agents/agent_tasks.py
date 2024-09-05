# agent_tasks.py

# Description for the task of the summary agent
task_summary_agent = """
Provide a detailed summary of the provided DataFrame 'df'.
Include information about its structure, data types, basic statistics, and any notable patterns or insights.
    
1. First give a general summary about the content of the data.

2. Then describe the format of the dataframe in detail. Pay special attention to the following points:
    - nuber of rows and columns
        * are the number of columns consistent throughout the rows? Or is there a mismatch?
    - column names
        * what are the column names?
        * is the same naming convention used?
        * are there spaces before or after the names that could lead to issues?
    - which columns contain dates? The name of the column could be an indicator but check also for values inside the rows
    - data types of each column
    - any missing values
    - additional potential formatting issues with the original file
        * especially if the file contains additional text information that is not part of the actual data but 
        data that is added manually on top of the actual rows e.g. meta data.
        * especially if the file contains additional text information that is not part of the actual data but
        data that is added below the actual rows e.g. footnotes.

Give thoughts about how to solve these issues based on your analysis.
"""

# Description for the task of the extraction agent
task_extraction_agent = """
Your task is to extract the following data from the provided dataframe 'df'.
1. What is the region that the data is associated with? 
    - Be specific. E.g. if only a country is mentioned, then the region is the country. 
    - If a city or a region (e.g. a state) is mentioned, use the specific city or region. 
2. What is the temporal resolution of the data? Are the data points ordered by days, weeks, month or years?
3. What is the associated sector according to Greenhouse Gas Protocol for Cities (GPC)
4. What is the accociated sub-sector according to Greenhouse Gas Protocol for Cities (GPC)

For valid sectors and sub-sectors, refer to the provided context.
Specifically take the user provided context into account.

You return only a valid JSON schema without any additional text or hints like:

{
    "region": string,
    "temporal_resolution": string,
    "sector": string,
    "sub-sector": string
}
"""

# Description for the task of the reasoning agent
task_reasoning_agent = f"""
Your task is to check and verify the output of a previous extraction agent. 
The task of the previous extraction agent was:
{task_extraction_agent}

            
If you approve, return 'APPROVED'. If not, return 'FEEDBACK: [Your feedback here]'
"""

# Description for the task of the code generation agent
task_code_generation_agent = """
Your task is to create a python script. 
This script must be executable!

Do not delete any empty columns. Keep the original data intact. If rows have data for certain columns, keep them!

Based on the provided original dataframe 'df', and the summary which provides you with insights about the data and potential formatting issues, 
create a python script which generates a better formatted pandas dataframe with clearly ordered and named columns. E.g., if the previous agent found that there are formatting issues, 
try to solve them so that the original data stays intact, but the dataframe is properly formatted. 
The new script must only focus on the actual data which can be displayed as rows and columns in a pandas dataframe.
E.g. if there is meta data above the actual data in the original file, the script should not include this meta data in the final .csv output.
Also if there is meta data below the actual data in the original file like footnotes, the script should not include this meta data in the final .csv output.

The script must have the following:
    - code to load the original file into a pandas dataframe 'df',
    - a dict variable "extracted_data" = { ... } with the the extracted data from the previous agent,
    - a new pandas dataframe 'df_new' as a copy of the original dataframe 'df'
    - for the new dataframe 'df_new' do the following:
        * preserve the original values of each row, if they seem valid. Otherwise:
            - try to fix the values if you identified issues
        * if there are no proper clumns names, create new columns based on the first row of the dataframe,
        * normalize column names to 'lower case' and strip them of any leading or trailing white spaces,
        * convert any date columns to a valid datetime format based on the available data.
            - Automatically infer the format from the available data. E.g. use the extracted value 'temporal_resolution' as a guiding point.
            - Pay attention to columns that might not be clearly labeled as 'date' or 'dates' or similar.
        * create new columns 'gpc sector' and 'gpc sub-sector' which contain the corresponding values of the dict variable "extracted_data",
        * improve the formatting based on the initial analysis of the summary agent (e.g., format or data type issues),
    - code that creates a .csv file from the new dataframe 'df_new'. The name of .csv file should be 'formatted.csv'.

THE CODE MUST BE EXECUTABLE WITHOUT ANY ERRORS!

Do not give any additional text or explanations and ONLY return the python code.
Do not include ```python``` before or after the code.

Example:
[Your python code here]
"""

# Description for the task of the code reasoning agent
task_code_reasoning_agent = f"""
Your task is to check and verify the output of a previous code generation agent. 
Check for any code errors that occur when running the code. If you execute the code and you are running into an error, provide the entire detailed error description as feedback. 
Check if the previous agent fullfilled the requirements of its task.

The task of the previous extraction agent was:
{task_code_generation_agent}

If you approve, return 'APPROVED'. If not, return 'FEEDBACK: [Your feedback here]'.
"""
