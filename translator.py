from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, Dict, List
import yaml
from pathlib import Path
import json
from langsmith.wrappers import wrap_openai
from langsmith import traceable
from pydantic import BaseModel, RootModel, Field

load_dotenv()

# Define paths
PATH_TO_YAML = Path("./cc-mage/datasets/datasource_seeder.yaml")

client = wrap_openai(OpenAI())


class TranslationModel(BaseModel):
    country_code: str
    translation: str


class DatasetModel(BaseModel):
    dataset_name: TranslationModel
    dataset_description: TranslationModel
    methodology_description: TranslationModel
    transformation_description: TranslationModel


@traceable
def get_llm_response(user_prompt: str, target_language: str) -> Optional[str]:

    system_prompt = f"""
You are a professional translator with deep domain knowledge in data science with a focus on climate change.

Your task is to translate input strings to a target language.
The input strings are in English and potentially multiple other languages. 
Use the input provided in all languages to create a translation for the target language which has the same meaning as all the inputs.
The target language is provided as ISO 639 language codes. E.g. 'en' stands for English, 'es' for spanish and so on.

The target language is: {target_language}.

**Input:**
You are provided with multiple attribute names that need to be translated to the target language at the same time.
Each key contains a dictionary with a sentence in one or more languages.

**Output:**
The output must be a translation of the input sentence in the target language.
The output format must be in pure JSON format as follows:

{{
    "attribute_name_1": {{
        "country_code": "The country code of the target language",
        "translation": "Translated text in the target language"
    }},
    "attribute_name_2": {{
        ...
    }},
    ...
}}

**Important Guidelines:**

1. Maintain the original meaning and tone of the input while ensuring linguistic accuracy.
2. If there are ambiguities in the input, prioritize clarity in the translation.
3. If domain-specific terms appear, use appropriate equivalents in the target language if available and commonly used in that language. If no equivalent exists, use the English domain-specific term.
"""

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        response_format=DatasetModel,
    )
    return response.choices[0].message.content


def read_yaml(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


dict_yaml = read_yaml(PATH_TO_YAML)

for datascource in dict_yaml[:1]:

    # Extract keys to translate
    dataset_name = datascource["dataset_name"]
    dataset_description = datascource["dataset_description"]
    methodology_description = datascource["methodology_description"]
    transformation_description = datascource["transformation_description"]

    # Translate keys
    prompt = f"""
<inputs>
These are the current inputs:
- dataset_name: {json.dumps(dataset_name, indent=4)}
- dataset_description: {json.dumps(dataset_description, indent=4)}
- methodology_description: {json.dumps(methodology_description, indent=4)}
- transformation_description: {json.dumps(transformation_description, indent=4)}
</inputs>
"""
    translation_str = get_llm_response(prompt, target_language="de")

    if translation_str:
        print("Translation successful!")
        print(translation_str)
