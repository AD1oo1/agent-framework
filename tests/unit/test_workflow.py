import pytest

from agent_framework.node import Node
from agent_framework.state import AgentState
from agent_framework.workflow import Workflow
from agent_framework.node_execution import NodeExecutionStatus
from agent_framework.router import ConditionalRouter


class FakeNode(Node):

    def __init__(
        self,
        name: str,
        execution_log: list[str],
    ):
        self.name = name
        self.execution_log = execution_log

    def execute(
        self,
        state: AgentState,
    ) -> AgentState:

        self.execution_log.append(self.name)

        return state


class FailingNode(Node):

    def __init__(
        self,
        name: str,
        execution_log: list[str],
        failures_before_success: int,
    ):
        self.name = name
        self.execution_log = execution_log
        self.failures_before_success = failures_before_success
        self.attempt_count = 0

    def execute(
        self,
        state: AgentState,
    ) -> AgentState:

        self.execution_log.append(self.name)

        self.attempt_count += 1

        if self.attempt_count <= self.failures_before_success:
            raise RuntimeError(
                f"Temporary failure on attempt "
                f"{self.attempt_count}"
            )

        return state


def test_workflow_rejects_duplicate_nodes():

    workflow = Workflow()

    node = FakeNode(
        name="start",
        execution_log=[],
    )

    workflow.add_node(
        "start",
        node,
    )

    with pytest.raises(
        ValueError,
        match="Node 'start' is already registered.",
    ):
        workflow.add_node(
            "start",
            node,
        )


def test_workflow_rejects_invalid_source_node():

    workflow = Workflow()

    target_node = FakeNode(
        name="target",
        execution_log=[],
    )

    workflow.add_node(
        "target",
        target_node,
    )

    with pytest.raises(
        ValueError,
        match="Source node 'missing' is not registered.",
    ):
        workflow.add_edge(
            "missing",
            "target",
        )


def test_workflow_rejects_invalid_target_node():

    workflow = Workflow()

    source_node = FakeNode(
        name="source",
        execution_log=[],
    )

    workflow.add_node(
        "source",
        source_node,
    )

    with pytest.raises(
        ValueError,
        match="Target node 'missing' is not registered.",
    ):
        workflow.add_edge(
            "source",
            "missing",
        )


def test_workflow_rejects_invalid_entry_point():

    workflow = Workflow()

    with pytest.raises(
        ValueError,
        match="Entry point 'missing' is not registered.",
    ):
        workflow.set_entry_point(
            "missing",
        )


def test_workflow_requires_entry_point():

    workflow = Workflow()

    node = FakeNode(
        name="start",
        execution_log=[],
    )

    workflow.add_node(
        "start",
        node,
    )

    with pytest.raises(
        ValueError,
        match="Workflow entry point is not configured.",
    ):
        workflow.run(
            AgentState(
                goal="Test workflow",
            )
        )


def test_workflow_runs_single_node():

    workflow = Workflow()

    execution_log = []

    node = FakeNode(
        name="start",
        execution_log=execution_log,
    )

    workflow.add_node(
        "start",
        node,
    )

    workflow.set_entry_point(
        "start",
    )

    state = AgentState(
        goal="Test workflow",
    )

    result = workflow.run(
        state,
    )

    assert result is state

    assert execution_log == [
        "start",
    ]


def test_workflow_runs_nodes_in_sequence():

    workflow = Workflow()

    execution_log = []

    first_node = FakeNode(
        name="first",
        execution_log=execution_log,
    )

    second_node = FakeNode(
        name="second",
        execution_log=execution_log,
    )

    workflow.add_node(
        "first",
        first_node,
    )

    workflow.add_node(
        "second",
        second_node,
    )

    workflow.add_edge(
        "first",
        "second",
    )

    workflow.set_entry_point(
        "first",
    )

    state = AgentState(
        goal="Test workflow",
    )

    workflow.run(
        state,
    )

    assert execution_log == [
        "first",
        "second",
    ]


