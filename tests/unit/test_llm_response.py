from agent_framework.llm_response import LLMResponse


def test_llm_response_creation():

    response = LLMResponse(
        content="Apple's revenue increased.",
        model="test-model",
        prompt_tokens=100,
        completion_tokens=50,
    )

    assert response.content == "Apple's revenue increased."
    assert response.model == "test-model"
    assert response.prompt_tokens == 100
    assert response.completion_tokens == 50

def test_llm_response_metadata_is_independent():

    response_one = LLMResponse(
        content="Response one"
    )

    response_two = LLMResponse(
        content="Response two"
    )

    response_one.metadata["provider"] = "fake"

    assert response_one.metadata == {
        "provider": "fake"
    }

    assert response_two.metadata == {}

from agent_framework.tool_call import ToolCall


def test_llm_response_stores_tool_calls():

    tool_call = ToolCall(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2",
        },
    )

    response = LLMResponse(
        content="",
        tool_calls=[tool_call],
    )

    assert response.tool_calls == [tool_call]


def test_llm_response_defaults_tool_calls_to_empty_list():

    response = LLMResponse(
        content="Final answer",
    )

    assert response.tool_calls == []
