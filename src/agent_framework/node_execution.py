from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class NodeExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class NodeExecution:
    node_name: str
    status: NodeExecutionStatus

    run_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration: float | None = None

    attempts: int = 0
