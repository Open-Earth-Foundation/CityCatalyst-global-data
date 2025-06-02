"""
This script automates the translation of dataset seeder YAML files for the CityCatalyst project.
It reads the YAML file containing dataset metadata (such as dataset name, description, methodology, and transformation description), uses an LLM (OpenAI) to generate translations for a specified target language, and updates the YAML file with the new translations.

Usage:
    python translator.py --language <language_code>

Arguments:
    --language: The ISO 639-1 code of the target language (e.g., 'es' for Spanish, 'pt' for Portuguese).

Example:
    python translator.py --language es

Requirements:
- Dependencies listed in requirements.txt (including openai, langsmith, pydantic, yaml, dotenv)
- An OpenAI API key set in your environment (see .env or dev.env)

The script will update the YAML file in-place with the new translations for the specified language.
"""

from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional
import yaml
from pathlib import Path
import json
from langsmith.wrappers import wrap_openai
from langsmith import traceable
from pydantic import BaseModel
import argparse

load_dotenv()

# Define paths
PATH_TO_YAML = Path("./cc-mage/datasets/datasource_seeder.yaml")
UPDATED_YAML_PATH = Path("./cc-mage/datasets/datasource_seeder_updated.yaml")

client = wrap_openai(OpenAI())


class TranslationModel(BaseModel):
    country_code: str
    translation: str


class DatasetModel(BaseModel):
    dataset_name: TranslationModel
    dataset_description: TranslationModel
    methodology_description: TranslationModel
    transformation_description: TranslationModel
    datasource_description: TranslationModel


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


def write_yaml(data: dict, file_path: Path):
    """
    Writes the updated YAML data back to the file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        yaml.dump(
            data, file, allow_unicode=True, sort_keys=False, default_flow_style=False
        )


def update_datasource(datasource: dict, updates: dict):
    """
    Updates a single datasource with the provided translations.

    Args:
        datasource (dict): The datasource to update.
        updates (dict): The translations to apply.
    """
    for key, value in updates.items():
        if key in datasource and isinstance(datasource[key], dict):
            # Add the new language translation under the existing key
            datasource[key][value["country_code"]] = value["translation"]


def translate(target_language: str):
    # Read the YAML file
    datasources = read_yaml(PATH_TO_YAML)

    for datasource in datasources:
        print("Now translating: ", datasource["datasource_id"])

        # Extract keys to translate
        # If values are empty, default to empty dictionaries
        dataset_name = datasource.get("dataset_name")
        dataset_description = datasource.get("dataset_description")
        methodology_description = datasource.get("methodology_description")
        transformation_description = datasource.get("transformation_description")
        datasource_description = datasource.get("datasource_description")

        # Translate keys
        prompt = f"""
        <inputs>
        These are the current inputs:
        - dataset_name: {json.dumps(dataset_name, indent=4)}
        - dataset_description: {json.dumps(dataset_description, indent=4)}
        - methodology_description: {json.dumps(methodology_description, indent=4)}
        - transformation_description: {json.dumps(transformation_description, indent=4)}
        - datasource_description: {json.dumps(datasource_description, indent=4)}
        </inputs>
        """
        translation_str = get_llm_response(prompt, target_language=target_language)  # type: ignore

        if translation_str:
            print("Translation by LLM completed!")

            # Parse the translation string into a dictionary
            translation_dict = json.loads(translation_str)

            # Update only the current datasource
            update_datasource(datasource, translation_dict)

        else:
            print("No output generated!")

    # Write all updated datasources back to the YAML file
    write_yaml(datasources, PATH_TO_YAML)

    print("All translations completed and YAML file updated!")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Translate YAML file to chosen language"
    )

    parser.add_argument(
        "--language",
        type=str,
        required=True,
        help="The language code to translate the YAML file to, e.g. 'es' for Spanish",
    )

    args = parser.parse_args()

    translate(args.language)
