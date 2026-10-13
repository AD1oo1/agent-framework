import pytest

from agent_framework.tool import Tool, ToolResult


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


def test_tool_implementation_exposes_name():

    tool = CalculatorTool()

    assert tool.name == "calculator"


def test_tool_implementation_exposes_description():

    tool = CalculatorTool()

    assert tool.description == (
        "Performs calculations."
    )


def test_tool_executes_and_returns_result():

    tool = CalculatorTool()

    result = tool.execute(
        expression="2 + 2",
    )

    assert isinstance(
        result,
        ToolResult,
    )

    assert result.tool_name == "calculator"
    assert result.result == "2 + 2"
    assert result.success is True


def test_tool_is_abstract():

    with pytest.raises(TypeError):
        Tool()
