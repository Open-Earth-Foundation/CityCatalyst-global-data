import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_core.pydantic_v1 import BaseModel, Field


# Create agent for code generation
def create_coding_agent(df: pd.DataFrame, verbose: bool) -> AgentExecutor:

    model = "gpt-4o-2024-08-06"

    # Initialize the LLM
    llm = ChatOpenAI(model=model, temperature=0)

    return create_pandas_dataframe_agent(
        llm,
        df,
        verbose=verbose,
        agent_type="tool-calling",
        prefix="""
You are a professional data engineer who is specialized in data analysis and creating functional python scripts with the pandas library.

You have access to one main tool:
1. A Python REPL tool for data analysis, which can be used to manipulate and query the pandas DataFrame 'df'

When using the Python REPL tool make sure to always import all necessary libraries at the beginning of your code. 
Especially always import pandas in the first line.
```python
import pandas as pd
```
""",
        suffix="",
        include_df_in_prompt=False,
        allow_dangerous_code=True,
    )


# The following agent is currently not used, but could potentially be used to fix output format issues
# Those are currently handled manually without the use of an LLM agent
# Define the input schema for the GenerateOutput tool
class GenerateOutputInput(BaseModel):
    reasoning: str = Field(..., description="Your detailed reasoning here...")
    code: str = Field(..., description="Your pure executable Python code here...")


# Create agent for code generation
def create_coding_agent_with_structured_output(
    df: pd.DataFrame, verbose: bool
) -> AgentExecutor:

    model = "gpt-4o-2024-08-06"

    # Define a function to generate structured output
    def generate_output(reasoning: str, code: str) -> dict:
        return {"reasoning": reasoning, "code": code}

    # Create a tool for generating structured output
    output_tool = StructuredTool(
        name="GenerateOutput",
        func=generate_output,
        args_schema=GenerateOutputInput,
        description="""
        Use this tool to output structured JSON data including reasoning and executable code. 
        The reasoning should explain the approach, and the code should be pure executable Python code.
        """,
    )

    # Initialize the LLM
    llm = ChatOpenAI(model=model, temperature=0)
    # llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0)

    return create_pandas_dataframe_agent(
        llm,
        df,
        verbose=verbose,
        agent_type="tool-calling",
        prefix="""
You are a professional software engineer who is specialized in creating functional python scripts.

You have access to two main tools:
1. A Python REPL tool for data analysis, which can be used to manipulate and query the DataFrame 'df'
2. A GenerateOutput tool for generating structured outputs, including reasoning and code. At the end of each run, always use this tool to output a structured JSON response.

When using the Python REPL tool:
- make sure to always import all necessary libraries at the beginning of your code. Especially always import pandas.
<code>
import pandas as pd
</code>
- Use the following code every time you are asked to inspect the dataframe 'df':
<code>
import pandas as pd
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns 
print(df)
</code>

When using the GenerateOutput tool:
- Provide clear, structured reasoning and executable Python code.
""",
        suffix="""
Important:
- Do not just use df.head() to make assumptions over the content of the entire dataframe. This will only print the first 5 rows. You must always inspect the entire dataframe which means all rows and all columns.
- **ENSURE** that all your generated output of e.g. reasoning and python code uses UTF-8 encoding. Convert special characters to UTF-8 encoding.
- **ENSURE** that your final output is valid JSON ONLY and does not include any additional commentary or explanation.
- **DO NOT** surround the JSON output with any code block markers or tags like ```json```.
""",
        allow_dangerous_code=True,
        include_df_in_prompt=False,
        extra_tools=[output_tool],
    )


# Define input schema for structured output
class GenerateOutputInput(BaseModel):
    reasoning: str = Field(..., description="Your detailed reasoning here...")
    code: str = Field(..., description="Your pure executable Python code here...")


# Create the agent for JSON output
def llm_with_structured_output(verbose: bool) -> AgentExecutor:

    model = "gpt-4o-mini"

    llm = ChatOpenAI(model=model, temperature=0, verbose=verbose)
    structured_llm = llm.with_structured_output(GenerateOutputInput)
    return structured_llm
