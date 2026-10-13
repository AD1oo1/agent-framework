from agent_framework.llm import LLMProvider
from agent_framework.llm_response import LLMResponse


def test_llm_provider_contract():

    class FakeLLMProvider:

        def generate(self, prompt: str) -> LLMResponse:
            return LLMResponse(
                content=f"Generated: {prompt}",
                model="fake-model",
                prompt_tokens=10,
                completion_tokens=20,
            )

        def is_retryable_error(self, error: Exception) -> bool:
            return True

    provider: LLMProvider = FakeLLMProvider()

    result = provider.generate(
        "Analyze Apple's financial health."
    )

    assert isinstance(result, LLMResponse)
    assert result.content == (
        "Generated: Analyze Apple's financial health."
    )
    assert result.model == "fake-model"
    assert result.prompt_tokens == 10
    assert result.completion_tokens == 20
