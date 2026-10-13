import pytest
from agent_framework.agent_loop import AgentLoop
from agent_framework.llm_response import LLMResponse
from agent_framework.state import AgentState
from agent_framework.tool import Tool, ToolResult
from agent_framework.tool_call import ToolCall
from agent_framework.tool_executor import ToolExecutor
from agent_framework.prompt_builder import PromptBuilder
from agent_framework.prompt_renderer import PromptRenderer


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

class FakeLLMClient:

    def __init__(self):
        self.call_count = 0
        self.prompts = []

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        self.call_count += 1
        self.prompts.append(prompt)

        if self.call_count == 1:

            return LLMResponse(
                content="",
                tool_calls=[
                    ToolCall(
                        tool_name="calculator",
                        arguments={
                            "expression": "2 + 2",
                        },
                    )
                ],
            )

        return LLMResponse(
            content="The answer is 4."
        )

def test_agent_loop_executes_tool_and_returns_final_answer():

    llm_client = FakeLLMClient()

    tool_executor = ToolExecutor(
        tools=[
            CalculatorTool(),
        ],
    )

    loop = AgentLoop(
        llm_client=llm_client,
        tool_executor=tool_executor,
        prompt_builder=PromptBuilder(),
        prompt_renderer=PromptRenderer(),
    )

    state = AgentState(
        goal="Calculate 2 + 2",
    )

    result = loop.run(state)

    assert result.final_answer == (
        "The answer is 4."
    )

    assert len(result.tool_results) == 1

    assert result.tool_results[0].tool_name == (
        "calculator"
    )

    assert result.tool_results[0].result == 4

    assert llm_client.call_count == 2

    assert "Calculate 2 + 2" in (
        llm_client.prompts[0]
    )

    assert "4" in (
        llm_client.prompts[1]
    )


class AlwaysToolCallingLLM:

    def __init__(self):
        self.call_count = 0

    def generate(
        self,
        prompt: str,
    ) -> LLMResponse:

        self.call_count += 1

        return LLMResponse(
            content="",
            tool_calls=[
                ToolCall(
                    tool_name="calculator",
                    arguments={
                        "expression": "2 + 2",
                    },
                )
            ],
        )

def test_agent_loop_stops_after_max_iterations():

    llm_client = AlwaysToolCallingLLM()

    tool_executor = ToolExecutor(
        tools=[
            CalculatorTool(),
        ],
    )

    loop = AgentLoop(
        llm_client=llm_client,
        tool_executor=tool_executor,
        prompt_builder=PromptBuilder(),
        prompt_renderer=PromptRenderer(),
        max_iterations=3,
    )

    state = AgentState(
        goal="Calculate 2 + 2",
    )

    with pytest.raises(
        RuntimeError,
        match="Agent loop exceeded maximum iterations.",
    ):
        loop.run(state)

    assert llm_client.call_count == 3
