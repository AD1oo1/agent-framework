from agent_framework.llm_client import LLMClient, RealSleeper
from agent_framework.llm_response import LLMResponse


def test_llm_client_delegates_to_provider():

    class FakeLLMProvider:

        def generate(self, prompt: str) -> LLMResponse:
            return LLMResponse(
                content=f"Generated: {prompt}"
            )

    provider = FakeLLMProvider()
    client = LLMClient(provider)

    result = client.generate(
        "Analyze Apple's financial health."
    )

    assert result.content == "Generated: Analyze Apple's financial health."


def test_llm_client_retries_on_provider_failure():

    class FakeLLMProvider:

        def __init__(self):
            self.attempts = 0

        def generate(self, prompt: str) -> LLMResponse:
            self.attempts += 1

            if self.attempts < 3:
                raise RuntimeError("Temporary provider failure")

            return LLMResponse(
                content="Successful response"
            )

        def is_retryable_error(self, error: Exception) -> bool:
            return True

    provider = FakeLLMProvider()

    client = LLMClient(
        provider=provider,
        max_retries=2,
    )

    result = client.generate(
        "Analyze Apple's financial health."
    )

    assert result.content == "Successful response"
    assert provider.attempts == 3


def test_llm_client_raises_after_max_retries():

    class FakeLLMProvider:

        def __init__(self):
            self.attempts = 0

        def generate(self, prompt: str) -> LLMResponse:
            self.attempts += 1
            raise RuntimeError("Provider unavailable")

        def is_retryable_error(self, error: Exception) -> bool:
            return True

    provider = FakeLLMProvider()

    client = LLMClient(
        provider=provider,
        max_retries=2,
    )

    try:
        client.generate(
            "Analyze Apple's financial health."
        )
        assert False, "Expected RuntimeError"

    except RuntimeError as exc:
        assert str(exc) == "Provider unavailable"

    assert provider.attempts == 3


def test_llm_client_does_not_retry_non_retryable_error():

    class NonRetryableError(Exception):
        pass

    class FakeLLMProvider:

        def __init__(self):
            self.attempts = 0

        def generate(self, prompt: str) -> LLMResponse:
            self.attempts += 1
            raise NonRetryableError("Invalid request")

        def is_retryable_error(self, error: Exception) -> bool:
            return False

    provider = FakeLLMProvider()

    client = LLMClient(
        provider=provider,
        max_retries=2,
    )

    try:
        client.generate(
            "Analyze Apple's financial health."
        )
        assert False, "Expected NonRetryableError"

    except NonRetryableError as exc:
        assert str(exc) == "Invalid request"

    assert provider.attempts == 1


def test_llm_client_caps_exponential_backoff():

    class FakeLLMProvider:

        def __init__(self):
            self.attempts = 0

        def generate(self, prompt: str) -> LLMResponse:
            self.attempts += 1

            if self.attempts < 6:
                raise RuntimeError("Temporary failure")

            return LLMResponse(
                content="Successful response"
            )

        def is_retryable_error(self, error: Exception) -> bool:
            return True

    class FakeSleeper:

        def __init__(self):
            self.delays = []

        def sleep(self, seconds: float) -> None:
            self.delays.append(seconds)

    provider = FakeLLMProvider()
    sleeper = FakeSleeper()

    client = LLMClient(
        provider=provider,
        max_retries=5,
        max_backoff=4,
        sleeper=sleeper,
    )

    result = client.generate(
        "Analyze Apple's financial health."
    )

    assert result.content == "Successful response"
    assert sleeper.delays == [1, 2, 4, 4, 4]


def test_real_sleeper_delegates_to_time_sleep(monkeypatch):

    calls = []

    def fake_sleep(seconds: float) -> None:
        calls.append(seconds)

    monkeypatch.setattr(
        "agent_framework.llm_client.time.sleep",
        fake_sleep,
    )

    sleeper = RealSleeper()

    sleeper.sleep(2.5)

    assert calls == [2.5]
