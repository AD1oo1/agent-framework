import pytest

from agent_framework.node import Node
from agent_framework.state import AgentState


def test_node_is_abstract():
    with pytest.raises(TypeError):
        Node()


def test_node_contract():
    class TestNode(Node):
        def execute(self, state: AgentState) -> AgentState:
            return state

    state = AgentState(goal="Analyze Apple")

    node = TestNode()

    result = node.execute(state)

    assert result is state
