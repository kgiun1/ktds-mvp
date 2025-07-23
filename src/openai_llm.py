import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API configuration from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("OPENAI_API_ENDPOINT")
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_version = os.getenv("OPENAI_API_VERSION")


def ask_openai(prompt: str) -> str:
    """
    Sends a prompt to OpenAI (Azure) and returns the response.
    """
    response = openai.chat.completions.create(
            temperature=0.7,
            max_tokens=300,
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    return response.choices[0].message.content