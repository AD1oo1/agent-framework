from datetime import datetime, timezone

import pytest

from agent_framework.message import (
    AssistantMessage,
    Message,
    Role,
    ToolMessage,
    UserMessage,
)

def test_message_is_abstract():
    with pytest.raises(TypeError):
        Message(content="Hello")

def test_message_creation():
    message = UserMessage(
        content="Analyze Apple's financial health",

    )

    assert message.content == "Analyze Apple's financial health"
    assert message.role == Role.USER
    assert isinstance(message.id, str)
    assert message.id != ""
    assert isinstance(message.timestamp, datetime)
    assert message.timestamp.tzinfo == timezone.utc
    assert message.metadata == {}

def test_message_has_unique_id_and_metadata():
    message_1 = UserMessage(
        content="Hello",

    )

    message_2 = UserMessage(
        content="Hello",

    )

    assert message_1.id != message_2.id
    assert message_1.metadata is not message_2.metadata

def test_user_message():
    message = UserMessage(
        content="Analyze Apple's financial health",
        intent="financial_analysis",
        preferences={"detail": "high"},
    )

    assert message.role == Role.USER
    assert message.content == "Analyze Apple's financial health"
    assert message.intent == "financial_analysis"
    assert message.preferences == {"detail": "high"}


def test_assistant_message():
    message = AssistantMessage(
        content="Apple shows strong financial performance.",
        reasoning_trace="Analyzed revenue, profitability, and debt.",
        actions=["analyze_revenue", "analyze_debt"],
    )

    assert message.role == Role.ASSISTANT
    assert message.reasoning_trace == "Analyzed revenue, profitability, and debt."
    assert message.actions == ["analyze_revenue", "analyze_debt"]


def test_tool_message():
    message = ToolMessage(
        content="Tool execution result",
        tool_name="financial_data_tool",
        result={"revenue": 100},
        success=True,
    )

    assert message.role == Role.TOOL
    assert message.tool_name == "financial_data_tool"
    assert message.result == {"revenue": 100}
    assert message.success is True
    assert message.error is None
