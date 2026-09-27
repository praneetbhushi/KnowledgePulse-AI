from ollama import Client

from app.core.config import settings

from app.core.exceptions.custom_exceptions import (
    LLMServiceException,
    LLMUnavailableException,
)


class LLMService:

    def __init__(self):
        self.client = Client(
            host=settings.OLLAMA_HOST
        )

    def generate_answer(
        self,
        prompt: str
    ) -> str:

        try:

            print("Using model:", settings.OLLAMA_MODEL)

            response = self.client.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            keep_alive="10m",
            options={
                "temperature": 0.1,
                "num_predict": 256,
                "num_ctx": 2048,
            },
        )

            answer = response["message"]["content"]

            if not answer:
                raise LLMServiceException(
                    "The language model returned an empty response."
                )

            return answer.strip()

        except LLMServiceException:
            raise

        except ConnectionError as exc:
            raise LLMUnavailableException(
                "The local AI service is unavailable. Please make sure Ollama is running."
            ) from exc

        except Exception as exc:

            error_message = str(exc).lower()

            if (
                "connection" in error_message
                or "refused" in error_message
            ):
                raise LLMUnavailableException(
                    "The local AI service is unavailable. Please make sure Ollama is running."
                ) from exc

            raise LLMServiceException(
                f"Failed to generate an AI response. {exc}"
            ) from exc


llm_service = LLMService()