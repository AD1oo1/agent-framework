import pytest

from agent_framework.tool import Tool, ToolResult
from agent_framework.tool_executor import ToolExecutor


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
            result=expression,
        )


def test_tool_executor_executes_registered_tool():

    tool = CalculatorTool()

    executor = ToolExecutor(
        tools=[tool],
    )

    result = executor.execute(
        tool_name="calculator",
        expression="2 + 2",
    )

    assert result.tool_name == "calculator"
    assert result.result == "2 + 2"
    assert result.success is True


def test_tool_executor_rejects_unknown_tool():

    executor = ToolExecutor(
        tools=[],
    )

    with pytest.raises(
        ValueError,
        match="Unknown tool: calculator",
    ):
        executor.execute(
            tool_name="calculator",
            expression="2 + 2",
        )


def test_tool_executor_exposes_registered_tools():

    calculator = CalculatorTool()

    executor = ToolExecutor(
        tools=[calculator],
    )

    assert executor.available_tools() == [
        "calculator",
    ]
