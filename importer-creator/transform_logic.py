import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor
from langchain_experimental.agents import create_pandas_dataframe_agent

from dotenv import load_dotenv

# Load the .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

context = """
The following gives an overview of the different GPC sectors, subsectors and what they are associated with.

There are 3 sectors to choose from:
- **"Stationary Energy"**,
- **"Transportation"**,
- **"Waste"**

For **"Stationary Energy"** there are 9 sub-sectors to choose from:
- "Residential buildings"
- "Commercial and institutional buildings and facilities"
- "Manufacturing industries and construction"
- "Energy industries
- "Energy generation supplied to the grid"
- "Agriculture, forestry, and fishing activities"
- "Non-specified sources"
- "Fugitive emissions from mining, processing, storage, and transportation of coal"
- "Fugitive emissions from oil and natural gas systems"

For **"Transportation"** there are 5 sub-sectors to choose from:
- "On-road"
- "Railways"
- "Waterborne navigation"
- "Aviation"
- "Off-road"

For **"Waste"** there are 8 sub-sectors to choose from:
- "Disposal of solid waste generated in the city"
- "Disposal of solid waste generated outside the city"
- "Biological treatment of waste generated in the city"
- "Biological treatment of waste generated outside the city"
- "Incineration and open burning of waste generated in the city"
- "Incineration and open burning of waste generated outside the city"
- "Wastewater generated in the city"
- "Wastewater generated outside the city"

Each data file can only be associated with one sector and one sub-sector and can never have multiple sectors or multiple sub-sectors.

The following is a description of the different sectors to help identify the correct sector:
- Stationary Energy: 
    Stationary energy sources are one of the largest contributors to a city’s GHG emissions.
    These emissions come from the combustion of fuel in residential, commercial and
    institutional buildings and facilities and manufacturing industries and construction, as well
    as power plants to generate grid-supplied energy. This sector also includes fugitive
    emissions, which typically occur during extraction, transformation, and transportation of
    primary fossil fuels.

- Transportation:
    Transportation covers all journeys by road, rail, water and air, including inter-city and
    international travel. GHG emissions are produced directly by the combustion of fuel or
    indirectly by the use of grid-supplied electricity. Collecting accurate data for transportation
    activities, calculating emissions and allocating these emissions to cities can be a particularly
    challenging process. To accommodate variations in data availability, existing transportation
    models, and inventory purposes, the GPC offers additional flexibility in calculating emissions
    from transportation.

- Waste:
    Waste disposal and treatment produces GHG emissions through aerobic or anaerobic
    decomposition, or incineration. GHG emissions from solid waste shall be calculated by disposal
    route, namely landfill, biological treatment and incineration and open burning. If methane is
    recovered from solid waste or wastewater treatment facilities as an energy source, it shall be
    reported under Stationary Energy. Similarly, emissions from incineration with energy recovery
    are reported under Stationary Energy.

- Industrial Process And Product Use (IPPU):
    GHG emissions are produced from a wide variety of non-energy related industrial activities.
    The main emission sources are releases from industrial processes that chemically or physically
    transform materials (e.g., the blast furnace in the iron and steel industry, and ammonia and
    other chemical products manufactured from fossil fuels and used as chemical feedstock).
    During these processes many different GHGs can be produced. In addition, certain products
    used by industry and end-consumers, such as refrigerants, foams or aerosol cans, also contain
    GHGs which can be released during use and disposal.

- Agriculture, Forestry and other Land Use (AFOLU):
    Emissions and removals from the Agriculture, Forestry and Other Land Use (AFOLU) sector are
    produced through a variety of pathways, including livestock (enteric fermentation and manure
    management), land use and land use change (e.g., forested land being cleared for cropland
    or settlements), and aggregate sources and non-CO2 emission sources on land (e.g., fertilizer
    application and rice cultivation).    
"""


