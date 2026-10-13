from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ToolResult:
    tool_name: str
    result: object | None = None
    success: bool = True
    error: str | None = None


class Tool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique tool name."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the tool does."""
        ...

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool."""
        ...
