import pytest

from agent_framework.gemini_provider import GeminiProvider


class FakeResponse:

    def __init__(self, text: str | None) -> None:
        self.text = text


class FakeModels:

    def __init__(self, response: FakeResponse) -> None:
        self.response = response
        self.last_model = None
        self.last_contents = None

    def generate_content(
        self,
        model: str,
        contents: str,
    ) -> FakeResponse:
        self.last_model = model
        self.last_contents = contents
        return self.response


class FakeGeminiClient:

    def __init__(self, response: FakeResponse) -> None:
        self.models = FakeModels(response)


def test_gemini_provider_generates_response() -> None:
    client = FakeGeminiClient(
        response=FakeResponse(text="Revenue increased by 15%.")
    )

    provider = GeminiProvider(
        client=client,
        model="gemini-2.5-flash",
    )

    response = provider.generate(
        "Analyze the company's revenue."
    )

    assert response.content == "Revenue increased by 15%."
    assert response.model == "gemini-2.5-flash"
    assert client.models.last_model == "gemini-2.5-flash"
    assert client.models.last_contents == (
        "Analyze the company's revenue."
    )


def test_gemini_provider_rejects_empty_prompt() -> None:
    provider = GeminiProvider(
        client=FakeGeminiClient(FakeResponse(text="unused"))
    )

    with pytest.raises(ValueError, match="Prompt cannot be empty."):
        provider.generate("")


def test_gemini_provider_rejects_whitespace_prompt() -> None:
    provider = GeminiProvider(
        client=FakeGeminiClient(FakeResponse(text="unused"))
    )

    with pytest.raises(ValueError, match="Prompt cannot be empty."):
        provider.generate("   ")


def test_gemini_provider_rejects_empty_response() -> None:
    provider = GeminiProvider(
        client=FakeGeminiClient(FakeResponse(text=None))
    )

    with pytest.raises(
        ValueError,
        match="LLM response content is empty.",
    ):
        provider.generate("Generate an analysis.")


def test_gemini_provider_identifies_retryable_errors() -> None:
    provider = GeminiProvider(
        client=FakeGeminiClient(FakeResponse(text="unused"))
    )

    assert provider.is_retryable_error(Exception("Resource exhausted"))
    assert provider.is_retryable_error(Exception("Request timeout"))
    assert provider.is_retryable_error(
        Exception("Internal server error")
    )


def test_gemini_provider_identifies_non_retryable_errors() -> None:
    provider = GeminiProvider(
        client=FakeGeminiClient(FakeResponse(text="unused"))
    )

    assert not provider.is_retryable_error(Exception("Invalid API key"))
    assert not provider.is_retryable_error(Exception("Permission denied"))
