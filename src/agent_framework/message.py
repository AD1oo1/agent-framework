from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class Message(ABC):
    content: str
    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict = field(default_factory=dict)

    @property
    @abstractmethod
    def role(self) -> Role:
        """Return the role associated with this message."""
        ...


@dataclass
class UserMessage(Message):
    intent: str | None = None
    preferences: dict = field(default_factory=dict)

    @property
    def role(self) -> Role:
        return Role.USER


@dataclass
class AssistantMessage(Message):
    reasoning_trace: str | None = None
    actions: list[str] = field(default_factory=list)

    @property
    def role(self) -> Role:
        return Role.ASSISTANT


@dataclass
class ToolMessage(Message):
    tool_name: str = ""
    result: object = None
    success: bool = True
    error: str | None = None

    @property
    def role(self) -> Role:
        return Role.TOOL
