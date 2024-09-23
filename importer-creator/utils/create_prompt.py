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

    3. You are already provided with the dataframe 'df' containing the activities.

    4. To complete this task: 
        {completion_steps}

    5. Present your answer in the following format: 
        {answer_format}

    6. You are given additional information that is helpful in completing your task:
        {additional_information}

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