# Define the state
class AgentState(TypedDict):
    agent: Annotated[AgentExecutor, "The pre-instantiated agent"]
    context: Annotated[str, "The context of the task"]
    user_provided_context: Annotated[str, "The user provided context"]
    task: Annotated[str, "The task to be performed"]
    pandas_df: Annotated[pd.DataFrame, "The input pandas DataFrame"]
    file_path: Annotated[str, "The file path of the original data file"]
    summary: Annotated[str, "Summary and detailed description of the file"]
    extracted_data: Annotated[dict, "Extracted specific data from the file"]
    reasoning_agent_feedback: Annotated[str, "Feedback from the reasoning agent"]
    final_output: Annotated[dict, "Final approved output"]
    reasoning_agent_iterations: Annotated[
        int, "Number of iterations by the reasoning agent"
    ]
    coding_agent: Annotated[AgentExecutor, "The pre-instantiated coding agent"]
    coding_task: Annotated[str, "The task to be performed for code generation"]
    generated_code: Annotated[str, "Generated code"]
    code_reasoning_agent_feedback: Annotated[
        str, "Feedback from the code reasoning agent"
    ]
    code_reasoning_agent_iterations: Annotated[
        int, "Number of iterations by the code reasoning agent"
    ]
    final_code_output: Annotated[str, "Final code output"]


def load_datafile_into_df(file_path):

    # Check if the file exists and its type
    if os.path.exists(file_path):
        print(f"File found: {os.path.basename(file_path)}")
        if file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)

        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)

        else:
            print("Unsupported file type. Please provide a CSV or Excel file.")
            return None

        return df
    else:
        print(f"File not found: {os.path.basename(file_path)}")


