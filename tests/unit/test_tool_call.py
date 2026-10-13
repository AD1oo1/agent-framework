from agent_framework.tool_call import ToolCall


def test_tool_call_stores_tool_name():

    tool_call = ToolCall(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2",
        },
    )

    assert tool_call.tool_name == "calculator"


def test_tool_call_stores_arguments():

    arguments = {
        "expression": "2 + 2",
    }

    tool_call = ToolCall(
        tool_name="calculator",
        arguments=arguments,
    )

    assert tool_call.arguments == arguments


def test_tool_call_generates_unique_id():

    first = ToolCall(
        tool_name="calculator",
        arguments={},
    )

    second = ToolCall(
        tool_name="calculator",
        arguments={},
    )

    assert first.id != second.id


def test_tool_call_defaults_arguments_to_empty_dict():

    tool_call = ToolCall(
        tool_name="calculator",
    )

    assert tool_call.arguments == {}
