from google import genai

from agent_framework.llm_response import LLMResponse


class GeminiProvider:

    def __init__(
        self,
        client: genai.Client,
        model: str = "gemini-2.5-flash",
    ) -> None:
        self.client = client
        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        if not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        content = response.text

        if content is None or not content.strip():
            raise ValueError(
                "LLM response content is empty."
            )

        return LLMResponse(
            content=content,
            model=self.model,
        )

    def is_retryable_error(
        self,
        error: Exception,
    ) -> bool:

        error_message = str(error).lower()

        retryable_keywords = (
            "rate limit",
            "resource exhausted",
            "timeout",
            "temporarily unavailable",
            "internal server error",
            "service unavailable",
        )

        return any(
            keyword in error_message
            for keyword in retryable_keywords
        )