def transform(file_path, user_provided_context, verbose):
    # Transformation logic

    # Create pandas dataframe agent
    def create_agent(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

        # Initialize the LLM
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        return create_pandas_dataframe_agent(
            llm,
            df,
            verbose=verbose,
            agent_type="tool-calling",
            allow_dangerous_code=True,
        )

    # Create agent for code generation
    def create_coding_agent(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

        # Initialize the LLM
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        # llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)

        return create_pandas_dataframe_agent(
            llm,
            df,
            verbose=verbose,
            agent_type="tool-calling",
            # return_intermediate_steps=True,
            # max_iterations=5, # this value can be adapted to speed up the process but potentially decrease accuracy
            allow_dangerous_code=True,
        )

    def summary_agent(state: AgentState) -> dict:
        print("\nSUMMARY AGENT\n")

        prompt = f"""

            This is the user provided context: {state['user_provided_context']}.
            Provide a detailed summary of this DataFrame {state['pandas_df']}. 
            This is the path to the original data file: {state['file_path']}.
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

        # Invoke summary agent with custom prompt
        summary = state["agent"].invoke(prompt)
        return {"summary": summary.get("output")}

    def extraction_agent(state: AgentState) -> dict:
        print("\nEXTRACTION AGENT\n")

        # print("\n", state["reasoning_agent_feedback"], "\n")

        # Agent logic to extract specific data
        prompt = f"""
            This is the provided context: {state['context']},
            This is the user provided context: {state['user_provided_context']},
            This is your task: {state['task']},
            This is the summary of the previous agent: {state['summary']}.
            This is the orgignal dataframe 'df': {state['pandas_df']}. 
            This is the path to the original data file: {state['file_path']}.

            If you have received feedback from the reasoning agent, you find it here: {state['reasoning_agent_feedback']}
            If feedback is available, pay special attention to this feedback and incorporate into your data extracation process.
            """
        extracted_data = state["agent"].invoke(prompt)

        return {"extracted_data": extracted_data.get("output")}

    def reasoning_agent(state: AgentState) -> dict:
        print("\nREASONING AGENT\n")

        # Check if the iteration limit has been reached
        if state["reasoning_agent_iterations"] >= 5:
            print(
                "\nIteration limit reached. Automatically approving the extraction agent's output.\n"
            )
            return {"final_output": state["extracted_data"]}

        prompt = f"""
            Your task is to check and verify the output of a previous agent. You have access to the following information:
            1. the original pandas dataframe: {state['pandas_df']},
            2. the path to the original data file: {state['file_path']}.
            3. the summary and detailed description of this dataframe provided by the previous agent: {state['summary']},
            4. the original task: {state['task']},
            5. the extracted data of the previous agent: {state['extracted_data']},
                - this contains only a json without further explanations. Only check if the values are correctly extracted.
            6. the provided context: {state['context']},
            7. the user provided context: {state['user_provided_context']}.

            If you have given previous feedback to the extraction agent, you find it here: {state['reasoning_agent_feedback']}
            If you have given feedback, check the extracted data of the agent against your feedback. 
            If the extracted data aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.
            
            If you approve, return 'APPROVED'. If not, return 'FEEDBACK: [Your feedback here]'
            """
        response = state["agent"].invoke(prompt)

        if "APPROVED" in response.get("output"):

            return {"final_output": state["extracted_data"]}
        else:
            return {
                "reasoning_agent_feedback": response.get("output"),
                "reasoning_agent_iterations": state["reasoning_agent_iterations"] + 1,
            }

    # Define code generation agent
    def code_generation_agent(state: AgentState) -> dict:
        print("\nCODE GENERATION AGENT\n")

        prompt = f"""
            This is your task: {state['coding_task']}.
            This is the summary of the previous agent: {state['summary']}.
            This is the extracted data from the previous agent: {state['final_output']}.
            This is the pandas dataframe of the original data file: {state['pandas_df']}.
            This is the file name of the original data file: {state['file_path']}.

            If you have received feedback from the 'code reasoning agent', you find it here: {state['code_reasoning_agent_feedback']}.
            If feedback is available, pay special attention to this feedback and incorporate into your data extracation process.
            Especially pay attention to feedback related to errors in code. 

            THE CODE MUST BE EXECUTABLE!
            """

        # Invoke code agent with custom prompt
        response = state["coding_agent"].invoke(prompt)

        return {"generated_code": response.get("output")}

    def code_reasoning_agent(state: AgentState) -> dict:
        print("\nCODE REASONING AGENT\n")

        # Check if the iteration limit has been reached
        if state["code_reasoning_agent_iterations"] >= 5:
            print(
                "\nIteration limit reached. Automatically approving the last output of the code generation agent.\n"
            )
            return {"final_code_output": state["generated_code"]}

        prompt = f"""
            Your task is to run the code and check for any code errors that occur when running the code. If you execute the code and you are running into an error,
            provide the entire detailed error description as feedback.

            This is the generated code of the previous agent: {state['generated_code']}
            This is the task of the previous agent: {state['coding_task']}

            If you have given previous feedback to the code generation agent, you find it here: {state['code_reasoning_agent_feedback']}
            If you have given feedback, check the generated code of the previous agent against your feedback. 
            If the generated code aligns with your provided feedback, accept the answer. Othwerwise, provide new feedback.

            THE CODE MUST BE EXECUTABLE WITHOUT ANY ERRORS!
            
            If you approve, return 'APPROVED'. If not, return 'FEEDBACK: [Your feedback here]'
            """
        response = state["coding_agent"].invoke(prompt)

        if "APPROVED" in response.get("output"):
            return {"final_code_output": state["generated_code"]}
        else:
            return {
                "code_reasoning_agent_feedback": response.get("output"),
                "code_reasoning_agent_iterations": state[
                    "code_reasoning_agent_iterations"
                ]
                + 1,
            }

    # Define the conditional edge
    def should_extraction_continue(state: AgentState) -> str:
        if state.get("final_output"):
            return "code_generatoin_agent"
        return "extraction_agent"

    # Define the conditional edge
    def should_code_continue(state: AgentState) -> str:
        if state.get("final_code_output"):
            return "end"
        return "code_generation_agent"

    # Define the graph
    def create_workflow():
        workflow = StateGraph(AgentState)

        # Add nodes to the graph
        workflow.add_node("summary_agent", summary_agent)
        workflow.add_node("extraction_agent", extraction_agent)
        workflow.add_node("reasoning_agent", reasoning_agent)
        workflow.add_node("code_generation_agent", code_generation_agent)
        workflow.add_node("code_reasoning_agent", code_reasoning_agent)

        # Set the entrypoint
        workflow.set_entry_point("summary_agent")

        # Add edge to end the workflow after summary
        workflow.add_edge("summary_agent", "extraction_agent")
        workflow.add_edge("extraction_agent", "reasoning_agent")

        # Add conditional edge
        workflow.add_conditional_edges(
            "reasoning_agent",
            should_extraction_continue,
            {
                "extraction_agent": "extraction_agent",
                "code_generatoin_agent": "code_generation_agent",
            },
        )

        workflow.add_edge("code_generation_agent", "code_reasoning_agent")

        # Add conditional edge
        workflow.add_conditional_edges(
            "code_reasoning_agent",
            should_code_continue,
            {
                "code_generation_agent": "code_generation_agent",
                "end": END,
            },
        )

        return workflow.compile()

    # Function to run the workflow
    def process_dataframe(
        context: str,
        user_provided_context: str,
        task: str,
        coding_task: str,
        df: pd.DataFrame,
        file_path: str,
        verbose: bool = False,
    ):

        agent = create_agent(df, verbose)
        coding_agent = create_coding_agent(df, verbose)
        app = create_workflow()

        inputs = AgentState(
            agent=agent,
            context=context,
            user_provided_context=user_provided_context,
            task=task,
            pandas_df=df,
            file_path=file_path,
            summary="",
            extracted_data={},
            reasoning_agent_feedback="",
            final_output={},
            reasoning_agent_iterations=0,
            coding_agent=coding_agent,
            coding_task=coding_task,
            generated_code="",
            code_reasoning_agent_feedback="",
            code_reasoning_agent_iterations=0,
            final_code_output="",
        )

        print(app.get_graph().draw_ascii())

        result = app.invoke(inputs)

        return result

    df = load_datafile_into_df(file_path)

    task = """
        Your task is to extract the following data from the provided dataframe.
        1. What is the region that the data is associated with? 
            - Be specific. E.g. if only a country is mentioned, then the region is the country. 
            - If a city or a region (e.g. a state) is mentioned, use the specific city or region. 
        2. What is the temporal resolution of the data? Are the data points ordered by days, weeks, month or years?
        3. What is the associated sector according to Greenhouse Gas Protocol for Cities (GPC)
        4. What is the accociated sub-sector according to Greenhouse Gas Protocol for Cities (GPC)

        For valid sectors and sub-sectors, refer to the provided context.
        Specifically take the user provided context into account.

        You return only a valid JSON schema without any additional text or notes like:

        {
            "region": "value",
            "temporal_resolution": "value",
            "sector": "value",
            "sub-sector": "value"
        }
        """

    coding_task = """
        Your task is to create a python script. This script must be runnable and executable.

        You have access to the following:
        - original pandas dataframe
        - summary and detailed description of this dataframe provided by the previous agent
        - the extracted data of the previous agent

        Do not delete any empty columns. Keep the original data intact. If rows have data for certain columns, keep them!

        Based on the original dataframe, and the summary which provides you with insights about the data and potential formatting issues, 
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
            * keep the original values of each row
                try to fix format or data type issues but preserve the original data as much as possible,
            * if there are no proper clumns names, create new columns based on the first row of the dataframe,
            * normalize column names to 'lower case' and strip them of any leading or trailing white spaces,
            * convert any date columns to a valid datetime format based on the available data. 
            Automatically infer the format from the available data. E.g. use the extracted value 'temporal_resolution' as a guiding point. 
            Pay attention to columns that might not be clearly labeled as 'date' or 'dates' or similar. 
            * create new columns 'gpc sector' and 'gpc sub-sector' which contain the corresponding values of the dict variable "extracted_data",
            * improve the formatting based on the initial analysis of the summary agent,
        - code that creates a .csv file from the new dataframe 'df_new'. The name of .csv file should be 'formatted.csv',

        THE CODE MUST BE EXECUTABLE WITHOUT ANY ERRORS!

        Do not give any additional text or explanations and ONLY return the python code.
        Do not include ```python``` before or after the code.

        Example:
        [Your python code here]
        """

    state = process_dataframe(
        context=context,
        user_provided_context=user_provided_context,
        task=task,
        coding_task=coding_task,
        df=df,
        file_path=file_path,
        verbose=verbose,
    )

    generated_script = state.get("final_code_output")

    return generated_script