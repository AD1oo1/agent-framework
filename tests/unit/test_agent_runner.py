from agent_framework.agent_runner import AgentRunner
from agent_framework.node import Node
from agent_framework.state import AgentState
from agent_framework.workflow import Workflow


class FakeNode(Node):

    def __init__(self):
        self.executed = False

    def execute(
        self,
        state: AgentState,
    ) -> AgentState:

        self.executed = True

        state.set_final_answer(
            "Agent execution completed."
        )

        return state


def test_agent_runner_executes_workflow():

    workflow = Workflow()

    node = FakeNode()

    workflow.add_node(
        "agent",
        node,
    )

    workflow.set_entry_point(
        "agent",
    )

    runner = AgentRunner(
        workflow=workflow,
    )

    state = AgentState(
        goal="Analyze company financials",
    )

    result = runner.run(state)

    assert node.executed is True

    assert result.final_answer == (
        "Agent execution completed."
    )


def test_agent_runner_returns_final_state():

    workflow = Workflow()

    node = FakeNode()

    workflow.add_node(
        "agent",
        node,
    )

    workflow.set_entry_point(
        "agent",
    )

    runner = AgentRunner(
        workflow=workflow,
    )

    state = AgentState(
        goal="Analyze company financials",
    )

    result = runner.run(state)

    assert isinstance(
        result,
        AgentState,
    )

    assert result is state
