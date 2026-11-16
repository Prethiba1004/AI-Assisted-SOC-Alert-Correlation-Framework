
import os
from google import genai

# Gemini model selected for the SOC-AI project
MODEL_NAME = "gemini-3.5-flash-lite"


def create_gemini_client():
    """Create a Gemini API client using the environment variable."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not configured."
        )

    return genai.Client(api_key=api_key)


def generate_llm_response(prompt):
    """Send a prompt to Gemini and return its text response."""

    client = create_gemini_client()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    print("Gemini LLM client module loaded successfully.")
    print(f"Selected model: {MODEL_NAME}")
