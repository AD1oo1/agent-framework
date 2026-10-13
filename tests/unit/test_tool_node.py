from agent_framework.state import AgentState
from agent_framework.tool import Tool, ToolResult
from agent_framework.tool_call import ToolCall
from agent_framework.tool_executor import ToolExecutor
from agent_framework.tool_node import ToolNode


class CalculatorTool(Tool):

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Performs calculations."

    def execute(
        self,
        expression: str,
    ) -> ToolResult:

        return ToolResult(
            tool_name=self.name,
            result=4,
        )


def test_tool_node_executes_tool_call():

    tool = CalculatorTool()

    executor = ToolExecutor(
        tools=[tool],
    )

    tool_call = ToolCall(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2",
        },
    )

    node = ToolNode(
        executor=executor,
        tool_call=tool_call,
    )

    state = AgentState(
        goal="Calculate 2 + 2",
    )

    result = node.execute(state)

    assert len(result.tool_results) == 1

    tool_result = result.tool_results[0]

    assert tool_result.tool_name == "calculator"
    assert tool_result.result == 4
    assert tool_result.success is True


def test_tool_node_returns_same_state():

    tool = CalculatorTool()

    executor = ToolExecutor(
        tools=[tool],
    )

    tool_call = ToolCall(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2",
        },
    )

    node = ToolNode(
        executor=executor,
        tool_call=tool_call,
    )

    state = AgentState(
        goal="Calculate 2 + 2",
    )

    result = node.execute(state)

    assert result is state
