from agent_framework.financial_node import FinancialDataNode
from agent_framework.state import AgentState


class FakeFinancialDataProvider:
    def fetch_financial_data(self, company: str) -> dict:
        return {
            "company": company,
            "revenue": 100,
        }


def test_financial_data_node_fetches_and_stores_data():
    provider = FakeFinancialDataProvider()

    node = FinancialDataNode(provider)

    state = AgentState(
        goal="Apple"
    )

    result = node.execute(state)

    assert result is state
    assert len(state.tool_results) == 1

    tool_result = state.tool_results[0]

    assert tool_result.tool_name == "financial_data"
    assert tool_result.success is True
    assert tool_result.result == {
        "company": "Apple",
        "revenue": 100,
    }