def test_workflow_tracks_node_executions():

    workflow = Workflow()

    execution_log = []

    first_node = FakeNode(
        name="first",
        execution_log=execution_log,
    )

    second_node = FakeNode(
        name="second",
        execution_log=execution_log,
    )

    workflow.add_node(
        "first",
        first_node,
    )

    workflow.add_node(
        "second",
        second_node,
    )

    workflow.add_edge(
        "first",
        "second",
    )

    workflow.set_entry_point(
        "first",
    )

    workflow.run(
        AgentState(
            goal="Test workflow",
        )
    )

    executions = workflow.executions

    assert len(executions) == 2

    assert executions[0].node_name == "first"
    assert executions[1].node_name == "second"

    assert executions[0].status == NodeExecutionStatus.COMPLETED
    assert executions[1].status == NodeExecutionStatus.COMPLETED

    assert executions[0].started_at is not None
    assert executions[0].completed_at is not None
    assert executions[0].duration is not None


def test_workflow_executions_are_read_only():

    workflow = Workflow()

    execution_log = []

    node = FakeNode(
        name="start",
        execution_log=execution_log,
    )

    workflow.add_node(
        "start",
        node,
    )

    workflow.set_entry_point(
        "start",
    )

    workflow.run(
        AgentState(
            goal="Test workflow",
        )
    )

    executions = workflow.executions

    assert isinstance(
        executions,
        tuple,
    )


def test_workflow_generates_same_run_id_for_all_node_executions():

    workflow = Workflow()

    execution_log = []

    first_node = FakeNode(
        name="first",
        execution_log=execution_log,
    )

    second_node = FakeNode(
        name="second",
        execution_log=execution_log,
    )

    workflow.add_node(
        "first",
        first_node,
    )

    workflow.add_node(
        "second",
        second_node,
    )

    workflow.add_edge(
        "first",
        "second",
    )

    workflow.set_entry_point(
        "first",
    )

    workflow.run(
        AgentState(
            goal="Test workflow",
        )
    )

    executions = workflow.executions

    assert len(executions) == 2

    assert executions[0].run_id == executions[1].run_id


def test_workflow_generates_new_run_id_for_each_run():

    workflow = Workflow()

    execution_log = []

    node = FakeNode(
        name="start",
        execution_log=execution_log,
    )

    workflow.add_node(
        "start",
        node,
    )

    workflow.set_entry_point(
        "start",
    )

    state = AgentState(
        goal="Test workflow",
    )

    workflow.run(
        state,
    )

    first_run_id = workflow.executions[0].run_id

    workflow.run(
        state,
    )

    second_run_id = workflow.executions[0].run_id

    assert first_run_id != second_run_id


def test_workflow_clears_execution_history_before_new_run():

    workflow = Workflow()

    execution_log = []

    node = FakeNode(
        name="start",
        execution_log=execution_log,
    )

    workflow.add_node(
        "start",
        node,
    )

    workflow.set_entry_point(
        "start",
    )

    state = AgentState(
        goal="Test workflow",
    )

    workflow.run(
        state,
    )

    assert len(workflow.executions) == 1

    workflow.run(
        state,
    )

    assert len(workflow.executions) == 1


def test_workflow_runs_all_branch_nodes():

    workflow = Workflow()

    execution_log = []

    start_node = FakeNode(
        name="start",
        execution_log=execution_log,
    )

    financial_node = FakeNode(
        name="financial",
        execution_log=execution_log,
    )

    market_node = FakeNode(
        name="market",
        execution_log=execution_log,
    )

    workflow.add_node(
        "start",
        start_node,
    )

    workflow.add_node(
        "financial",
        financial_node,
    )

    workflow.add_node(
        "market",
        market_node,
    )

    workflow.add_edge(
        "start",
        "financial",
    )

    workflow.add_edge(
        "start",
        "market",
    )

    workflow.set_entry_point(
        "start",
    )

    workflow.run(
        AgentState(
            goal="Test workflow",
        )
    )

    assert execution_log == [
        "start",
        "financial",
        "market",
    ]


