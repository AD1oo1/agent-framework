from typing import Protocol

from agent_framework.llm_response import LLMResponse


class LLMProvider(Protocol):

    def generate(self, prompt: str) -> LLMResponse:
        ...

    def is_retryable_error(self, error: Exception) -> bool:
        ...
