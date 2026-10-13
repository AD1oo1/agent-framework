from agent_framework.prompt_builder import PromptBuilder
from agent_framework.state import AgentState
from agent_framework.tool import ToolResult
from agent_framework.message import UserMessage


def test_prompt_builder_builds_prompt_from_state():
    state = AgentState(
        goal="Analyze Apple",
    )

    state.add_tool_result(
        ToolResult(
            tool_name="financial_data",
            result={"revenue": 100},
        )
    )

    builder = PromptBuilder()

    prompt = builder.build(state)

    assert prompt.system == "You are a financial analyst."
    assert prompt.goal == "Analyze Apple"
    assert prompt.context == "{'revenue': 100}"
    assert prompt.available_tools == ["financial_data"]
    assert prompt.output_format == "Return a concise financial analysis."


def test_prompt_builder_ignores_failed_tool_results():
    state = AgentState(
        goal="Analyze Apple",
    )

    state.add_tool_result(
        ToolResult(
            tool_name="financial_data",
            result={"revenue": 100},
            success=False,
            error="API failed",
        )
    )

    builder = PromptBuilder()

    prompt = builder.build(state)

    assert prompt.context == ""
    assert prompt.available_tools == []


def test_prompt_builder_handles_multiple_tool_results():
    state = AgentState(
        goal="Analyze Apple",
    )

    state.add_tool_result(
        ToolResult(
            tool_name="financial_data",
            result={"revenue": 100},
        )
    )

    state.add_tool_result(
        ToolResult(
            tool_name="stock_price",
            result={"price": 200},
        )
    )

    builder = PromptBuilder()

    prompt = builder.build(state)

    assert prompt.available_tools == [
        "financial_data",
        "stock_price",
    ]

    assert prompt.context == (
        "{'revenue': 100}\n{'price': 200}"
    )

def test_prompt_builder_preserves_messages():
    state = AgentState(
        goal="Analyze Apple",
    )

    message = UserMessage(
        content="What is Apple's revenue?"
    )

    state.add_message(message)

    builder = PromptBuilder()

    prompt = builder.build(state)

    assert len(prompt.messages) == 1
    assert prompt.messages[0] is message

from agent_framework.chunk import DocumentChunk

def test_prompt_builder_includes_retrieved_chunks():

    state = AgentState(
        goal="What was the company's revenue?"
    )

    state.add_retrieved_chunk(
        DocumentChunk(
            content="Revenue was $394 billion.",
            metadata={
                "source": "annual_report.pdf",
                "page": 10,
            },
        )
    )

    prompt = PromptBuilder().build(state)

    assert (
        "Revenue was $394 billion."
        in prompt.context
    )
