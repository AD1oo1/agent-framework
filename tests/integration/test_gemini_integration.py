import pytest
from google import genai

from agent_framework.gemini_provider import GeminiProvider


@pytest.mark.integration
def test_gemini_provider_real_generation() -> None:

    client = genai.Client()

    provider = GeminiProvider(
        client=client,
        model="gemini-2.5-flash",
    )

    response = provider.generate(
        "In one sentence, explain what revenue means."
    )

    assert response.content
    assert response.model == "gemini-2.5-flash"
