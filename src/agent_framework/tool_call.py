from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class ToolCall:

    tool_name: str

    arguments: dict = field(
        default_factory=dict
    )

    id: str = field(
        default_factory=lambda: str(uuid4())
    )
