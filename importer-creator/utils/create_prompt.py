# prompt_template.py

from langchain.prompts import PromptTemplate


def create_prompt(
    task: str, completion_steps: str, answer_format: str, additional_information: str
) -> str:

    template = """
{task} 

Use the additional provided information below marked with <additional_information> tags.

Follow these instructions carefully:
1. Think step-by-step.

2. Consider the human-in-the-loop feedback provided in the <feedback_human-in-the-loop> tags below if available. This is the most important feedback to consider for your data extraction process. Rank this specific human-in-the-loop feedback highest in your considerations and make sure to incorporate it into your thinking.

3. To complete this task: 
{completion_steps}

4. Present your answer in the following format: 
{answer_format}

5. You are given additional information that is helpful in completing your task:
{additional_information}

Important:
- Do not just use df.head() to make assumptions over the content of the entire dataframe. This will only print the first 5 rows. You must always inspect all the unique values of each column containing strings or objects to get an understanding of all the values inside the dataframe for all rows and all columns.
- **ENSURE** that all your generated output of e.g. reasoning and python code uses UTF-8 encoding. Convert special characters to UTF-8 encoding.
- **ENSURE** that your final output is valid JSON ONLY and does not include any additional commentary or explanation.
- **DO NOT** surround the JSON output with any code block markers or tags like ```json```.

Base your code generation on pandas version 2.2.2 and Python version 3.12.4.

Remember to base your response solely on the information provided in the dataframe and additional information. Do not make assumptions or use external knowledge.
"""

    prompt_template = PromptTemplate(
        input_variables=[
            "task",
            "completion_steps",
            "answer_format",
            "additional_information",
        ],
        template=template,
    )

    prompt = prompt_template.format(
        task=task,
        completion_steps=completion_steps,
        answer_format=answer_format,
        additional_information=additional_information,
    )

    return prompt
