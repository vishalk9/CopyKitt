
import os
from typing import List
import openai
import argparse
import re

MAX_INPUT_LENGTH = 32


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input
    if validate_length(user_input):
        print(f"user input: {user_input}")
        branding_result = generate_branding_snippet(user_input)
        keyword_result = generate_keywords(user_input)
    else:
        raise ValueError(f"User input is too long, it should be less than {MAX_INPUT_LENGTH}")

def validate_length(prompt):
    if len(prompt)>MAX_INPUT_LENGTH:
        return False
    return True

def generate_keywords(prompt: str) -> List[str]:
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate related branding keywords for {prompt}: "
    print(enriched_prompt)

    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3", prompt=enriched_prompt, max_tokens=32
    )
    keyword_text = response["choices"][0]["text"].strip()
    keyword_array = re.split(",|\n|;|-", keyword_text)
    keyword_array = [k.lower().strip() for k in keyword_array]
    keyword_array = [k for k in keyword_array if len(k)>0]
    print(f"Keywords: {keyword_array}")
    return keyword_array


def generate_branding_snippet(prompt: str) -> str:
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate upbeat branding snippet for {prompt}: "
    print(enriched_prompt)
    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3", prompt=enriched_prompt, max_tokens=50
    )
    # print(response)
    branding_text = response["choices"][0]["text"].strip()
    # Add ... to truncated statements.
    last_char = branding_text[-1]
    if last_char not in {".", "!", "?"}:
        branding_text += "..."
    print(f"Branding Text: {branding_text}")
    return branding_text

if __name__ == "__main__":
    main()