from unittest.mock import Mock

from openai import AuthenticationError, RateLimitError

from agent_framework.llm_response import LLMResponse
from agent_framework.openai_provider import OpenAIProvider


def test_openai_provider_generates_llm_response():

    class FakeCompletions:

        def create(self, **kwargs):
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
                    "usage": type(
                        "FakeUsage",
                        (),
                        {
                            "prompt_tokens": 10,
                            "completion_tokens": 20,
                        },
                    )(),
                },
            )()


    class FakeChat:

        def __init__(self):
            self.completions = FakeCompletions()


    class FakeOpenAIClient:

        def __init__(self):
            self.chat = FakeChat()


    provider = OpenAIProvider(
        client=FakeOpenAIClient(),
        model="fake-openai-model",
    )

    result = provider.generate(
        "Analyze Apple's financial health."
    )

    assert isinstance(result, LLMResponse)
    assert result.content == "Generated response"
    assert result.model == "fake-openai-model"
    assert result.prompt_tokens == 10
    assert result.completion_tokens == 20


def test_openai_provider_handles_missing_usage():

    class FakeCompletions:

        def create(self, **kwargs):
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


    provider = OpenAIProvider(
        client=FakeOpenAIClient(),
        model="fake-openai-model",
    )

    result = provider.generate(
        "Analyze Apple's financial health."
    )

    assert isinstance(result, LLMResponse)
    assert result.content == "Generated response"
    assert result.model == "fake-openai-model"
    assert result.prompt_tokens is None
    assert result.completion_tokens is None


def test_openai_provider_rejects_missing_content():

    class FakeCompletions:

        def create(self, **kwargs):
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
                                        "content": None
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


    provider = OpenAIProvider(
        client=FakeOpenAIClient(),
        model="fake-openai-model",
    )

    try:
        provider.generate(
            "Analyze Apple's financial health."
        )
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "LLM response content is empty."


def test_openai_provider_sends_correct_request():

    class FakeCompletions:

        def __init__(self):
            self.last_kwargs = None

        def create(self, **kwargs):
            self.last_kwargs = kwargs

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


    client = FakeOpenAIClient()

    provider = OpenAIProvider(
        client=client,
        model="fake-openai-model",
    )

    prompt = "Analyze Apple's financial health."

    provider.generate(prompt)

    assert client.chat.completions.last_kwargs == {
        "model": "fake-openai-model",
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }


def test_openai_provider_marks_rate_limit_error_as_retryable():

    class FakeOpenAIClient:
        pass

    provider = OpenAIProvider(
        client=FakeOpenAIClient(),
        model="fake-openai-model",
    )

    response = Mock()
    response.request = Mock()
    response.status_code = 429

    error = RateLimitError(
        message="Rate limit exceeded",
        response=response,
        body=None,
    )

    assert provider.is_retryable_error(error) is True


def test_openai_provider_marks_authentication_error_as_non_retryable():

    class FakeOpenAIClient:
        pass

    provider = OpenAIProvider(
        client=FakeOpenAIClient(),
        model="fake-openai-model",
    )

    response = Mock()
    response.request = Mock()
    response.status_code = 401

    error = AuthenticationError(
        message="Invalid API key",
        response=response,
        body=None,
    )

    assert provider.is_retryable_error(error) is False
