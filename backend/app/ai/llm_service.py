import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class LLMService:
    """
    Service for interacting with Google's Gemini model.
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in .env file."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model_name = "gemini-flash-latest"

    def generate_answer(
        self,
        question: str,
        context: str,
    ) -> str:

        prompt = f"""
You are KnowledgePulse AI.

Answer ONLY using the context below.

If the answer is not present in the context,
reply exactly:

"I couldn't find that information in the uploaded documents."

--------------------
Context:
{context}

--------------------
Question:
{question}

Answer:
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        return response.text


llm_service = LLMService()