def test_workflow_runs_converging_nodes_only_once():

    workflow = Workflow()

    execution_log = []

    start_node = FakeNode(
        name="start",
        execution_log=execution_log,
    )

    financial_node = FakeNode(
        name="financial",
        execution_log=execution_log,
    )

    market_node = FakeNode(
        name="market",
        execution_log=execution_log,
    )

    final_node = FakeNode(
        name="final",
        execution_log=execution_log,
    )

    workflow.add_node(
        "start",
        start_node,
    )

    workflow.add_node(
        "financial",
        financial_node,
    )

    workflow.add_node(
        "market",
        market_node,
    )

    workflow.add_node(
        "final",
        final_node,
    )

    workflow.add_edge(
        "start",
        "financial",
    )

    workflow.add_edge(
        "start",
        "market",
    )

    workflow.add_edge(
        "financial",
        "final",
    )

    workflow.add_edge(
        "market",
        "final",
    )

    workflow.set_entry_point(
        "start",
    )

    workflow.run(
        AgentState(
            goal="Test workflow",
        )
    )

    assert execution_log == [
        "start",
        "financial",
        "market",
        "final",
    ]


def test_workflow_detects_cycle():

    workflow = Workflow()

    execution_log = []

    first_node = FakeNode(
        name="first",
        execution_log=execution_log,
    )

    second_node = FakeNode(
        name="second",
        execution_log=execution_log,
    )

    workflow.add_node(
        "first",
        first_node,
    )

    workflow.add_node(
        "second",
        second_node,
    )

    workflow.add_edge(
        "first",
        "second",
    )

    workflow.add_edge(
        "second",
        "first",
    )

    workflow.set_entry_point(
        "first",
    )

    with pytest.raises(
        ValueError,
        match="Workflow contains a cycle.",
    ):
        workflow.run(
            AgentState(
                goal="Test workflow",
            )
        )


def test_workflow_supports_positive_conditional_branch():

    workflow = Workflow()

    execution_log = []

    start_node = FakeNode(
        name="start",
        execution_log=execution_log,
    )

    financial_node = FakeNode(
        name="financial",
        execution_log=execution_log,
    )

    market_node = FakeNode(
        name="market",
        execution_log=execution_log,
    )

    workflow.add_node(
        "start",
        start_node,
    )

    workflow.add_node(
        "financial",
        financial_node,
    )

    workflow.add_node(
        "market",
        market_node,
    )

    router = ConditionalRouter(
        routes={
            "financial": lambda state: True,
            "market": lambda state: False,
        },
    )

    workflow.add_conditional_edge(
        "start",
        router.route,
    )

    workflow.set_entry_point(
        "start",
    )

    workflow.run(
        AgentState(
            goal="Test workflow",
        )
    )

    assert execution_log == [
        "start",
        "financial",
    ]


def test_workflow_supports_negative_conditional_branch():

    workflow = Workflow()

    execution_log = []

    start_node = FakeNode(
        name="start",
        execution_log=execution_log,
    )

    financial_node = FakeNode(
        name="financial",
        execution_log=execution_log,
    )

    market_node = FakeNode(
        name="market",
        execution_log=execution_log,
    )

    workflow.add_node(
        "start",
        start_node,
    )

    workflow.add_node(
        "financial",
        financial_node,
    )

    workflow.add_node(
        "market",
        market_node,
    )

    router = ConditionalRouter(
        routes={
            "financial": lambda state: False,
            "market": lambda state: True,
        },
    )

    workflow.add_conditional_edge(
        "start",
        router.route,
    )

    workflow.set_entry_point(
        "start",
    )

    workflow.run(
        AgentState(
            goal="Test workflow",
        )
    )

    assert execution_log == [
        "start",
        "market",
    ]


