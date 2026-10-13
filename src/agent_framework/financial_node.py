from agent_framework.node import Node
from agent_framework.providers import FinancialDataProvider
from agent_framework.state import AgentState
from agent_framework.tool import ToolResult


class FinancialDataNode(Node):
    def __init__(self, provider: FinancialDataProvider) -> None:
        self.provider = provider

    def execute(self, state: AgentState) -> AgentState:
        data = self.provider.fetch_financial_data(
            state.goal
        )

        tool_result = ToolResult(
            tool_name="financial_data",
            result=data,
        )

        state.add_tool_result(tool_result)

        return state
