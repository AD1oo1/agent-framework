from agent_framework.agent_action import (
    ActionType,
    AgentAction,
)
from agent_framework.tool_call import ToolCall


def test_agent_action_represents_final_answer():

    action = AgentAction(
        action_type=ActionType.FINAL_ANSWER,
    )

    assert action.action_type == (
        ActionType.FINAL_ANSWER
    )


def test_agent_action_represents_tool_call():

    tool_call = ToolCall(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2",
        },
    )

    action = AgentAction(
        action_type=ActionType.TOOL_CALL,
        tool_call=tool_call,
    )

    assert action.action_type == (
        ActionType.TOOL_CALL
    )

    assert action.tool_call is tool_call


def test_agent_action_defaults_tool_call_to_none():

    action = AgentAction(
        action_type=ActionType.FINAL_ANSWER,
    )

    assert action.tool_call is None


def test_agent_action_requires_tool_call_for_tool_action():

    tool_call = ToolCall(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2",
        },
    )

    action = AgentAction(
        action_type=ActionType.TOOL_CALL,
        tool_call=tool_call,
    )

    assert action.tool_call is not None