def test_workflow_rejects_invalid_conditional_target():

    workflow = Workflow()

    execution_log = []

    start_node = FakeNode(
        name="start",
        execution_log=execution_log,
    )

    workflow.add_node(
        "start",
        start_node,
    )

    router = ConditionalRouter(
        routes={
            "missing": lambda state: True,
        },
    )

    workflow.add_conditional_edge(
        "start",
        router.route,
    )

    workflow.set_entry_point(
        "start",
    )

    with pytest.raises(
        ValueError,
        match=(
            "Conditional target node "
            "'missing' is not registered."
        ),
    ):
        workflow.run(
            AgentState(
                goal="Test workflow",
            )
        )


def test_workflow_detects_conditional_cycle():

    workflow = Workflow()

    execution_log = []

    first_node = FakeNode(
        name="first",
        execution_log=execution_log,
    )

    second_node = FakeNode(
        name="second",
        execution_log=execution_log,
    )

    workflow.add_node(
        "first",
        first_node,
    )

    workflow.add_node(
        "second",
        second_node,
    )

    router = ConditionalRouter(
        routes={
            "second": lambda state: True,
        },
    )

    workflow.add_conditional_edge(
        "first",
        router.route,
    )

    reverse_router = ConditionalRouter(
        routes={
            "first": lambda state: True,
        },
    )

    workflow.add_conditional_edge(
        "second",
        reverse_router.route,
    )

    workflow.set_entry_point(
        "first",
    )

    with pytest.raises(
        ValueError,
        match="Workflow contains a cycle.",
    ):
        workflow.run(
            AgentState(
                goal="Test workflow",
            )
        )

def test_workflow_integrates_with_conditional_router():

    workflow = Workflow()

    execution_log = []

    start_node = FakeNode(
        name="start",
        execution_log=execution_log,
    )

    financial_node = FakeNode(
        name="financial",
        execution_log=execution_log,
    )

    workflow.add_node(
        "start",
        start_node,
    )

    workflow.add_node(
        "financial",
        financial_node,
    )

    router = ConditionalRouter(
        routes={
            "financial": lambda state: True,
        },
    )

    workflow.add_conditional_edge(
        "start",
        router.route,
    )

    workflow.set_entry_point(
        "start",
    )

    workflow.run(
        AgentState(
            goal="Test workflow",
        )
    )

    assert execution_log == [
        "start",
        "financial",
    ]


def test_workflow_rejects_static_and_conditional_edges_on_same_node():

    workflow = Workflow()

    start_node = FakeNode(
        name="start",
        execution_log=[],
    )

    target_node = FakeNode(
        name="target",
        execution_log=[],
    )

    workflow.add_node(
        "start",
        start_node,
    )

    workflow.add_node(
        "target",
        target_node,
    )

    workflow.add_edge(
        "start",
        "target",
    )

    router = ConditionalRouter(
        routes={
            "target": lambda state: True,
        },
    )

    with pytest.raises(
        ValueError,
        match=(
            "Node 'start' cannot have both "
            "static and conditional edges."
        ),
    ):
        workflow.add_conditional_edge(
            "start",
            router.route,
        )


def test_workflow_retries_failed_node():

    workflow = Workflow(
        max_node_retries=2,
    )

    execution_log = []

    node = FailingNode(
        name="financial",
        execution_log=execution_log,
        failures_before_success=2,
    )

    workflow.add_node(
        "financial",
        node,
    )

    workflow.set_entry_point(
        "financial",
    )

    state = AgentState(
        goal="Analyze company financials",
    )

    workflow.run(
        state,
    )

    assert execution_log == [
        "financial",
        "financial",
        "financial",
    ]

    execution = workflow.executions[0]

    assert execution.status == NodeExecutionStatus.COMPLETED
    assert execution.attempts == 3
