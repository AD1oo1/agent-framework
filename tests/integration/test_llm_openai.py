from unittest.mock import Mock

from openai import RateLimitError

from agent_framework.llm_client import LLMClient
from agent_framework.llm_response import LLMResponse
from agent_framework.openai_provider import OpenAIProvider


class FakeSleeper:

    def __init__(self):
        self.delays = []

    def sleep(self, seconds: float) -> None:
        self.delays.append(seconds)


class FakeCompletions:

    def __init__(self):
        self.call_count = 0

    def create(self, **kwargs):

        self.call_count += 1

        if self.call_count == 1:
            response = Mock()
            response.request = Mock()
            response.status_code = 429

            raise RateLimitError(
                message="Rate limit exceeded",
                response=response,
                body=None,
            )

        return type(
            "FakeResponse",
            (),
            {
                "choices": [
                    type(
                        "FakeChoice",
                        (),
                        {
                            "message": type(
                                "FakeMessage",
                                (),
                                {
                                    "content": "Generated response"
                                },
                            )()
                        },
                    )()
                ],
                "model": "fake-openai-model",
                "usage": None,
            },
        )()


class FakeChat:

    def __init__(self):
        self.completions = FakeCompletions()


class FakeOpenAIClient:

    def __init__(self):
        self.chat = FakeChat()


def test_llm_client_retries_openai_rate_limit_error():

    provider = OpenAIProvider(
        client=FakeOpenAIClient(),
        model="fake-openai-model",
    )

    sleeper = FakeSleeper()

    client = LLMClient(
        provider=provider,
        max_retries=1,
        sleeper=sleeper,
    )

    result = client.generate(
        "Analyze Apple's financial health."
    )

    assert isinstance(result, LLMResponse)
    assert result.content == "Generated response"

    assert provider.client.chat.completions.call_count == 2
    assert sleeper.delays == [1]
