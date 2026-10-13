import time
from typing import Protocol

from agent_framework.llm import LLMProvider
from agent_framework.llm_response import LLMResponse


class Sleeper(Protocol):

    def sleep(self, seconds: float) -> None:
        ...


class RealSleeper:

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


class LLMClient:

    def __init__(
        self,
        provider: LLMProvider,
        max_retries: int = 0,
        max_backoff: float = 60.0,
        sleeper: Sleeper | None = None,
    ) -> None:
        self.provider = provider
        self.max_retries = max_retries
        self.max_backoff = max_backoff
        self.sleeper = sleeper or RealSleeper()

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        attempts = 0

        while True:
            try:
                return self.provider.generate(prompt)

            except Exception as error:

                # Non-retryable errors should immediately
                # propagate to the caller.
                if not self.provider.is_retryable_error(error):
                    raise

                # max_retries represents the number of
                # additional attempts after the first attempt.
                if attempts >= self.max_retries:
                    raise

                attempts += 1

                # Exponential backoff:
                # 1s, 2s, 4s, 8s, ...
                # capped at max_backoff.
                delay = min(
                    2 ** (attempts - 1),
                    self.max_backoff,
                )

                self.sleeper.sleep(delay)
