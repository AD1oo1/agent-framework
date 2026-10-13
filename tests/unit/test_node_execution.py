from datetime import datetime, timezone

from agent_framework.node_execution import (
    NodeExecution,
    NodeExecutionStatus,
)


def test_node_execution_can_be_created():

    execution = NodeExecution(
        node_name="financial_data",
        status=NodeExecutionStatus.PENDING,
    )

    assert execution.node_name == "financial_data"
    assert execution.status == NodeExecutionStatus.PENDING
    assert execution.started_at is None
    assert execution.completed_at is None
    assert execution.duration is None


def test_node_execution_stores_timing_information():

    started_at = datetime(
        2026,
        1,
        1,
        10,
        0,
        0,
        tzinfo=timezone.utc,
    )

    completed_at = datetime(
        2026,
        1,
        1,
        10,
        0,
        2,
        tzinfo=timezone.utc,
    )

    execution = NodeExecution(
        node_name="financial_data",
        status=NodeExecutionStatus.COMPLETED,
        started_at=started_at,
        completed_at=completed_at,
        duration=2.0,
    )

    assert execution.started_at == started_at
    assert execution.completed_at == completed_at
    assert execution.duration == 2.0


def test_node_execution_statuses_are_defined():

    assert NodeExecutionStatus.PENDING.value == "pending"
    assert NodeExecutionStatus.RUNNING.value == "running"
    assert NodeExecutionStatus.COMPLETED.value == "completed"
    assert NodeExecutionStatus.FAILED.value == "failed"
