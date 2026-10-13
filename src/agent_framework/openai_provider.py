from openai import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)

from agent_framework.llm_response import LLMResponse


class OpenAIProvider:

    def __init__(
        self,
        client: OpenAI,
        model: str,
    ) -> None:
        self.client = client
        self.model = model

    def generate(self, prompt: str) -> LLMResponse:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content

        if content is None:
            raise ValueError("LLM response content is empty.")

        usage = response.usage

        return LLMResponse(
            content=content,
            model=response.model,
            prompt_tokens=(
                usage.prompt_tokens
                if usage is not None
                else None
            ),
            completion_tokens=(
                usage.completion_tokens
                if usage is not None
                else None
            ),
        )

    def is_retryable_error(self, error: Exception) -> bool:

        if isinstance(error, RateLimitError):
            return True

        if isinstance(error, APIConnectionError):
            return True

        if isinstance(error, APIStatusError):
            return error.status_code >= 500

        if isinstance(error, AuthenticationError):
            return False

        return False
